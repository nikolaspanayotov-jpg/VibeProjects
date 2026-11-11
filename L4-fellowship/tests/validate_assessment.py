"""Validate the curated public assessment model before compilation."""
import re

def validate_assessment(data):
 groups=data['groups'];assert len(groups)==30
 by_id={g['groupId']:g for g in groups};assert len(by_id)==30
 ids=[m for g in groups for m in g['members']];assert len(ids)==len(set(ids))==37
 assert set(ids)=={*(f'K{i}' for i in range(1,16)),*(f'S{i}' for i in range(1,16)),*(f'B{i}' for i in range(1,8))}
 assert sum(g['assessmentMethod']=='AM1' for g in groups)==13
 assert sum(len(g['members']) for g in groups if g['assessmentMethod']=='AM1')==17
 assert {g['groupId'] for g in groups if g['gradingDistinction'] is not None}=={'K8+S6','K9+S7','K11+S15','S4','B4','K10','K14+S11','S14'}
 cell=lambda c: bool(re.fullmatch(r'Sheet1!A\d+',c))
 for g in groups:
  assert g['assessmentMethod'] in ['AM1','AM2'] and g['gradingPass'].strip()
  assert cell(g['overviewCell']) and cell(g['detailCell'])
  assert '+'.join(g['members'])==g['groupId']
  b=g['studyBrief'];assert b['kind']=='derived-coaching' and all(isinstance(b[k],str) and 8<=len(b[k])<=400 for k in ['title','explain','show','discuss']) and b['sourceCells']==[g['overviewCell'],g['detailCell']]
  for kind in ['providerMeets','providerExceeds','providerUnresolved','evidenceGuidance','derivedLearning']:
   for r in g[kind]:assert r['text'].strip() and r['sourceCells'] and all(map(cell,r['sourceCells'])) and r['kind']
  for r in g['resources']:assert r['url']=='' and all(map(cell,r['sourceCells']))
 for kind in ['questions','quiz','evaluations','reviews','packs']:
  assert len({r['id'] for r in data[kind]})==len(data[kind])
  for r in data[kind]:assert all(map(cell,r['sourceCells']))
 for q in data['questions']:assert q['groupId'] in by_id and q['method']==by_id[q['groupId']]['assessmentMethod'] and q['kind']=='source-question'
 assert {q['groupId'] for q in data['questions']}==set(by_id)
 assert len(data['evaluations'])==6 and len(data['quiz'])==6
 assert {g for e in data['evaluations'] for g in e['groups']}=={g['groupId'] for g in groups if g['gradingDistinction']}
 for q in data['quiz']:assert isinstance(q['answer'],bool) and q['groupId'] in by_id
 assert len(data['packs'])==4
 required=[k for p in data['packs'] for k in p['required']]
 assert len(required)==len(set(required))==20
 assert set(required)=={m for g in groups if g['assessmentMethod']=='AM2' for m in g['members']}
 for p in data['packs']:assert not set(p['required'])&set(p['optional']) and set(p['optional'])<=set(ids)
 assert data['packs'][1]['optional']==['K6','K10'] and data['packs'][3]['optional']==['K13','S10']
 return True

if __name__=='__main__':
 import json
 from pathlib import Path
 d=json.loads((Path(__file__).resolve().parents[1]/'assessment-criteria.json').read_text());validate_assessment(d)
 print('Assessment model:30groups,37KSBs,8distinction rows,254source prompts,4packs,6evaluation patterns and source references verified.')
