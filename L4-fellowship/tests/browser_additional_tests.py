"""Forty appended tests, original-release progress and a browsable fifty-test bank."""
import argparse,copy,hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-additional-tests-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);c=b.new_context(service_workers='block',accept_downloads=True,viewport={'width':1440,'height':1000});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 def saved():page.wait_for_timeout(350);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def restore(value,choice=None):
  page.locator('#backup-file').set_input_files({'name':'synthetic-expanded-tests.json','mimeType':'application/json','buffer':json.dumps(value).encode()});expect(page.locator('#restore-dialog')).to_be_visible()
  if choice:page.locator('[data-restore-conflict="'+choice+'"]').select_option('import')
  page.locator('[data-action=apply-restore]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 def catalog():
  if page.locator('[data-mc=catalog]').count():page.locator('[data-mc=catalog]').click()
  expect(page.locator('#mc-search')).to_be_visible()
 def start(id):
  catalog();page.locator('#mc-band').select_option('all');page.locator('#mc-search').fill(id);expect(page.locator('[data-mc-card]')).to_have_count(1);page.locator('[data-mc=start][data-id="'+id+'"]').click()
 page.goto(args.url+'#tests');expect(page.locator('h1')).to_have_text('Tests');expect(page.locator('.mc-intro-number strong')).to_have_text('500');expect(page.locator('[data-mc-card]')).to_have_count(10);data=page.evaluate('L4_TEST_DATA');assert len(data['tests'])==50
 for i in range(1,5):
  assert data['packSha256']['additional-'+str(i)]==hashlib.sha256((root/f'test-packs/additional-{i}.json').read_bytes()).hexdigest()
  assert data['revisedPackSha256']['revised-'+str(i)]==hashlib.sha256((root/f'test-packs/revised-{i}.json').read_bytes()).hexdigest()
 with page.expect_download():page.locator('[data-action=backup]').first.click()
 baseline=saved();legacy=json.loads((root/'tests/multiple_choice_legacy_state.json').read_text());old=copy.deepcopy(baseline);old['multipleChoice']=legacy;restore(old);assert saved()['multipleChoice']==legacy
 page.screenshot(path=str(out/'catalog-desktop.png'));page.locator('[data-mc=show-new]').click();seen=[]
 for n in range(4):
  ids=page.locator('[data-mc-card]').evaluate_all('(es)=>es.map(e=>e.dataset.mcCard)');assert ids==[f'T{i:02}' for i in range(11+n*10,21+n*10)];seen+=ids
  if n<3:page.locator('[data-mc=catalog-next]').click()
 expect(page.locator('[data-mc=catalog-next]')).to_be_disabled();assert len(set(seen))==40;page.locator('[data-mc=catalog-prev]').click();expect(page.locator('[data-mc-card]').first).to_have_attribute('data-mc-card','T31')
 page.locator('#mc-search').fill('');page.locator('#mc-search').press_sequentially('FORECAST');expect(page.locator('#mc-search')).to_be_focused();expect(page.locator('#mc-search')).to_have_value('FORECAST');assert page.locator('[data-mc-card=T38]').count()==1
 page.locator('#mc-search').fill('<img src=x onerror=window.testInjected=1>');expect(page.locator('.mc-catalog-count')).to_contain_text('No tests match');assert page.evaluate('window.testInjected') is None;page.locator('[data-mc=filter-clear]').first.click();expect(page.locator('[data-mc-card]').first).to_have_attribute('data-mc-card','T01')
 checks.append('All50tests/500questions and four matching pack hashes load;new collection reaches all40IDs;page boundaries,case-insensitive topic search,focus/caret,no-match reset and inert input work')
 # New/old drafts coexist and resume without rewriting legacy records.
 start('T11');page.locator('[data-mc-option=A]').check();page.locator('[data-mc=jump][data-index="2"]').click();page.locator('[data-mc-option=D]').check();start('T50');page.locator('[data-mc-option=C]').check();saved();page.reload();page.locator('#mc-band').select_option('drafts');assert set(page.locator('[data-mc-card]').evaluate_all('(es)=>es.map(e=>e.dataset.mcCard)'))=={'T02','T11','T50'};start('T11');expect(page.locator('h1')).to_have_text('Question 3 of 10');expect(page.locator('[data-mc-option=D]')).to_be_checked();assert saved()['multipleChoice']['drafts']['T02']==legacy['drafts']['T02']
 # Actual checkbox interaction and submission for each of400newquestions.
 for ti,t in enumerate(data['tests'][10:]):
  start(t['id'])
  for i,q in enumerate(t['questions']):
   page.locator('[data-mc=jump][data-index="'+str(i)+'"]').click();expect(page.locator('#mc-question-prompt')).to_have_text(q['prompt']);expect(page.locator('[data-mc-option]')).to_have_count(8);expect(page.locator('.mc-complete-answer')).to_have_count(0)
   for option in q['options']:page.locator('[data-mc-option="'+option['id']+'"]').set_checked(option['correct'])
  page.locator('[data-mc=submit]').click();expect(page.locator('.mc-result-score>div>strong')).to_have_text('10 / 10');expect(page.locator('.mc-review-question')).to_have_count(10)
  if t['id'] in ['T20','T23','T35','T38']:page.screenshot(path=str(out/(t['id']+'-result.png')))
  print(t['id']+' submitted and scored10/10',flush=True)
 current=saved();assert len(current['multipleChoice']['attempts'])==41;assert current['multipleChoice']['attempts']['r-legacy-result']==legacy['attempts']['r-legacy-result'];assert current['multipleChoice']['drafts']==legacy['drafts'];assert current['ksbs']==baseline['ksbs'] and current['evidence']==baseline['evidence'] and current['game']==baseline['game'];assert page.evaluate('L4_TESTS.score('+json.dumps(legacy['attempts']['r-legacy-result'])+').total')==9
 checks.append('All40newtests submitted through400actual multi-select questions with10/10results;original-release9/10result and unfinished draft remain exact;KSB/evidence/reward state unchanged')
 # Older backups merge without erasing new submissions.
 restore(old);assert len(saved()['multipleChoice']['attempts'])==41;start('T47');page.locator('[data-mc-option=A]').check();incoming=saved();incoming['multipleChoice']['drafts']['T47']['index']=5;restore(incoming,'multiple-choice-drafts-T47');expect(page.locator('h1')).to_have_text('Question 6 of 10')
 before=saved();bad=copy.deepcopy(before);bad['multipleChoice']['drafts']['T51']=copy.deepcopy(bad['multipleChoice']['drafts']['T47']);page.locator('#backup-file').set_input_files({'name':'invalid-new-id.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});expect(page.locator('#toast')).to_contain_text('Invalid multiple-choice test data');assert saved()==before
 with page.expect_download() as dl:page.locator('[data-action=backup]').first.click()
 dl.value.save_as(str(out/'expanded-backup.json'));backup=json.loads((out/'expanded-backup.json').read_text());fresh=b.new_context(service_workers='block');other=fresh.new_page();other.goto(args.url+'#tests');other.locator('#backup-file').set_input_files(str(out/'expanded-backup.json'));other.locator('[data-action=apply-restore]').click();expect(other.locator('#restore-dialog')).not_to_be_visible();assert other.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).multipleChoice',KEY)==backup['multipleChoice'];fresh.close()
 catalog();last=next(a for a in backup['multipleChoice']['attempts'].values() if a['testId']=='T50');page.locator('[data-mc=delete][data-id="'+last['id']+'"]').click();restore(backup);assert last['id'] not in saved()['multipleChoice']['attempts'];page.reload();expect(page.locator('#celebration')).to_be_hidden()
 checks.append('Old-release backup retains all40newresults;new draft conflicts are explicit;T51is rejected without mutation;fresh-profile backup restores old/new data;removed new results cannot reappear from older backups;reload does not celebrate')
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':900});catalog();page.locator('[data-mc=show-new]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');page.screenshot(path=str(out/f'catalog-{width}.png'));start('T50');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');assert page.locator('.mc-option').first.bounding_box()['height']>=44
 page.set_viewport_size({'width':390,'height':900});page.screenshot(path=str(out/'new-question-phone.png'));catalog();page.locator('#mc-band').select_option('all');page.locator('#mc-search').fill('T38');page.locator('[data-mc-card=T38] [data-mc=review]').click();page.screenshot(path=str(out/'result-phone.png'))
 direct=b.new_page(service_workers='block');direct.on('pageerror',lambda e:errors.append(str(e)));direct.goto((root/'index.html').as_uri()+'#tests');direct.locator('#mc-search').fill('T50');direct.locator('[data-mc=start]').click();expect(direct.locator('[data-mc-option]')).to_have_count(8);assert direct.evaluate('L4_TEST_DATA.tests.length')==50;direct.close();assert not errors,errors
 checks.append('320/390/768/1440px catalogue,filters,paging,new questions/results,touch targets and direct-file T50work without page errors')
 b.close()
(out/'results.json').write_text(json.dumps({'status':'passed','checks':checks,'errors':errors},indent=2));print(json.dumps({'status':'passed','checks':checks},indent=2))
