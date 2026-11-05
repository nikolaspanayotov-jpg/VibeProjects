"""Behavior and print checks for the five November reading tools."""
from pathlib import Path
import json
import os
import re
import subprocess
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests' / 'screenshots'
URL = os.environ.get('ANTHROPIC_TEST_URL', 'http://127.0.0.1:8806/')
results = []


def record(name):
    results.append({'check': name, 'result': 'passed'})


def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')


def screenshot(page, target, name):
    page.locator(target).evaluate("e=>e.scrollIntoView({block:'start'})")
    page.screenshot(path=str(OUT / name))


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                               args=['--no-sandbox', '--disable-dev-shm-usage'])
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    errors, network = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda e: errors.append(e.text) if e.type == 'error' else None)
    page.on('request', lambda r: network.append(r.url))
    page.goto(URL, wait_until='networkidle')
    expect(page.locator('#valuation-equity')).to_have_text('$400.00bn')
    expect(page.locator('#valuation-multiple')).to_have_text('12.03×')
    expect(page.locator('#valuation-context')).to_contain_text('January–September 2026')
    expect(page.locator('#valuation-calculator')).to_contain_text('invented teaching inputs')
    record('Initial valuation is explicitly hypothetical and uses reported nine-month revenue without annualising')

    query = page.locator('#briefing-query')
    query.fill('compute')
    query.press('Enter')
    expect(page.locator('#search-results > li')).to_have_count(10)
    page.locator('#search-more').click()
    expect(page.locator('#search-results > li')).to_have_count(20)
    assert page.locator('#search-results > li').nth(10).locator('a').evaluate('e=>e===document.activeElement')
    texts = page.locator('#search-results p').all_text_contents()
    assert len(set(texts)) == len(texts)
    record('Search finds current article text, paginates and gives keyboard focus to newly shown results')

    query.fill('900%')
    query.press('Enter')
    hidden_link = page.locator('#search-results a').filter(has_text='What can build value').first
    hidden_link.click()
    selected_hash = page.evaluate('location.hash')
    destination = page.locator(selected_hash)
    assert destination.evaluate('e=>e===document.activeElement')
    assert destination.evaluate("e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS'&&!p.open)return false;p=p.parentElement;}return true;}")
    assert destination.bounding_box()['y'] >= page.locator('.masthead').bounding_box()['height']
    page.reload(wait_until='networkidle')
    expect(page.locator(selected_hash)).to_be_visible()
    assert page.locator(selected_hash).evaluate('e=>e===document.activeElement')
    record('Search opens collapsed financial definitions, clears the mobile header and supports reloading its passage URL')

    query.fill('non-cash')
    query.press('Enter')
    assert page.locator('#search-results > li').count() > 0
    query.fill('zzzzuniqueabsenttopic')
    query.press('Enter')
    expect(page.locator('#search-status')).to_contain_text('No matching passages')
    expect(page.locator('#search-results > li')).to_have_count(0)
    query.fill('<img src=x onerror=alert(1)>')
    query.press('Enter')
    expect(page.locator('#search-results img')).to_have_count(0)
    page.locator('#search-clear').click()
    expect(query).to_have_value('')
    assert query.evaluate('e=>e===document.activeElement')
    query.press('Enter')
    expect(page.locator('#search-status')).to_contain_text('Enter a topic')
    record('Search handles punctuation, empty and absent queries, treats input as text and clears without navigation')

    price, shares = page.locator('#valuation-price'), page.locator('#valuation-shares')
    price.focus()
    for _ in range(4):
        rects = page.evaluate("""()=>({control:document.activeElement.getBoundingClientRect().top, summary:document.getElementById('valuation-summary').getBoundingClientRect().bottom})""")
        assert rects['control'] >= rects['summary']
        page.keyboard.press('Tab')
    record('Mobile keyboard traversal keeps price, shares, revenue choice and reset below the sticky valuation result')
    price.fill('25')
    shares.fill('8')
    expect(page.locator('#valuation-equity')).to_have_text('$200.00bn')
    expect(page.locator('#valuation-multiple')).to_have_text('6.02×')
    page.locator('#valuation-basis').select_option('hypothetical')
    expect(page.locator('#valuation-multiple')).to_have_text('4.00×')
    expect(page.locator('#valuation-context')).to_contain_text('hypothetical 12-month revenue')
    expect(page.locator('#valuation-sensitivity tr').first.locator('td').first).to_have_text('$144bn2.88×')
    expect(page.locator('#valuation-sensitivity .is-base')).to_have_text('$200bn4.00× · current')
    for i, row in enumerate(page.locator('#valuation-sensitivity tr').all()):
        for j, cell in enumerate(row.locator('td').all()):
            expected = 25 * [.8, 1, 1.2][i] * 8 * [.9, 1, 1.1][j]
            expect(cell.locator('strong')).to_have_text(f'${expected:,.2f}'.rstrip('0').rstrip('.')+'bn')
    record('Valuation and all nine sensitivity cases reconcile independently; changing revenue basis updates the period')

    for invalid in ['', '0', '-5', '1000001']:
        price.fill(invalid)
        expect(page.locator('#valuation-error')).to_be_visible()
        expect(page.locator('#valuation-results')).to_be_hidden()
        expect(price).to_have_attribute('aria-invalid', 'true')
    price.fill('25')
    page.locator('#valuation-revenue').fill('0')
    expect(page.locator('#valuation-results')).to_be_hidden()
    page.locator('#valuation-basis').select_option('reported')
    expect(page.locator('#valuation-results')).to_be_visible()
    expect(page.locator('#valuation-revenue')).to_be_disabled()
    price.fill('.01')
    shares.fill('.001')
    expect(page.locator('#valuation-equity')).to_have_text('<$0.01bn')
    expect(page.locator('#valuation-multiple')).to_have_text('<0.01×')
    page.locator('#valuation-form button[type=reset]').click()
    expect(price).to_have_value('20')
    expect(shares).to_have_value('20')
    expect(page.locator('#valuation-equity')).to_have_text('$400.00bn')
    record('Invalid inputs hide stale outputs, basis changes ignore disabled fields, tiny positives stay non-zero and reset restores the example')

    for node in page.locator('.partner-node').all():
        node.locator('summary').click()
        expect(node.locator('.partner-detail')).to_be_visible()
        expect(node).to_contain_text('analysis')
        link = node.locator('a[href^="#source-"]').first
        link.click()
        expect(page.locator('#source-preview')).to_be_visible()
        page.keyboard.press('Escape')
        assert link.evaluate('e=>e===document.activeElement')
        node.locator('summary').click()
    record('All partner relationships expand natively and their evidence previews restore focus')

    for scenario in page.locator('#evidence-tracker .scenario').all():
        scenario.locator('summary').click()
        expect(scenario).to_contain_text('Would strengthen this scenario')
        expect(scenario).to_contain_text('Would weaken this scenario')
        expect(scenario).to_contain_text('Next evidence:')
    record('Each scenario exposes both directions of evidence and the next disclosure to assess')

    for width in [320, 390, 768, 1440]:
        page.set_viewport_size({'width': width, 'height': 1000})
        for node in page.locator('.partner-node').all():
            node.evaluate('e=>e.open=true')
        no_overflow(page)
        for key in ['#valuation-price', '#valuation-shares']:
            page.locator(key).fill('10000')
        no_overflow(page)
        page.locator('#valuation-form button[type=reset]').click()
    record('Search, valuation including large values, expanded partners and scenarios reflow at 320, 390, 768 and 1440px')

    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('.partner-node').evaluate_all('es=>es.forEach(e=>e.open=false)')
    for target, name in [('#reading-toolbox','tools-mobile-search.png'),('#valuation-calculator','tools-mobile-valuation.png'),('#valuation-sensitivity','tools-mobile-sensitivity.png'),('#partner-map','tools-mobile-partners.png'),('#evidence-tracker','tools-mobile-evidence.png')]:
        screenshot(page, target, name)
    page.locator('#partner-amazon > summary').click()
    screenshot(page, '#partner-amazon', 'tools-mobile-partner-open.png')
    page.set_viewport_size({'width': 1440, 'height': 1050})
    for target, name in [('#valuation-calculator','tools-desktop-valuation.png'),('#partner-map','tools-desktop-partners.png'),('#evidence-tracker','tools-desktop-evidence.png')]:
        screenshot(page, target, name)

    brief = ctx.new_page()
    brief.on('pageerror', lambda e: errors.append(str(e)))
    brief.goto(URL+'investment-brief.html', wait_until='networkidle')
    expect(brief.locator('h1')).to_have_count(1)
    expect(brief.get_by_role('button', name='Print / save PDF')).to_be_visible()
    brief.evaluate('window.print=()=>{window.printRequested=true;}')
    brief.get_by_role('button', name='Print / save PDF').click()
    assert brief.evaluate('window.printRequested') is True
    for width in [320, 390, 1440]:
        brief.set_viewport_size({'width': width, 'height': 1000})
        no_overflow(brief)
    brief.set_viewport_size({'width': 390, 'height': 844})
    brief.screenshot(path=str(OUT/'brief-mobile.png'))
    brief.set_viewport_size({'width': 1440, 'height': 1100})
    brief.screenshot(path=str(OUT/'brief-desktop.png'))
    brief.pdf(path=str(ROOT/'tests'/'investment-brief.pdf'), print_background=True, prefer_css_page_size=True)
    record('Separate brief has a working print action, mobile/desktop reflow and a generated print PDF')

    nojs = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844}).new_page()
    nojs.goto(URL)
    expect(nojs.locator('#briefing-search')).to_be_hidden()
    expect(nojs.locator('.search-fallback')).to_be_visible()
    expect(nojs.locator('#valuation-form')).to_be_hidden()
    expect(nojs.locator('#valuation-equity')).to_have_text('$400.00bn')
    expect(nojs.locator('#valuation-sensitivity .is-base')).to_contain_text('12.03×')
    nojs.locator('#partner-google > summary').click()
    expect(nojs.locator('#partner-google .partner-detail')).to_be_visible()
    nojs.locator('#scenario-funding summary').click()
    expect(nojs.locator('#scenario-funding .signal-grid')).to_be_visible()
    no_overflow(nojs)
    nojs.goto(URL+'investment-brief.html')
    expect(nojs.locator('#print-brief')).to_be_hidden()
    expect(nojs.locator('body')).to_contain_text("browser's Print command")
    nojs.pdf(path=str(ROOT/'tests'/'investment-brief-nojs.pdf'), print_background=True, prefer_css_page_size=True)
    record('No-JavaScript path retains the worked valuation, partner/scenario disclosures and printable brief')

    assert errors == [], errors
    assert all(url.startswith(URL) or url.startswith('data:') for url in network), network
    record('No page or console errors and no runtime third-party requests')
    browser.close()

for name in ['investment-brief.pdf','investment-brief-nojs.pdf']:
    pdf = ROOT/'tests'/name
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    assert pages == 2, (name, pages)
    text = subprocess.check_output(['pdftotext', str(pdf), '-'], text=True)
    for required in ['Three tailwinds', 'Three headwinds', 'Retail access', '79%', '25%', '$69.8bn', 'not free cash flow', '135', '143.89', 'January/March 2027', '5 November 2026']:
        assert required in text, (name, required)
record('Brief prints as exactly two A4 pages with and without JavaScript, preserving dates, conditions and material evidence')
(ROOT/'tests'/'reading-tools-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
