"""Uncertainty calculations, calibration, changed cases, briefings and evidence retrieval."""
import argparse,copy,json,math,re
from pathlib import Path
from statistics import NormalDist
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-rehearsal-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def upload(v):page.locator('#backup-file').set_input_files({'name':'synthetic.json','mimeType':'application/json','buffer':json.dumps(v).encode()})
 def merge(v,key=None):
  upload(v);expect(page.locator('#restore-dialog')).to_be_visible()
  if key:page.locator('[data-restore-conflict="'+key+'"]').select_option('import')
  page.locator('[data-action="apply-restore"]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 go('uncertainty')
 for n,sd,effect,level in [(10,1,0,90),(25,8,2,95),(50,30,-10,99),(500,1,.5,95),(100,8,0,99),(10,30,10,90),(500,30,-.5,95),(250,10,2,99)]:
  for key,v in [('n',n),('sd',sd),('effect',effect)]:page.locator('#uncertainty-'+key).evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}))}',v)
  page.locator('#uncertainty-level').select_option(str(level));se=sd*math.sqrt(2/n);z=NormalDist().inv_cdf(.5+level/200);margin=z*se
  for stat,target in [('se',se),('lower',effect-margin),('upper',effect+margin)]:assert math.isclose(float(page.locator('[data-stat="'+stat+'"]').inner_text()),target,abs_tol=.0006)
  pvalue=math.erfc(abs(effect/se)/math.sqrt(2));text=page.locator('[data-stat="p"]').inner_text();assert (pvalue<.000001 if text.startswith('<') else abs(float(text)-pvalue)<.000001)
 page.locator('#uncertainty-results details').evaluate('(el)=>el.open=true')
 rows=page.locator('#uncertainty-results tbody tr').all_text_contents();assert len(rows)==100
 values=page.locator('#uncertainty-results tbody tr').evaluate_all('(rows)=>rows.map(r=>Array.from(r.cells).map(c=>c.textContent))')
 covered=0
 for _,mean,lo,hi,contains in values:
  mean,lo,hi=map(float,[mean,lo,hi]);assert abs((hi-lo)-2*margin)<.0002
  inside=lo<=effect<=hi;assert inside==(contains=='Yes');covered+=inside
 assert page.locator('[data-stat="coverage"]').inner_text()==f'{covered} of 100'
 oldvalues=values;page.locator('[data-action="resample-intervals"]').click();assert page.locator('#uncertainty-results tbody tr').evaluate_all('(rows)=>rows.map(r=>Array.from(r.cells).map(c=>c.textContent))')!=oldvalues
 seed=saved()['rehearsal']['uncertainty']['seed'];page.reload();assert saved()['rehearsal']['uncertainty']['seed']==seed
 baseline=saved();checks.append('Eight uncertainty settings match independent NormalDist intervals and erfc p-values; all 100 simulated intervals reconcile with their displayed coverage and width; seed/settings persist')
 go('quiz');page.locator('[data-action="start-quiz"]').click()
 for confidence,correct in [('high',False),('low',True),('',True)]:
  qid=page.locator('.quiz-question .inline-badge').first.inner_text();answer=page.evaluate('(id)=>L4_CURRICULUM.activities.quiz.find(q=>q.id===id).answer',qid)
  value=answer if correct else not answer;page.locator(f'input[name="quiz-choice"][value="{str(value).lower()}"]').check();page.locator('#quiz-certainty').select_option(confidence)
  page.reload();expect(page.locator('#quiz-certainty')).to_have_value(confidence)
  page.locator('#quiz-form button[type="submit"]').click();snapshot=saved()['rehearsal']['calibration'];page.reload();assert saved()['rehearsal']['calibration']==snapshot
  page.locator('[data-action="next-quiz-question"]').click()
 assert len(saved()['rehearsal']['calibration'])==2
 pending=copy.deepcopy(saved()['learningTools']['quizSession']);go('calibration');page.locator('#calibration-filter').select_option('confident-error');expect(page.locator('.quiz-review-list li')).to_have_count(1)
 page.locator('[data-action="calibration-revisit"]').click();expect(page.locator('#quiz-form')).to_be_visible();assert saved()['learningTools']['quizSession']==pending
 page.once('dialog',lambda d:d.accept());page.locator('[data-action="end-quiz"]').click();go('calibration');page.locator('[data-action="calibration-revisit"]').click();expect(page.locator('.quiz-question')).to_be_visible()
 qid=page.locator('.quiz-question .inline-badge').first.inner_text();answer=page.evaluate('(id)=>L4_CURRICULUM.activities.quiz.find(q=>q.id===id).answer',qid);page.locator(f'input[name="quiz-choice"][value="{str(answer).lower()}"]').check();page.locator('#quiz-certainty').select_option('high');page.locator('#quiz-form button[type="submit"]').click();page.locator('[data-action="next-quiz-question"]').click();assert len(saved()['rehearsal']['calibration'])==2
 go('calibration');page.locator('#calibration-filter').select_option('unsure-correct');expect(page.locator('.quiz-review-list li')).to_have_count(1)
 assert saved()['ksbs']==baseline['ksbs'];checks.append('Confidence is captured before feedback, survives an unfinished quiz, is idempotent on reload, excludes unrated attempts and preserves an existing quiz when revisiting')
 for case,choice in [('paired','paired'),('lookup','resolve'),('policy','adjust')]:
  go('changes-'+case);page.locator('#changed-case-form button[type="submit"]').click();expect(page.locator('#changed-error')).to_contain_text('explain')
  page.locator('input[name="changed-choice"][value="'+choice+'"]').check();page.locator('#changed-reason').fill('I would revisit the changed assumption while preserving the business question.');page.locator('#changed-case-form button[type="submit"]').click();expect(page.locator('#changed-feedback')).to_contain_text('What can stay');page.reload();expect(page.locator('#changed-feedback')).to_be_visible()
 page.locator('#changed-reason').fill('A revised explanation.');expect(page.locator('#changed-feedback')).not_to_be_visible()
 checks.append('All three counterfactual cases require a choice/reason, distinguish changed and retained assumptions and preserve drafts/reveal state')
 go('briefing');page.locator('[data-action="briefing-example"]').click();expect(page.locator('.briefing-example')).to_contain_text('110')
 for field,text in [('question','Should we review capacity?'),('finding','110 versus 100 requests, a 10% increase.'),('uncertainty','Two months do not establish a trend.'),('action','Review capacity and a longer history.'),('reference','SYNTHETIC-01')]:page.locator('#briefing-'+field).fill(text)
 page.locator('#briefing-audience').select_option('technical');expect(page.locator('#briefing-finding')).to_have_value('');page.locator('#briefing-finding').fill('Same scope and denominator; (110−100)/100 = 10%.');page.locator('#briefing-form button').click()
 page.locator('#briefing-audience').select_option('lead');expect(page.locator('#briefing-finding')).to_have_value('110 versus 100 requests, a 10% increase.');page.reload();expect(page.locator('#briefing-finding')).to_have_value('110 versus 100 requests, a 10% increase.')
 with page.expect_download() as dl:page.locator('[data-action="download-briefing"]').click()
 dl.value.save_as(str(out/'briefing.md'));assert 'SYNTHETIC-01' in (out/'briefing.md').read_text()
 page.locator('#briefing-case').select_option('own');payload='<img src=x onerror="window.injected=1">';page.locator('#briefing-finding').fill(payload);expect(page.locator('#briefing-preview')).to_contain_text(payload);assert page.locator('#briefing-preview img').count()==0
 checks.append('Briefings keep separate scenario/audience drafts, provide tailored examples, update an escaped preview and download the authored draft with its source reference')
 seed=copy.deepcopy(saved());seed['evidence']=[dict(id='retrieval-test',title='Synthetic QA evidence',project='Test only',reference='QA-SYNTHETIC',reflection='Test reflection',learning='',date='2026-11-05',reviewDate='',reviewNote='',status='linked',links=[dict(id='K8',rationale='Shows my recorded quality checks.')])];merge(seed)
 go('retrieval-k8');page.locator('#retrieval-evidence').select_option('retrieval-test');page.locator('#retrieval-form button[type="submit"]').click();expect(page.locator('#retrieval-error')).to_contain_text('three explanation')
 for f in ['support','contribution','limitations']:page.locator('#retrieval-'+f).fill('Synthetic '+f+' explanation.')
 page.locator('#retrieval-form button[type="submit"]').click();expect(page.locator('#retrieval-feedback')).to_contain_text('Shows my recorded quality checks.');page.reload();expect(page.locator('#retrieval-feedback')).to_be_visible()
 go('retrieval-s10');page.locator('#retrieval-gap').fill('I need an approved statistical test output and my interpretation.');page.locator('#retrieval-form button[type="submit"]').click();expect(page.locator('#retrieval-feedback')).to_contain_text('Turn the gap')
 go('evidence');page.locator('[data-action="delete-evidence"][data-id="retrieval-test"]').click();go('retrieval-k8');expect(page.locator('main')).to_contain_text('no longer available');expect(page.locator('#retrieval-support')).to_have_value('Synthetic support explanation.');page.locator('#retrieval-form button[type="submit"]').click();expect(page.locator('#retrieval-error')).to_contain_text('available reference')
 assert saved()['ksbs']==baseline['ksbs'];checks.append('Evidence rehearsal requires support/contribution/limits, shows saved rationales after review, supports explicit gaps and retains explanations if an evidence reference is removed')
 with page.expect_download() as dl:page.locator('[data-action="backup"]').first.click()
 dl.value.save_as(str(out/'backup.json'));snapshot=json.loads((out/'backup.json').read_text());assert snapshot['rehearsal']['lastBackupOn']
 incoming=copy.deepcopy(snapshot);incoming['rehearsal']['briefings']['capacity-lead']['finding']='Imported synthetic finding';merge(incoming);assert saved()['rehearsal']['briefings']['capacity-lead']['finding']!='Imported synthetic finding';merge(incoming,'rehearsal-briefings-capacity-lead');assert saved()['rehearsal']['briefings']['capacity-lead']['finding']=='Imported synthetic finding'
 old=copy.deepcopy(snapshot);del old['rehearsal'];merge(old);assert saved()['rehearsal']['briefings']['capacity-lead']['finding']=='Imported synthetic finding'
 bads=[]
 for kind,id in [('calibration','constructor'),('changes','__proto__'),('briefings','bad'),('retrieval','K99')]:
  bad=copy.deepcopy(snapshot);bad['rehearsal'][kind][id]={};bads.append(bad)
 bad=copy.deepcopy(snapshot);bad['rehearsal']['uncertainty']['n']=0;bads.append(bad)
 bad=copy.deepcopy(snapshot);bad['rehearsal']['calibration']['Q01']['certainty']='certain';bads.append(bad)
 for bad in bads:
  prior=saved();upload(bad);expect(page.locator('#toast')).to_contain_text('Backup not imported');assert saved()==prior
 fresh=browser.new_context(accept_downloads=True);fp=fresh.new_page();fp.goto(args.url+'#plan');fp.locator('#backup-file').set_input_files(str(out/'backup.json'));expect(fp.locator('#restore-dialog')).to_be_visible();fp.locator('[data-action="apply-restore"]').click();assert fp.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).rehearsal',KEY)==snapshot['rehearsal'];fresh.close()
 checks.append('All new state and backup dates round-trip; conflict-safe merges preserve current work; old v1 imports retain new records; invalid IDs, confidence and controls are rejected')
 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['uncertainty','calibration','changes','briefing','retrieval','offline']:
   go(route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
 page.set_viewport_size({'width':390,'height':900});go('uncertainty');page.locator('#uncertainty-results').screenshot(path=str(out/'uncertainty-mobile.png'));page.locator('#practice-activity').select_option('briefing');expect(page.locator('#briefing-form')).to_be_visible();page.locator('[data-action="text-size"]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 page.set_viewport_size({'width':1440,'height':1000});go('uncertainty');page.screenshot(path=str(out/'uncertainty-desktop.png'),full_page=True)
 go('briefing');page.screenshot(path=str(out/'briefing-desktop.png'),full_page=True)
 file=ctx.new_page();file.on('pageerror',lambda e:errors.append(str(e)));file.goto((Path(__file__).resolve().parents[1]/'index.html').as_uri()+'#offline');expect(file.locator('#offline-status')).to_contain_text('Direct file opening works');file.goto((Path(__file__).resolve().parents[1]/'index.html').as_uri()+'#uncertainty');expect(file.locator('[data-stat="se"]')).to_be_visible();file.close()
 assert not errors,errors;checks.append('New routes reflow at 320/390/768/1280px, mobile activity selection works, enlarged text fits and direct-file support remains intact without page errors')
 ctx.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2));print(json.dumps(dict(status='passed',checks=checks),indent=2))
