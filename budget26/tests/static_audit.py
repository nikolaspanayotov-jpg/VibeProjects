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
        self.policy_text=[]; self.in_policy=False; self.fact_depth=0
        self.assessments=0; self.timelines=0; self.takeaways=0
        self.list_name=None

    def handle_starttag(self, tag, attrs):
        a=dict(attrs); classes=a.get('class','').split()
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag=='article' and 'policy' in classes:
            self.counts[a['data-topic']]+=1; self.titles.append(a['data-original-title'])
            self.in_policy=True; self.policy_text.append('')
        if self.fact_depth: self.fact_depth+=1
        if self.in_policy and any(c in classes for c in ('policy-summary','policy-comparison','policy-meta','source-detail')):
            self.fact_depth=1
            self.policy_text[-1]+=' '
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
        if self.fact_depth: self.policy_text[-1]+=' '+text

    def handle_endtag(self, tag):
        if self.fact_depth: self.fact_depth-=1
        if tag=='article': self.in_policy=False
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
assert (page.assessments,page.timelines,page.takeaways)==(8,20,6)
assert html.count('<details class="policy-details">')==48
assert html.count('<p class="citation"><a href="./sources/budget-2026.pdf#page=')>=47
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
# Facts may appear in the summary, metadata or complementary expanded prose.
# Preserve every original numerical value without requiring verbatim duplication.
def values(text):
    return set(re.findall(r'(?<![\w.])£?\d+(?:,\d{3})*(?:\.\d+)?(?:%|p)?',text))
for title,source,rendered in zip(titles,originals,page.policy_text):
    source=re.sub(r'OOTLAR, sections .+$','',plain(source))
    assert values(source)<=values(plain(rendered)), 'Missing source values: '+title+' '+str(values(source)-values(plain(rendered)))

forecast=next(x for x in sections if x.startswith('7. '))
expected_rows=[]
for line in forecast.splitlines():
    if line.startswith('| ') and not line.startswith(('| ---','| Economic indicator','| Fiscal indicator')):
        expected_rows.append([plain(x.strip()) for x in line.strip('|').split('|')])
assert list(page.rows.values())==expected_rows, 'Forecast table cells differ'
assert 'Annex A' in html and 'inaccessible' in html
assert not re.search(r'<script[^>]+src=',html), 'Unexpected runtime script dependency'
assert '{{' not in html

# Parse the new reading aids without adding a third-party test dependency.
class Node:
    def __init__(self,tag,attrs=()):
        self.tag=tag; self.attrs=dict(attrs); self.children=[]
    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child,Node): yield from child.walk()
    def has_class(self,name): return name in self.attrs.get('class','').split()
    def text(self):
        return ''.join(child.text() if isinstance(child,Node) else child for child in self.children)
    def find(self,tag): return [node for node in self.walk() if node.tag==tag]

class FeatureTree(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root=Node('document'); self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs); self.stack[-1].children.append(node)
        if tag not in self.VOID: self.stack.append(node)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in self.VOID: self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:
                del self.stack[i:]; break
    def handle_data(self,text): self.stack[-1].children.append(text)

features=FeatureTree(); features.feed(html)
nodes=list(features.root.walk()); by_id={n.attrs['id']:n for n in nodes if 'id' in n.attrs}
def with_class(name): return [n for n in nodes if n.has_class(name)]
def clean(node): return ' '.join(node.text().split())
routes=with_class('route-grid')
assert len(routes)==1
audiences=[n for n in routes[0].children if isinstance(n,Node) and n.tag=='li']
assert [clean(n.find('h3')[0]) for n in audiences]==['First-time buyers','Pensioners','Drivers','Small-business owners']
assert all(len(n.find('a'))==3 for n in audiences)
assert all(a.attrs['href'].startswith('#policy-') for a in routes[0].find('a'))

comparisons=with_class('policy-comparison')
assert len(comparisons)==3 and all(n.tag=='dl' and n.attrs.get('aria-label') for n in comparisons)
cash=next(n for n in by_id['policy-cash-isa'].walk() if n.has_class('policy-comparison'))
trading=next(n for n in by_id['policy-trading-allowance'].walk() if n.has_class('policy-comparison'))
badr=next(n for n in by_id['policy-badr'].walk() if n.has_class('policy-comparison'))
assert [clean(n) for n in cash.find('dd')][:2]==['£20,000','£20,000']
assert [clean(n) for n in trading.find('dd')]==['£1,000 a year','£3,000 a year','£2,000 more income covered']
assert [clean(n) for n in badr.find('dd')]==['£1 million','£500,000','£500,000 lower limit']

examples=with_class('worked-example')
assert {n.attrs.get('id') for n in examples}=={'example-business-mileage','example-lifetime-isa'}
def example_amounts(name):
    calculation=next(n for n in by_id[name].walk() if n.has_class('example-calculation'))
    return [int(clean(n).replace('£','').replace(',','')) for n in calculation.find('dd')]
assert example_amounts('example-business-mileage')==[10000*55//100,2000*35//100,(10000*55+2000*35)//100]
assert example_amounts('example-lifetime-isa')==[10000*25//100,10000*20//100,10000*(25-20)//100]
mileage=clean(by_id['example-business-mileage']); lisa=clean(by_id['example-lifetime-isa'])
assert all(s in mileage for s in ('qualifying','6 April 2027–5 April 2028','tax relief depends'))
assert all(s in lisa for s in ('gross withdrawal','above £450,000','other qualifying rules','£8,000','£7,500','29 October 2026','unauthorised withdrawals'))

terms=with_class('term-link')
assert len(terms)==6 and len({n.attrs.get('id') for n in terms})==6
assert {n.attrs['href'] for n in terms}=={'#term-'+s for s in ('rateable-value','writing-down-allowance','equity-loan','real-terms','annualised-estimate','gdp')}
for term in terms:
    definition=by_id[term.attrs['href'][1:]]
    assert definition.attrs.get('tabindex')=='-1'
    assert len(definition.find('dt'))==len(definition.find('dd'))==1
    assert clean(definition.find('dd')[0])
    assert term.attrs['id'].startswith('read-term-')
assert 'hidden' in by_id['glossary-return'].attrs

timeline=with_class('timeline')[0]
events=[n for n in timeline.children if isinstance(n,Node) and n.tag=='li']
kind_classes={'Starts':'timeline-starts','Relief ends':'timeline-ends','Planned':'timeline-planned'}
assert len(events)==20
for event in events:
    kind=next(n for n in event.walk() if n.has_class('date-kind'))
    assert event.has_class(kind_classes[clean(kind)])
    assert len(event.find('time'))==1
    assert re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?',event.find('time')[0].attrs.get('datetime',''))
    assert event.find('a')
def event_for(date,target):
    return next(n for n in events if n.find('time')[0].attrs['datetime']==date and any(a.attrs.get('href')=='#policy-'+target for a in n.find('a')))
assert event_for('2027-04-01','minimum-wages').has_class('timeline-starts')
assert event_for('2027-04-06','savings-income').has_class('timeline-starts')
assert event_for('2028-01-02','private-hire').has_class('timeline-planned')
assert 'consultation' in clean(event_for('2028-01-02','private-hire'))
assert event_for('2027-06-30','electricity-vat').has_class('timeline-ends')
assert event_for('2027-06-30','fuel-duty').has_class('timeline-ends')
assert event_for('2027-07-01','fuel-duty').has_class('timeline-starts')
assert event_for('2028-04-01','gaming-machines').has_class('timeline-planned')
assert '2030–31' in clean(event_for('2030','carers-allowance'))
assert event_for('2030','carers-allowance').has_class('timeline-planned')

print('PASS: 48 policies retain source order and numerical values; 6 topics; 6 takeaways; 20 dates; 8 OBR points.')
print('PASS: forecast table cells, unique IDs, fragments, local documents and static runtime.')
print('PASS: four audience routes, three comparisons, two worked calculations and six linked definitions.')
print('PASS: timeline labels distinguish starts, relief expiry and planned delivery with precise key dates.')
