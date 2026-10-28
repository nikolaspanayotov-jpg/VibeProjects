"""Exercise the actual page in Chromium on file:// and nested HTTP hosting."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright, expect, Error as PlaywrightError
import json, os

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests'/'artifacts'; OUT.mkdir(exist_ok=True)
results=[]; errors=[]; skipped=[]; completed=False; browser_version=None
def passed(name):
    results.append(name); print('PASS:',name,flush=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/budget26/'

def prepare(page,error_log=None):
    log=errors if error_log is None else error_log
    page.on('pageerror',lambda e: log.append(str(e)))
    page.on('console',lambda m: log.append(m.text) if m.type=='error' else None)
    page.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))

def shown(page): return page.locator('.policy:visible').count()
def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), 'Global horizontal overflow'

try:
  with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('BUDGET26_CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    browser_version=browser.version
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page(); prepare(page)
    page.goto(url)
    expect(page.locator('#result-count')).to_have_text('48 of 48 policies shown')
    assert shown(page)==48
    expect(page.locator('#forecast-panel')).to_be_visible()
    passed('Nested static HTTP loading with optional font unavailable')
    page.screenshot(path=str(OUT/'desktop.png'))

    query=page.locator('#policy-query')
    assert page.locator('.route-grid>li').count()==4
    for link in page.locator('.route-grid a').all():
        target=link.get_attribute('href')
        query.fill('unmatchableqzx')
        page.locator('button[data-topic="business"]').click()
        link.click()
        expect(page.locator(target)).to_be_visible()
        expect(page.locator(target+' .policy-details')).to_have_attribute('open','')
        expect(page.locator(target+' h3')).to_be_focused()
        expect(query).to_have_value('')
    passed('All twelve audience links recover filtered policies and focus their headings')

    assert page.locator('.policy-comparison').count()==3
    query.fill('£20,000')
    expect(page.locator('#policy-cash-isa')).to_be_visible()
    query.fill('£6,200')
    assert shown(page)==1 and page.locator('#policy-business-mileage').is_visible()
    page.locator('#reset-filters').click()
    page.goto(url+'#example-business-mileage')
    expect(page.locator('#policy-business-mileage .policy-details')).to_have_attribute('open','')
    expect(page.locator('#example-business-mileage')).to_be_focused()
    expect(page.locator('#example-business-mileage .calculation-total dd')).to_have_text('£6,200')
    page.goto(url+'#example-lifetime-isa')
    expect(page.locator('#example-lifetime-isa .calculation-total dd')).to_have_text('£500')
    passed('Comparisons/examples are searchable; deep examples reveal their closed policies')

    for term in page.locator('.term-link').all():
        origin=term.get_attribute('id'); definition=term.get_attribute('href')
        page.evaluate('(id)=>location.hash=id',origin)
        expect(term).to_be_focused()
        term.click()
        expect(page.locator(definition)).to_be_focused()
        page.locator('#glossary-return').click()
        expect(term).to_be_focused()
        assert page.evaluate('location.hash')=='#'+origin
    passed('All six glossary links focus definitions and return to the exact reading passage')
    assert page.locator('.timeline>li').count()==20
    assert set(page.locator('.date-kind').all_text_contents())=={'Starts','Relief ends','Planned'}
    expect(page.locator('.timeline time[datetime="2027-04-01"]')).to_have_text('1 April 2027')
    expect(page.locator('.timeline time[datetime="2027-04-06"]')).to_have_text('6 April 2027')
    expect(page.locator('.timeline-planned:has(time[datetime="2028-01-02"]) a')).to_have_attribute('href','#policy-private-hire')
    passed('Timeline distinguishes exact starts, relief expiries and planned delivery')
    page.goto(url)
    page.locator('#reading-routes').scroll_into_view_if_needed()
    page.screenshot(path=str(OUT/'reading-routes.png'))

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

    tax_context=page.locator('#savings-property-context')
    assert tax_context.evaluate('(e)=>e.previousElementSibling.id')=='policy-property-income'
    assert tax_context.evaluate('(e)=>e.nextElementSibling.id')=='policy-cash-isa'
    for phrase in ['savings income','property income']:
        query.fill(phrase); expect(tax_context).to_be_visible()
    query.fill('Casey pension'); expect(tax_context).to_be_hidden()
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    expect(tax_context).to_be_visible()
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    expect(tax_context).to_be_hidden()
    for width,name in [(1440,'desktop'),(390,'mobile')]:
        page.set_viewport_size({'width':width,'height':920})
        page.goto(url+'#policy-property-income')
        page.locator('#policy-property-income .policy-details').evaluate('(e)=>e.open=false')
        page.screenshot(path=str(OUT/(name+'-tax-context.png')))
    page.set_viewport_size({'width':1440,'height':1000})
    page.goto(url)

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
    page.evaluate("() => { window.print = () => { throw new Error('Blocked'); }; }")
    page.locator('#print-guide').click()
    expect(page.locator('#print-status')).to_contain_text('Printing could not open')
    assert query.input_value()=='ISA' and shown(page)==count
    passed('Full-content print/PDF, exact state restoration and print failure recovery')

    page.goto(url)
    page.goto(url+'#policy-household-energy-payment')
    page.screenshot(path=str(OUT/'desktop-policies.png'))
    page.locator('.policy-details').evaluate_all('(els)=>els.forEach(e=>e.open=true)')
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
    # Let hashchange's scheduled focus complete before moving to another control.
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
    page.locator('#policy-query').focus()
    expect(page.locator('#policy-query')).to_be_focused()
    expect(page.locator('#policy-query')).to_have_css('outline-style','solid')
    page.emulate_media(reduced_motion='reduce')
    assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
    page.evaluate("document.documentElement.style.zoom='2'")
    no_overflow(page)
    page.screenshot(path=str(OUT/'zoom-200.png'))
    passed('Keyboard skip link, visible focus, reduced motion and 200% CSS zoom layout')

    file_page=context.new_page(); file_errors=[]; prepare(file_page,file_errors)
    try:
        file_page.goto((ROOT/'index.html').as_uri()+'#policy-your-first-home')
    except PlaywrightError as e:
        if 'ERR_BLOCKED_BY_ADMINISTRATOR' not in str(e): raise
        reason='file:// loading is blocked by this Chromium runtime administrator policy'
        skipped.append(reason); print('SKIP:',reason,flush=True)
    else:
        expect(file_page.locator('#policy-your-first-home details')).to_have_attribute('open','')
        file_page.locator('#policy-query').fill('Casey')
        assert shown(file_page)==1
        assert not file_errors,file_errors
        passed('file:// loading, initial deep fragment and search')
    finally:
        file_page.close()
    plain_context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    plain=plain_context.new_page(); prepare(plain); plain.goto(url)
    assert shown(plain)==48
    expect(plain.locator('.search-controls')).to_be_hidden()
    expect(plain.locator('.baseline-topics')).to_be_visible()
    plain.locator('#policy-minimum-wages summary').click()
    expect(plain.locator('#policy-minimum-wages .source-detail')).to_be_visible()
    assert plain.locator('.route-grid a').count()==12
    expect(plain.locator('#policy-trading-allowance .policy-comparison')).to_be_visible()
    plain.locator('#policy-lifetime-isa .policy-details>summary').click()
    expect(plain.locator('#example-lifetime-isa')).to_be_visible()
    plain.locator('#read-term-your-first-home').click()
    expect(plain.locator('#term-equity-loan')).to_be_in_viewport()
    expect(plain.locator('#glossary-return')).to_be_hidden()
    no_overflow(plain)
    passed('No-JavaScript reading, audience/glossary links, comparisons, examples and native details')

    touch_context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    touch=touch_context.new_page(); prepare(touch); touch.goto(url)
    touch.locator('#contents-menu summary').tap()
    touch.get_by_role('link',name='Reading routes',exact=True).tap()
    expect(touch.locator('#contents-menu')).not_to_have_attribute('open','')
    touch.locator('.route-grid').screenshot(path=str(OUT/'mobile-reading-routes.png'))
    touch.locator('.route-grid a[href="#policy-trading-allowance"]').tap()
    expect(touch.locator('#policy-trading-allowance .policy-details')).to_have_attribute('open','')
    touch.locator('#policy-trading-allowance').screenshot(path=str(OUT/'mobile-comparison.png'))
    touch.goto(url+'#example-business-mileage')
    expect(touch.locator('#example-business-mileage')).to_be_focused()
    touch.locator('#example-business-mileage').screenshot(path=str(OUT/'mobile-mileage-example.png'))
    touch.goto(url+'#example-lifetime-isa')
    touch.locator('#example-lifetime-isa').screenshot(path=str(OUT/'mobile-lisa-example.png'))
    touch.goto(url+'#policy-your-first-home')
    touch.locator('#read-term-your-first-home').tap()
    expect(touch.locator('#term-equity-loan')).to_be_focused()
    touch.locator('.glossary-grid').screenshot(path=str(OUT/'mobile-glossary.png'))
    touch.locator('#glossary-return').tap()
    expect(touch.locator('#read-term-your-first-home')).to_be_focused()
    touch.locator('#contents-menu summary').tap()
    touch.get_by_role('link',name='Dates to watch',exact=True).tap()
    touch.screenshot(path=str(OUT/'mobile-timeline.png'))
    touch.locator('.policy-details').evaluate_all('(els)=>els.forEach(e=>e.open=true)')
    no_overflow(touch)
    passed('390px touch-mobile routes, comparisons, both examples, glossary return and timeline')

    native_context=browser.new_context(permissions=['clipboard-read','clipboard-write'])
    native=native_context.new_page(); prepare(native); native.goto(url+'#policy-household-energy-payment')
    native.locator('#policy-household-energy-payment .copy-link').click()
    expect(native.locator('#copy-status')).to_contain_text('Link copied for Household Energy Payment')
    assert native.evaluate('() => navigator.clipboard.readText()')==url+'#policy-household-energy-payment'
    passed('Real Chromium clipboard writes and reads the expected permanent URL with permission granted')
    assert not errors, errors
    passed('No browser page or console errors')
    completed=True
    browser.close()
finally:
    server.shutdown(); server.server_close()
    (OUT/'results.json').write_text(json.dumps({'completed':completed,'browser_version':browser_version,'passed':results,'skipped':skipped,'errors':errors},indent=2))
print('All',len(results),'browser scenarios passed.')
