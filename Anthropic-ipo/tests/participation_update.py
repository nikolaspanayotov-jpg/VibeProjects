"""Check expected timing, regional scope and attribution in the 14 November update."""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get('ANTHROPIC_TEST_URL', 'http://127.0.0.1:8814/')
OUT = ROOT/'tests'/'screenshots'
results = []


def record(name):
    results.append({'check': name, 'result': 'passed'})


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':390,'height':844})
    errors, requests = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda e: errors.append(e.text) if e.type=='error' else None)
    page.on('request', lambda r: requests.append(r.url))
    page.goto(URL, wait_until='networkidle')
    expect(page.locator('.status-list')).to_contain_text('$70–$78')
    expect(page.locator('.status-list')).to_contain_text('18 November 2026')
    expect(page.locator('.status-list')).to_contain_text('19 November 2026')
    expect(page.locator('.status-panel')).to_contain_text('subject to regulatory clearance')
    expect(page.locator('.status-list')).to_contain_text('final price pending')
    metadata = json.loads(page.locator('#source-preview-data').text_content())
    assert len(metadata)==56
    assert metadata['source-a-cover']['date']=='2026-11-10'
    assert metadata['source-a-register']['date']=='2026-11-14'
    for key in ['ipo','uk','eea','au-ca','jp']:
        source_id='source-a-'+key+'-fwp'
        assert metadata[source_id]['kind']=='Issuer FWP'
        assert metadata[source_id]['date']=='2026-11-12'
        expect(page.locator('#'+source_id)).to_contain_text('Issuer-dated')
    record('Official expected EST dates are conditional; five additional FWPs have filing dates distinct from the S-1/A and review date')

    page.locator('#what-changed a[href="#regional-access"]').click()
    assert page.locator('#regional-access').bounding_box()['y']>=page.locator('.masthead').bounding_box()['height']
    page.locator('#regional-documents summary').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#regional-documents')).to_have_attribute('open','')
    region=page.locator('#regional-access')
    for text in ['$120 maximum', '$70–$78', 'not a newly announced U.S. range', '16:00 CET / 10:00 ET', 'each intermediary sets its own closing time', '20 November', 'AEDT', 'EST', 'Switzerland', 'Germany', 'Sweden']:
        expect(region).to_contain_text(text)
    expect(region).to_contain_text('not additional shares')
    expect(region).to_contain_text('does not establish your eligibility')
    record('Regional scope, broker cutoffs, the legal price ceiling and AEDT/EST civil-date difference remain visible and qualified')

    link=page.locator('#regional-access a[href="#source-a-eea-fwp"]')
    link.click()
    expect(page.locator('#source-preview-kind')).to_have_text('Issuer FWP')
    expect(page.locator('#source-preview-date-label')).to_have_text('SEC filing date')
    expect(page.locator('#source-preview-context')).to_contain_text('Issuer-dated 11 November')
    page.keyboard.press('Escape')
    assert link.evaluate('e=>e===document.activeElement')
    record('Regional source preview distinguishes issuer and SEC dates and restores keyboard focus')

    expect(page.locator('#order-book')).to_contain_text('Reuters')
    expect(page.locator('#order-book')).to_contain_text('at Thursday’s close')
    expect(page.locator('#order-book')).to_contain_text('not six-times revenue demand')
    expect(page.locator('#order-book')).to_contain_text('one-in-six allocation probability')
    expect(page.locator('#order-book')).to_contain_text('not new company guidance')
    page.locator('#roadshow-evidence summary').click()
    expect(page.locator('#roadshow-evidence')).to_contain_text('not measure hardware speed directly')
    expect(page.locator('#roadshow-evidence')).to_contain_text('Q2-to-Q3 increase')
    record('Reported orders and issuer efficiency/customer claims retain attribution and do not become revenue, hardware or return forecasts')

    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    for width,name in [(390,'mobile'),(1440,'desktop')]:
        page.set_viewport_size({'width':width,'height':1000})
        for target in ['overview','what-changed','regional-access','order-book']:
            page.locator('#'+target).evaluate("e=>e.scrollIntoView({block:'start'})")
            page.screenshot(path=str(OUT/f'nov14-{name}-{target}.png'))
    record('Updated status, regional disclosure and demand evidence reflow at 320, 390, 768 and 1440px')

    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844}).new_page()
    nojs.goto(URL)
    nojs.locator('#regional-documents summary').click()
    expect(nojs.locator('#regional-documents')).to_contain_text('16:00 CET / 10:00 ET')
    expect(nojs.locator('#order-book')).to_contain_text('About 6×')
    nojs.locator('#roadshow-evidence summary').click()
    expect(nojs.locator('#roadshow-evidence')).to_contain_text('revenue divided by compute')
    assert nojs.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert errors==[],errors
    assert all(url.startswith(URL) or url.startswith('data:') for url in requests),requests
    record('New evidence remains complete without JavaScript; enhanced page has no errors or third-party runtime requests')
    browser.close()

(ROOT/'tests'/'participation-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
