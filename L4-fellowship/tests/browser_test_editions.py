"""Original-edition continuity and stable, fresh multi-select presentation."""
import argparse,copy,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-editions-qa');args=pa.parse_args();root=Path(__file__).resolve().parents[1];out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
KEY='l4-fellowship.v1';checks=[];errors=[];old_revision='2026-11-12-tests-1'
legacy=json.loads((root/'tests/multiple_choice_edition_one_state.json').read_text())
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);c=b.new_context(service_workers='block',accept_downloads=True,viewport={'width':1440,'height':1000});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def restore(value,choice=None):
  page.locator('#backup-file').set_input_files({'name':'synthetic-editions.json','mimeType':'application/json','buffer':json.dumps(value).encode()});expect(page.locator('#restore-dialog')).to_be_visible()
  if choice:page.locator('[data-restore-conflict="'+choice+'"]').select_option('import')
  page.locator('[data-action=apply-restore]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 def catalog():
  if page.locator('[data-mc=catalog]').count():page.locator('[data-mc=catalog]').click()
  expect(page.locator('#mc-search')).to_be_visible()
 def start(id):
  catalog();page.locator('#mc-band').select_option('all');page.locator('#mc-search').fill(id);page.locator('[data-mc=start][data-id="'+id+'"]').click()
 def order():return page.locator('[data-mc-option]').evaluate_all('(es)=>es.map(e=>e.dataset.mcOption)')
 def finish(t,correct=10):
  orders=[]
  for i,q in enumerate(t['questions']):
   page.locator('[data-mc=jump][data-index="'+str(i)+'"]').click();expect(page.locator('#mc-question-prompt')).to_have_text(q['prompt']);orders.append(order())
   for o in q['options']:page.locator('[data-mc-option="'+o['id']+'"]').set_checked(o['correct'] if i<correct else True)
  page.locator('[data-mc=submit]').click();expect(page.locator('.mc-result-score>div>strong')).to_have_text(f'{correct} / 10');return orders
 page.goto(args.url+'#tests')
 with page.expect_download():page.locator('[data-action=backup]').first.click()
 baseline=saved();data=page.evaluate('L4_TEST_DATA');original=data['editions'][old_revision];incoming=copy.deepcopy(baseline);incoming['multipleChoice']=legacy;restore(incoming)
 # Original T50 review and export retain the original key, text and alphabetic order.
 page.locator('[data-mc=review][data-id=r-edition-one-result]').click();expect(page.locator('.mc-result-score')).to_contain_text('Earlier edition');expect(page.locator('.mc-review-question').first).to_contain_text(original[49]['questions'][0]['prompt'])
 with page.expect_download() as dl:page.locator('[data-mc=export]').click()
 dl.value.save_as(str(out/'original-review.md'));text=(out/'original-review.md').read_text();assert original[49]['questions'][0]['prompt'] in text and data['tests'][49]['questions'][0]['prompt'] not in text
 for o in original[49]['questions'][0]['options']:assert o['id']+'. '+o['text'] in text
 start('T11');expect(page.locator('h1')).to_have_text('Question 3 of 10');expect(page.locator('main')).to_contain_text('Earlier edition:');expect(page.locator('#mc-question-prompt')).to_have_text(original[10]['questions'][2]['prompt']);assert order()==list('ABCDEFGH');expect(page.locator('[data-mc-option=A]')).to_be_checked();expect(page.locator('[data-mc-option=D]')).to_be_checked();assert saved()['multipleChoice']==legacy
 finish(original[10]);assert saved()['multipleChoice']['attempts']['r-edition-one-draft']['revision']==old_revision
 checks.append('Validated original T11 draft resumes and submits unchanged; original T50 review/export retains wording, score, keys and presentation')
 # A new retake gets current content. Actual UI order survives navigation and reload.
 page.locator('[data-mc=start]').click();expect(page.locator('#mc-question-prompt')).to_have_text(data['tests'][10]['questions'][0]['prompt']);first_order=order();first_record=saved()['multipleChoice']['drafts']['T11'];assert first_record['revision']==data['revision'];page.locator('[data-mc-option]').first.focus();page.keyboard.press('Space');chosen=first_order[0];saved();page.reload();start('T11');assert order()==first_order;expect(page.locator('[data-mc-option="'+chosen+'"]')).to_be_checked();expect(page.locator('.mc-option-letter')).to_have_text(list('ABCDEFGH'))
 backup=saved();fresh=b.new_context(service_workers='block');other=fresh.new_page();other.goto(args.url+'#tests');other.locator('#backup-file').set_input_files({'name':'synthetic-shuffled-backup.json','mimeType':'application/json','buffer':json.dumps(backup).encode()});other.locator('[data-action=apply-restore]').click();expect(other.locator('#restore-dialog')).not_to_be_visible();other.locator('#mc-search').fill('T11');other.locator('[data-mc=start]').click();assert other.locator('[data-mc-option]').evaluate_all('(es)=>es.map(e=>e.dataset.mcOption)')==first_order;expect(other.locator('[data-mc-option="'+chosen+'"]')).to_be_checked();fresh.close()
 first_orders=finish(data['tests'][10],1);expect(page.locator('#celebration-detail')).to_have_text('1/10 answers fully correct. Review the remaining 9.')
 # Feedback and exported letters describe the displayed positions, not canonical IDs.
 review=page.locator('.mc-review-question').first;review.locator('summary').click() if review.get_attribute('open') is None else None
 by={o['id']:o for o in data['tests'][10]['questions'][0]['options']}
 for i,id in enumerate(first_orders[0]):expect(review.locator('.mc-option-review>li').nth(i).locator('p').first).to_have_text(by[id]['text']);expect(review.locator('.mc-review-option-label').nth(i)).to_contain_text(chr(65+i)+' ·')
 with page.expect_download() as dl:page.locator('[data-mc=export]').click()
 dl.value.save_as(str(out/'shuffled-review.md'));text=(out/'shuffled-review.md').read_text()
 for i,id in enumerate(first_orders[0]):assert chr(65+i)+'. '+by[id]['text'] in text
 catalog();expect(page.locator('[data-mc-card=T11] .mc-card-status')).to_contain_text('Best in this edition: 1/10');start('T11');second_id=saved()['multipleChoice']['drafts']['T11']['id'];assert second_id!=first_record['id'];second_orders=[]
 for i in range(10):page.locator('[data-mc=jump][data-index="'+str(i)+'"]').click();second_orders.append(order())
 assert first_orders!=second_orders
 checks.append('Current retake gets new questions; shuffled order survives reload/JSON restore; keyboard selections, feedback and exported letters agree; subsequent retake differs; best score stays within its edition')
 # Conflicts retain the local edition by default and accept the old one only explicitly.
 current=saved();restore(incoming);assert saved()['multipleChoice']['drafts']['T11']==current['multipleChoice']['drafts']['T11'] # submitted old draft cannot resurrect
 new_old=copy.deepcopy(incoming);new_old['multipleChoice']['drafts']['T11']['id']='r-other-old-draft';restore(new_old);assert saved()['multipleChoice']['drafts']['T11']['id']==second_id
 restore(new_old,'multiple-choice-drafts-T11');assert saved()['multipleChoice']['drafts']['T11']['id']=='r-other-old-draft';expect(page.locator('#mc-question-prompt')).to_have_text(original[10]['questions'][2]['prompt']);assert order()==list('ABCDEFGH')
 before=saved()
 for mutate in [lambda s:s['multipleChoice']['drafts']['T11'].update(revision=data['revision']),lambda s:s['multipleChoice']['drafts']['T11'].update(revision='unknown')]:
  bad=copy.deepcopy(before);mutate(bad);page.locator('#backup-file').set_input_files({'name':'invalid-edition.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});expect(page.locator('#toast')).to_contain_text('Invalid multiple-choice test data');assert saved()==before
 catalog();page.locator('[data-mc=delete][data-id=r-edition-one-result]').click();restore(incoming);assert 'r-edition-one-result' not in saved()['multipleChoice']['attempts']
 now=saved();assert now['ksbs']==baseline['ksbs'] and now['evidence']==baseline['evidence'] and now['game']==baseline['game']
 checks.append('Mixed-edition conflicts keep local data by default; explicit replacement uses old bank; cross-edition/unknown imports fail before mutation; old tombstones block resurrection; learning/evidence/rewards unchanged')
 # All new packs are required before any learner state is read or written.
 broken=b.new_context(service_workers='block');broken.add_init_script('localStorage.setItem('+json.dumps(KEY)+','+json.dumps(json.dumps(now))+');window.stateReads=0;window.stateWrites=0;const read=Storage.prototype.getItem,write=Storage.prototype.setItem;Storage.prototype.getItem=function(k){if(k==='+json.dumps(KEY)+')window.stateReads++;return read.call(this,k)};Storage.prototype.setItem=function(k,v){if(k==='+json.dumps(KEY)+')window.stateWrites++;return write.call(this,k,v)};');broken.route('**/test-packs/revised-3.js*',lambda r:r.abort());badpage=broken.new_page();badpage.goto(args.url+'#tests');expect(badpage.locator('h1')).to_have_text('The answer bank could not load.');assert badpage.evaluate('[stateReads,stateWrites]')==[0,0];assert badpage.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)==now;broken.close()
 checks.append('Missing revised pack stops boot before touching learner state')
 # Responsive new content and direct-file loading, including the current edition.
 start('T50')
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');page.screenshot(path=str(out/f'question-{width}.png'))
 direct=b.new_page(service_workers='block');direct.on('pageerror',lambda e:errors.append(str(e)));direct.goto((root/'index.html').as_uri()+'#tests');direct.locator('#mc-search').fill('T48');direct.locator('[data-mc=start]').click();expect(direct.locator('#mc-question-prompt')).to_have_text(data['tests'][47]['questions'][0]['prompt']);assert direct.evaluate('L4_TEST_DATA.revision')==data['revision'];direct.close();assert not errors,errors;b.close()
 checks.append('320/390/768/1440px new scenarios and direct-file revised edition work without page errors')
(out/'results.json').write_text(json.dumps({'status':'passed','checks':checks},indent=2));print(json.dumps({'status':'passed','checks':checks},indent=2))
