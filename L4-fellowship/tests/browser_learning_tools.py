"""Labs, scenario branches and misconception review; run against the scoped local server."""
import argparse
from datetime import datetime,timezone
import json
import math
from pathlib import Path
import sqlite3
import statistics
from playwright.sync_api import sync_playwright,expect

parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8000/');parser.add_argument('--output',default='/tmp/l4-learning-tools-qa');args=parser.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True);KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce',timezone_id='UTC')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.clock.install(time=datetime(2026,11,4,12,tzinfo=timezone.utc))
 def go(route):
  page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
 def metrics():return [float(v) for v in page.locator('.lab-metrics strong').all_text_contents()]
 go('labs-statistics')
 assert metrics()==[4,3,5]
 page.locator('#lab-outlier').focus();page.keyboard.press('End')
 assert page.locator('#lab-outlier').input_value()=='80'
 assert metrics()==[18.4,3,5]
 page.locator('#lab-missing').select_option('zero')
 assert math.isclose(metrics()[0],statistics.mean([2,3,3,4,80,0]),abs_tol=.0006)
 assert metrics()[1:]==[3,6]
 page.locator('#lab-missing').select_option('median')
 assert math.isclose(metrics()[0],statistics.mean([2,3,3,4,80,3]),abs_tol=.0006)
 page.locator('[data-lab-field="excludeOutlier"]').check()
 assert metrics()==[3,3,5]
 page.reload();assert metrics()==[3,3,5]
 assert saved()['learningTools']['labs']['statistics']['outlier']==80
 page.locator('[data-action="reset-lab"]').click();assert metrics()==[4,3,5]
 checks.append('Outlier, exclusion and three missing-value treatments reconcile with independent Python statistics; controls persist and reset locally')

 go('labs-joins')
 con=sqlite3.connect(':memory:');con.executescript('CREATE TABLE requests(id TEXT,k TEXT,v INTEGER); CREATE TABLE lookup(k TEXT,label TEXT);')
 con.executemany('INSERT INTO requests VALUES (?,?,?)',[('R1','A',10),('R2','A',20),('R3','B',30),('R4','X',40)])
 for duplicate in [True,False]:
  con.execute('DELETE FROM lookup');con.executemany('INSERT INTO lookup VALUES (?,?)',[('A','Alpha'),('B','Beta'),('C','Gamma')]+([('A','Conflicting Alpha')] if duplicate else []))
  page.locator('#lab-duplicate').set_checked(duplicate)
  for operation,sql in [('inner','INNER JOIN'),('left','LEFT JOIN'),('right','RIGHT JOIN'),('full','FULL OUTER JOIN')]:
   page.locator('#lab-join-type').select_option(operation)
   rows=con.execute(f'SELECT requests.id,requests.v FROM requests {sql} lookup ON requests.k=lookup.k').fetchall()
   expected=[len(rows),len({r[0] for r in rows if r[0]}),sum(r[1] or 0 for r in rows)]
   assert metrics()==expected,(operation,duplicate,metrics(),expected)
 for operation,count,total in [('union',5,150),('unionall',6,180)]:
  page.locator('#lab-join-type').select_option(operation)
  assert metrics()==[count,5,total]
  expect(page.locator('#lab-duplicate')).to_be_disabled()
 page.reload();assert metrics()==[6,5,180]
 checks.append('Four joins with/without duplicate keys match actual SQLite row counts, distinct requests and sums; UNION and UNION ALL append correctly')

 go('labs-forecast');series=[116,120,121,125,128,131,133,138,140,144,149,151]
 for n in [6,7,8,9]:
  page.locator('#lab-window').select_option(str(n))
  slope,intercept=statistics.linear_regression(range(1,n+1),series[:n])
  for horizon in [1,3,6]:
   page.locator('#lab-horizon').select_option(str(horizon));actual=series[n:n+horizon]
   for model in ['trend','naive']:
    page.locator('#lab-model').select_option(model)
    predicted=[intercept+slope*(n+i+1) if model=='trend' else series[n-1] for i in range(len(actual))]
    expected=math.sqrt(statistics.mean([(a-b)**2 for a,b in zip(actual,predicted)]))
    baseline=math.sqrt(statistics.mean([(a-series[n-1])**2 for a in actual]))
    values=metrics();assert math.isclose(values[0],expected,abs_tol=.0006) and math.isclose(values[1],baseline,abs_tol=.0006) and values[2]==len(actual)
 page.locator('#lab-window').select_option('9');page.locator('#lab-horizon').select_option('6');page.locator('#lab-model').select_option('trend')
 assert metrics()==[2.160,8.524,3]
 expect(page.locator('#lab-result')).to_contain_text('3 projections do not enter RMSE')
 assert page.locator('#lab-result tbody tr').count()==6
 page.screenshot(path=str(out/'forecast-desktop.png'),full_page=True)
 checks.append('24 forecast configurations match independent regressions/RMSE; only later available actuals enter error, with separate unknown projections')

 go('scenarios-quality-deadline')
 def choose(choice,reason='Synthetic QA reasoning: assess the risk, authority and validation before delivery.'):
  page.locator(f'input[name="scenario-choice"][value="{choice}"]').check()
  page.locator('#scenario-reason').fill(reason)
  page.locator('#scenario-form button[type="submit"]').click()
 page.locator('#scenario-form button[type="submit"]').click()
 expect(page.locator('#scenario-error')).to_contain_text('Choose an approach')
 assert page.locator('#scenario-reason').get_attribute('maxlength')=='2000'
 page.locator('#scenario-reason').fill('Draft justification survives reload.')
 page.reload();expect(page.locator('#scenario-reason')).to_have_value('Draft justification survives reload.')
 choose('drop','QA <img src=x onerror="window.__xss=1"> chosen to inspect the assumption.')
 expect(page.locator('[data-node]')).to_have_attribute('data-node','disagreement')
 choose('confirm');expect(page.locator('[data-node]')).to_have_attribute('data-node','owner')
 choose('limited');expect(page.locator('[data-node]')).to_have_attribute('data-node','limited')
 page.reload();expect(page.locator('[data-node]')).to_have_attribute('data-node','limited')
 assert len(saved()['learningTools']['scenarios']['quality-deadline']['trail'])==3
 assert page.evaluate('window.__xss') is None
 page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-action="restart-scenario"]').click()
 choose('footnote');choose('continue');expect(page.locator('[data-node]')).to_have_attribute('data-node','unresolved')
 go('scenarios-conflicting-requirements');choose('align');choose('priority')
 expect(page.locator('[data-node]')).to_have_attribute('data-node','tradeoff')
 go('scenarios-scope-change');choose('absorb');choose('reset');choose('baseline')
 expect(page.locator('[data-node]')).to_have_attribute('data-node','transparent')
 page.screenshot(path=str(out/'scenario-desktop.png'),full_page=True)
 checks.append('All three scenarios branch on real choices; justifications are required, drafts/outcomes survive reload, risky and defensible alternatives differ, and text stays escaped')

 go('quiz');assert saved()['learningTools']['quiz']=={}
 page.locator('[data-action="start-quiz"]').click()
 expect(page.locator('.quiz-statement')).to_contain_text('left join always')
 expect(page.locator('.quiz-feedback')).to_have_count(0)
 page.locator('#quiz-form button[type="submit"]').click();expect(page.locator('#quiz-error')).to_contain_text('Choose True or False')
 answers=page.evaluate('Object.fromEntries(window.L4_CURRICULUM.activities.quiz.map(q=>[q.id,q.answer]))')
 ids=[]
 for i in range(5):
  qid=page.locator('.quiz-question .session-strip .inline-badge').inner_text();ids.append(qid)
  choice=not answers[qid] if i==0 else answers[qid]
  page.locator(f'input[name="quiz-choice"][value="{str(choice).lower()}"]').check()
  page.locator('#quiz-reason').fill('QA reasoning <img src=x onerror="window.__xss=1">')
  page.locator('#quiz-form button[type="submit"]').click()
  expect(page.locator('.quiz-feedback')).to_be_visible()
  if i==0:
   assert saved()['learningTools']['quiz']['Q01']['nextReview']=='2026-11-05'
   page.reload();expect(page.locator('.quiz-feedback')).to_be_visible()
   assert saved()['learningTools']['quiz']['Q01']['attempts']==1
  page.locator('[data-action="next-quiz-question"]').click()
  if i==0:
   page.locator('#quiz-reason').fill('Unfinished QA reasoning.')
   page.locator('[data-action="pause-quiz"]').click();page.reload()
   expect(page.locator('.tool-cards a[href="#quiz"]')).to_contain_text('Resume your saved quiz')
   page.locator('.tool-cards a[href="#quiz"]').click()
   expect(page.locator('#quiz-reason')).to_have_value('Unfinished QA reasoning.')
 assert ids==['Q01','Q02','Q03','Q04','Q05']
 assert page.evaluate('window.__xss') is None
 assert saved()['learningTools']['quizSession'] is None
 page.locator('#quiz-mode').select_option('mistakes')
 expect(page.locator('[data-action="start-quiz"]')).to_have_text('Start 1-question quiz')
 page.clock.fast_forward(24*60*60*1000)
 page.locator('#quiz-mode').select_option('due')
 expect(page.locator('[data-action="start-quiz"]')).to_have_text('Start 1-question quiz')
 page.locator('[data-action="start-quiz"]').click()
 page.locator('input[name="quiz-choice"][value="false"]').check();page.locator('#quiz-form button[type="submit"]').click()
 record=saved()['learningTools']['quiz']['Q01'];assert record['attempts']==2 and record['correct']==1 and record['nextReview']=='2026-11-12'
 page.screenshot(path=str(out/'quiz-feedback-desktop.png'),full_page=True)
 page.locator('[data-action="next-quiz-question"]').click()
 state=saved();assert all(k['recall']=='none' and k['learning']=='new' and not k['exampleConfirmed'] for k in state['ksbs'].values()) and not state['evidence'] and not state['attempts']
 checks.append('30-question quiz reveals explanations only after submission, counts once through reload, resumes drafts, schedules mistakes and due reviews, and leaves KSB/evidence status separate')

 go('ksb-k8');page.locator('#my-response').fill('QA personal response retained independently of practice tools.');page.locator('[data-action="save-response"]').click()
 with page.expect_download() as info:page.locator('.topbar [data-action="backup"]').click()
 original=json.loads(Path(info.value.path()).read_text())
 def import_data(data):
  page.set_input_files('#backup-file',{'name':'tools-backup.json','mimeType':'application/json','buffer':json.dumps(data).encode()})
 invalid=[]
 bad=json.loads(json.dumps(original));bad['learningTools']['quiz']['constructor']={'attempts':1};invalid.append(bad)
 bad=json.loads(json.dumps(original));bad['learningTools']['quiz']['__proto__']={'attempts':1};invalid.append(bad)
 bad=json.loads(json.dumps(original));bad['learningTools']['labs']['forecast']['window']=99;invalid.append(bad)
 bad=json.loads(json.dumps(original));bad['learningTools']['scenarios']['quality-deadline']['trail'][0]['node']='owner';invalid.append(bad)
 for bad in invalid:
  import_data(bad);expect(page.locator('#toast')).to_contain_text('Backup not imported')
  assert saved()==original or saved()=={k:v for k,v in original.items() if k!='exportedOn'}
 incoming=json.loads(json.dumps(original));incoming['learningTools']['quiz']['Q30']={'attempts':1,'correct':1,'streak':1,'lastChoice':True,'lastAttempt':'2026-11-05','nextReview':'2026-11-12'}
 go('labs-statistics');page.locator('#lab-outlier').focus();page.keyboard.press('End');page.locator('#lab-missing').select_option('median');page.wait_for_timeout(350)
 import_data(incoming);expect(page.locator('#restore-dialog')).to_be_visible();expect(page.locator('#restore-content')).to_contain_text('misconception records')
 page.locator('[data-action="apply-restore"]').click()
 assert saved()['learningTools']['labs']['statistics']['outlier']==80
 assert 'Q30' in saved()['learningTools']['quiz']
 assert saved()['ksbs']['K8']['response']==original['ksbs']['K8']['response']
 old={'version':1,'settings':{},'ksbs':{'K9':{'response':'Legacy QA response without new tool fields.'}},'evidence':[],'attempts':[],'session':None,'studySession':None}
 import_data(old);page.locator('[data-action="apply-restore"]').click()
 assert 'Q30' in saved()['learningTools']['quiz'] and saved()['ksbs']['K9']['response'].startswith('Legacy QA')
 import_data(original);page.locator('#restore-mode').select_option('replace');page.locator('#confirm-replace').check();page.locator('[data-action="apply-restore"]').click()
 restored=saved();assert restored['learningTools']==original['learningTools'] and restored['ksbs']['K8']['response']==original['ksbs']['K8']['response']
 checks.append('New tool data round-trips through JSON; merge retains conflicts and adds records; old v1 imports preserve new work; malformed graphs, IDs and control values are rejected without mutation')

 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['practice','labs-statistics','labs-joins','labs-forecast','scenarios-quality-deadline','scenarios-conflicting-requirements','scenarios-scope-change','quiz']:
   go(route);assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,route)
   if route=='labs-forecast':
    bounds=page.locator('.lab-month-label:visible').evaluate_all('(els)=>els.map(el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right};})')
    assert all(bounds[i]['right']<=bounds[i+1]['left'] for i in range(len(bounds)-1)),(width,bounds)
  if width==390:
   go('labs-forecast');page.screenshot(path=str(out/'forecast-mobile.png'),full_page=True)
   go('scenarios-scope-change');page.screenshot(path=str(out/'scenario-mobile.png'),full_page=True)
   go('quiz')
   if page.locator('[data-action="clear-quiz-filters"]').count():page.locator('[data-action="clear-quiz-filters"]').click()
   page.locator('[data-action="start-quiz"]').click();page.screenshot(path=str(out/'quiz-mobile.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});go('labs-statistics');page.locator('[data-action="text-size"]').click();assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 checks.append('All new views reflow at 320/390/768/1280px; range control works by keyboard and enlarged text does not cause page overflow')
 direct=browser.new_page();direct.goto((Path(__file__).resolve().parent.parent/'index.html').as_uri()+'#labs-forecast');expect(direct.locator('.lab-metrics')).to_be_visible()
 direct.goto((Path(__file__).resolve().parent.parent/'index.html').as_uri()+'#quiz');expect(direct.locator('[data-action="start-quiz"]')).to_be_visible()
 checks.append('Analysis labs and misconception data load directly from disk without fetch or external libraries')
 assert not errors,errors
 browser.close()

report={'status':'passed','checks':checks,'page_errors':errors,'screenshots':[p.name for p in out.glob('*.png')]};(out/'results.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
