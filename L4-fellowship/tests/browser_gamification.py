"""Mission rewards are backed by real UI completions and conflict-safe history."""
import argparse,copy,json,re
from datetime import datetime,timezone
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-gamification-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce',timezone_id='Europe/London');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install(time=datetime(2026,11,5,8,30,tzinfo=timezone.utc))
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def metrics():return page.evaluate('(k)=>L4_GAME.metrics(JSON.parse(localStorage.getItem(k)).game,Object.fromEntries(L4_CURRICULUM.activities.quiz.map(q=>[q.id,q])),"2026-11-05")',KEY)
 def upload(value):page.locator('#backup-file').set_input_files({'name':'synthetic.json','mimeType':'application/json','buffer':json.dumps(value).encode()})
 def merge(value,conflict=None):
  upload(value);expect(page.locator('#restore-dialog')).to_be_visible()
  if conflict:page.locator('[data-restore-conflict="'+conflict+'"]').select_option('import')
  page.locator('[data-action="apply-restore"]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 def finish(note):
  page.locator('[data-action="game-open-finish"]').click();page.locator('#game-reflection').fill(note);page.locator('#game-reviewed').check();page.locator('#game-finish-form button[type="submit"]').click();expect(page.locator('#game-finish-dialog')).not_to_be_visible();expect(page.locator('.game-home')).to_be_visible()
 go('today');expect(page.locator('.game-mission')).to_have_count(3);expect(page.locator('.game-scoreline')).to_contain_text('0 XP')
 with page.expect_download() as dl:page.locator('[data-action="backup"]').first.click()
 assert saved()['game']['events']==[];assert saved()['game']['active'] is None
 # Recall is recorded only after an actual review outcome, including Needed help.
 page.locator('[data-action="study"]').click();expect(page.locator('.practice-question')).to_be_visible();assert saved()['game']['events']==[]
 page.locator('#practice-response').fill('Synthetic recall: accuracy differs from completeness.');page.locator('[data-action="reveal-answer"]').click();page.locator('[data-action="rate-practice"][data-result="help"]').click();assert metrics()['total']==20
 progress=copy.deepcopy(saved()['ksbs']);evidence=copy.deepcopy(saved()['evidence']);go('today');assert metrics()['current']==1
 # Apply: a reviewed reasoning task plus explicit completion, without mutating KSB progress.
 page.clock.set_fixed_time(datetime(2026,11,5,13,tzinfo=timezone.utc));page.locator('[data-game-block="apply"]').click();expect(page.locator('#reasoning-form')).to_be_visible()
 page.locator('[data-action="game-open-finish"]').click();page.locator('#game-reflection').fill('Synthetic early reflection.');page.locator('#game-reviewed').check();page.locator('#game-finish-form button[type="submit"]').click();expect(page.locator('#game-finish-error')).to_contain_text('Work through');page.locator('[data-action="game-close-finish"]').click()
 page.locator('#reasoning-diagnosis').fill('Two lookup rows match each A request.');page.locator('#reasoning-impact').fill('The total is inflated from 60 to 90.');page.locator('input[name="reasoning-choice"][value="resolve"]').check();page.locator('#reasoning-form button[type="submit"]').click()
 page.locator('[data-action="game-open-finish"]').click();page.locator('#game-reflection').fill('I checked the duplicate key and row grain.');page.locator('#game-reviewed').check();page.locator('[data-action="game-close-finish"]').click();page.reload();page.locator('[data-action="game-open-finish"]').click();expect(page.locator('#game-reflection')).to_have_value('I checked the duplicate key and row grain.');page.locator('#game-finish-form button[type="submit"]').click();assert metrics()['total']==40
 # Explain: an evidence gap is an honest completed rehearsal, not fabricated evidence.
 page.clock.set_fixed_time(datetime(2026,11,5,19,tzinfo=timezone.utc));page.locator('[data-game-block="explain"]').click();page.locator('#retrieval-gap').fill('I need a sanitised root-cause log showing my investigation and prevention.');page.locator('#retrieval-form button[type="submit"]').click();finish('I distinguished a symptom from a cause and identified an evidence gap.')
 m=metrics();assert m['total']==100 and m['counts']['trios']==1 and m['counts']['checkins']==1 and m['counts']['quests']==1;assert saved()['ksbs']==progress and saved()['evidence']==evidence
 page.reload();assert metrics()['total']==100;assert 'game-unlock' not in (page.locator('.game-home').get_attribute('class') or '')
 checks.append('Actual Recall/Apply/Explain completions earn 20+20+20+40 once, count three time windows, complete the quality quest and leave evidence/KSB progress separate; unfinished reflection survives reload')
 # Further practice counts as real activity but has no extra daily XP.
 go('labs-joins');page.locator('[data-action="game-track"]').click();page.locator('#lab-join-type').select_option('inner');finish('An inner join removes unmatched requests while duplicate keys still multiply rows.');assert metrics()['total']==100 and metrics()['counts']['blocks']==4
 # Badges explain their provenance; pinning and downloads do not create practice.
 go('rewards');page.locator('[data-action="game-badge"][data-id="trio"]').click();expect(page.locator('#game-detail-content')).to_contain_text('Earned 5 Nov 2026');before=len(saved()['game']['events']);page.locator('[data-action="game-pin"]').click();expect(page.locator('#game-detail-content')).to_contain_text('Unpin')
 with page.expect_download() as dl:page.locator('[data-action="game-download-badge"]').click()
 dl.value.save_as(str(out/'badge.svg'));assert 'Triple play' in (out/'badge.svg').read_text();page.locator('[data-action="game-close-detail"]').click();assert len(saved()['game']['events'])==before;expect(page.locator('.game-desk a[aria-label^="Lamp:"]')).to_have_attribute('aria-label',re.compile('illuminated'))
 page.screenshot(path=str(out/'rewards-desktop.png'),full_page=True)
 go('today');expect(page.locator('.game-pins')).to_contain_text('Triple play');go('quests');expect(page.locator('.game-quest').first.locator('li.done')).to_have_count(3);page.locator('[data-action="game-select-pack"][data-id="forecast"]').click();go('today');expect(page.locator('.game-mission').nth(1)).to_contain_text('Forecast windows');assert saved()['game']['settings']['pack']=='forecast'
 checks.append('Extra practice respects the XP cap; earned badges show real qualifying dates, pin/export without points, unlock desk art and select weekly quest-backed missions')
 # Five reviewed quiz answers create one recall block; reloads cannot duplicate it.
 page.clock.set_fixed_time(datetime(2026,11,6,8,30,tzinfo=timezone.utc));go('quiz');page.locator('[data-action="start-quiz"]').click()
 for i in range(5):
  page.locator('input[name="quiz-choice"][value="false"]').check();page.locator('#quiz-form button[type="submit"]').click();page.locator('[data-action="next-quiz-question"]').click()
 assert len([e for e in saved()['game']['events'] if e['kind']=='quiz-answer'])==5;assert len([e for e in saved()['game']['events'] if e['kind']=='quiz'])==1
 old=copy.deepcopy(saved()['game']['events']);page.reload();assert saved()['game']['events']==old;assert metrics()['total']==120
 go('quests');page.locator('[data-action="game-weekly-challenge"]').click()
 for i in range(3):
  page.locator('#practice-response').fill('Synthetic rehearsal: my approach, checks and limits.');page.locator('[data-action="reveal-answer"]').click();page.locator('[data-action="rate-practice"][data-result="partial"]').click()
 assert metrics()['counts']['challenges']==1 and metrics()['total']==120
 checks.append('Reviewed quiz history supports one block after five questions and survives reload; optional three-topic discussion records its attempts and badge without extra daily XP')
 # Rhythms validate boundaries; calendar export uses local floating time and alarms.
 go('habit-settings');prior=copy.deepcopy(saved()['game']['settings']);page.locator('#game-end-0').fill('18:00');page.locator('#game-settings-form button').click();expect(page.locator('#game-settings-error')).to_contain_text('increasing');assert saved()['game']['settings']==prior
 windows=[e['window'] for e in saved()['game']['events']];page.locator('#game-end-0').fill('10:00');page.locator('#game-end-1').fill('16:00');page.locator('#game-settings-form button').click();assert [e['window'] for e in saved()['game']['events']]==windows
 before=len(saved()['game']['events'])
 with page.expect_download() as dl:page.locator('[data-action="game-calendar"]').click()
 dl.value.save_as(str(out/'reminders.ics'));ics=(out/'reminders.ics').read_text();assert all(len(line.encode())<=75 for line in ics.splitlines());assert 'URL:https://nikolaspanayotov-jpg.github.io/VibeProjects/L4-fellowship/#today' in ics.replace('\n ','');assert ics.count('BEGIN:VEVENT')==3 and ics.count('BEGIN:VALARM')==3 and ics.count('RRULE:FREQ=DAILY;COUNT=90')==3;assert all(not line.endswith('Z') for line in ics.splitlines() if line.startswith('DTSTART:'));assert len(saved()['game']['events'])==before
 checks.append('Time settings reject overlapping windows, retain historical window assignments and export three 90-day local-time calendar reminders without awarding practice')
 # Record correction recalculates points and rewards; merge carries deletion markers.
 with page.expect_download() as dl:page.locator('[data-action="backup"]').first.click()
 dl.value.save_as(str(out/'before-delete.json'));snapshot=json.loads((out/'before-delete.json').read_text());target=next(e for e in snapshot['game']['events'] if e['kind']=='retrieval')
 go('habits');page.once('dialog',lambda d:d.accept());page.locator('[data-action="game-delete-event"][data-id="'+target['id']+'"]').click();assert metrics()['total']==60;assert 'trio' not in metrics()['earned'];assert target['id'] in saved()['game']['deleted']
 merge(snapshot);assert metrics()['total']==60;assert not any(e['id']==target['id'] for e in saved()['game']['events']);page.locator('[data-action="game-undo-delete"]').click();assert metrics()['total']==120
 # Re-importing identical records cannot multiply XP; current conflicting records remain by default.
 base=saved();merge(base);assert metrics()['total']==120
 conflicting=copy.deepcopy(base);conflicting['game']['events'][0]['reflection']='Imported synthetic reflection';merge(conflicting);assert saved()['game']['events'][0]['reflection']!='Imported synthetic reflection';merge(conflicting,'game-event-'+base['game']['events'][0]['id']);assert saved()['game']['events'][0]['reflection']=='Imported synthetic reflection'
 legacy=copy.deepcopy(base);del legacy['game'];merge(legacy);assert metrics()['total']==120
 invalids=[]
 for tweak in ['duplicate','date','kind','offset','window','settings','active']:
  bad=copy.deepcopy(base)
  if tweak=='duplicate':bad['game']['events'].append(copy.deepcopy(bad['game']['events'][0]))
  if tweak=='date':bad['game']['events'][0]['date']='2026-11-04'
  if tweak=='kind':bad['game']['events'][0]['kind']='constructor'
  if tweak=='offset':bad['game']['events'][0]['offset']=900
  if tweak=='window':bad['game']['events'][0]['window']=3
  if tweak=='settings':bad['game']['settings']['ends']=[1000,900]
  if tweak=='active':bad['game']['active']={'activity':'constructor','target':'x'}
  invalids.append(bad)
 for bad in invalids:
  before=saved();upload(bad);expect(page.locator('#toast')).to_contain_text('Backup not imported');assert saved()==before
 fresh=browser.new_context(accept_downloads=True);fp=fresh.new_page();fp.clock.install(time=datetime(2026,11,6,9,tzinfo=timezone.utc));fp.goto(args.url+'#plan');fp.locator('#backup-file').set_input_files(str(out/'before-delete.json'));expect(fp.locator('#restore-dialog')).to_be_visible();fp.locator('[data-action="apply-restore"]').click();assert fp.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).game',KEY)==snapshot['game'];fresh.close()
 checks.append('Removal and undo recalculate XP/quests/badges; deletion markers survive merging older backups; identical imports deduplicate and explicit conflicts resolve per record; malformed histories are rejected without mutation')
 # Normal-motion replay advances, then pauses when hidden and when navigating away.
 normal=browser.new_context(accept_downloads=True,reduced_motion='no-preference');rp=normal.new_page();rp.clock.install(time=datetime(2026,11,6,9,tzinfo=timezone.utc));rp.goto(args.url+'#plan');rp.locator('#backup-file').set_input_files(str(out/'before-delete.json'));expect(rp.locator('#restore-dialog')).to_be_visible();rp.locator('[data-action="apply-restore"]').click();rp.goto(args.url+'#habits');rp.locator('[data-action="game-replay-toggle"]').click();expect(rp.locator('[data-action="game-replay-toggle"]')).to_have_text('Pause');rp.clock.fast_forward(3100);assert rp.locator('#game-replay-position').input_value()=='1';rp.evaluate('()=>{Object.defineProperty(document,"hidden",{configurable:true,value:true});document.dispatchEvent(new Event("visibilitychange"));}');expect(rp.locator('[data-action="game-replay-toggle"]')).to_have_text('Play');position=rp.locator('#game-replay-position').input_value();rp.clock.fast_forward(4000);assert rp.locator('#game-replay-position').input_value()==position;normal.close()
 # Real weekly replay and exported recap, then mobile accessibility and file opening.
 go('habits');expect(page.locator('#game-replay')).to_contain_text('K8');page.locator('[data-action="game-replay-next"]').click();expect(page.locator('#game-replay')).to_contain_text('A join');page.locator('[data-action="game-replay-toggle"]').click();expect(page.locator('#toast')).to_contain_text('reduced motion')
 with page.expect_download() as dl:page.locator('[data-action="game-download-recap"]').click()
 dl.value.save_as(str(out/'recap.md'));assert '2026-11-05' in (out/'recap.md').read_text()
 with page.expect_download() as card:page.locator('[data-action="game-weekly-card"]').click()
 card.value.save_as(str(out/'weekly-card.svg'));assert '120 XP' in (out/'weekly-card.svg').read_text();page.screenshot(path=str(out/'habits-desktop.png'),full_page=True)
 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['today','habits','quests','rewards','habit-settings','labs-statistics']:
   go(route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
 page.set_viewport_size({'width':390,'height':900});go('today');page.screenshot(path=str(out/'today-mobile.png'),full_page=True);go('quests');page.screenshot(path=str(out/'quests-mobile.png'),full_page=True);go('rewards');page.screenshot(path=str(out/'rewards-mobile.png'),full_page=True)
 page.locator('[data-action="text-size"]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 page.set_viewport_size({'width':1440,'height':1000});go('today');page.screenshot(path=str(out/'today-desktop.png'),full_page=True)
 direct=browser.new_page();direct.on('pageerror',lambda e:errors.append(str(e)));direct.goto((Path(__file__).resolve().parents[1]/'index.html').as_uri()+'#rewards');expect(direct.locator('.game-desk')).to_be_visible();direct.close();assert not errors,errors
 checks.append('Weekly history/replay/recap use recorded events, reduced motion keeps replay manual, all reward views reflow at 320/390/768/1280px and direct file opening loads the helper without errors')
 ctx.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2));print(json.dumps(dict(status='passed',checks=checks),indent=2))
