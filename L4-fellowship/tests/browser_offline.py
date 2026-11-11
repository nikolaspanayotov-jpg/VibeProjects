"""Real service-worker lifecycle at a project subpath, including failed/update releases.

Run a localhost server rooted at --fixture.parent on port 8001 before this test.
The fixture is disposable. Original project files are never modified by this test.
"""
import argparse,copy,json,re,shutil,struct,subprocess,sys,time,math
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8001/L4-fellowship/');pa.add_argument('--fixture',type=Path,default=Path('/tmp/l4-pwa-fixture/L4-fellowship'));pa.add_argument('--output',type=Path,default=Path('/tmp/l4-offline-qa'));args=pa.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[1];fixture=args.fixture.resolve();assert fixture!=root and '/tmp/' in str(fixture)
fixture.mkdir(parents=True,exist_ok=True)
for file in root.iterdir():
 if file.is_file():shutil.copy2(file,fixture/file.name)
 if file.is_dir() and file.name=='vendor':shutil.copytree(file,fixture/file.name,dirs_exist_ok=True)
(fixture.parent/'other-project.txt').write_text('A different synthetic project.')
KEY='l4-fellowship.v1';checks=[];errors=[]
def build():
 # SimpleHTTPServer validates sw.js by whole-second Last-Modified, not content ETags.
 # Ensure successive fixture releases have different timestamps.
 time.sleep(max(0,math.floor((fixture/'sw.js').stat().st_mtime)+1.05-time.time()))
 subprocess.run([sys.executable,str(root/'tests/build_offline.py'),'--root',str(fixture)],check=True,capture_output=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);ctx=browser.new_context(viewport={'width':1280,'height':900},accept_downloads=True);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():page.wait_for_timeout(450);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 go('offline');expect(page.locator('#offline-status')).to_contain_text('available offline',timeout=30000);page.wait_for_function('Boolean(navigator.serviceWorker.controller)')
 scope=page.evaluate('async()=> (await navigator.serviceWorker.getRegistration()).scope');assert scope==args.url
 manifest=page.evaluate('async()=>await (await fetch("./manifest.webmanifest")).json()');assert manifest['scope']=='./' and manifest['start_url']=='./' and manifest['display']=='standalone'
 for n in [192,512]:assert struct.unpack('!II',(fixture/f'icon-{n}.png').read_bytes()[16:24])==(n,n)
 cached=page.evaluate('async()=>{let found=[];for(const name of await caches.keys()){const c=await caches.open(name);found.push(...(await c.keys()).map(r=>r.url));}return found}')
 assert cached and all(url.startswith(args.url) for url in cached) and not any('other-project' in url for url in cached)
 assert not any('backup' in url or 'personal' in url for url in cached)
 checks.append('Manifest and 192/512 PNG icons are valid; registration and all cached URLs stay inside the project subpath; cache contains public assets only')
 go('workshop-k8');page.locator('#workshop-draft').fill('Synthetic offline draft, original.');saved()
 go('briefing');page.locator('#briefing-finding').fill('Synthetic briefing saved before disconnecting.');saved()
 ctx.set_offline(True)
 go('ksb-k8');page.locator('#lesson-recall').select_option('help');page.locator('[data-action="record-lesson-review"]').click();assert saved()['game']['events'];offline_game=copy.deepcopy(saved()['game'])
 for route in ['today','ksb-k13','uncertainty','quiz','changes','briefing','retrieval','organisation','connections','visual-map','methods-chart-change','methods-forecast-rmse','plan','readiness','quests','prep','mock','mistakes','sql','compare','materials','terms','speak','assessment','assessment-practice','evidence-packs','offline']:
  go(route);page.reload();expect(page.locator('h1')).to_be_visible();assert 'could not load' not in page.locator('main').inner_text()
 go('sql');page.locator('#prep-sql-query').fill("SELECT request_id, days FROM requests WHERE status = 'closed' AND days > 5 ORDER BY request_id;");page.locator('[data-prep=sql-run]').click();expect(page.locator('#prep-sql-result')).to_contain_text('The result matches.',timeout=12000)
 go('materials');page.locator('[data-prep=resource-new]').click();page.locator('#prep-resource-title').fill('Synthetic offline course note');page.locator('#prep-resource-notes').fill('Remember to validate join cardinality.');page.locator('[data-resource-ksb=K10]').check();page.locator('#prep-resource-form button[type=submit]').click();offline_preparation=copy.deepcopy(saved()['preparation']);page.reload();expect(page.locator('main')).to_contain_text('Synthetic offline course note')
 go('ksb-k13');page.locator('[data-step=full]').click();expect(page.locator('.full-answer')).to_be_visible();expect(page.locator('.lesson-title .cue-accent')).not_to_have_count(0)
 go('assessment');expect(page.locator('.as-group')).to_have_count(30);page.locator('.as-group>summary').first.click();expect(page.locator('.as-group[open] .as-study-brief')).to_contain_text('Explain')
 go('assessment-practice');page.locator('#as-response').fill('Synthetic source answer written while offline.');page.locator('[data-assess=reveal]').click();expect(page.locator('.as-feedback')).to_be_visible();offline_assessment=copy.deepcopy(saved()['assessmentReview']);page.locator('#as-search').fill('quality');assert page.locator('#as-question option').count()>1;page.locator('[data-assess=next]').click();expect(page.locator('[data-as-position]')).to_contain_text('2 of');page.locator('[data-assess=clear]').first.click()
 go('methods-chart-change');expect(page.locator('.challenge-chart')).to_be_visible()
 go('readiness');expect(page.locator('.readiness-row')).to_have_count(10)
 go('quests');expect(page.locator('.game-quest')).to_have_count(6)
 go('visual-map');expect(page.locator('[data-visual-card]')).to_have_count(37)
 source=page.evaluate('async()=>{let r=await fetch("./solutions.md");return {status:r.status,text:await r.text()}}');assert source['status']==200 and 'Knowledge' in source['text']
 go('workshop-k8');expect(page.locator('#workshop-draft')).to_have_value('Synthetic offline draft, original.');page.locator('#workshop-draft').fill('Synthetic offline draft, edited without a connection.');page.reload();expect(page.locator('#workshop-draft')).to_have_value('Synthetic offline draft, edited without a connection.')
 go('offline');expect(page.locator('main')).to_contain_text('Connection: Offline');page.screenshot(path=str(out/'offline-desktop.png'),full_page=True)
 checks.append('Actual offline reloads work across lessons and all new activity routes; source guide fetches succeed; edits persist while disconnected')
 ctx.set_offline(False)
 # A worker whose manifest does not match its files must never replace the active copy.
 oldversion=page.locator('main').inner_text();index=(fixture/'index.html').read_text();curriculum=(fixture/'curriculum.js').read_text()
 (fixture/'index.html').write_text(index.replace('<head>','<head><meta name="test-release" content="rejected">',1));build();(fixture/'curriculum.js').write_text(curriculum+'\n/* deliberately mismatched test release */\n')
 page.locator('[data-action="check-offline"]').click();expect(page.locator('#offline-status')).to_contain_text(re.compile('could not be installed|update check failed'),timeout=30000)
 assert not page.evaluate('async()=>Boolean((await navigator.serviceWorker.getRegistration()).waiting)')
 page.reload();expect(page.locator('meta[name="test-release"]')).to_have_count(0);go('workshop-k8');expect(page.locator('#workshop-draft')).to_have_value('Synthetic offline draft, edited without a connection.')
 checks.append('A deliberately mismatched HTML/curriculum release is rejected; the previous complete cached version and personal progress remain usable')
 # A valid release waits for explicit application and saves before replacing the current tab.
 (fixture/'curriculum.js').write_text(curriculum);(fixture/'index.html').write_text(index.replace('<head>','<head><meta name="test-release" content="second">',1));build()
 go('offline');expect(page.locator('[data-action="check-offline"]')).to_be_enabled();page.locator('[data-action="check-offline"]').click();expect(page.locator('[data-action="apply-offline"]')).to_be_visible(timeout=30000)
 assert page.locator('meta[name="test-release"]').count()==0
 # Exercise the in-memory protection while an update is waiting.
 page.evaluate('()=>{window.savedSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new Error("synthetic quota failure")}}')
 go('workshop-k8');page.locator('#workshop-draft').fill('Synthetic temporary draft must survive the update.');page.wait_for_timeout(500)
 go('offline');page.locator('[data-action="apply-offline"]').click();expect(page.locator('#toast')).to_contain_text('temporary memory');assert page.locator('meta[name="test-release"]').count()==0
 with page.expect_download() as dl:page.locator('[data-action="backup"]').first.click()
 dl.value.save_as(str(out/'temporary-backup.json'));backup=json.loads((out/'temporary-backup.json').read_text());assert backup['studyTools']['workshops']['K8']['draft']=='Synthetic temporary draft must survive the update.'
 page.evaluate('()=>{Storage.prototype.setItem=window.savedSetItem}');page.locator('#backup-file').set_input_files(str(out/'temporary-backup.json'));expect(page.locator('#restore-dialog')).to_be_visible();page.locator('[data-action="apply-restore"]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 page.locator('[data-action="apply-offline"]').click();page.wait_for_function('document.querySelector(\'meta[name="test-release"]\')?.content==="second"',timeout=30000)
 go('workshop-k8');expect(page.locator('#workshop-draft')).to_have_value('Synthetic temporary draft must survive the update.')
 ctx.set_offline(True);page.reload();expect(page.locator('#workshop-draft')).to_have_value('Synthetic temporary draft must survive the update.');assert page.locator('meta[name="test-release"]').get_attribute('content')=='second';assert saved()['game']['events']==offline_game['events'];assert saved()['preparation']==offline_preparation;assert saved()['assessmentReview']==offline_assessment
 checks.append('A verified update waits for application, blocks reload when saving fails, permits export/restore of temporary work and preserves it through activation and offline reload')
 go('offline');page.set_viewport_size({'width':390,'height':900});page.screenshot(path=str(out/'offline-mobile.png'),full_page=True);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 assert not errors,errors
 ctx.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2));print(json.dumps(dict(status='passed',checks=checks),indent=2))
