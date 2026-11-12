"""Actual 10x10 submissions, independent state, exact-set feedback and recovery."""
import argparse,copy,hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-multiple-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);c=b.new_context(service_workers='block',accept_downloads=True,viewport={'width':1440,'height':1000});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def catalog():
  if page.locator('[data-mc=catalog]').count():page.locator('[data-mc=catalog]').click()
  expect(page.locator('[data-mc-card]')).to_have_count(10)
 def restore(value,choice=None):
  page.locator('#backup-file').set_input_files({'name':'synthetic-tests.json','mimeType':'application/json','buffer':json.dumps(value).encode()});expect(page.locator('#restore-dialog')).to_be_visible()
  if choice:page.locator('[data-restore-conflict="'+choice+'"]').select_option('import')
  page.locator('[data-action=apply-restore]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 page.goto(args.url);expect(page.locator('#nav a[href="#tests"]')).to_have_count(1)
 with page.expect_download():page.locator('[data-action=backup]').first.click()
 baseline=saved();data=page.evaluate('L4_TEST_DATA');assert len(data['tests'])==10 and sum(len(t['questions']) for t in data['tests'])==100
 assert data['dataSha256']==hashlib.sha256((root/'multiple-choice-tests.json').read_bytes()).hexdigest()
 for route in ['today','library','project','practice','readiness','evidence','plan','prep']:
  page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible();assert page.locator('a[href="#tests"]').count()==1;assert page.locator('#main a[href="#tests"]').count()==0
 page.locator('#nav a[href="#tests"]').click();expect(page.locator('[data-mc-card]')).to_have_count(10);page.screenshot(path=str(out/'catalog-desktop.png'))
 for ti,t in enumerate(data['tests']):
  catalog();page.locator('[data-mc=start][data-id="'+t['id']+'"]').click();expect(page.locator('[data-mc=submit]')).to_be_disabled()
  for qi,q in enumerate(t['questions']):
   expect(page.locator('#mc-question-prompt')).to_have_text(q['prompt']);expect(page.locator('[data-mc-option]')).to_have_count(8);expect(page.locator('.mc-complete-answer')).to_have_count(0);chosen=[o['id'] for o in q['options'] if o['correct']]
   if ti==0 and qi==0:chosen=chosen[1:]+[next(o['id'] for o in q['options'] if not o['correct'])]
   for option in chosen:page.locator('[data-mc-option="'+option+'"]').check()
   if qi<9:page.locator('[data-mc=next]').click()
  expect(page.locator('#mc-progress')).to_have_text('10 of 10 questions have selections');expect(page.locator('[data-mc=submit]')).to_be_enabled();page.locator('[data-mc=submit]').click();expected=9 if ti==0 else 10
  expect(page.locator('.mc-result-score>div>strong')).to_have_text(f'{expected} / 10');expect(page.locator('.mc-review-question')).to_have_count(10)
  if ti==0:
   expect(page.locator('.mc-review-question[open]')).to_contain_text('1 required option missed · 1 incorrect option selected.');expect(page.locator('.mc-missed')).to_have_count(1);expect(page.locator('.mc-extra')).to_have_count(1);page.screenshot(path=str(out/'result-desktop.png'));page.locator('.mc-review-question[open] .mc-complete-answer').screenshot(path=str(out/'complete-answer.png'))
  assert len(saved()['multipleChoice']['attempts'])==ti+1
 state=saved();assert state['ksbs']==baseline['ksbs'] and state['evidence']==baseline['evidence'] and state['game']==baseline['game'] and state['session']==baseline['session'];assert len(state['multipleChoice']['attempts'])==10
 checks.append('All10tests completed through100real checkbox questions;8options each,keys withheld before submission,exact-set results,missed/extra feedback and no changes to KSB/evidence/reward/discussion state')
 # Result export and a full-guide jump use the real submitted selections.
 with page.expect_download() as dl:page.locator('[data-mc=export]').click()
 dl.value.save_as(str(out/'review.md'));text=(out/'review.md').read_text();assert '10/10' in text and data['tests'][-1]['questions'][0]['prompt'] in text
 page.locator('.mc-review-question[open] [data-mc=guide]').click();expect(page.locator('#lesson-full-guide')).to_have_attribute('open','');expect(page.locator('#lesson-full-guide>summary')).to_be_focused();page.locator('#nav a[href="#tests"]').click();expect(page.locator('.mc-result-score')).to_be_visible();page.reload();catalog();expect(page.locator('#celebration')).to_be_hidden()
 # Different unfinished tests keep independent selections and positions.
 page.locator('[data-mc=start][data-id=T01]').click();page.locator('[data-mc-option=A]').focus();page.keyboard.press('Space');expect(page.locator('[data-mc-option=A]')).to_be_checked();page.locator('[data-mc=next]').click();page.locator('[data-mc-option=B]').check();catalog();page.locator('[data-mc=start][data-id=T02]').click();page.locator('[data-mc-option=C]').check();catalog();page.reload();page.locator('[data-mc=start][data-id=T01]').click();expect(page.locator('h1')).to_have_text('Question 2 of 10');expect(page.locator('[data-mc-option=B]')).to_be_checked();page.locator('[data-mc=previous]').click();expect(page.locator('[data-mc-option=A]')).to_be_checked();assert set(saved()['multipleChoice']['drafts'])=={'T01','T02'}
 # Take a retest with every option selected; exact-set scoring must reject all10.
 for i in range(10):
  page.locator('[data-mc=jump][data-index="'+str(i)+'"]').click()
  for checkbox in page.locator('[data-mc-option]').all():checkbox.check()
 page.locator('[data-mc=submit]').click();expect(page.locator('.mc-result-score>div>strong')).to_have_text('0 / 10');expect(page.locator('#celebration')).to_be_hidden();assert len(saved()['multipleChoice']['attempts'])==11
 checks.append('Review export contains actual answers;source link opens detailed guide;keyboard and reload retain independent drafts;retake retains earlier history;selecting all options scores0and does not celebrate')
 # An old-v1 backup has no new section and must not erase current records.
 complete=saved();older=copy.deepcopy(complete);older.pop('multipleChoice');restore(older);assert saved()['multipleChoice']==complete['multipleChoice']
 incoming=copy.deepcopy(complete);incoming['multipleChoice']['drafts']['T02']['index']=3;restore(incoming,'multiple-choice-drafts-T02');assert saved()['multipleChoice']['drafts']['T02']['index']==3
 # Invalid choices,counts,forged scores and identifiers fail before mutation.
 for mutate in [lambda d:d['multipleChoice']['drafts']['T02'].update(index=10),lambda d:d['multipleChoice']['drafts']['T02']['answers'].update({'unknown':['A']}),lambda d:d['multipleChoice']['drafts']['T02']['answers'].update({'T02-Q01':['Z']}),lambda d:next(iter(d['multipleChoice']['attempts'].values())).update(score=10),lambda d:d['multipleChoice'].update(removed=['constructor'])]:
  before=saved();bad=copy.deepcopy(before);mutate(bad);page.locator('#backup-file').set_input_files({'name':'invalid-tests.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});expect(page.locator('#toast')).to_contain_text('Invalid multiple-choice test data');assert saved()==before
 # Deleted attempts cannot reappear from an older backup.
 catalog();old=saved();page.locator('[data-mc=history]').click();deleted=next(iter(old['multipleChoice']['attempts']));page.locator('[data-mc=delete][data-id="'+deleted+'"]').click();assert deleted not in saved()['multipleChoice']['attempts'];restore(old);assert deleted not in saved()['multipleChoice']['attempts']
 with page.expect_download() as dl:page.locator('[data-action=backup]').first.click()
 dl.value.save_as(str(out/'tests-backup.json'));backup=json.loads((out/'tests-backup.json').read_text());assert len(backup['multipleChoice']['attempts'])==10
 fresh=b.new_context(service_workers='block');other=fresh.new_page();other.goto(args.url+'#tests');other.locator('#backup-file').set_input_files(str(out/'tests-backup.json'));expect(other.locator('#restore-dialog')).to_be_visible();other.locator('[data-action=apply-restore]').click();expect(other.locator('#restore-dialog')).not_to_be_visible();assert other.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).multipleChoice',KEY)==backup['multipleChoice'];fresh.close()
 checks.append('Old-v1 merge preserves tests;per-draft conflicts require choices;malformed options/IDs/counts/forged scores fail without mutation;history deletion survives old-backup merge;fresh JSON restoration retains all tests')
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':900});catalog();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');page.locator('[data-mc=start][data-id=T02]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');assert page.locator('.mc-option').first.bounding_box()['height']>=44
  page.screenshot(path=str(out/f'question-{width}.png'));catalog();page.locator('[data-mc=review]').first.click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 page.set_viewport_size({'width':390,'height':900});page.screenshot(path=str(out/'result-phone.png'));page.evaluate('window.print=()=>{}');page.locator('[data-action=print]').click();page.emulate_media(media='print');page.pdf(path=str(out/'review.pdf'),format='A4');assert (out/'review.pdf').stat().st_size>10000;page.emulate_media(media='screen');page.evaluate('dispatchEvent(new Event("afterprint"))')
 direct=b.new_page(service_workers='block');direct.on('pageerror',lambda e:errors.append(str(e)));direct.goto((root/'index.html').as_uri()+'#tests');expect(direct.locator('[data-mc-card]')).to_have_count(10);direct.locator('[data-mc=start]').first.click();expect(direct.locator('[data-mc-option]')).to_have_count(8);direct.close()
 catalog();page.locator('[data-mc=start][data-id=T02]').click();page.evaluate('()=>{Storage.prototype.setItem=function(){throw Error("synthetic test quota")};}');page.locator('[data-mc-option=D]').check();expect(page.locator('#storage-warning')).to_contain_text('temporary memory')
 with page.expect_download() as dl:page.locator('#storage-warning [data-action=backup]').click()
 dl.value.save_as(str(out/'temporary-tests.json'));temp=json.loads((out/'temporary-tests.json').read_text());assert 'D' in temp['multipleChoice']['drafts']['T02']['answers']['T02-Q04'];assert not errors,errors
 checks.append('320/390/768/1440px layouts,44px options,print/PDF,direct-file tests and real export after failed storage passed without page errors')
 b.close()
(out/'results.json').write_text(json.dumps({'status':'passed','checks':checks,'page_errors':errors},indent=2));print(json.dumps({'status':'passed','checks':checks},indent=2))
