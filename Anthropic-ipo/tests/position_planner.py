"""Exercise the valuation and position decision tools, not a broker workflow."""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
URL=os.environ.get('ANTHROPIC_TEST_URL','http://127.0.0.1:8824/')
OUT=ROOT/'tests'/'screenshots'
OUT.mkdir(exist_ok=True)
results=[]
def record(name): results.append({'check':name,'result':'passed'})
def open_details(page, selector):
    loc=page.locator(selector)
    if loc.get_attribute('open') is None: loc.locator(':scope > summary').click()
def row(page, label):
    return page.locator('#position-output-rows tr').filter(has=page.get_by_role('rowheader',name=label,exact=True))

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':390,'height':1000})
    errors,requests=[],[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda e:errors.append(e.text) if e.type=='error' else None)
    page.on('request',lambda r:requests.append(r.url))
    page.goto(URL,wait_until='networkidle')
    expect(page.locator('#valuation-equity')).to_have_text('$400.00bn')
    expect(page.locator('#valuation-basis')).to_have_value('reported')
    expect(page.locator('#independent-valuations')).to_contain_text('$92')
    expect(page.locator('#independent-valuations')).to_contain_text('$94.38')
    expect(page.locator('#independent-valuations')).to_contain_text('$25 bear and $188 bull')
    expect(page.locator('#independent-valuations')).to_contain_text('403')
    expect(page.locator('#forecast-assumptions')).to_contain_text('not company guidance')
    expect(page.locator('#forecast-assumptions')).to_contain_text('+159.0%')
    expect(page.locator('#forecast-assumptions')).to_contain_text('+102.2%')
    expect(page.locator('#hl-access-example')).to_contain_text('15:00 London')
    expect(page.locator('#hl-access-example')).to_contain_text('not IBKR')
    expect(page.locator('#position-plan')).to_contain_text('not recover the initial $1,480')
    expect(page.locator('#position-method')).to_contain_text('not an HMRC tax calculator')
    record('Published opinions, access limits, attributed forecasts, broker-specific terms and author rules remain separate from filed results')

    expect(page.locator('#entry-reference-rows tr')).to_have_count(5)
    expect(page.locator('#entry-reference-rows tr').nth(1)).to_contain_text('+$360.00')
    expect(page.locator('#entry-reference-rows tr').last).to_contain_text('−$160.00')
    page.locator('#entry-reference').fill('100')
    expect(page.locator('#entry-reference-context')).to_contain_text('Custom illustrative reference')
    expect(page.locator('#entry-reference-rows tr').last).to_contain_text('$0.00')
    page.locator('#entry-reference').fill('')
    expect(page.locator('#entry-reference-error')).to_be_visible()
    expect(page.locator('#entry-reference-results')).to_be_hidden()
    page.locator('#entry-reference-form button[type="reset"]').click()
    expect(page.locator('#entry-reference')).to_have_value('92')
    record('Entry table recalculates all five prices, labels a custom reference, hides invalid results and resets to the published opinion')

    expect(page.locator('#forward-price')).to_have_text('$91.60 per share')
    expect(page.locator('#forward-matrix tr')).to_have_count(3)
    assert page.locator('#forward-matrix td').count()==9
    open_details(page,'#forward-advanced')
    page.locator('#forward-dilution').fill('10')
    expect(page.locator('#forward-price')).to_have_text('$83.27 per share')
    expect(page.locator('#position-mark')).to_have_value('92')
    page.locator('#use-forward-mark').click()
    assert abs(float(page.locator('#position-mark').input_value())-83.2732)<.0001
    assert page.locator('#position-mark').evaluate('e=>e===document.activeElement')
    assert page.locator('#position-mark').bounding_box()['y']>=page.locator('.masthead').bounding_box()['height']
    page.locator('#forward-shares').fill('0')
    expect(page.locator('#forward-error')).to_be_visible()
    expect(page.locator('#forward-results')).to_be_hidden()
    page.locator('#forward-form button[type="reset"]').click()
    expect(page.locator('#forward-price')).to_have_text('$91.60 per share')
    record('Forward model includes every cross-combination, isolates fixed-equity dilution and transfers a mark only after an explicit keyboard-accessible action')

    page.locator('#position-form button[type="reset"]').click()
    expect(page.locator('#position-cost-status')).to_contain_text('not net profit')
    page.locator('#position-price').fill('100')
    expect(page.locator('#position-context')).to_contain_text('exceeds the framework’s illustrative $78')
    page.locator('#position-price').fill('74')
    expect(row(page,'Gross purchase outflows')).to_contain_text('$1,480.00')
    expect(row(page,'Gross purchase outflows')).to_contain_text('£1,184.00')
    expect(row(page,'Realised economic P/L')).to_contain_text('$0.00')
    expect(row(page,'Unrealised P/L at assumed mark')).to_contain_text('+$360.00')
    open_details(page,'#position-lots')
    page.locator('#position-mark').fill('40')
    expect(row(page,'Acquired / remaining shares')).to_contain_text('20 / 20')
    expect(page.locator('#position-buy1-enabled')).not_to_be_checked()
    page.locator('#position-buy1-enabled').check()
    expect(row(page,'Remaining acquisition average')).to_contain_text('$71.78')
    page.locator('#position-buy2-enabled').check()
    expect(row(page,'Gross purchase outflows')).to_contain_text('$2,053.50')
    expect(page.locator('#position-comparison tr').last).to_contain_text('−$853.50')
    page.locator('#position-buy2-review').fill('1')
    expect(page.locator('#position-error')).to_contain_text('at most one addition')
    expect(page.locator('#position-results')).to_be_hidden()
    page.locator('#position-buy2-review').fill('2')
    expect(page.locator('#position-results')).to_be_visible()
    record('No price fall enables a purchase; optional tranches change average/loss only when selected and require distinct reviews')

    page.locator('#load-sale-example').click()
    expect(row(page,'Acquired / remaining shares')).to_contain_text('20 / 10')
    expect(row(page,'Sale receipts')).to_contain_text('$1,017.50')
    expect(row(page,'Realised economic P/L')).to_contain_text('+$277.50')
    page.locator('#position-sell1-qty').fill('21')
    expect(page.locator('#position-error')).to_contain_text('exceeds')
    page.locator('#position-form button[type="reset"]').click()
    page.locator('#position-sell1-enabled').check()
    page.locator('#position-sell1-qty').fill('20')
    page.locator('#position-sell1-price').fill('92')
    page.locator('#position-sell1-fx').fill('1.4')
    expect(row(page,'Combined P/L after holding costs')).to_contain_text('+£130.29')
    expect(row(page,'Remaining acquisition average')).to_contain_text('Not applicable')
    record('Staged-sale example preserves remaining exposure; overselling is rejected and a full exit with different FX reconciles sterling profit')

    page.locator('#position-form button[type="reset"]').click()
    cap_details=page.locator('#position-cap').locator('xpath=ancestor::details[1]')
    cap_details.locator(':scope > summary').click() if cap_details.get_attribute('open') is None else None
    page.locator('#position-cost-mode').select_option('included')
    expect(page.locator('#position-error')).to_contain_text('explicit zero')
    expect(page.locator('#position-results')).to_be_hidden()
    for input_el in page.locator('#position-form [data-position-fee]:enabled').all(): input_el.fill('0')
    expect(page.locator('#position-cost-status')).to_contain_text('Supplied costs included')
    page.locator('#position-initial-usd-fee').fill('2')
    expect(row(page,'Gross purchase outflows')).to_contain_text('$1,482.00')
    page.locator('#position-cap-currency').select_option('GBP')
    page.locator('#position-cap').fill('1184')
    expect(page.locator('#position-breaches')).to_contain_text('GBP contribution cap exceeded by 1.60')
    assert page.locator('#position-results').is_visible()
    page.locator('#position-qty').fill('0')
    expect(row(page,'Acquired / remaining shares')).to_contain_text('0 / 0')
    expect(row(page,'Remaining acquisition average')).to_contain_text('Not applicable')
    page.locator('#position-qty').fill('1.5')
    expect(page.locator('#position-results')).to_be_hidden()
    page.locator('#position-form button[type="reset"]').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#position-announcement')).to_contain_text('before-costs arithmetic')
    record('Unknown fees cannot produce a net result; explicit fees, GBP cap breach, zero/fractional allocations and keyboard reset have meaningful states')

    metadata=json.loads(page.locator('#source-preview-data').text_content())
    assert len(metadata)==56
    for source_id in ['source-morningstar11','source-morningstar9','source-damodaran3','source-hl-offer','source-hl-first-day','source-sec-orders','source-hmrc-shares','source-hmrc-matching']:
        link=page.locator('a.source-link[href="#'+source_id+'"]').first
        link.evaluate("e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}}")
        link.click()
        expect(page.locator('#source-preview-kind')).to_have_text(metadata[source_id]['kind'])
        page.keyboard.press('Escape')
        assert link.evaluate('e=>e===document.activeElement')
    for key in ['fair-value','price-target','average-cost','realised-unrealised','forward-ps','currency-risk']:
        link=page.locator('a[data-term="'+key+'"]').first;link.click()
        assert page.locator('#term-preview-relevance').inner_text().strip()
        page.keyboard.press('Escape');assert link.evaluate('e=>e===document.activeElement')
    record('Eight new sources and six definitions preserve dated provenance, access limits, dialog behaviour and keyboard focus')

    page.locator('#briefing-query').fill('not recover the initial')
    page.locator('#briefing-query').press('Enter')
    page.locator('#search-results a').first.click()
    selected=page.evaluate('location.hash')
    assert page.locator(selected).evaluate("e=>!!e.closest('#position-sale-rules')")
    page.reload(wait_until='networkidle')
    assert page.locator(selected).evaluate('e=>e===document.activeElement')
    assert page.locator(selected).bounding_box()['y']>=page.locator('.masthead').bounding_box()['height']
    record('New position evidence is searchable inside native disclosures and its focused passage link survives reload')

    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        page.locator('#position-plan details').evaluate_all('es=>es.forEach(e=>e.open=true)')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    for width,name in [(390,'mobile'),(1440,'desktop')]:
        page.set_viewport_size({'width':width,'height':1100})
        for target in ['independent-valuations','forward-results','position-planner','position-results']:
            page.locator('#'+target).evaluate("e=>e.scrollIntoView({block:'start'})")
            page.screenshot(path=str(OUT/f'position-{name}-{target}.png'))
    page.emulate_media(media='print')
    expect(page.locator('#position-form')).to_be_hidden()
    expect(page.locator('#position-cost-status')).to_contain_text('not net profit')
    record('Expanded controls/results reflow at 320–1440px; printed figures retain the before-costs qualification with controls hidden')

    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':1000}).new_page()
    nojs.goto(URL)
    expect(nojs.locator('#position-form')).to_be_hidden()
    expect(nojs.locator('#entry-reference-rows tr')).to_have_count(5)
    assert nojs.locator('#forward-matrix td').count()==9
    for label in ['Gross purchase outflows','Remaining acquisition average','Realised economic P/L','Combined P/L after holding costs']:
        assert row(nojs,label).locator('th,td').all_text_contents()==row(page,label).locator('th,td').all_text_contents()
    nojs.locator('#position-addition-rules summary').click()
    expect(nojs.locator('#position-addition-rules .detail-body')).to_be_visible()
    assert nojs.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert errors==[],errors
    assert all(u.startswith(URL) or u.startswith('data:') for u in requests),requests
    assert page.evaluate('localStorage.length')==0
    record('Static examples remain complete without JavaScript; no errors, external runtime requests or persisted positions were observed')
    browser.close()

(ROOT/'tests'/'position-browser-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
