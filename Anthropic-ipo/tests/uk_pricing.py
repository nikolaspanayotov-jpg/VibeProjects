"""Verify matched IPO pricing, conditional IBKR currency costs and accessible fallbacks."""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get('ANTHROPIC_TEST_URL', 'http://127.0.0.1:8820/')
OUT = ROOT/'tests'/'screenshots'
OUT.mkdir(exist_ok=True)
results = []


def record(name):
    results.append({'check': name, 'result': 'passed'})


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':390, 'height':1000})
    errors, requests = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda e: errors.append(e.text) if e.type=='error' else None)
    page.on('request', lambda r: requests.append(r.url))
    page.goto(URL, wait_until='networkidle')
    region = page.locator('#uk-ipo-costs')
    for text in ['no UK-residency premium', 'final price equal to the final U.S. IPO price',
                 'maximum can be amended', 'do not establish $120 as a universal or separate UK cap',
                 'one for each underlying share', 'unverified', 'not a maximum all-in cost']:
        expect(region).to_contain_text(text)
    expect(page.locator('#uk-ibkr-checks')).to_contain_text('cash-only subscription cannot guarantee exactly 20 shares')
    expect(page.locator('#uk-cost-method')).to_contain_text('not verified IPO subscription fees')
    record('Common issuer pricing, amendable regional ceiling, CDI route and unknown IPO-specific charges remain distinct')

    page.locator('#what-changed a[href="#uk-ipo-costs"]').click()
    assert region.bounding_box()['y']>=page.locator('.masthead').bounding_box()['height']
    page.reload()
    assert page.url.endswith('#uk-ipo-costs')
    assert region.bounding_box()['y']>=page.locator('.masthead').bounding_box()['height']
    expect(page.locator('#uk-cost-shares')).to_have_value('20')
    expect(page.locator('#uk-cost-consideration')).to_have_text('$1,480.00 for the shares')
    expect(page.locator('#uk-usd-total')).to_have_text('£1,184.00')
    expect(page.locator('#uk-auto-extra')).to_have_text('≈ £0.36')
    expect(page.locator('#uk-auto-per-share')).to_have_text('≈ 1.78p')
    expect(page.locator('#uk-auto-total')).to_have_text('≈ £1,184.36')
    expect(page.locator('#uk-manual-extra')).to_have_text('£1.60')
    expect(page.locator('#uk-manual-per-share')).to_have_text('8.00p')
    expect(page.locator('#uk-manual-percent')).to_have_text('0.135%')
    query = page.locator('#briefing-query')
    query.fill('0.20 basis point')
    query.press('Enter')
    page.locator('#search-results a').first.click()
    passage = page.locator(page.evaluate('location.hash'))
    assert passage.evaluate("e=>!!e.closest('#uk-ipo-costs')")
    assert passage.evaluate('e=>e===document.activeElement')
    expect(page.locator('#uk-cost-method')).to_have_attribute('open','')
    page.reload(wait_until='networkidle')
    assert passage.evaluate('e=>e===document.activeElement')
    assert passage.bounding_box()['y']>=page.locator('.masthead').bounding_box()['height']
    page.locator('#uk-cost-method summary').click()
    record('Direct and search passage links survive reload with header clearance; 20-share midpoint illustration rounds only after calculation')

    page.locator('#uk-cost-price').fill('78')
    page.locator('#uk-cost-shares').fill('5')
    page.locator('#uk-cost-rate').fill('1.3')
    expect(page.locator('#uk-cost-consideration')).to_have_text('$390.00 for the shares')
    expect(page.locator('#uk-usd-total')).to_have_text('£300.00')
    expect(page.locator('#uk-auto-extra')).to_have_text('≈ £0.09')
    expect(page.locator('#uk-manual-extra')).to_have_text('£1.54')
    expect(page.locator('#uk-manual-per-share')).to_have_text('30.77p')
    expect(page.locator('#uk-manual-percent')).to_have_text('0.513%')
    page.locator('#uk-cost-shares').fill('20')
    page.locator('#uk-cost-price').fill('10000')
    page.locator('#uk-cost-rate').fill('1.25')
    expect(page.locator('#uk-manual-extra')).to_have_text('£3.20')
    expect(page.locator('#uk-manual-percent')).to_have_text('0.002%')
    expect(page.locator('#uk-manual-usd')).to_contain_text('exceeds the $2 minimum')
    record('Smaller allocations raise minimum cost per share; manual FX correctly switches to 0.002% above its minimum')

    for field,value in [('price',''),('price','0'),('shares','21'),('shares','1.5'),('shares','0'),('rate','0'),('rate','-1')]:
        page.locator('#uk-cost-form button').click()
        page.locator('#uk-cost-'+field).fill(value)
        expect(page.locator('#uk-cost-error')).to_be_visible()
        expect(page.locator('#uk-cost-'+field)).to_have_attribute('aria-invalid','true')
        expect(page.locator('#uk-cost-results')).to_be_hidden()
        expect(page.locator('#uk-cost-announcement')).to_have_text('')
    page.locator('#uk-cost-form button').click()
    page.locator('#uk-cost-price').fill('0.01')
    page.locator('#uk-cost-shares').fill('1')
    page.locator('#uk-cost-rate').fill('100')
    expect(page.locator('#uk-cost-error')).to_be_hidden()
    expect(page.locator('#uk-usd-total')).to_have_text('<£0.01')
    expect(page.locator('#uk-auto-extra')).to_have_text('≈ <£0.01')
    expect(page.locator('#uk-auto-per-share')).to_have_text('≈ <0.01p')
    page.locator('#uk-cost-form button').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#uk-cost-shares')).to_have_value('20')
    expect(page.locator('#uk-cost-rate')).to_have_value('1.25')
    expect(page.locator('#uk-cost-announcement')).to_contain_text('IPO application charges are not included')
    record('Invalid, empty, fractional and above-cap inputs hide results; tiny values stay nonzero and keyboard reset announces assumptions')

    metadata = json.loads(page.locator('#source-preview-data').text_content())
    assert len(metadata)==56
    for source_id,kind,label in [('source-a-international-brokers','Company page','Checked'),
                                  ('source-ibkr-uk-offer','Broker announcement','Published'),
                                  ('source-ibkr-fx','Broker fee schedule','Checked'),
                                  ('source-ibkr-stocks','Broker fee schedule','Checked')]:
        assert metadata[source_id]['kind']==kind
        link = region.locator('a[href="#'+source_id+'"]')
        link.click()
        expect(page.locator('#source-preview-kind')).to_have_text(kind)
        expect(page.locator('#source-preview-date-label')).to_have_text(label)
        page.keyboard.press('Escape')
        assert link.evaluate('e=>e===document.activeElement')
    record('Four new source previews distinguish broker notices, checked tariffs and issuer evidence, with focus restoration')

    page.locator('#uk-cost-method summary').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#uk-cost-method')).to_have_attribute('open','')
    page.locator('#uk-ibkr-checks summary').click()
    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    for width,name in [(390,'mobile'),(1440,'desktop')]:
        page.set_viewport_size({'width':width,'height':1100})
        for target in ['uk-ipo-costs','uk-cost-calculator','uk-cost-results']:
            page.locator('#'+target).evaluate("e=>e.scrollIntoView({block:'start'})")
            page.screenshot(path=str(OUT/f'uk-{name}-{target}.png'))
    page.emulate_media(media='print')
    expect(page.locator('#uk-cost-form')).to_be_hidden()
    expect(page.locator('#uk-cost-context')).to_contain_text('20 allocated shares')
    expect(page.locator('#uk-manual-total')).to_have_text('£1,185.60')
    record('Expanded UK content reflows at 320, 390, 768 and 1440px; printed results retain assumptions with controls hidden')

    nojs = browser.new_context(java_script_enabled=False,viewport={'width':390,'height':1000}).new_page()
    nojs.goto(URL+'#uk-ipo-costs')
    expect(nojs.locator('#uk-cost-form')).to_be_hidden()
    for selector in ['#uk-usd-total','#uk-auto-extra','#uk-auto-per-share','#uk-auto-total',
                     '#uk-manual-extra','#uk-manual-per-share','#uk-manual-percent','#uk-manual-total']:
        expect(nojs.locator(selector)).to_have_text(page.locator(selector).text_content())
    nojs.locator('#uk-cost-method summary').click()
    nojs.locator('#uk-ibkr-checks summary').click()
    expect(nojs.locator('#uk-cost-method .detail-body')).to_be_visible()
    expect(nojs.locator('#uk-ibkr-checks .detail-body')).to_be_visible()
    assert nojs.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert errors==[],errors
    assert all(u.startswith(URL) or u.startswith('data:') for u in requests),requests
    record('No-JavaScript funding figures match enhanced defaults; native details work without errors or third-party runtime requests')
    browser.close()

(ROOT/'tests'/'uk-pricing-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
