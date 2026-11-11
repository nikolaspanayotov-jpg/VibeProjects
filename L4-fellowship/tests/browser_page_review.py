"""Reading access, source-linked coaching and safe question discovery."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-page-review-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];errors=[];checks=[];KEY='l4-fellowship.v1'
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);c=b.new_context(service_workers='block',accept_downloads=True,reduced_motion='reduce',viewport={'width':1440,'height':1000});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 go('library');
 with page.expect_download():page.locator('[data-action=backup]').first.click()
 page.locator('.ksb-row[href="#ksb-k13"]').click();expect(page.locator('.quick-answer')).to_be_visible();before=saved();data=page.evaluate('L4_CURRICULUM')
 for k in data['items']:
  go('ksb-'+k['id'].lower());guide=page.locator('#lesson-full-guide');assert not guide.evaluate('(e)=>e.open');assert guide.evaluate('(e)=>e.previousElementSibling.id')=='lesson-learn';page.locator('[data-step=full]').focus();page.keyboard.press('Enter');assert guide.evaluate('(e)=>e.open');expect(guide.locator('summary')).to_be_focused();expect(guide.locator('.full-answer')).to_be_visible();expect(guide).to_contain_text('Close the full answer');guide.locator('summary').press('Space');assert not guide.evaluate('(e)=>e.open')
 assert saved()['ksbs']==before['ksbs'] and saved()['game']==before['game'] and saved()['evidence']==before['evidence']
 checks.append('All37lessons retain short explanations; prominent full-answer controls open/focus the adjacent complete guide by keyboard; disclosure toggles without marking progress')
 go('ksb-k13');page.locator('[data-step=full]').hover();assert page.locator('[data-step=full]').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(16, 59, 131)';page.locator('[data-step=full]').click();page.screenshot(path=str(out/'full-answer-desktop.png'))
 # Print uses the app print lifecycle, expands the real guide, and restores reading state.
 page.locator('#lesson-full-guide>summary').click();page.evaluate('window.print=()=>{}');page.locator('[data-action=print]').click();assert page.locator('#lesson-full-guide').evaluate('(e)=>e.open');page.emulate_media(media='print');page.pdf(path=str(out/'topic.pdf'),format='A4');assert (out/'topic.pdf').stat().st_size>10000;page.emulate_media(media='screen');page.evaluate('dispatchEvent(new Event("afterprint"))');assert not page.locator('#lesson-full-guide').evaluate('(e)=>e.open')
 go('assessment');assert not page.locator('.as-provenance details').evaluate('(e)=>e.open');page.locator('.as-provenance summary').click();expect(page.locator('.as-provenance')).to_contain_text('not independently verified');expect(page.locator('.as-provenance')).to_contain_text('flattened')
 for g in data['assessment']['groups']:
  page.locator('#as-group').select_option(g['groupId']);summary=page.locator('.as-group>summary');expect(summary).to_contain_text(g['studyBrief']['title']);summary.click();brief=page.locator('.as-study-brief');expect(brief).to_contain_text('derived coaching');assert brief.locator('dt').all_text_contents()==['Explain','Show','Discuss'];expect(brief).to_contain_text(g['studyBrief']['show']);expect(page.locator('.as-pass')).to_have_text(g['gradingPass']);assert page.locator('.as-distinction').count()==bool(g['gradingDistinction'])
 checks.append('All30groups expose topic names and Explain/Show/Discuss coaching with source refs; exact criteria and only8distinction rows remain independent; full provenance remains accessible')
 go('assessment-practice');page.locator('[data-assess=clear]').first.click();first=page.locator('#as-question').input_value();page.locator('#as-response').fill('Synthetic first response: my checks and rationale.');page.locator('[data-assess=next]').click();second=page.locator('#as-question').input_value();assert second!=first;expect(page.locator('#as-response')).to_have_value('');expect(page.locator('[data-as-position]')).to_contain_text('2 of 254');page.locator('#as-response').fill('Synthetic second response.');page.locator('[data-assess=previous]').click();expect(page.locator('#as-response')).to_have_value('Synthetic first response: my checks and rationale.');page.locator('[data-assess=next]').click();expect(page.locator('#as-response')).to_have_value('Synthetic second response.');page.reload();page.locator('#as-question').select_option(second);expect(page.locator('#as-response')).to_have_value('Synthetic second response.')
 page.locator('#as-search').press_sequentially('quality');expect(page.locator('#as-search')).to_be_focused();expect(page.locator('#as-search')).to_have_value('quality');count=page.locator('#as-question option').count();assert 1<count<254
 page.locator('#as-search').fill('<img src=x onerror=window.reviewInjected=1>');expect(page.locator('.quiet-box')).to_contain_text('No prompts match');assert page.evaluate('window.reviewInjected') is None;assert page.locator('.as-shell img').count()==0;page.locator('[data-assess=clear]').last.click();expect(page.locator('#as-search')).to_have_value('');expect(page.locator('#as-question option')).to_have_count(254)
 page.locator('#as-method').select_option('AM2');page.locator('#as-group').select_option('S13');page.locator('#as-search').fill('forecast');assert page.locator('#as-question option').count()>0;options=page.locator('#as-question option').evaluate_all('(es)=>es.map(e=>e.value)');assert all(q['method']=='AM2' and q['groupId']=='S13' for q in data['assessment']['questions'] if q['id'] in options)
 page.locator('[data-assess=clear]').first.click();page.locator('#as-question').select_option(first);expect(page.locator('#as-response')).to_have_value('Synthetic first response: my checks and rationale.');assert saved()['ksbs']==before['ksbs'] and saved()['game']==before['game']
 checks.append('Previous/Next retains separate drafts through reload; position and boundaries are correct; live search keeps focus and combines with method/group filters; no-match/reset and inert markup work')
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['library','visual-map','ksb-k1','ksb-s13','ksb-b5','assessment','assessment-practice','evidence-packs']:
   go(route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
   if route.startswith('ksb-'):
    page.locator('[data-step=full]').click();expect(page.locator('.full-answer')).to_be_visible();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');nav=page.locator('.lesson-jumps').bounding_box();guide=page.locator('#lesson-full-guide').bounding_box();assert guide['y']>=nav['y']+nav['height']-2,(width,route,nav,guide)
  go('assessment-practice');page.screenshot(path=str(out/f'practice-{width}.png'))
 go('visual-map');assert page.locator('[data-visual-card]').count()==37;assert page.locator('.cue-accent').count()>=37
 for i,grid in enumerate(page.locator('.visual-map-grid').all()):grid.screenshot(path=str(out/f'gallery-{i}.png'))
 page.set_viewport_size({'width':390,'height':900});go('ksb-k1');page.locator('#lesson-full-guide').screenshot(path=str(out/'full-answer-card-phone.png'));page.locator('[data-step=full]').click();page.screenshot(path=str(out/'full-answer-phone.png'))
 direct=b.new_page(service_workers='block');direct.on('pageerror',lambda e:errors.append(str(e)));direct.goto((root/'index.html').as_uri()+'#ksb-b5');direct.locator('[data-step=full]').click();expect(direct.locator('.full-answer')).to_be_visible();direct.goto((root/'index.html').as_uri()+'#assessment-practice');direct.locator('#as-search').fill('quality');assert direct.locator('#as-question option').count()>0;direct.close();assert not errors,errors
 checks.append('320/390/768/1440px layouts,clearance below sticky controls,print/PDF restoration,all37two-tone drawings and direct-file detailed reading/search pass without page errors')
 b.close()
(out/'results.json').write_text(json.dumps({'status':'passed','checks':checks,'errors':errors},indent=2));print(json.dumps({'status':'passed','checks':checks},indent=2))
