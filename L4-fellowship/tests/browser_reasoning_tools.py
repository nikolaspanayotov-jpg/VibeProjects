"""Reasoning tools, private notebook, connected evidence and safe v1 persistence."""
import argparse,copy,json,sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8000/');parser.add_argument('--output',default='/tmp/l4-reasoning-qa');args=parser.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True);KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce',timezone_id='Europe/London')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 def go(route):
  page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():
  page.wait_for_timeout(400)
  return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
 def upload(value):
  page.locator('#backup-file').set_input_files({'name':'synthetic.json','mimeType':'application/json','buffer':json.dumps(value).encode()})
 def merge(value,choice=None):
  upload(value);expect(page.locator('#restore-dialog')).to_be_visible()
  if choice:page.locator('[data-restore-conflict="'+choice+'"]').select_option('import')
  page.locator('[data-action="apply-restore"]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 go('repairs')
 expect(page.locator('.reasoning-feedback')).to_have_count(0)
 page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('#reasoning-error')).to_contain_text('complete both')
 baseline=saved();assert baseline['version']==1
 seed=copy.deepcopy(baseline);seed['ksbs']['K8']['response']='My original synthetic response';seed['ksbs']['K8']['exampleConfirmed']=True
 seed['evidence']=[dict(id='synthetic-quality',title='Synthetic quality log',project='Test fixture',reference='QA-TEST',reflection='Synthetic only',learning='',date='2026-11-05',reviewDate='',reviewNote='',status='linked',links=[dict(id='K8',rationale='Accuracy checks'),dict(id='S6',rationale='Resolved missing fields'),dict(id='B5',rationale='Investigated a duplicate-key cause')])]
 merge(seed)
 before=copy.deepcopy(saved())
 con=sqlite3.connect(':memory:');con.executescript('CREATE TABLE r(k TEXT,v INTEGER);CREATE TABLE l(k TEXT,label TEXT);INSERT INTO r VALUES ("A",10),("A",20),("B",30);INSERT INTO l VALUES ("A","Alpha"),("A","Old"),("B","Beta");')
 assert con.execute('SELECT COUNT(*),SUM(v) FROM r LEFT JOIN l ON r.k=l.k').fetchone()==(5,90)
 assert con.execute('SELECT SUM(v) FROM r').fetchone()==(60,)
 for case,correct in [('duplicate-join','resolve'),('chart-scale','zero'),('p-value','conditional'),('forecast-leakage','time')]:
  go('repairs-'+case)
  page.locator('#reasoning-diagnosis').fill('Synthetic diagnosis: inspect the assumptions and source.')
  page.locator('#reasoning-impact').fill('The briefing could support an incorrect decision.')
  page.locator('input[name="reasoning-choice"][value="'+correct+'"]').check()
  page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('.reasoning-feedback')).to_be_visible()
  expect(page.locator('#reasoning-feedback-title')).to_contain_text('fits this example')
  page.reload();expect(page.locator('.reasoning-feedback')).to_be_visible()
 go('repairs-duplicate-join');expect(page.locator('.reasoning-feedback')).to_contain_text('90 across five rows')
 page.locator('input[value="distinct"]').check();expect(page.locator('.reasoning-feedback')).not_to_be_visible()
 page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('.reasoning-feedback')).to_contain_text('legitimate equal amounts')
 assert saved()['ksbs']==before['ksbs'] and saved()['evidence']==before['evidence']
 checks.append('All four diagnosis/correction flows require explanations, reveal option-specific feedback, persist through reload and leave KSB/evidence state unchanged; SQL totals verified independently')
 for case,correct in [('paired-change','paired'),('independent-groups','welch'),('association','pearson'),('continuous-prediction','linear'),('binary-prediction','logistic'),('monthly-demand','seasonal')]:
  go('methods-'+case)
  expect(page.locator('.reasoning-feedback')).to_have_count(0)
  page.locator('input[value="'+correct+'"]').check();page.locator('#reasoning-reason').fill('The target and sampling design fit this method.')
  page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('#reasoning-error')).to_contain_text('complete both')
  page.locator('#reasoning-assumptions').fill('Investigate independence, missing values and appropriate validation.')
  page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('.reasoning-feedback')).to_contain_text('When another method may fit')
  assert saved()['studyTools']['methods'][case]['revealed']
 checks.append('Six method decisions require rationale and assumption checks, then show selection feedback, limitations and alternatives')
 go('workshop-k8');page.locator('[data-action="workshop-load"]').click();expect(page.locator('#workshop-draft')).to_have_value('My original synthetic response')
 page.locator('[data-action="workshop-reveal"]').click();expect(page.locator('.annotated-answer section')).to_have_count(6)
 page.locator('#workshop-draft').fill('My revised synthetic explanation: I investigated, checked and documented the outcome.')
 page.locator('[data-workshop-check="contribution"]').check();assert saved()['studyTools']['workshops']['K8']['checks']==['contribution']
 page.reload();expect(page.locator('[data-workshop-check="contribution"]')).to_be_checked()
 page.locator('#workshop-draft').fill('My final synthetic explanation with a checkable result.')
 assert saved()['studyTools']['workshops']['K8']['checks']==[]
 page.once('dialog',lambda d:d.dismiss());page.locator('[data-action="workshop-use"]').click();assert saved()['ksbs']['K8']['response']=='My original synthetic response'
 page.once('dialog',lambda d:d.accept());page.locator('[data-action="workshop-use"]').click();assert saved()['ksbs']['K8']['response']=='My final synthetic explanation with a checkable result.'
 assert not saved()['ksbs']['K8']['exampleConfirmed'];assert saved()['ksbs']['K8']['coverage']==before['ksbs']['K8']['coverage']
 for ksb in ['S8','B5']:
  page.locator('#workshop-ksb').select_option(ksb);page.locator('[data-action="workshop-reveal"]').click();expect(page.locator('.annotated-answer section')).to_have_count(6)
 page.locator('#workshop-ksb').select_option('K8');expect(page.locator('#workshop-draft')).to_have_value('My final synthetic explanation with a checkable result.')
 checks.append('Workshops show six annotated aspects for K/S/B, retain per-KSB drafts, clear checks after editing and require confirmation before replacing existing responses')
 attack='<img src=x onerror="window.injected=true"> Synthetic policy note'
 go('organisation-policies');page.locator('#organisation-note').fill(attack);page.locator('#organisation-reference').fill('javascript:alert(1)');page.locator('#organisation-verified').fill('2026-11-04');page.locator('#organisation-form button[type="submit"]').click()
 go('organisation-tools');page.locator('#organisation-note').fill('Synthetic tool: SQL for repeatable queries.');page.locator('#organisation-form button[type="submit"]').click()
 go('ksb-k2');page.locator('.notebook-context summary').click();expect(page.locator('.notebook-context')).to_contain_text(attack);assert page.locator('.notebook-context img').count()==0;assert page.locator('a[href^="javascript:"]').count()==0
 go('workshop-k2');page.locator('.notebook-context summary').click();expect(page.locator('.notebook-context')).to_contain_text('javascript:alert(1)')
 assert not page.evaluate('Boolean(window.injected)')
 go('organisation-policies');expect(page.locator('#organisation-verified')).to_have_value('2026-11-04')
 page.once('dialog',lambda d:d.dismiss());page.locator('[data-action="clear-organisation"]').click();expect(page.locator('#organisation-note')).to_have_value(attack)
 checks.append('Organisation notes and verification dates persist, appear in relevant lessons/workshops and render text/reference IDs without executing markup or URLs')
 go('connections-quality');expect(page.locator('.connection-map .connection-node')).to_have_count(3)
 expect(page.locator('.connection-evidence')).to_contain_text('Synthetic quality log');expect(page.locator('.connection-evidence')).to_contain_text('Investigated a duplicate-key cause')
 page.locator('#connection-response').fill('I linked the quality dimension, resolution and root cause using QA-TEST.')
 go('connections-structure');page.locator('#connection-filter').select_option('S9');expect(page.locator('.connection-picker a')).to_have_count(1)
 go('connections-quality');expect(page.locator('#connection-response')).to_have_value('I linked the quality dimension, resolution and root cause using QA-TEST.')
 coverage=page.evaluate('window.L4_CURRICULUM.reasoning.connections.flatMap(x=>x.ksbs)');assert len(set(coverage))==37
 page.screenshot(path=str(out/'connections-desktop.png'),full_page=True)
 checks.append('Nine learning paths cover all 37 KSBs, filter by topic, link to lessons and show actual matching evidence rationales with saved combined explanations')
 # Download and restore through the user-facing controls.
 with page.expect_download() as dl:page.locator('[data-action="backup"]').first.click()
 download=dl.value;download.save_as(str(out/'synthetic-backup.json'));snapshot=json.loads((out/'synthetic-backup.json').read_text())
 incoming=copy.deepcopy(snapshot);incoming['studyTools']['organisation']['policies']['note']='Imported synthetic note'
 merge(incoming);assert saved()['studyTools']['organisation']['policies']['note']==attack
 merge(incoming,'study-organisation-policies');assert saved()['studyTools']['organisation']['policies']['note']=='Imported synthetic note'
 legacy=copy.deepcopy(snapshot);del legacy['studyTools'];merge(legacy);assert saved()['studyTools']['organisation']['policies']['note']=='Imported synthetic note'
 malformed=[]
 for category,key in [('workshops','constructor'),('repairs','__proto__'),('connections','not-a-path')]:
  invalid=copy.deepcopy(snapshot);invalid['studyTools'][category][key]={};malformed.append(invalid)
 invalid=copy.deepcopy(snapshot);invalid['studyTools']['repairs']['duplicate-join']['choice']='invented';malformed.append(invalid)
 invalid=copy.deepcopy(snapshot);invalid['studyTools']['methods']['paired-change']['reason']='';malformed.append(invalid)
 invalid=copy.deepcopy(snapshot);invalid['studyTools']['workshops']['K8']['checks']=['evidence','evidence'];malformed.append(invalid)
 invalid=copy.deepcopy(snapshot);invalid['studyTools']['organisation']['policies']['verifiedOn']='2026-02-30';malformed.append(invalid)
 for invalid in malformed:
  previous=saved();upload(invalid);expect(page.locator('#toast')).to_contain_text('Backup not imported');expect(page.locator('#restore-dialog')).not_to_be_visible();assert saved()==previous
 fresh=browser.new_context(accept_downloads=True);fresh_page=fresh.new_page();fresh_page.goto(args.url+'#plan');fresh_page.locator('#backup-file').set_input_files(str(out/'synthetic-backup.json'));expect(fresh_page.locator('#restore-dialog')).to_be_visible();fresh_page.locator('[data-action="apply-restore"]').click();expect(fresh_page.locator('#restore-dialog')).not_to_be_visible();assert fresh_page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).studyTools',KEY)==snapshot['studyTools'];fresh.close()
 go('plan')
 with page.expect_download() as dl:page.locator('[data-action="export-summary"]').click()
 dl.value.save_as(str(out/'synthetic-summary.md'));summary=(out/'synthetic-summary.md').read_text();assert 'My final synthetic explanation' in summary and 'Imported synthetic note' in summary and 'I linked the quality' in summary
 checks.append('New records round-trip in JSON and Markdown exports, merge conflicts keep current by default, old v1 imports retain new work, and malformed IDs/choices/dates/checks are rejected without mutation')
 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['repairs-chart-scale','methods-paired-change','workshop-k8','organisation-architecture','connections-quality','practice']:
   go(route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
  go('connections-quality');assert page.locator('.connection-map').bounding_box()['width']<=width
 page.set_viewport_size({'width':390,'height':900});go('connections-quality');page.locator('.connection-map').screenshot(path=str(out/'connections-mobile.png'))
 go('workshop-k8');page.screenshot(path=str(out/'workshop-mobile.png'),full_page=True)
 page.locator('[data-action="text-size"]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 go('methods-paired-change');page.locator('input[value="independent"]').focus();page.keyboard.press('ArrowDown');expect(page.locator('input[value="paired"]')).to_be_checked()
 page.set_viewport_size({'width':1440,'height':1000});go('repairs-duplicate-join');page.locator('.reasoning-feedback').screenshot(path=str(out/'repair-feedback-desktop.png'))
 # All authored data is shipped locally; file opening needs no fetch or backend.
 offline=browser.new_context();op=offline.new_page();op.on('pageerror',lambda e:errors.append(str(e)))
 file_url=(Path(__file__).resolve().parents[1]/'index.html').as_uri()
 for route in ['repairs','methods','workshop','organisation','connections']:
  op.goto(file_url+'#'+route);expect(op.locator('h1')).to_be_visible();assert 'could not load' not in op.locator('main').inner_text()
 offline.close();assert not errors,errors
 checks.append('All new routes reflow at 320/390/768/1280px, keyboard selection works, enlarged text stays within the page and direct file opening loads every new tool without JavaScript errors')
 context.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2))
print(json.dumps(dict(status='passed',checks=checks),indent=2))
