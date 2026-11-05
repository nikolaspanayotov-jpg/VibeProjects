"""Visible practice shortcuts and transient feedback from actual submissions."""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
from playwright.sync_api import sync_playwright,expect

pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-feedback-qa');args=pa.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True);checks=[];errors=[];KEY='l4-fellowship.v1'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':1440,'height':1000},timezone_id='Europe/London',reduced_motion='no-preference');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install(time=datetime(2026,11,5,9,tzinfo=timezone.utc))
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def finish(note):
  page.locator('[data-action="game-open-finish"]').click();page.locator('#game-reflection').fill(note);page.locator('#game-reviewed').check();page.locator('#game-finish-form button[type="submit"]').click();expect(page.locator('#game-finish-dialog')).not_to_be_visible()
 def correct_quiz(matched=True):
  answer=page.evaluate('(k)=>{const s=JSON.parse(localStorage.getItem(k)).learningTools.quizSession;return L4_CURRICULUM.activities.quiz.find(q=>q.id===s.ids[s.index]).answer}',KEY)
  page.locator('input[name="quiz-choice"][value="'+str(answer if matched else not answer).lower()+'"]').check();page.locator('#quiz-form button[type="submit"]').click()
 def success(title):expect(page.locator('#celebration')).to_be_visible();expect(page.locator('#celebration-title')).to_have_text(title)

 go('today');before=saved()
 shortcuts=page.get_by_role('navigation',name='Your practice shortcuts');expect(shortcuts.locator('a')).to_have_count(4)
 for route in ['quests','rewards','habits','habit-settings']:
  link=shortcuts.locator('a[href="#'+route+'"]');box=link.bounding_box();assert box['height']>=44
  link.focus();expect(link).to_be_focused();assert link.evaluate('el=>getComputedStyle(el).outlineStyle')!='none'
  page.keyboard.press('Enter');expect(page).to_have_url(args.url+'#'+route);go('today')
 assert saved()==before
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':1000});go('today');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  for link in shortcuts.locator('a').all():assert link.bounding_box()['height']>=44
  if width in [390,1440]:
   page.screenshot(path=str(out/f'shortcuts-{width}.png'),full_page=True)
   shortcuts.screenshot(path=str(out/f'shortcut-panel-{width}.png'))
 checks.append('Four labelled shortcut buttons work by keyboard, preserve state, have visible focus and 44px targets, and reflow at 320/390/768/1440px')

 go('quiz');page.locator('[data-action="start-quiz"]').click();page.locator('#quiz-form button[type="submit"]').click();expect(page.locator('#celebration')).not_to_be_visible()
 correct_quiz(False);expect(page.locator('#celebration')).not_to_be_visible();page.locator('[data-action="next-quiz-question"]').click();correct_quiz();success('Well done!')
 assert page.locator('#quiz-feedback-heading').evaluate('el=>document.activeElement===el')
 page.wait_for_function('getComputedStyle(document.getElementById("celebration")).opacity==="1"');box=page.locator('#celebration').bounding_box();assert box['y']>page.viewport_size['height']-180 and box['y']+box['height']<=page.viewport_size['height']-15,(box,page.viewport_size,page.locator('#celebration').evaluate('el=>({cls:el.className,opacity:getComputedStyle(el).opacity,transform:getComputedStyle(el).transform})'))
 assert page.locator('#celebration').evaluate('el=>getComputedStyle(el).pointerEvents')=='none'
 page.screenshot(path=str(out/'correct-desktop.png'))
 page.wait_for_function('(()=>{const o=Number(getComputedStyle(document.getElementById("celebration")).opacity);return o>0&&o<1})()')
 expect(page.locator('#celebration')).not_to_be_visible();page.reload();expect(page.locator('#celebration')).not_to_be_visible()
 page.locator('[data-action="next-quiz-question"]').click();correct_quiz();success('Well done!')
 # A later wrong answer clears a preceding answer celebration rather than praising the wrong answer.
 page.locator('[data-action="next-quiz-question"]').click();correct_quiz(False);expect(page.locator('#celebration')).not_to_be_visible()
 checks.append('Only submitted correct answers show Well done; messages fade and hide, repeat for new correct answers, clear on wrong answers, preserve focus and do not replay on reload')

 for route,choice,fields in [('repairs-duplicate-join','resolve',['diagnosis','impact']),('methods-paired-change','paired',['reason','assumptions'])]:
  go(route);page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('#celebration')).not_to_be_visible()
  for field in fields:page.locator('#reasoning-'+field).fill('Synthetic explanation of the analytical decision.')
  page.locator('input[name="reasoning-choice"][value="'+choice+'"]').check();page.locator('#reasoning-form button[type="submit"]').click();success('Well done!');page.reload();expect(page.locator('#celebration')).not_to_be_visible()
 go('changes-paired');page.locator('#changed-reason').fill('Pairing changes the sampling design and standard error.');page.locator('input[name="changed-choice"][value="retain"]').check();page.locator('#changed-case-form button[type="submit"]').click();expect(page.locator('#celebration')).not_to_be_visible()
 page.locator('input[name="changed-choice"][value="paired"]').check();page.locator('#changed-case-form button[type="submit"]').click();success('Well done!')
 checks.append('Correction challenges, method decisions and changed-assumption questions celebrate authored correct choices after explanation gating')

 # Complete the same real three-step quest in two weeks; the second completion has no new quest badge.
 for day in [5,12]:
  page.clock.set_fixed_time(datetime(2026,11,day,9,tzinfo=timezone.utc));go('today');page.locator('[data-action="study"]').first.click();page.locator('#practice-response').fill('Synthetic recall of data quality dimensions.');page.locator('[data-action="reveal-answer"]').click();page.locator('[data-action="rate-practice"][data-result="partial"]').click()
  go('repairs-duplicate-join');page.locator('[data-action="game-track"]').click();page.locator('#reasoning-diagnosis').fill('A duplicate lookup key multiplies source rows.');page.locator('#reasoning-impact').fill('It inflates the total; validate row grain and authorised mapping.');page.locator('input[name="reasoning-choice"][value="resolve"]').check();page.locator('#reasoning-form button[type="submit"]').click();finish('I verified the duplicate lookup and the intended row grain.');expect(page.locator('#celebration-title')).not_to_have_text('Congratulations!')
  go('retrieval-b5');page.locator('[data-action="game-track"]').click();page.locator('#retrieval-gap').fill('I need a sanitised investigation log for my own root-cause example.');page.locator('#retrieval-form button[type="submit"]').click();finish('I identified the supporting evidence needed for root-cause analysis.');success('Congratulations!');expect(page.locator('#celebration-detail')).to_contain_text('Data quality detective')
  page.set_viewport_size({'width':390,'height':844});page.wait_for_function('getComputedStyle(document.getElementById("celebration")).opacity==="1"');page.screenshot(path=str(out/f'quest-mobile-week-{day}.png'));page.reload();expect(page.locator('#celebration')).not_to_be_visible()
 assert len([e for e in saved()['game']['events'] if e['kind'] in ['recall','repair','retrieval']])==6
 checks.append('Weekly quest congratulations require all three real steps, fire again in a subsequent week, survive navigation and never replay on reload')

 page.emulate_media(reduced_motion='reduce');go('quiz')
 # The unfinished quiz set resumes at the most recently checked question.
 page.locator('[data-action="next-quiz-question"]').click();correct_quiz();success('Well done!')
 assert page.locator('#celebration').evaluate('el=>getComputedStyle(el).transitionDuration')=='0s'
 page.clock.run_for(3300);expect(page.locator('#celebration')).not_to_be_visible()
 go('habit-settings');page.locator('#game-celebrations').uncheck();page.locator('#game-settings-form button').click();go('methods-paired-change');page.locator('#reasoning-reason').fill('A new synthetic explanation while celebrations are off.');page.locator('#reasoning-form button[type="submit"]').click();expect(page.locator('#celebration')).not_to_be_visible()
 go('habit-settings');page.locator('#game-celebrations').check();page.locator('#game-settings-form button').click();go('methods-paired-change');page.locator('#reasoning-reason').fill('Another synthetic explanation after enabling celebrations.');page.locator('#reasoning-form button[type="submit"]').click();success('Well done!')
 # A normal toast retains its own live region and sits above the celebration.
 go('habit-settings');page.locator('#game-settings-form button').click();success('Well done!');toast=page.locator('#toast').bounding_box();message=page.locator('#celebration').bounding_box();assert toast['y']+toast['height']<=message['y']
 checks.append('Reduced motion shows static success feedback; the saved celebration preference disables/enables it; ordinary status toasts remain visible without overlap')
 snapshot=saved();fresh=browser.new_context();fp=fresh.new_page();fp.clock.install(time=datetime(2026,11,12,9,tzinfo=timezone.utc));fp.goto(args.url+'#plan');fp.locator('#backup-file').set_input_files({'name':'synthetic-feedback.json','mimeType':'application/json','buffer':json.dumps(snapshot).encode()});expect(fp.locator('#restore-dialog')).to_be_visible();fp.locator('[data-action="apply-restore"]').click();expect(fp.locator('#restore-dialog')).not_to_be_visible();expect(fp.locator('#celebration')).not_to_be_visible();fp.goto(args.url+'#quests');expect(fp.locator('#celebration')).not_to_be_visible();fresh.close()
 checks.append('Restoring a backup with completed quests and correct answers never replays historical celebrations')
 assert not errors,errors;ctx.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2));print(json.dumps(dict(status='passed',checks=checks),indent=2))
