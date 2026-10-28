"""Exercise the actual page in Chromium on file:// and nested HTTP hosting."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright, expect
import json, os

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests'/'artifacts'; OUT.mkdir(exist_ok=True)
results=[]; errors=[]
def passed(name):
    results.append(name); print('PASS:',name,flush=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/budget26/'

def prepare(page):
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
    page.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))

def shown(page): return page.locator('.policy:visible').count()
def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), 'Global horizontal overflow'

try:
  with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('BUDGET26_CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page(); prepare(page)
    page.goto(url)
    expect(page.locator('#result-count')).to_have_text('48 of 48 policies shown')
    assert shown(page)==48
    expect(page.locator('#forecast-panel')).to_be_visible()
    passed('Nested static HTTP loading with optional font unavailable')
    page.screenshot(path=str(OUT/'desktop.png'))

    query=page.locator('#policy-query')
    query.fill('CASEY pension')
    assert shown(page)==1
    assert page.locator('#policy-state-pension').is_visible()
    assert not page.locator('#policy-state-pension details').evaluate('(e)=>e.open')
    assert query.evaluate('(e)=>e===document.activeElement')
    passed('Case-insensitive multi-word search finds closed detail without changing focus')
    page.locator('button[data-topic="business"]').click()
    assert shown(page)==0
    expect(page.locator('#no-results')).to_be_visible()
    page.locator('#empty-reset').click()
    assert shown(page)==48 and query.input_value()==''
    assert query.evaluate('(e)=>e===document.activeElement')
    passed('Search AND topic, no-results recovery and reset focus')

    for topic,count in [('bills',8),('tax',8),('work',8),('business',11),('funding',8),('spending',5),('all',48)]:
        page.locator(f'button[data-topic="{topic}"]').click()
        assert shown(page)==count
        assert page.locator('#topic-select').input_value()==topic
        expect(page.locator(f'button[data-topic="{topic}"]')).to_have_attribute('aria-pressed','true')
    passed('All six topic counts and desktop/mobile state synchronisation')

    page.locator('button[data-topic="business"]').click()
    query.fill('unmatchableqzx')
    page.evaluate("location.hash='policy-household-energy-payment'")
    expect(query).to_have_value('')
    expect(page.locator('#policy-household-energy-payment details')).to_have_attribute('open','')
    assert shown(page)==48
    page.wait_for_function("document.activeElement===document.querySelector('#policy-household-energy-payment h3')")
    assert page.locator('#policy-household-energy-payment h3').bounding_box()['y']>=72
    page.locator('button[data-topic="business"]').click()
    page.get_by_role('link',name='Some breathing space for energy costs').click()
    expect(page.locator('#topic-select')).to_have_value('all')
    assert shown(page)==48
    page.evaluate("location.hash='economy-table'")
    expect(page.locator('#forecast-data')).to_have_attribute('open','')
    page.evaluate("location.hash='%E0%A4%A'")
    passed('Changed and repeated filtered fragments, focus clearance, nested disclosure and malformed hash')

    for metric in ['gdp','cpi','unemployment','borrowing','borrowing-share','debt']:
        page.locator('#forecast-metric').select_option(metric)
        assert page.locator('#forecast-chart circle').count()==6
        assert 'financial years' in page.locator('#chart-desc').text_content() if metric in ['borrowing','borrowing-share','debt'] else 'calendar years' in page.locator('#chart-desc').text_content()
        values=page.locator(f'tr[data-metric="{metric}"] td').all_text_contents()
        chart=page.locator('#forecast-chart text').all_text_contents()[5::2]
        assert chart==values,(metric,chart,values)
    passed('Every chart metric uses exact table values, correct year type and six labelled points')

    page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('Denied')}}})")
    article=page.locator('#policy-household-energy-payment')
    article.locator('.copy-link').click()
    fallback=article.locator('.copy-fallback input')
    expect(fallback).to_be_visible()
    assert fallback.input_value().endswith('#policy-household-energy-payment')
    assert fallback.evaluate('(e)=>e.selectionEnd-e.selectionStart')==len(fallback.input_value())
    passed('Clipboard denial provides a selected read-only permanent URL')
    page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async(text)=>{window.copiedBudgetUrl=text}}})")
    article.locator('.copy-link').click()
    expect(page.locator('#copy-status')).to_contain_text('Link copied for Household Energy Payment')
    expect(article.locator('.copy-fallback')).to_be_hidden()
    passed('Clipboard success announces the correct policy and clears stale fallback')

    for article in page.locator('.policy').all():
        detail=article.locator('details')
        if not detail.evaluate('(e)=>e.open'): detail.locator('summary').click()
        article.locator('.copy-link').click()
        expect(page.locator('#copy-status')).to_contain_text('Link copied')
        assert page.evaluate('window.copiedBudgetUrl').endswith('#'+article.get_attribute('id'))
        detail.locator('summary').click()
    passed('Every native policy disclosure and all 48 copy buttons exercised')

    query.fill('ISA')
    page.locator('button[data-topic="tax"]').click()
    page.locator('#policy-cash-isa details').evaluate('(e)=>e.open=true')
    before=page.locator('details').evaluate_all('(els)=>els.map(e=>e.open)')
    count=shown(page)
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    assert shown(page)==48
    assert all(page.locator('details').evaluate_all('(els)=>els.map(e=>e.open)'))
    page.emulate_media(media='print')
    no_overflow(page)
    page.pdf(path=str(OUT/'print-guide.pdf'),format='A4',print_background=True)
    page.emulate_media(media='screen')
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert query.input_value()=='ISA' and page.locator('#topic-select').input_value()=='tax'
    assert shown(page)==count
    assert page.locator('details').evaluate_all('(els)=>els.map(e=>e.open)')==before
    page.evaluate("window.print=()=>{throw new Error('Blocked')}")
    page.locator('#print-guide').click()
    expect(page.locator('#print-status')).to_contain_text('Printing could not open')
    assert query.input_value()=='ISA' and shown(page)==count
    passed('Full-content print/PDF, exact state restoration and print failure recovery')

    page.goto(url)
    page.locator('#changes-heading').scroll_into_view_if_needed()
    page.screenshot(path=str(OUT/'desktop-policies.png'))
    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':920})
        no_overflow(page)
        page.locator('#forecast-metric').select_option('debt')
        if width<960:
            page.locator('#topic-select').select_option('tax')
            assert shown(page)==8
            page.locator('#reset-filters').click()
        if width==390:
            page.goto(url)
            page.screenshot(path=str(OUT/'mobile.png'))
            page.locator('#contents-menu summary').click()
            page.get_by_role('link',name='The OBR outlook',exact=True).click()
            assert not page.locator('#contents-menu').evaluate('(e)=>e.open')
            page.locator('#forecast-metric').select_option('debt')
            page.screenshot(path=str(OUT/'mobile-obr.png'))
            page.locator('#contents-menu summary').click()
            page.keyboard.press('Escape')
            assert not page.locator('#contents-menu').evaluate('(e)=>e.open')
            assert page.locator('#contents-menu summary').evaluate('(e)=>e===document.activeElement')
    passed('320/390/768/1440 layouts, no global overflow, mobile Contents and Escape focus')

    page.goto(url)
    page.keyboard.press('Tab')
    expect(page.locator('.skip')).to_be_focused()
    page.keyboard.press('Enter')
    expect(page.locator('#main')).to_be_focused()
    page.locator('#policy-query').focus()
    assert page.locator('#policy-query').evaluate('(e)=>getComputedStyle(e).outlineStyle')=='solid'
    page.emulate_media(reduced_motion='reduce')
    assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
    page.evaluate("document.documentElement.style.zoom='2'")
    no_overflow(page)
    page.screenshot(path=str(OUT/'zoom-200.png'))
    passed('Keyboard skip link, visible focus, reduced motion and 200% CSS zoom layout')

    file_page=context.new_page(); prepare(file_page)
    file_page.goto((ROOT/'index.html').as_uri()+'#policy-your-first-home')
    expect(file_page.locator('#policy-your-first-home details')).to_have_attribute('open','')
    file_page.locator('#policy-query').fill('Casey')
    assert shown(file_page)==1
    passed('file:// loading, initial deep fragment and search')
    plain_context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    plain=plain_context.new_page(); prepare(plain); plain.goto(url)
    assert shown(plain)==48
    expect(plain.locator('.search-controls')).to_be_hidden()
    expect(plain.locator('.baseline-topics')).to_be_visible()
    plain.locator('#policy-minimum-wages summary').click()
    expect(plain.locator('#policy-minimum-wages .source-detail')).to_be_visible()
    no_overflow(plain)
    passed('No-JavaScript reading, topic anchors and native details')
    assert not errors, errors
    passed('No browser page or console errors')
    browser.close()
finally:
    server.shutdown(); server.server_close()
    (OUT/'results.json').write_text(json.dumps({'passed':results,'errors':errors},indent=2))
print('All',len(results),'browser scenarios passed.')
