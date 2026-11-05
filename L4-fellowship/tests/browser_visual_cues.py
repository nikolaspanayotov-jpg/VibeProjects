"""All 37 memory cues stay consistent across learning surfaces without changing progress."""
import argparse,hashlib,json
from pathlib import Path
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-visual-cues-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];KEY='l4-fellowship.v1';checks=[];errors=[]
source=json.loads((root/'ksb-visuals.json').read_text());expected=[*[f'K{i}' for i in range(1,16)],*[f'S{i}' for i in range(1,16)],*[f'B{i}' for i in range(1,8)]]
assert list(source)==expected and len({v['svg'] for v in source.values()})==37 and len({v['name'] for v in source.values()})==37
for value in source.values():ET.fromstring('<svg>'+value['svg']+'</svg>')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 go('today')
 with page.expect_download():page.locator('[data-action="backup"]').first.click()
 before=saved();expect(page.locator('.ksb-cell')).to_have_count(37)
 for id in expected:
  tile=page.locator('.ksb-cell[href="#ksb-'+id.lower()+'"]');expect(tile.locator('[data-ksb-visual="'+id+'"]')).to_have_count(1);assert source[id]['name'] in tile.get_attribute('title')
 go('visual-map');expect(page.locator('.visual-memory-card')).to_have_count(37);art={}
 for id in expected:
  card=page.locator('[data-visual-card="'+id+'"]');expect(card).to_contain_text(source[id]['name']);expect(card).to_contain_text(source[id]['caption']);expect(card).to_have_attribute('href','#ksb-'+id.lower());image=card.locator('[data-ksb-visual]');expect(image).to_have_attribute('aria-hidden','true');expect(image).to_have_attribute('focusable','false');art[id]=image.locator('g').inner_html()
 assert len(set(art.values()))==37
 assert page.evaluate('L4_CURRICULUM.visualSha256')==hashlib.sha256((root/'ksb-visuals.json').read_bytes()).hexdigest()
 page.screenshot(path=str(out/'visual-map-desktop.png'),full_page=True)
 for id in expected:
  go('ksb-'+id.lower());expect(page.locator('.lesson-title .ksb-with-visual')).to_contain_text(id);expect(page.locator('.lesson-title [data-ksb-visual]')).to_have_attribute('data-ksb-visual',id);assert page.locator('.lesson-title [data-ksb-visual] g').inner_html()==art[id];expect(page.locator('.lesson-title .ksb-memory')).to_contain_text(source[id]['name']);expect(page.locator('.lesson-title .ksb-memory')).to_contain_text(source[id]['caption'])
 after=saved();assert after['ksbs']==before['ksbs'] and after['game']==before['game'] and after['evidence']==before['evidence']
 checks.append('All 37 distinct authored SVGs/names/captions appear in the map, index and matching lesson; browsing every cue preserves answers, rewards and evidence')
 go('library');expect(page.locator('.ksb-row')).to_have_count(37);expect(page.locator('.ksb-row .ksb-with-visual')).to_have_count(37)
 page.locator('#library-search').fill('roadblock');expect(page.locator('.ksb-row')).to_have_count(1);expect(page.locator('.ksb-row .ksb-tag')).to_have_text('B2');page.locator('[data-action="clear-filters"]').click()
 go('readiness');expect(page.locator('.readiness-topic [data-ksb-visual]')).to_have_count(37)
 go('connections-quality');assert page.locator('.connection-node [data-ksb-visual]').evaluate_all('(els)=>els.map(e=>e.dataset.ksbVisual)')==['K8','S6','B5']
 go('practice');page.locator('#practice-topic').select_option('K1');page.locator('[data-action="start-practice"]').click();expect(page.locator('.session-strip [data-ksb-visual]')).to_have_attribute('data-ksb-visual','K1');expect(page.locator('.ksb-memory')).to_contain_text('Law scales');assert saved()['game']['events']==[]
 go('labs-statistics');assert page.locator('.activity-ksbs [data-ksb-visual]').count()>0
 checks.append('Library search finds memory names; the same shapes accompany readiness, connection nodes, practice prompts and related KSB chips; visuals create no practice rewards')
 go('visual-map');page.locator('[data-visual-card="S13"]').focus();page.keyboard.press('Enter');expect(page.locator('h1')).to_contain_text('Time Series');page.screenshot(path=str(out/'s13-desktop.png'),full_page=True)
 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for route in ['today','library','visual-map','ksb-k1','ksb-s13','readiness','connections-quality','practice','quests']:
   go(route);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
  go('visual-map');assert page.locator('[data-visual-card="K1"] .ksb-visual').bounding_box()['width']>=60
 page.set_viewport_size({'width':390,'height':900});go('ksb-s13');page.screenshot(path=str(out/'s13-mobile.png'),full_page=True);go('visual-map');page.screenshot(path=str(out/'visual-map-mobile.png'),full_page=True)
 page.locator('[data-action="text-size"]').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 page.emulate_media(media='print');expect(page.locator('.visual-memory-card [data-ksb-visual]')).to_have_count(37);expect(page.locator('[data-action="print"]')).not_to_be_visible();page.pdf(path=str(out/'visual-memory-sheet.pdf'),format='A4',print_background=True);assert (out/'visual-memory-sheet.pdf').stat().st_size>10000;page.emulate_media(media='screen')
 direct=browser.new_page();direct.on('pageerror',lambda e:errors.append(str(e)));direct.goto((root/'index.html').as_uri()+'#visual-map');expect(direct.locator('[data-visual-card]')).to_have_count(37);assert direct.locator('[data-ksb-visual="B5"] g').inner_html()==art['B5'];direct.close();assert not errors,errors
 checks.append('Keyboard links, 320/390/768/1280px reflow, readable cue sizes, enlarged text, a 37-picture print/PDF sheet and direct file opening work without page errors')
 ctx.close();browser.close()
(out/'results.json').write_text(json.dumps(dict(status='passed',checks=checks,page_errors=errors),indent=2));print(json.dumps(dict(status='passed',checks=checks),indent=2))
