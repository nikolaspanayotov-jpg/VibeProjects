"""Audit the static page against the preserved editorial source, without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import re

ROOT = Path(__file__).resolve().parents[1]

class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.counts=Counter(); self.titles=[]
        self.rows={}; self.metric=None; self.cells=[]; self.cell=None
        self.details=[]; self.detail=None; self.detail_depth=0
        self.assessments=0; self.timelines=0; self.takeaways=0
        self.list_name=None

    def handle_starttag(self, tag, attrs):
        a=dict(attrs); classes=a.get('class','').split()
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag=='article' and 'policy' in classes:
            self.counts[a['data-topic']]+=1; self.titles.append(a['data-original-title'])
        if tag=='tr' and 'data-metric' in a:
            self.metric=a['data-metric']; self.cells=[]
        if self.metric and tag in ('th','td'): self.cell=''
        if self.detail is not None: self.detail_depth+=1
        if 'source-detail' in classes: self.detail=''; self.detail_depth=1
        if tag in ('ul','ol') and a.get('class') in ('assessments','timeline','takeaways'): self.list_name=a['class']
        if tag=='li' and self.list_name:
            setattr(self,{'assessments':'assessments','timeline':'timelines','takeaways':'takeaways'}[self.list_name],getattr(self,{'assessments':'assessments','timeline':'timelines','takeaways':'takeaways'}[self.list_name])+1)

    def handle_data(self, text):
        if self.cell is not None: self.cell+=text
        if self.detail is not None: self.detail+=text

    def handle_endtag(self, tag):
        if self.metric and tag in ('th','td') and self.cell is not None:
            self.cells.append(self.cell.strip()); self.cell=None
        if tag=='tr' and self.metric:
            self.rows[self.metric]=self.cells; self.metric=None
        if self.detail is not None:
            self.detail_depth-=1
            if self.detail_depth==0: self.details.append(self.detail); self.detail=None
        if tag in ('ul','ol'): self.list_name=None

page=Audit(); html=(ROOT/'index.html').read_text(); page.feed(html)
assert len(page.ids)==len(set(page.ids)), 'Duplicate IDs'
assert page.counts==Counter(bills=8,tax=8,work=8,business=11,funding=8,spending=5), page.counts
assert (page.assessments,page.timelines,page.takeaways)==(8,10,6)
assert len(page.details)==48
assert len(page.titles)==len(set(page.titles))==48
for link in page.links:
    parsed=urlsplit(link)
    if parsed.scheme in ('http','https'): continue
    if not parsed.path:
        assert unquote(parsed.fragment) in page.ids, 'Broken fragment: '+link
    else: assert (ROOT/unquote(parsed.path)).is_file(), 'Missing local link: '+link

md=(ROOT/'key-budget-points.md').read_text()
sections=re.split(r'^## ',md,flags=re.M)
originals=[]; titles=[]
for n in range(1,7):
    text=next(x for x in sections if x.startswith(str(n)+'. '))
    for line in text.splitlines():
        if line.startswith('| ') and not line.startswith(('| ---','| Measure |')):
            c=[x.strip() for x in line.strip('|').split('|')]
            titles.append(c[0]); originals.append(c[1]+' '+c[2])
        elif line.startswith('- **'):
            m=re.match(r'- \*\*(.+?)\*\*\s*(.*)',line)
            titles.append(m[1].rstrip(':')); originals.append(m[2])
    for label in ['Longer-term energy changes:','State Pension Triple Lock:','Additional points in OOTLAR:']:
        m=re.search(r'^\*\*'+re.escape(label)+r'\*\* (.+)$',text,re.M)
        if m: titles.append(label.rstrip(':')); originals.append(m[1])

def plain(s):
    s=re.sub(r'\[([^\]]+)\]\[[^\]]+\]',r'\1',s)
    s=s.replace('**','')
    return ' '.join(s.split())
assert page.titles==titles, 'Policy inventory/order differs from source'
for title,source,rendered in zip(titles,originals,page.details):
    assert plain(source)==plain(rendered), 'Lost or changed source detail: '+title

forecast=next(x for x in sections if x.startswith('7. '))
expected_rows=[]
for line in forecast.splitlines():
    if line.startswith('| ') and not line.startswith(('| ---','| Economic indicator','| Fiscal indicator')):
        expected_rows.append([plain(x.strip()) for x in line.strip('|').split('|')])
assert list(page.rows.values())==expected_rows, 'Forecast table cells differ'
assert 'Annex A' in html and 'inaccessible' in html
assert not re.search(r'<script[^>]+src=',html), 'Unexpected runtime script dependency'
assert '{{' not in html
print('PASS: 48 complete source-matched policies; 6 topics; 6 takeaways; 10 dates; 8 OBR points.')
print('PASS: forecast table cells, unique IDs, fragments, local documents and static runtime.')
