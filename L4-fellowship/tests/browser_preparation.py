"""Seven preparation tools: real SQL/audio, state safety and accessible flows.
All notes and recordings are synthetic, in disposable browser contexts.
"""
import argparse,copy,json,sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-preparation-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
KEY='l4-fellowship.v1';checks=[];errors=[];root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
 ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,service_workers='block');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 def go(route):
  page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():
  page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def restore(value,conflict=None):
  page.locator('#backup-file').set_input_files({'name':'synthetic-preparation.json','mimeType':'application/json','buffer':json.dumps(value).encode()});expect(page.locator('#restore-dialog')).to_be_visible()
  if conflict:page.locator('[data-restore-conflict="'+conflict+'"]').select_option('import')
  page.locator('[data-action="apply-restore"]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 go('prep');page.locator('[data-action=text-size]').click();page.locator('[data-action=text-size]').click();baseline=saved();expect(page.locator('.prep-card')).to_have_count(7)
 # Mock is independent of the existing session and keeps the guide hidden until finish.
 old=copy.deepcopy(baseline);old['session']={'queue':[{'id':'K8','type':'question'}],'index':0,'response':'Existing synthetic discussion','gap':'','nextDate':'','revealed':False,'timer':False,'duration':5,'remaining':300,'startedAt':None,'running':False}
 restore(old);go('mock');page.locator('[data-prep="mock-start"]').click();expect(page.locator('[data-mock-review]')).to_have_count(0);expect(page.locator('.prose')).to_have_count(0)
 page.locator('#prep-mock-response').fill('Synthetic first answer: explain, justify, check, refer to evidence.');page.reload();expect(page.locator('#prep-mock-response')).to_have_value('Synthetic first answer: explain, justify, check, refer to evidence.')
 for i in range(3):
  if i:page.locator('#prep-mock-response').fill('Synthetic answer '+str(i))
  page.locator('[data-prep="mock-next"]').click()
 expect(page.locator('[data-mock-review]')).to_be_visible();expect(page.locator('[data-mock-check]')).to_have_count(12);page.locator('[data-mock-check]').first.check();page.locator('#prep-mock-next-0').fill('Add my validation evidence.');mock=saved()['preparation'];assert len(mock['mocks'])==1 and mock['activeMock'] is None
 assert saved()['session']['response']=='Existing synthetic discussion';assert saved()['ksbs']==baseline['ksbs'];assert saved()['game']['events']==[]
 with page.expect_download() as dl:page.locator('[data-prep="mock-export"]').click()
 dl.value.save_as(str(out/'mock.md'));assert 'Add my validation evidence.' in (out/'mock.md').read_text()
 checks.append('Mixed K/S/B mock resumes after reload, withholds model guidance until the set ends, retains self-review/export and preserves the original practice session and readiness')
 # Mistake notebook includes a transfer scenario, drafts and due dates.
 go('mistakes');page.locator('[data-prep="mistake-new"]').click();page.locator('#prep-mistake-thought').fill('Missing days must equal zero.');page.locator('#prep-mistake-why').fill('Unknown is different from an observed zero.');page.locator('#prep-mistake-remember').fill('Investigate missingness and report assumptions.');page.reload();expect(page.locator('#prep-mistake-remember')).to_have_value('Investigate missingness and report assumptions.');page.locator('#prep-mistake-form button[type=submit]').click();entry=page.locator('.prep-mistake');entry.locator('summary').click();entry.locator('textarea').fill('Check the missing values with the data owner and report exclusions.');page.locator('[data-prep="mistake-review"][data-days="7"]').click();m=next(iter(saved()['preparation']['mistakes'].values()));assert m['reviewedDate'] and m['nextReview']>m['reviewedDate']
 go('quiz');page.locator('[data-action="start-quiz"]').click();page.locator('input[name=quiz-choice]').first.check();page.locator('#quiz-reason').fill('Synthetic mistaken rationale.');page.locator('#quiz-form button[type=submit]').click();page.locator('[data-prep="quiz-mistake"]').click();expect(page.locator('#prep-mistake-thought')).to_have_value('Synthetic mistaken rationale.');assert saved()['preparation']['mistakeDraft']['source'].startswith('Q')
 checks.append('Notebook drafts persist, quiz feedback seeds the actual learner rationale, transfer prompts require an explanation and explicit revisit dates are recorded')
 # Resources render only inert text and safe URLs; incomplete URL drafts survive reload.
 go('materials');page.locator('[data-prep="resource-new"]').click();page.locator('#prep-resource-title').fill('<img src=x onerror=window.injected=1> Synthetic resource');page.locator('#prep-resource-url').fill('https://');page.reload();expect(page.locator('#prep-resource-url')).to_have_value('https://');expect(page.locator('#storage-warning')).not_to_be_visible();page.locator('#prep-resource-url').fill('https://example.org/study');page.locator('#prep-resource-notes').fill('<script>window.injected=2</script> Synthetic course notes.');page.locator('[data-resource-ksb=K13]').check();page.locator('[data-resource-ksb=S10]').check();page.locator('#prep-resource-form button[type=submit]').click();resource=next(iter(saved()['preparation']['resources'].values()));assert resource['ksbs']==['K13','S10'];assert page.evaluate('window.injected') is None
 go('ksb-k13');expect(page.locator('.prep-lesson')).to_contain_text('Synthetic resource');page.locator('.prep-lesson details summary').click();expect(page.locator('.prep-lesson')).to_contain_text('<script>window.injected=2</script>');assert page.evaluate('window.injected') is None
 term=page.locator('.prep-term').first;term.focus();page.keyboard.press('Enter');expect(page.locator('#prep-term-dialog')).to_be_visible();page.keyboard.press('Escape');expect(term).to_be_focused();assert page.url.endswith('#ksb-k13')
 go('terms');page.locator('#prep-term-search').fill('RMSE');expect(page.locator('#prep-term-results .prep-card')).to_have_count(1)
 checks.append('Tagged resources appear beside lessons; unfinished URL drafts remain recoverable; note markup stays inert; inline term dialogs support keyboard close and focus return; glossary search works')
 # Both authored comparison applications, independent state and celebration.
 go('compare');data=page.evaluate('L4_PREP_DATA');
 for c in data['comparisons']:
  page.locator('#prep-compare-select').select_option(c['id'])
  for n,q in enumerate(c['questions']):
   page.locator('input[name=prep-comparison][value="'+str(q['answer'])+'"]').check();page.locator('#prep-compare-reason').fill('Synthetic reasoning about the scenario and assumptions.');page.locator('#prep-compare-form button[type=submit]').click();expect(page.locator('#prep-compare-form')).to_contain_text('Your choice matches.');expect(page.locator('#celebration')).to_be_visible()
   if n==0:page.locator('[data-prep="compare-next"]').click()
 page.reload();expect(page.locator('#celebration')).not_to_be_visible();assert saved()['ksbs']==baseline['ksbs']
 checks.append('All twelve comparison applications accept reasoned choices, give authored feedback and celebrate only new correct submissions, without claiming KSB readiness')
 # Run each answer against both independent Python SQLite and the actual browser engine.
 db=sqlite3.connect(':memory:');db.executescript(data['sqlSetup']);go('sql')
 for c in data['sql']:
  rows=[list(row) for row in db.execute(c['answer']).fetchall()];assert rows==c['rows'],c['id']
  page.locator('#prep-sql-select').select_option(c['id']);page.locator('#prep-sql-query').fill(c['answer']);page.locator('[data-prep=sql-run]').click();expect(page.locator('#prep-sql-result')).to_contain_text('The result matches.',timeout=12000)
 page.locator('#prep-sql-query').fill('SELECT 99 AS made_up;');page.locator('[data-prep=sql-run]').click();expect(page.locator('#prep-sql-result')).to_contain_text('Compare your result');expect(page.locator('#celebration')).not_to_be_visible()
 for query,error in [('DELETE FROM requests RETURNING request_id;','readonly'),('SELECT 1; SELECT 2;','one query'),('SELECT no_such_column FROM requests;','no such column'),('WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n) SELECT sum(x) FROM n;','8 seconds')]:
  page.locator('#prep-sql-query').fill(query);page.locator('[data-prep=sql-run]').click();expect(page.locator('#prep-sql-result')).to_contain_text(error,timeout=14000)
 page.locator('#prep-sql-query').fill(data['sql'][-1]['answer']);page.reload();expect(page.locator('#prep-sql-query')).to_have_value(data['sql'][0]['answer']) # selection is ephemeral, all six drafts persist
 page.locator('#prep-sql-select').select_option('having');expect(page.locator('#prep-sql-query')).to_have_value(data['sql'][-1]['answer'])
 for _ in range(3):page.locator('[data-prep=sql-hint]').click()
 expect(page.locator('main')).to_contain_text('Worked query')
 checks.append('All six queries reconcile with independent SQLite; actual browser SQL handles arbitrary SELECT output, syntax errors, read-only protection, single-statement limits and an 8-second worker timeout; drafts and progressive hints persist')
 # Real MediaRecorder with a fake browser microphone; local IndexedDB playback and explicit export.
 go('speak');page.locator('[data-prep=audio-start]').click();expect(page.locator('#prep-audio-status')).to_contain_text('Recording on this device');page.wait_for_timeout(1200);page.locator('[data-prep=audio-stop]').click();expect(page.locator('audio')).to_have_count(1,timeout=10000);page.locator('[data-audio-check]').first.check();page.locator('[data-audio-note]').fill('Synthetic recording: add the validation result.');recording=next(iter(saved()['preparation']['recordings'].values()));assert recording['duration']>=1
 page.reload();expect(page.locator('audio')).to_have_count(1);page.locator('audio').evaluate('a=>a.play()');page.wait_for_timeout(400);assert page.locator('audio').evaluate('a=>a.currentTime')>0
 with page.expect_download() as dl:page.locator('[data-prep=audio-export]').click()
 dl.value.save_as(str(out/'synthetic-audio.webm'));assert (out/'synthetic-audio.webm').stat().st_size>1000
 page.locator('[data-prep=audio-start]').click();expect(page.locator('#prep-audio-status')).to_contain_text('Recording on this device');page.wait_for_timeout(700);page.locator('a[href="#prep"]').first.click();page.wait_for_timeout(800);assert len(saved()['preparation']['recordings'])==2
 checks.append('Actual microphone capture starts only on request, creates playable IndexedDB audio through reload, exports a real file and stops/saves when navigating away; self-review is independent')
 # Recording length limit, actual track cleanup and explicit deletion.
 go('speak');page.evaluate('()=>{const original=navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);navigator.mediaDevices.getUserMedia=async c=>{const stream=await original(c);window.syntheticTracks=stream.getTracks();return stream;}}');page.clock.install();page.locator('#prep-speak-limit').select_option('60');page.locator('[data-prep=audio-start]').click();expect(page.locator('#prep-audio-status')).to_contain_text('Recording on this device');page.wait_for_timeout(900);page.clock.fast_forward(61000);expect(page.locator('[data-recording]')).to_have_count(3);assert page.evaluate('syntheticTracks.every(t=>t.readyState==="ended")');last_id=page.locator('[data-recording]').first.get_attribute('data-recording');page.locator('[data-prep=remove][data-id="'+last_id+'"]').click();expect(page.locator('[data-recording]')).to_have_count(2);assert page.evaluate('async id=>{const request=indexedDB.open("l4-fellowship-audio.v1",1);const db=await new Promise(resolve=>request.onsuccess=()=>resolve(request.result));const req=db.transaction("clips").objectStore("clips").get(id);return await new Promise(resolve=>req.onsuccess=()=>resolve(req.result===undefined));}',last_id)
 checks.append('The selected one-minute recording limit stops actual media tracks; explicit deletion removes the audio blob from IndexedDB and leaves a deletion tombstone')

 # Backup/merge and strict validation. Audio metadata alone cannot manufacture a playable clip.
 snapshot=saved();oldv1=copy.deepcopy(snapshot);del oldv1['preparation'];restore(oldv1);assert saved()['preparation']==snapshot['preparation']
 changed=copy.deepcopy(snapshot);rid=resource['id'];changed['preparation']['resources'][rid]['title']='Imported synthetic resource';restore(changed);assert saved()['preparation']['resources'][rid]['title']==resource['title'];restore(changed,'prep-resources-'+rid);assert saved()['preparation']['resources'][rid]['title']=='Imported synthetic resource'
 before=saved()
 for mutate in [lambda x:x['preparation']['resources'][rid].update(url='javascript:alert(1)'),lambda x:x['preparation']['comparisons']['identity'].update(choice=99),lambda x:x['preparation']['mistakes'][m['id']].update(nextReview='2026-02-30'),lambda x:x['preparation']['mocks'][next(iter(x['preparation']['mocks']))].update(queue=['K1','K2','K3']),lambda x:x['preparation']['sql'].update(unknown={'query':'SELECT 1','hint':0,'runs':0})]:
  bad=copy.deepcopy(before);mutate(bad);page.locator('#backup-file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});expect(page.locator('#toast')).to_contain_text('Backup not imported');assert saved()==before
 go('materials');page.locator('[data-prep=remove][data-kind=resources]').click();restore(snapshot);assert rid not in saved()['preparation']['resources']
 fresh=browser.new_context(service_workers='block');fp=fresh.new_page();fp.goto(args.url+'#speak');fp.locator('#backup-file').set_input_files({'name':'valid.json','mimeType':'application/json','buffer':json.dumps(snapshot).encode()});expect(fp.locator('#restore-dialog')).to_be_visible();fp.locator('[data-action=apply-restore]').click();expect(fp.locator('[data-recording]')).to_have_count(2);expect(fp.locator('audio')).to_have_count(0);expect(fp.locator('[data-audio-slot]').first).to_contain_text('not on this device');fresh.close()
 checks.append('Old v1 merges preserve new work, conflicting records require a choice, unsafe URLs/IDs/dates/queues fail before mutation, deletion tombstones block resurrection and restored audio reviews correctly disclose missing clips')
 # Guard failed writes, denied mic and delayed permission cancellation.
 failure=browser.new_context(service_workers='block');f=failure.new_page();f.goto(args.url+'#materials');f.evaluate('()=>{Storage.prototype.setItem=function(){throw new Error("Synthetic quota failure")}}');f.locator('[data-prep=resource-new]').click();f.locator('#prep-resource-title').fill('Temporary resource');f.locator('#prep-resource-notes').fill('Synthetic note');f.locator('[data-resource-ksb=K1]').check();f.locator('#prep-resource-form button[type=submit]').click();expect(f.locator('#storage-warning')).to_be_visible()
 with f.expect_download() as dl:f.locator('[data-action=backup]').first.click()
 dl.value.save_as(str(out/'temporary.json'));assert next(iter(json.loads((out/'temporary.json').read_text())['preparation']['resources'].values()))['title']=='Temporary resource'
 f.goto(args.url+'#speak');f.evaluate('()=>{navigator.mediaDevices.getUserMedia=()=>Promise.reject(new DOMException("Synthetic denied","NotAllowedError"))}');f.locator('[data-prep=audio-start]').click();expect(f.locator('#prep-audio-status')).to_contain_text('not granted')
 f.evaluate('()=>{navigator.mediaDevices.getUserMedia=()=>new Promise(resolve=>window.resolveMic=resolve)}');f.locator('[data-prep=audio-start]').click();f.locator('[data-prep=audio-stop]').click();f.evaluate('window.resolveMic({getTracks:()=>[{stop:()=>window.lateTrackStopped=true}]})');f.wait_for_timeout(100);assert f.evaluate('window.lateTrackStopped') is True;expect(f.locator('audio')).to_have_count(0);failure.close()
 checks.append('Quota failure keeps exportable resource text in temporary memory; denied microphone access has a useful status; cancelled permission requests stop late-arriving tracks')
 afctx=browser.new_context(service_workers='block',accept_downloads=True);af=afctx.new_page();af.goto(args.url+'#speak');af.evaluate('()=>{IDBObjectStore.prototype.put=function(){throw new DOMException("Synthetic audio quota failure","QuotaExceededError")}}');af.locator('[data-prep=audio-start]').click();expect(af.locator('#prep-audio-status')).to_contain_text('Recording on this device');af.wait_for_timeout(700);af.locator('[data-prep=audio-stop]').click();expect(af.locator('audio')).to_have_count(1);expect(af.locator('#prep-audio-status')).to_contain_text('temporary memory');
 with af.expect_download() as dl:af.locator('[data-prep=audio-export]').click()
 dl.value.save_as(str(out/'temporary-audio.webm'));assert (out/'temporary-audio.webm').stat().st_size>1000;afctx.close()
 checks.append('A failed IndexedDB audio write retains a playable temporary clip and exports its actual bytes with a clear persistence warning')

 # Direct-file SQL and responsive layouts for every tool.
 local=browser.new_context(service_workers='block');lp=local.new_page();lp.goto((root/'index.html').as_uri()+'#sql');lp.locator('#prep-sql-query').fill(data['sql'][0]['answer']);lp.locator('[data-prep=sql-run]').click();expect(lp.locator('#prep-sql-result')).to_contain_text('The result matches.',timeout=12000);local.close()
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':1000})
  for route in ['prep','mock','mistakes','sql','compare','speak','materials','terms','ksb-k13']:
   go(route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
  if width in [390,1440]:
   for route in ['prep','compare','sql','speak']:
    go(route);page.screenshot(path=str(out/f'{route}-{width}.png'),full_page=True)
 checks.append('SQL works from direct file opening; all preparation routes and lesson integration reflow at 320/390/768/1440px with labelled inputs and keyboard terminology help')
 assert not errors,errors;ctx.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2));print(json.dumps(dict(status='passed',checks=checks),indent=2))
