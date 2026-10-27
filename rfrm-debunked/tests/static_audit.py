#!/usr/bin/env python3
"""Integrity checks for the evidence inventory and generated static page."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.hashes=[]; self.policies=[]; self.disclosures=0; self.elements=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        self.elements.append((tag,attrs))
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#'):self.hashes.append(attrs['href'][1:])
        if tag=='article' and 'policy' in attrs.get('class','').split():self.policies.append(attrs)
        if tag=='details' and 'analysis' in attrs.get('class','').split():self.disclosures+=1
page=(ROOT/'index.html').read_text()
doc=Document();doc.feed(page)
assert len(doc.ids)==len(set(doc.ids)), 'Duplicate HTML IDs'
assert all(ref in doc.ids for ref in doc.hashes), 'Broken fragment link'
assert [a['id'] for a in doc.policies if a.get('data-number')]==[f'measure-{i:02d}' for i in range(1,65)]
assert len(doc.policies)==101 and doc.disclosures==101
assert len(set(a['data-topic'] for a in doc.policies[:64]))==10
assert '{{' not in page and 'fetch(' not in page
assert hashlib.sha256((ROOT/'economic-rescue-plan-summary.md').read_bytes()).hexdigest()=='6bd56fc035838ee613067efd673beaf0c02a8c3ae5893e38e489ac0d5ac76c8f'
articles=[];sources=[]
for file in ['energy','housing','infrastructure','deregulation','tax','support','updates']:
    data=json.loads((ROOT/'authoring'/f'{file}.json').read_text());articles+=data['articles'];sources+=data['sources']
source_ids={s['id'] for s in sources}; ids={a['id'] for a in articles}
for a in articles:
    assert a['evidenceLabel'] in {'Internal contradiction','Legal obstacle','Costing uncertainty','Strong evidence','Distributional trade-off','Reasonable policy with caveats'},a['id']
    assert 120<=len(a['critique'].split())<=200,a['id']
    for panel in a.get('evidencePanels',[]):
        assert panel['paragraphs'] and panel['sourceIds'] and all(i in source_ids for i in panel['sourceIds'])
    assert all(i['id'] in ids for i in a.get('dependencies',[]))
    assert all(s in source_ids for s in a['sourceIds']) and a['sourceIds']
    assert all(i in ids for i in a['related'])
    assert all(a.get(key) for key in ['category','page','title','proposal','counter','critique'])
for s in sources:
    assert all(s.get(key) for key in ['publisher','title','url','accessed','finding']),s['id']
    assert s['url'].startswith('https://')
tables=json.loads((ROOT/'authoring/tables.json').read_text())
assert tables['fiscal']['years']==['2026/27','2027/28','2028/29','2029/30','2030/31','2031/32']
for table in tables.values():
    assert all(len(row) in [1,len(table['years'])+1] for row in table['rows'])
assert tables['savings']['rows'][5]==['End migrant hotel spending','','1.60','1.70','1.70','1.80']
assert ['REDUCTION IN CURRENT DEFICIT','','(4.24)','1.39','9.63','21.83','24.11'] in tables['fiscal']['rows']
# Headline panels are not policy results; all links still resolve to static content.
assert len([a for tag,a in doc.elements if 'headline-card' in a.get('class','').split()])==8
assert len([a for tag,a in doc.elements if tag=='p' and a.get('class')=='evidence-label'])==101
assert page.index('id="biggest-problems"')<page.index('id="explorer"')
assert all(term in page for term in ["£218.70","£267.30","£7.14bn","£6.96bn","£6.76bn","£6.77bn","£14bn","£4.44","£8.54","Withdrawal Agreement"])
assert 'have not authenticated it against a publisher-hosted original' not in page
assert 'published <time datetime="2026-10-26">26 October 2026</time>' in page
assert all(selector in page for selector in ['.evidence-panel,.dependencies,.evidence-label',"document.querySelectorAll('details')"])
audit=json.loads((ROOT/'authoring/audit.json').read_text())
assert len(audit['rows'])==20 and len(audit['dimensions'])==6
from decimal import Decimal
eligible=[];in_policies=False
for row in tables['fiscal']['rows']:
    label=row[0]
    if label=='REVENUE':in_policies=True;continue
    if label=='Change in primary balance':break
    if not in_policies or len(row)==1 or (label.isupper() and not label.startswith('ADDITIONAL SPENDING')) or label.startswith('Memo:'):continue
    values=[abs(Decimal(value.replace(',','').replace('(','-').replace(')',''))) for value in row[2:] if value]
    if values and max(values)>=1:eligible.append(label)
assert len(eligible)==20
assert {r['tableLabel'] for r in audit['rows']}==set(eligible)
for row in audit['rows']:
    assert set(row['checks'])=={d['id'] for d in audit['dimensions']}
    assert all(c['status'] in {'Published','Partial','Not provided in the plan','Not applicable'} and c['note'] for c in row['checks'].values())
    assert row['target'] in ids
# Every original check is preserved either inline or by a resolving common-note link.
from html import unescape
items = re.findall(r'<details class="audit-item" id="([^"]+)">(.*?)</details>', page, re.S)
assert len(items) == 20 and 'table-costing-audit' not in page
assert len([1 for tag, attrs in doc.elements if tag == 'table']) == 2
for row, (item_id, markup) in zip(audit['rows'], items):
    assert item_id == 'audit-' + row['target']
    assert row['title'] in unescape(markup) and row['profile'] in unescape(markup)
    assert markup.count('class="audit-check"') == 6
    for dim in audit['dimensions']:
        check = row['checks'][dim['id']]
        block = re.search(r'<div class="audit-check" data-dimension="' + dim['id'] + r'">(.*?)</div>', markup, re.S).group(1)
        assert check['status'] in unescape(block)
        if check['note'] not in unescape(block):
            ref = re.search(r'href="#(audit-note-[^"]+)"', block).group(1)
            note = re.search(r'<div id="' + ref + r'">(.*?)</div>', page, re.S).group(1)
            assert check['note'] in unescape(note)
    summary = re.search(r'<summary>(.*?)</summary>', markup, re.S).group(1)
    assert 'View disclosure details' in summary
    assert 'audit-check' not in summary and 'Missing:' not in summary and 'Partly explained:' not in summary
highlights=json.loads((ROOT/'authoring/highlights.json').read_text())
assert len(highlights)==8 and all(card['sourceIds'] for card in highlights)
assert all(source_id in source_ids for card in highlights for source_id in card['sourceIds'])
assert all(link['id'] in doc.ids for card in highlights for link in card['links'])
assert '120 source records' in (ROOT/'RESEARCH.md').read_text()
print('PASS: 64 numbered +37 supporting; 8 headline panels;101 evidence labels;20 major lines ×6 disclosure tests; valid IDs/sources/links;120–200 word critiques; full tables; unchanged summary.')
