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
        self.ids=[]; self.hashes=[]; self.policies=[]; self.disclosures=0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#'):self.hashes.append(attrs['href'][1:])
        if tag=='article':self.policies.append(attrs)
        if tag=='details':self.disclosures+=1
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
for file in ['energy','housing','infrastructure','deregulation','tax','support']:
    data=json.loads((ROOT/'authoring'/f'{file}.json').read_text());articles+=data['articles'];sources+=data['sources']
source_ids={s['id'] for s in sources}; ids={a['id'] for a in articles}
for a in articles:
    assert 120<=len(a['critique'].split())<=200,a['id']
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
print('PASS: 64 numbered +37 supporting; unique IDs; 10 original categories; sources/relations; 120–200 words; full table structure; unchanged summary.')
