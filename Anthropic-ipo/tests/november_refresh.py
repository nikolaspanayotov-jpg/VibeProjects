"""Verify the 10 November proposal, distinct share bases and evidence integration."""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get('ANTHROPIC_TEST_URL', 'http://127.0.0.1:8810/')
OUT = ROOT / 'tests' / 'screenshots'
results = []


def record(name):
    results.append({'check': name, 'result': 'passed'})


with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = b.new_page(viewport={'width':390, 'height':844})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(URL, wait_until='networkidle')
    assert 801_351_354 + 23_648_646 == 825_000_000
    for expected in ['$70–$78', '825m', '$26bn', '$84.6bn']:
        expect(page.locator('#offering-terms')).to_contain_text(expected)
    expect(page.locator('#offering-terms')).to_contain_text('not cash received today')
    page.locator('#offering-breakdown summary').click()
    for expected in ['801,351,354', '23,648,646', '123,750,000', '351,351,348', '$3.8bn', 'reduces its remaining NPA facility to $10bn']:
        expect(page.locator('#offering-breakdown')).to_contain_text(expected)
    assert 825_000_000 * 70 / 1e9 == 57.75
    assert 825_000_000 * 78 / 1e9 == 64.35
    record('Primary/secondary shares and gross range reconcile; conditional placement, fees, tax use and funding overlap remain explicit')

    summary = 7_427_991_791 + 5_658_680_800
    expanded = 7_430_143_944 + 7_804_580_273 + 1_704_567_865 + 1_073_701_297
    assert summary == 13_086_672_591 and expanded == 18_012_993_379
    for button, count in [('load-summary-basis', summary), ('load-expanded-basis', expanded)]:
        page.locator('#'+button).click()
        expect(page.locator('#valuation-shares')).to_have_value(str(count/1e9))
        expect(page.locator('#valuation-price')).to_have_value('74')
        expect(page.locator('#valuation-equity')).to_have_text(f'${count*74/1e9:,.2f}bn')
        expect(page.locator('#valuation-multiple')).to_have_text(f'{count*74/1e9/33.242:,.2f}×')
    expect(page.locator('#valuation-bases')).to_contain_text('fund-held shares')
    record('Both $74 presets reconcile to independently summed economic columns and nine-month revenue; non-economic shares are excluded')

    expect(page.locator('#run-rate-update')).to_contain_text('$81bn')
    expect(page.locator('#run-rate-update')).to_contain_text('$71bn')
    expect(page.locator('#run-rate-update')).to_contain_text('not contracted recurring revenue or a forecast')
    expect(page.locator('#run-rate-update')).to_contain_text(f'{10/71*100:.1f}%')
    expect(page.locator('#retail-access')).to_contain_text('up to 20%')
    expect(page.locator('#retail-access')).to_contain_text('including underwriter allocations')
    expect(page.locator('#share-supply')).to_contain_text('not automatically freely tradable on day one')
    expect(page.locator('#share-supply')).to_contain_text('316m')
    expect(page.locator('#roadmap')).to_contain_text('does not verify new contracts or financial outcomes')
    expect(page.locator('#commitments')).to_contain_text('67m RSUs')
    expect(page.locator('#commitments')).to_contain_text('does not confirm the IPO date')
    page.locator('#new-financing-exposures summary').click()
    for required in ['$14.2bn', '$3.8bn', '$4.2bn', '$500m', '$2.8bn']:
        expect(page.locator('#new-financing-exposures')).to_contain_text(required)
    record('IPO accounting charge, cash withholding and differently scoped contingent infrastructure exposures remain distinct')
    record('Run-rate, retail cap, sale eligibility, placement restrictions, RSU event and scheduled livestream keep their material qualifications')

    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        page.locator('#valuation-bases').evaluate('e=>e.open=true')
        page.locator('#share-supply details').evaluate('e=>e.open=true')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    record('New proposal tables, expanded valuation bases and release schedule reflow at 320, 390, 768 and 1440px')
    for width,label in [(390,'mobile'),(1440,'desktop')]:
        page.set_viewport_size({'width':width,'height':1000})
        for id in ['offering-terms','run-rate-update','november-developments','share-supply']:
            page.locator('#'+id).evaluate("e=>e.scrollIntoView({block:'start'})")
            page.screenshot(path=str(OUT/f'nov10-{label}-{id}.png'))

    c = b.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    static = c.new_page();static.goto(URL)
    expect(static.locator('#offering-terms')).to_contain_text('$84.6bn')
    static.locator('#valuation-bases summary').click()
    expect(static.locator('#valuation-bases')).to_contain_text('18,012,993,379')
    expect(static.locator('#load-summary-basis')).not_to_be_visible()
    static.locator('#share-supply summary').click()
    expect(static.locator('.supply-table')).to_be_visible()
    assert errors == [], errors
    record('New substantive disclosures remain accessible without JavaScript; enhanced page has no script errors')
    b.close()

(ROOT/'tests'/'november-refresh-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
