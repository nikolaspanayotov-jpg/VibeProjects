"""Guided lessons, readiness actions and the worked-project integration.

Run beside a localhost server:
python3 tests/browser_enhancements.py --url http://127.0.0.1:8000/ --output /tmp/l4-enhancements-qa
"""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import sqlite3
from playwright.sync_api import sync_playwright, expect

parser=argparse.ArgumentParser()
parser.add_argument('--url',default='http://127.0.0.1:8000/')
parser.add_argument('--output',default='/tmp/l4-enhancements-qa')
args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
KEY='l4-fellowship.v1';checks=[];errors=[]

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(viewport={'width':390,'height':844},accept_downloads=True,reduced_motion='reduce')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(args.url+'#ksb-k10')
 expect(page.locator('.quick-answer')).to_be_visible()
 assert page.locator('#lesson-full-guide').evaluate('(el)=>el.open') is False
 content=page.evaluate('window.L4_CURRICULUM')
 assert len(content['items'])==37
 for k in content['items']:
  assert all(k[field] for field in ['quick','example','mistake','probe','guide'])
  assert 35<=len(re.sub('<[^>]+>',' ',k['quick']).split())<=110
 page.locator('[data-action="lesson-jump"][data-step="example"]').click()
 assert page.locator('#lesson-example').evaluate('(el)=>el.open')
 expect(page.locator('#lesson-example')).to_contain_text('57 extra rows')
 page.locator('[data-action="lesson-jump"][data-step="answer"]').click()
 expect(page.locator('#my-response')).to_be_focused()
 assert page.locator('.lesson-jumps').bounding_box()['y']>=-1
 assert page.locator('#my-response').bounding_box()['y']>page.locator('.lesson-jumps').bounding_box()['height']
 page.locator('#my-response').fill('Synthetic QA example: my own investigation, rationale and validation.')
 page.locator('[data-example-confirmed="K10"]').check()
 page.locator('[data-action="save-response"]').click()
 page.reload()
 expect(page.locator('[data-example-confirmed="K10"]')).to_be_checked()
 page.locator('#my-response').fill('Edited QA response needs a fresh self-check.')
 expect(page.locator('[data-example-confirmed="K10"]')).not_to_be_checked()
 page.locator('[data-action="save-response"]').click()
 page.locator('[data-action="lesson-jump"][data-step="learn"]').click()
 page.screenshot(path=str(out/'guided-mobile.png'))
 page.locator('#lesson-full-guide > summary').click()
 expect(page.locator('.full-answer')).to_be_visible()
 checks.append('All 37 concise explanations, examples, mistakes and probes; mobile jumps; full guidance remains available')
 checks.append('Explicit personal-example self-check persists, clears on response edits and does not imply evidence')

 page.evaluate("location.hash='readiness'")
 expect(page.locator('.readiness-row')).to_have_count(10)
 page.locator('[data-action="ready-all"]').click()
 expect(page.locator('.readiness-row')).to_have_count(37)
 page.locator('#readiness-category').select_option('S')
 expect(page.locator('.readiness-row')).to_have_count(15)
 page.locator('#readiness-gap').select_option('example')
 expect(page.locator('.readiness-row')).to_have_count(15)
 page.locator('[data-action="clear-readiness"]').click()
 expect(page.locator('.readiness-row')).to_have_count(37)
 checks.append('Readiness matrix and combined category/gap filters cover all 37 topics')

 seed={'version':1,'settings':{},'ksbs':{
  'K10':{'response':'QA join explanation','recall':'partial','lastReview':'2026-11-02','nextReview':'2099-01-01','gap':'<img src=x onerror="window.__xss=1"> Explain cardinality'},
  'S12':{'response':'QA draft for two different stakeholders','learning':'explain','recall':'independent','lastReview':'2026-11-02','nextReview':'2099-01-01'},
  'K1':{'response':'QA genuine-example self-check','exampleConfirmed':True,'recall':'independent','lastReview':'2026-11-02','nextReview':'2099-01-01'}},'evidence':[],'attempts':[],'session':None,'studySession':None}
 seeded=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
 seeded.add_init_script("if(!sessionStorage.getItem('qa-seeded')){localStorage.setItem("+json.dumps(KEY)+","+json.dumps(json.dumps(seed))+");sessionStorage.setItem('qa-seeded','1');}")
 ready=seeded.new_page();ready.on('pageerror',lambda e:errors.append(str(e)))
 ready.goto(args.url+'#readiness')
 actions=ready.locator('.action-list > li')
 assert actions.locator('.inline-badge').all_text_contents()==['K10','S12','K1']
 assert actions.locator('[data-gap-kind]').evaluate_all('(els)=>els.map(e=>e.dataset.gapKind)')==['probe','example','evidence']
 assert ready.evaluate('window.__xss') is None
 ready.screenshot(path=str(out/'readiness-desktop.png'),full_page=True)
 ready.locator('[data-action="ready-all"]').click()
 ready.locator('[data-readiness-ksb="S12"] summary').click()
 ready.locator('[data-readiness-ksb="S12"] [data-action="gap-action"]').click()
 expect(ready.locator('h1')).to_have_text('Stakeholder Communication & Collaboration')
 expect(ready.locator('#my-response')).to_be_focused()
 ready.locator('[data-example-confirmed="S12"]').check();ready.locator('[data-action="save-response"]').click()
 ready.evaluate("location.hash='readiness'")
 expect(ready.locator('[data-readiness-ksb="S12"]')).to_contain_text('Example self-checked')
 ready.locator('[data-readiness-ksb="K10"] summary').click()
 ready.locator('[data-readiness-ksb="K10"] [data-action="gap-action"]').click()
 expect(ready.locator('#practice-mode')).to_have_value('probe')
 expect(ready.locator('#practice-topic')).to_have_value('K10')
 ready.locator('[data-action="start-practice"]').click()
 expect(ready.locator('.practice-question')).to_have_text(next(k['probe'] for k in content['items'] if k['id']=='K10'))
 ready.locator('#practice-response').fill('QA probe response, kept through reload.')
 ready.locator('[data-action="pause-practice"]').click();ready.reload()
 ready.locator('[data-action="resume-practice"]').click()
 expect(ready.locator('#practice-response')).to_have_value('QA probe response, kept through reload.')
 stored=ready.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
 assert stored['session']['queue'][0]['type']=='probe'
 ready.locator('[data-action="reveal-answer"]').click()
 ready.locator('[data-action="rate-practice"][data-result="independent"]').click()
 ready.evaluate("location.hash='readiness'")
 expect(ready.locator('[data-readiness-ksb="K1"]')).to_be_visible()
 ready.locator('[data-readiness-ksb="K1"] summary').click()
 ready.locator('[data-readiness-ksb="K1"] [data-action="gap-action"]').click()
 expect(ready.locator('input[name="ev-ksbs"][value="K1"]')).to_be_checked()
 assert ready.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).evidence.length',KEY)==0
 checks.append('Next actions come from actual gaps; probe, personal-example and evidence actions reach the matching topic')
 checks.append('Probing questions pause/reload correctly; hostile notes stay text; no evidence is completed automatically')

 legacy=browser.new_context()
 old={'version':1,'settings':{'textSize':'large'},'ksbs':{'K8':{'response':'Legacy QA response retained','gap':'Legacy QA note','learning':'explain','confidence':'4'}},'evidence':[],'attempts':[],'session':None,'studySession':None}
 legacy.add_init_script("localStorage.setItem("+json.dumps(KEY)+","+json.dumps(json.dumps(old))+");")
 old_page=legacy.new_page();old_page.goto(args.url+'#ksb-k8')
 expect(old_page.locator('#my-response')).to_have_value('Legacy QA response retained')
 expect(old_page.locator('[data-example-confirmed="K8"]')).not_to_be_checked()
 expect(old_page.locator('#storage-warning')).to_be_hidden()
 old_page.locator('[data-action="save-response"]').click()
 old_saved=old_page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
 assert old_saved['version']==1 and old_saved['ksbs']['K8']['confidence']=='4' and old_saved['ksbs']['K8']['gap']=='Legacy QA note'
 checks.append('Existing version-1 progress loads without losing responses, confidence, notes or settings')

 case_context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce')
 case=case_context.new_page();case.on('pageerror',lambda e:errors.append(str(e)))
 case.goto(args.url+'#project-planning')
 expect(case.locator('.project-timeline button')).to_have_count(6)
 assert len(content['project']['mapping'])==37 and all(content['project']['mapping'].values())
 assert sum(len(s['artifacts']) for s in content['project']['stages'])==8
 expect(case.locator('.project-coverage-grid > div')).to_have_count(37)
 case.locator('[data-action="project-stage"][data-stage="preparation"]').first.click()
 expect(case.locator('[data-project-stage]')).to_have_attribute('data-project-stage','preparation')
 expect(case.locator('.join-result strong')).to_have_text('357')
 case.locator('[data-action="project-join"][data-join="approved"]').click()
 expect(case.locator('.join-result strong')).to_have_text('300')
 with case.expect_download() as info:case.locator('[data-action="approved-lookup"]').click()
 approved=list(csv.DictReader(io.StringIO(Path(info.value.path()).read_text())))
 assert len(approved)==5 and len({r['service_id'] for r in approved})==5
 case.locator('#project-ksb').select_option('K8')
 expect(case.locator('.project-annotations .highlighted')).to_have_count(1)
 expect(case.locator('.project-annotations .highlighted > a')).to_have_text('K8')
 with case.expect_download() as info:case.locator('[data-action="download-project"]').click()
 portfolio=Path(info.value.path()).read_text()
 assert portfolio.startswith('# Worked project:') and len(re.findall(r'^### P\d+',portfolio,re.M))==8
 checks.append('Six-stage interactive project, eight annotated artefacts, complete KSB map and downloadable fictional portfolio')
 case.evaluate("location.hash='studio'");expect(case.locator('.studio-task')).to_have_count(6)
 datasets={}
 for kind in ['requests','lookup']:
  with case.expect_download() as info:case.locator(f'[data-dataset="{kind}"]').click()
  datasets[kind]=list(csv.DictReader(io.StringIO(Path(info.value.path()).read_text())))
 con=sqlite3.connect(':memory:')
 for name,rows in [('service_requests',datasets['requests']),('service_lookup',datasets['lookup']),('approved_service_lookup',approved)]:
  columns=list(rows[0]);con.execute('CREATE TABLE '+name+' ('+', '.join(c+' TEXT' for c in columns)+')')
  con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in columns)+')',[[r[c] for c in columns] for r in rows])
 sql=re.search(r'```sql\n(.*?)```',portfolio,re.S)[1]
 statements=[s.strip() for s in sql.split(';') if s.strip()]
 results=[con.execute(s).fetchall() for s in statements]
 assert results[0]==[('S2',2)] and results[1]==[(357,)] and len(results[2])==300 and results[3]==[(4,8)]
 checks.append('Worked-project SQL executes against downloaded fixtures and approved lookup; all quality counts reconcile')
 case.evaluate("location.hash='project-analysis'");expect(case.locator('[data-project-stage]')).to_have_attribute('data-project-stage','analysis')
 expect(case.locator('.forecast-svg')).to_have_count(1)
 case.evaluate("location.hash='project-communication'");expect(case.locator('.case-kpis')).to_be_visible()
 assert case.locator('.case-kpis strong').all_text_contents()==['300','270','30','8']
 assert case.locator('.case-bars dd strong').all_text_contents()==['59','57','57','58','57','12']
 case.locator('[data-action="project-chart"][data-chart="feedback"]').click()
 expect(case.locator('[data-action="project-chart"][data-chart="feedback"]')).to_have_attribute('aria-pressed','true')
 assert case.locator('.case-bars dd strong').all_text_contents()==['6','12','6','12','6']
 expect(case.locator('.case-dashboard')).to_contain_text('42 theme assignments across 36 comments')
 case.screenshot(path=str(out/'project-desktop.png'),full_page=True)
 saved=case.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
 assert not saved['evidence'] and not saved['attempts']
 assert all(k['learning']=='new' and not k['exampleConfirmed'] for k in saved['ksbs'].values())
 case.locator('.project-annotations [data-action="project-personal-example"][data-id="S12"]').click()
 expect(case.locator('#my-response')).to_be_focused();expect(case.locator('#my-response')).to_have_value('')
 checks.append('Quantitative/qualitative dashboard values reconcile; project visits never inflate personal progress or copy fictional experience')

 for width in [320,390,768,1280]:
  case.set_viewport_size({'width':width,'height':900})
  for route in ['ksb-k10','readiness','project-planning','project-preparation','project-analysis','project-communication','project-reflection']:
   case.goto(args.url+'#'+route)
   expect(case.locator('h1')).to_be_visible()
   assert not case.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,route)
  if width==390:
   case.goto(args.url+'#project-communication');case.screenshot(path=str(out/'project-mobile.png'),full_page=True)
   ready.set_viewport_size({'width':390,'height':844});ready.goto(args.url+'#readiness');ready.screenshot(path=str(out/'readiness-mobile.png'),full_page=True)
 case.set_viewport_size({'width':390,'height':844});case.goto(args.url+'#ksb-s13')
 case.locator('[data-action="text-size"]').click()
 assert not case.evaluate('document.documentElement.scrollWidth>innerWidth')
 case.locator('[data-action="lesson-jump"][data-step="answer"]').focus();case.keyboard.press('Enter')
 expect(case.locator('#my-response')).to_be_focused()
 checks.append('Mobile sticky navigation, keyboard jumps, large text and all new views reflow at 320/390/768/1280px')
 direct=browser.new_page();direct.goto((Path(__file__).resolve().parent.parent/'index.html').as_uri()+'#project-communication')
 expect(direct.locator('.case-kpis')).to_be_visible();expect(direct.locator('h1')).to_have_text('Follow one complete project.')
 checks.append('New project and versioned curriculum work by opening the file directly')
 assert not errors,errors
 browser.close()

report={'status':'passed','checks':checks,'page_errors':errors,'screenshots':[p.name for p in out.glob('*.png')]}
(out/'results.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
