"""Browser checks for the standalone IPO guide. Requires installed Playwright/Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import json
import re
import os

PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / "tests" / "screenshots"
OUTPUT.mkdir(parents=True, exist_ok=True)
URL = os.environ.get("ANTHROPIC_TEST_URL", "http://127.0.0.1:8765/")
results = []


def record(name, detail="passed"):
    results.append({"check": name, "result": detail})


def no_overflow(page, name):
    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), name
    record(name)


def go_section(page, section_id):
    page.evaluate("""id => {
        const target = document.getElementById(id);
        const padding = innerWidth < 1100 && target.matches('.section-divider') ? parseFloat(getComputedStyle(target).paddingTop) : 0;
        const top = target.getBoundingClientRect().top + scrollY + padding;
        const offset = innerWidth >= 1100 ? 24 : document.querySelector('.masthead').getBoundingClientRect().height + 20;
        scrollTo(0, top - offset);
    }""", section_id)
    page.wait_for_timeout(100)


with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/usr/bin/chromium", headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    errors = []
    console_errors = []
    requests = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda e: console_errors.append(e.text) if e.type == "error" else None)
    page.on("request", lambda r: requests.append(r.url))
    response = page.goto(URL, wait_until="networkidle")
    assert response.status == 200
    page.evaluate("document.fonts.ready")
    expect(page.locator("h1")).to_have_count(1)
    expect(page.locator("#result-amount")).to_have_text("−$567m")
    expect(page.get_by_role("radio", name="Third quarter 2026")).to_be_checked()
    expect(page.locator("#ledger-title")).to_have_text("Third quarter 2026")
    expect(page.locator(".status-list")).to_contain_text("Not yet specified in the filing")
    expect(page.locator("#briefing h3")).to_have_count(3)
    expect(page.locator("#briefing")).to_contain_text("$70–$78 proposed")
    expect(page.locator("#per100-amount")).to_have_text("$103")
    expect(page.locator("#margin-amount")).to_have_text("−3.3%")
    expect(page.locator("#briefing")).to_contain_text("Q3 2026 GAAP operating loss")
    record("60-second briefing and latest-Q3 default explanation")
    no_overflow(page, "390px default reflow")
    record("HTTP 200, preliminary terms and Q3 default")

    invalid = page.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')]
        .filter(a => !document.getElementById(a.hash.slice(1))).map(a => a.hash)""")
    assert invalid == [], invalid
    record("All internal citation/navigation targets exist")
    ids = page.locator("[id]").evaluate_all("es => es.map(e => e.id)")
    assert len(ids) == len(set(ids)), "Duplicate IDs"
    record("Unique document and source identifiers")

    views = page.locator("#financial-views")
    expect(views.locator(".measure-card")).to_have_count(3)
    expect(views).to_contain_text("Nine months ended 30 September 2026")
    assert views.locator(".measure-value").all_text_contents() == ["−$1.26bn", "−$104.04bn", "+$6.57bn"]
    expect(views).to_contain_text("$94.324bn")
    expect(views).to_contain_text("$131.845bn")
    expect(views).to_contain_text("$2.540bn")
    expect(views).to_contain_text("excludes investing activities and financing proceeds")
    record("Nine-month financial measures, September liquidity and non-cash/investing qualifications")

    expect(page.locator(".status-list")).to_contain_text("$70–$78")
    expect(page.locator(".status-list")).to_contain_text("10 November 2026")
    page.locator("#filing-history > summary").click()
    expect(page.locator("#filing-history li")).to_have_count(3)
    expect(page.locator("#filing-history")).to_contain_text("26 October 2026")
    page.locator("#filing-history > summary").click()
    expect(page.locator('.comparison .historical-label')).to_contain_text("January–June 2026 for both")
    record("Latest amendment/check dates, original filing history and historical matched comparison")

    expect(page.locator("#what-changed")).to_contain_text("10 November 2026")
    expect(page.locator("#what-changed .update-grid > div")).to_have_count(3)
    expect(page.locator("#what-changed")).to_contain_text("new amendment proposes $70–$78")
    expect(page.locator("#what-changed")).to_contain_text("Supply and sentiment matter")
    for link in page.locator('#what-changed a:not(.source-link)').all():
        link.click()
        assert page.evaluate("location.hash") == link.get_attribute("href")
        target = page.locator(link.get_attribute("href"))
        assert target.bounding_box()["y"] >= page.locator(".masthead").bounding_box()["height"]
    record("Returning-reader changes distinguish filing, added context and unresolved terms; onward links work")

    retail = page.locator("#retail-access")
    expect(retail).to_contain_text("An allocation in the offering would use the final IPO price")
    expect(retail).to_contain_text("does not guarantee")
    expect(retail).to_contain_text("request deadlines and allocation rules require current platform confirmation")
    expect(retail).to_contain_text("up to 20% of the offering")
    assert retail.locator(".retail-dates time").evaluate_all("es=>es.map(e=>e.dateTime)") == [
        "2026-11-10", "2026-11-04", "2026-11-10"
    ]
    assert retail.locator(".retail-table tbody th").all_text_contents() == [
        "Schwab", "Fidelity", "Robinhood", "Trade-PMR", "SoFi", "E*TRADE"
    ]
    assert retail.locator(".retail-platforms li").all_text_contents() == [
        "Schwab", "Fidelity", "Robinhood", "Trade-PMR", "SoFi", "E*TRADE"
    ]
    expect(page.locator("#retail-broker-details")).not_to_have_attribute("open", "")
    expect(retail.locator(".retail-table")).to_contain_text("National Financial Services LLC")
    expect(retail.locator(".retail-table")).to_contain_text("Trade-PMR, Inc.")
    expect(retail).to_contain_text("availability depends on investor location")
    record("Retail access keeps six filed platform groups, legal entities, dates and unresolved allocation requirements explicit")

    expect(retail.locator(".retail-paths li")).to_have_count(2)
    expect(retail).to_contain_text("fewer shares than sought, or none")
    expect(retail.locator("#retail-market-effects")).to_contain_text("Analysis")
    expect(retail.locator("#retail-market-effects")).to_contain_text("Potential tailwind")
    expect(retail.locator("#retail-market-effects")).to_contain_text("Potential headwind")
    expect(retail.locator("#retail-market-effects")).to_contain_text("does not establish the price direction")
    record("IPO allocation and market purchases remain distinct; retail price implications are conditional analysis")

    for origin, target in [("#retail-access", "#entry-comparison"), ("#entry-comparison", "#retail-access")]:
        page.locator(f'{origin} a[href="{target}"]').click()
        assert page.evaluate("location.hash") == target
        assert page.locator(target).bounding_box()["y"] >= page.locator(".masthead").bounding_box()["height"]
    record("Bidirectional retail/SpaceX entry links work and clear the sticky header")

    ledger = json.loads(page.locator("#ledger-data").text_content())
    ratios = []
    for key in ["q2", "q3"]:
        period = ledger["periods"][key]
        ratio = period["costs"]["compute"] / period["revenue"] * 100
        ratios.append(ratio)
        expect(page.locator(f"#compute-ratio-{key}")).to_have_text(f"{ratio:.1f}%")
        width = page.locator(f"#compute-ratio-bar-{key}").evaluate("e=>parseFloat(e.style.width)")
        assert abs(width - ratio) < .001
    expect(page.locator("#compute-ratio-change")).to_have_text(f"{ratios[1]-ratios[0]:.1f} percentage points")
    expect(page.locator("#trend-revenue-growth")).to_have_text("+46.7%")
    expect(page.locator("#trend-compute-growth")).to_have_text("+77.5%")
    expect(page.locator("#compute-trend")).to_contain_text("not a cash-spending ratio")
    expect(page.locator("#compute-trend")).to_contain_text("$5.0bn")
    record("Compute ratios, percentage-point change, growth and bar scale reconcile to the financial dataset")

    expect(page.locator(".adoption-card")).to_have_count(3)
    expect(page.locator(".adoption-card dt")).to_have_count(9)
    expect(page.locator("#adoption-government")).to_contain_text("500")
    expect(page.locator("#adoption-government")).to_contain_text("40% discount")
    expect(page.locator("#adoption-government")).to_contain_text("No minimum spending commitment")
    expect(page.locator("#adoption-enterprise")).to_contain_text("trailing-year revenue")
    expect(page.locator("#adoption-science")).to_contain_text("preprint-stage")
    expect(page.locator("#adoption-science")).to_contain_text("does not establish incremental revenue")
    expect(page.locator(".adoption-watch")).to_contain_text("10 November")
    record("Commercial scorecards distinguish filed paid activity, company claims, opportunities and limits")

    expect(page.locator("#ownership-map .ownership-lanes > li")).to_have_count(3)
    assert page.locator("#ownership-map h5").all_text_contents() == [
        "Economic participation", "Voting and board control", "Tradable supply"
    ]
    expect(page.locator("#ownership-map")).to_contain_text("50.1%")
    expect(page.locator("#ownership-map")).to_contain_text("Class F has no economic rights")
    expect(page.locator("#ownership-map")).to_contain_text("does not create economic ownership a second time")
    expect(page.locator("#ownership-map")).to_contain_text("neither proves selling nor fixes the price direction")
    record("Ownership diagram separates economic, voting and trading rights without double-counting conversions")

    entry_data = json.loads(page.locator("#entry-return-data").text_content())
    assert entry_data["cutoff"] == "2026-10-29" and entry_data["endpointPrice"] == 14389
    assert [e["price"] for e in entry_data["entries"].values()] == [13500, 15000, 21139]
    assert entry_data["axisMaximum"] == 120
    for key, entry in entry_data["entries"].items():
        index = entry_data["endpointPrice"] / entry["price"] * 100
        change = index - 100
        sign = "+" if change >= 0 else "−"
        row = page.locator(f'[data-entry="{key}"]')
        expect(row.locator("[data-entry-index]")).to_have_text(f"{index:.1f}")
        expect(row.locator("[data-entry-return]")).to_have_text(f"{sign}{abs(change):.1f}%")
        assert abs(row.locator(".entry-bar").evaluate("e=>parseFloat(e.style.width)") - index/120*100) < .001
    expect(page.locator("#entry-comparison")).to_contain_text("not a live quote")
    expect(page.locator("#entry-comparison")).to_contain_text("closing price, not that day's higher intraday peak")
    expect(page.locator("#entry-comparison")).to_contain_text("Fees, taxes and distributions are excluded")
    record("Three SpaceX entry returns use one endpoint, integer-cent inputs and a common index scale")

    expect(page.locator("#operating-reconciliation .recon-steps li")).to_have_count(4)
    assert page.locator("#operating-reconciliation .recon-steps strong").all_text_contents() == ["−$567m", "+$1,070m", "+$1,960m", "+$2,463m"]
    expect(page.locator("#operating-reconciliation")).to_contain_text("not cash flow")
    record("Complete Q3 GAAP-to-adjusted bridge with economic qualification")

    commitments = json.loads(page.locator("#commitment-data").text_content())
    assert commitments["aggregate"] == 900900
    assert commitments["beforeEnd2030"] == 451600
    assert commitments["nextTwelveMonths"] == 70700
    assert commitments["preCommencementConditional"] == 186200
    assert commitments["narrowMaturityTable"] == 319993
    expect(page.locator("#commitment-overview")).to_contain_text("timing views overlap")
    expect(page.locator("#commitment-overview")).to_contain_text("$186.2bn")
    for key in ["aggregate", "beforeEnd2030", "nextTwelveMonths"]:
        width = page.locator(f'[data-commitment="{key}"]').evaluate("e=>parseFloat(e.style.width)")
        assert abs(width - commitments[key] / commitments["axisMaximum"] * 100) < .001
    page.locator("#maturity-schedule > summary").click()
    expect(page.locator("#maturity-schedule")).to_contain_text("narrower scope")
    expect(page.locator("#maturity-schedule")).to_contain_text("319.993")
    page.locator("#maturity-schedule > summary").click()
    record("Company aggregate, overlapping timing, conditions and narrower maturity scope")

    expect(page.locator("#dilution-result")).to_have_text("−4.0%")
    expect(page.locator("#per-share-index")).to_have_text("96")
    expect(page.locator("#dilution-formula")).to_have_text("120 ÷ 125 × 100 = 96 per-share index.")
    expect(page.locator("#dilution-assumptions")).to_contain_text("not Anthropic's valuation or a price forecast")
    company_slider = page.get_by_role("slider", name="Company value change")
    shares_slider = page.get_by_role("slider", name="Economic share count change")
    company_slider.focus()
    page.keyboard.press("ArrowRight")
    expect(page.locator("#company-value-output")).to_have_text("+25%")
    expect(page.locator("#dilution-result")).to_have_text("0.0%")
    assert company_slider.evaluate("e=>e===document.activeElement")
    page.keyboard.press("End")
    expect(page.locator("#dilution-result")).to_have_text("+60.0%")
    page.keyboard.press("Home")
    expect(page.locator("#dilution-result")).to_have_text("−60.0%")
    shares_slider.focus()
    page.keyboard.press("End")
    expect(page.locator("#dilution-result")).to_have_text("−75.0%")
    assert abs(page.locator("#per-share-index-bar").evaluate("e=>parseFloat(e.style.width)") - 12.5) < .01
    page.locator("#dilution-reset").click()
    expect(page.locator("#dilution-result")).to_have_text("−4.0%")
    expect(page.locator("#dilution-announcement")).to_contain_text("−4.0%")
    assert company_slider.input_value() == "20" and shares_slider.input_value() == "25"
    record("Illustrative dilution: formula, zero/gain/loss boundaries, native keys, reset and announcement")

    expect(page.locator("#roadmap .milestone")).to_have_count(6)
    expect(page.locator("#roadmap .expected")).to_contain_text("Expected")
    expect(page.locator("#roadmap .contract")).to_contain_text("90 days' advance written notice")
    expect(page.locator("#roadmap .contract")).to_contain_text("do not automatically end")
    expect(page.locator("#roadmap .unknown")).to_have_count(3)
    assert page.locator("#roadmap time").evaluate_all("es=>es.map(e=>e.dateTime)") == ["2026-11-10", "2026-12", "2027-01", "2027-03"]
    expect(page.locator("#roadmap .product-milestone")).to_contain_text("Final IPO pricing remains unconfirmed")
    record("Roadmap separates expected dates, contract windows and unresolved milestones")

    expect(page.locator("a[data-term]")).to_have_count(9)
    for link in page.locator("a[data-term]").all():
        if not link.is_visible():
            for ancestor in link.locator("xpath=ancestor::details").all():
                ancestor.evaluate("e=>e.open=true")
        key = link.get_attribute("data-term")
        link.click()
        expect(page.locator("#term-preview")).to_be_visible()
        expect(page.locator("#term-preview-title")).to_have_text(page.locator(f"#definition-{key}").text_content())
        assert len(page.locator("#term-preview-definition").inner_text()) > 35
        expect(page.locator("#term-preview-relevance")).not_to_have_text("")
        page.keyboard.press("Escape")
        expect(page.locator("#term-preview")).not_to_be_visible()
        assert link.evaluate("e=>e===document.activeElement")
    record("All nine first-use definitions and Anthropic explanations open and restore focus")
    term_link = page.locator('a[data-term="economic-shares"]')
    term_link.scroll_into_view_if_needed()
    scroll_before = page.evaluate("scrollY")
    term_link.focus();page.keyboard.press("Enter")
    page.keyboard.press("Shift+Tab")
    assert page.locator("#term-preview-glossary").evaluate("e=>e===document.activeElement")
    page.keyboard.press("Tab")
    assert page.locator("#term-preview-close").evaluate("e=>e===document.activeElement")
    page.locator("#term-preview-close").click()
    assert abs(page.evaluate("scrollY") - scroll_before) < 2
    term_link.click()
    page.locator("#term-preview-glossary").click()
    expect(page.locator("#glossary")).to_have_attribute("open", "")
    assert page.evaluate("location.hash") == "#definition-economic-shares"
    assert page.locator("#definition-economic-shares").evaluate("e=>e===document.activeElement")
    page.locator("details[open]").evaluate_all("es=>es.forEach(e=>e.open=false)")
    record("Definition keyboard containment, scroll restoration and glossary handoff")

    # Count only the main chapters; sources and closed disclosure bodies are excluded.
    expect(page.locator("#main-reading-time")).to_contain_text("min")
    expect(page.locator("[data-reading-time]")).to_have_count(5)
    before_times = page.locator("[data-reading-time]").all_text_contents()
    page.locator(".sources-list").evaluate("e=>{const p=document.createElement('p');p.id='test-source-words';p.textContent='reference '.repeat(3000);e.append(p);}")
    page.locator("#exact-figures").evaluate("e=>{const p=document.createElement('p');p.id='test-closed-words';p.textContent='optional '.repeat(3000);e.querySelector('.detail-body').append(p);}")
    page.locator("#exact-figures > summary").click()
    expect(page.locator('[data-reading-time="economics"]')).not_to_have_text(before_times[0])
    page.locator("#exact-figures > summary").click()
    expect(page.locator('[data-reading-time="economics"]')).to_have_text(before_times[0])
    assert page.locator("[data-reading-time]").all_text_contents() == before_times
    page.locator("#test-source-words, #test-closed-words").evaluate_all("es=>es.forEach(e=>e.remove())")
    record("Reading estimates exclude sources/closed details and include opened detail")
    go_section(page, "drivers")
    expect(page.locator("#mobile-chapter-label")).to_contain_text("Chapter 2 of 5")
    halfway = float(page.locator("#mobile-guide-progress").get_attribute("value"))
    assert 0 < halfway < 100
    go_section(page, "sources")
    expect(page.locator("#mobile-chapter-label")).to_contain_text("end of main guide")
    assert float(page.locator("#guide-progress").get_attribute("value")) == 100
    page.evaluate("scrollTo(0,0)");page.wait_for_timeout(100)
    assert float(page.locator("#guide-progress").get_attribute("value")) == 0
    record("Mobile chapter/position indicator and bounded 0–100 main-guide progress")

    assert page.locator(".priority-driver h3").all_text_contents() == [
        "Demand quality", "Compute economics", "Valuation and dilution"
    ]
    expect(page.locator("#supporting-drivers")).not_to_have_attribute("open", "")
    page.locator("#supporting-drivers > summary").click()
    expect(page.locator("#supporting-drivers .driver-row")).to_have_count(3)
    expect(page.locator("#supporting-drivers")).to_contain_text("Trust, safety and market access")
    no_overflow(page, "390px expanded supporting drivers")
    page.locator("#supporting-drivers > summary").click()
    record("Three reading priorities and preserved supporting evidence")

    expect(page.locator(".lesson-pair")).to_have_count(3)
    expect(page.locator(".anthropic-lesson")).to_have_count(3)
    expect(page.locator("#spacex-chronology")).not_to_have_attribute("open", "")
    expect(page.locator(".lesson-limits")).to_contain_text("not Anthropic's future price path")
    record("Three paired SpaceX lessons, visible limits and optional chronology")

    dialog = page.get_by_role("dialog", name="Amended results, compute and contractual obligations")
    trigger = page.locator('#economics .sources-inline a[href="#source-a-mda"]').first
    trigger.scroll_into_view_if_needed()
    before_scroll = page.evaluate("scrollY")
    trigger.focus()
    page.keyboard.press("Enter")
    expect(dialog).to_be_visible()
    expect(page.locator("#source-preview-kind")).to_have_text("Filing")
    expect(page.locator("#source-preview-date")).to_have_text("10 November 2026")
    expect(page.locator("#source-preview-excerpt")).not_to_be_visible()
    expect(page.locator("#source-preview-context")).to_contain_text("Q3")
    expect(page.locator("#source-preview-original")).to_have_attribute("href", re.compile(r"https://www.sec.gov/Archives/"))
    expect(page.locator("#source-preview-original")).to_have_attribute("target", "_blank")
    assert page.locator("#source-preview-close").evaluate("e=>e===document.activeElement")
    page.keyboard.press("Shift+Tab")
    assert page.locator("#source-preview-list").evaluate("e=>e===document.activeElement")
    page.keyboard.press("Tab")
    assert page.locator("#source-preview-close").evaluate("e=>e===document.activeElement")
    page.keyboard.press("Escape")
    expect(page.locator("#source-preview")).not_to_be_visible()
    assert trigger.evaluate("e=>e===document.activeElement")
    assert abs(page.evaluate("scrollY") - before_scroll) < 2
    record("Keyboard source preview, focus trap, Escape and reading-position restoration")

    page.locator('#briefing a[href="#source-a-mda"]').first.click()
    expect(page.locator("#source-preview-context")).to_contain_text("trailing-year")
    page.locator("#source-preview-close").click()
    page.locator('#commitment-overview a[href="#source-a-mda"]').click()
    expect(page.locator("#source-preview-context")).to_contain_text("$900.9bn")
    page.locator("#source-preview-close").click()
    record("Contextual research notes follow the amended customer, financial and commitment citations")

    metadata = json.loads(page.locator("#source-preview-data").text_content())
    source_ids = page.locator(".sources-list > li").evaluate_all("es=>es.map(e=>e.id)")
    assert sorted(source_ids) == sorted(metadata)
    for source_id, meta in metadata.items():
        link = page.locator(f'a[aria-haspopup="dialog"][href="#{source_id}"]').first
        if not link.is_visible():
            for ancestor in link.locator("xpath=ancestor::details").all():
                ancestor.evaluate("e=>e.open=true")
        link.click()
        expect(page.locator("#source-preview")).to_be_visible()
        expect(page.locator("#source-preview-kind")).to_have_text(meta["kind"])
        expect(page.locator("#source-preview-date")).to_have_text(meta["displayDate"])
        expect(page.locator("#source-preview-context")).to_contain_text("Research note:")
        assert page.locator("#source-preview-original").get_attribute("href").startswith("https://")
        page.locator("#source-preview-close").click()
    page.locator("details[open]").evaluate_all("es=>es.forEach(e=>e.open=false)")
    assert len(metadata) == 36
    assert metadata["source-a-gsa"]["kind"] == "Company announcement"
    assert metadata["source-a-science"]["kind"] == "Company research"
    assert metadata["source-a-event"]["date"] == "2026-11-10"
    assert metadata["source-a-register"]["date"] == "2026-11-10"
    assert metadata["source-a-retail"]["kind"] == "Filing" and metadata["source-a-retail"]["date"] == "2026-11-10"
    assert metadata["source-retail-barrons"]["kind"] == "Third-party report" and metadata["source-retail-barrons"]["date"] == "2026-11-04"
    record("All 36 source previews preserve provenance and distinguish retail filing, report and register-check dates")
    expect(page.locator("#definition-net-revenue-retention").locator("xpath=following-sibling::dd[1]")).to_contain_text("Ultra")
    record("Retention definition includes Pro, Max and Ultra cohort exclusions")

    page.locator('a[aria-haspopup="dialog"][href="#source-bloomberg"]').first.click()
    expect(page.locator("#source-preview-kind")).to_have_text("Third-party report")
    expect(page.locator("#source-preview-excerpt")).not_to_be_visible()
    page.screenshot(path=str(OUTPUT / "mobile-source-preview.png"))
    page.locator("#source-preview-list").click()
    expect(page.locator("#source-preview")).not_to_be_visible()
    assert page.evaluate("location.hash") == "#source-bloomberg"
    assert page.locator("#source-bloomberg").evaluate("e=>e===document.activeElement")
    record("Reported customer identification and explicit source-list handoff")

    page.set_viewport_size({"width": 320, "height": 568})
    page.locator('a[aria-haspopup="dialog"][href="#source-a-mda"]').first.click()
    no_overflow(page, "320px source preview reflow")
    box = page.locator("#source-preview").bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= 320
    assert box["height"] <= 568 * .89
    page.locator("#source-preview-original").scroll_into_view_if_needed()
    expect(page.locator("#source-preview-original")).to_be_in_viewport()
    page.keyboard.press("Escape")
    page.set_viewport_size({"width": 390, "height": 844})
    record("Small-screen source actions remain reachable by dialog scrolling")

    data = json.loads(page.locator("#ledger-data").text_content())
    for key, period in data["periods"].items():
        assert period["revenue"] - sum(period["costs"].values()) == period["reportedOperatingResult"]
        assert period["reportedOperatingResult"] + period["stockCompensation"] + period["charitableContributions"] == period["adjustedOperatingResult"]
    assert data["defaultPeriod"] == "q3" and len(data["periods"]) == 3
    record("Integer GAAP and adjusted reconciliation for all three periods")

    q2 = page.get_by_role("radio", name="Second quarter 2026")
    q2.check()
    expect(page.locator("#result-amount")).to_have_text("+$974m")
    expect(page.locator("#ledger-title")).to_have_text("Second quarter 2026")
    expect(page.locator("#revenue-amount")).to_have_text("$11.56bn")
    expect(page.locator("#expense-amount")).to_have_text("$10.58bn")
    expect(page.locator("#financial-views")).to_contain_text("Nine months ended 30 September 2026")
    expect(page.locator("#financial-views .measure-value").first).to_have_text("−$1.26bn")
    expect(page.locator("#per100-amount")).to_have_text("$92")
    expect(page.locator("#per100-period")).to_have_text("Q2 2026")
    expect(page.locator("#compute-ratio-q3")).to_have_text("58.2%")
    expect(page.locator("#margin-amount")).to_have_text("+8.4%")
    assert abs(float(page.locator("#revenue-bar").evaluate("e => parseFloat(e.style.width)")) - 11555 / 18000 * 100) < .001
    expect(page.locator("#period-announcement")).to_contain_text("974 million")
    record("Q2 updates values, sign, period, announcement and fixed-scale geometry")
    q2.focus()
    page.keyboard.press("ArrowLeft")
    expect(page.get_by_role("radio", name="First half 2026")).to_be_checked()
    expect(page.locator("#result-amount")).to_have_text("−$693m")
    expect(page.locator("#per100-amount")).to_have_text("$104")
    expect(page.locator("#margin-amount")).to_have_text("−4.3%")
    assert page.locator('input[value="h1"]').evaluate("e => e === document.activeElement")
    record("Native keyboard radio navigation and focus retention")
    page.get_by_role("radio", name="Third quarter 2026").check()
    expect(page.locator("#result-amount")).to_have_text("−$567m")
    expect(page.locator("#revenue-amount")).to_have_text("$16.96bn")
    expect(page.locator("#expense-amount")).to_have_text("$17.52bn")
    expect(page.locator("#per100-period")).to_have_text("Q3 2026")
    expect(page.locator("#per100-amount")).to_have_text("$103")
    assert abs(page.locator("#revenue-bar").evaluate("e=>parseFloat(e.style.width)") - 16956 / 18000 * 100) < .001
    record("Q3 selection restores latest values and the same fixed 0–18bn scale")

    page.locator("#exact-figures > summary").click()
    expect(page.locator("#exact-figures")).to_have_attribute("open", "")
    expect(page.locator("#exact-figures")).to_contain_text("16.286")
    expect(page.locator("#exact-figures")).to_contain_text("11.555")
    expect(page.locator("#exact-figures")).to_contain_text("16.956")
    no_overflow(page, "390px exact figures confined to table region")
    page.locator("#exact-figures > summary").click()

    menu = page.locator("#mobile-contents")
    menu.locator("summary").click()
    menu.get_by_role("link", name="Lessons from SpaceX").click()
    expect(menu).not_to_have_attribute("open", "")
    page.wait_for_timeout(100)
    top = page.locator("#spacex-title").bounding_box()["y"]
    header_height = page.locator(".masthead").bounding_box()["height"]
    assert top >= header_height and top <= header_height + 45, top
    record("Mobile contents closes and target clears sticky header")
    page.locator("#spacex-chronology > summary").click()
    page.locator(".event").nth(4).locator("summary").click()
    expect(page.locator(".event").nth(4)).to_contain_text("911.5m")
    page.screenshot(path=str(OUTPUT / "mobile-spacex.png"))
    page.locator(".event").nth(4).locator("summary").click()
    page.locator("#spacex-chronology > summary").click()

    page.goto(URL, wait_until="networkidle")
    page.screenshot(path=str(OUTPUT / "mobile-top.png"))
    go_section(page, "briefing")
    page.screenshot(path=str(OUTPUT / "mobile-briefing.png"))
    for section_id in ["financial-views", "dilution-example", "roadmap", "operating-reconciliation", "commitment-overview"]:
        go_section(page, section_id)
        page.screenshot(path=str(OUTPUT / f"r2-mobile-{section_id}.png"))
    for module_id in ["what-changed", "compute-trend", "commercial-evidence", "ownership-map", "entry-comparison"]:
        go_section(page, module_id)
        page.locator(":focus").evaluate_all("es=>es.forEach(e=>e.blur())")
        page.screenshot(path=str(OUTPUT / f"nov4-mobile-{module_id}.png"))
    for module_id in ["adoption-government", "adoption-enterprise", "adoption-science"]:
        go_section(page, module_id)
        page.screenshot(path=str(OUTPUT / f"nov4-mobile-{module_id}.png"))
    go_section(page, "retail-access")
    page.screenshot(path=str(OUTPUT / "retail-mobile-top.png"))
    page.locator("#retail-broker-details > summary").click()
    page.locator(".retail-brokers").screenshot(path=str(OUTPUT / "retail-mobile-brokers.png"))
    page.locator("#retail-broker-details > summary").click()
    go_section(page, "retail-market-effects")
    page.screenshot(path=str(OUTPUT / "retail-mobile-analysis.png"))
    page.locator('a[data-term="economic-shares"]').click()
    page.screenshot(path=str(OUTPUT / "r2-mobile-definition.png"))
    page.locator("#term-preview-close").click()
    go_section(page, "economics")
    page.screenshot(path=str(OUTPUT / "mobile-economics.png"))
    page.screenshot(path=str(OUTPUT / "mobile-full.png"), full_page=True)

    for width in [320, 768, 1440]:
        page.set_viewport_size({"width": width, "height": 1000})
        page.goto(URL, wait_until="networkidle")
        no_overflow(page, f"{width}px default reflow")
        assert page.locator(".expense-stack").bounding_box()["height"] >= 30
        assert page.locator("#cost-compute").bounding_box()["height"] >= 30
        record(f"{width}px expense segments have visible height")
        page.locator("#exact-figures > summary").click()
        no_overflow(page, f"{width}px expanded table reflow")
        page.locator("#exact-figures > summary").click()
        page.locator("#retail-broker-details > summary").click()
        no_overflow(page, f"{width}px expanded retail names table reflow")
        page.locator("#retail-broker-details > summary").click()
    page.evaluate("scrollTo(0,0)")
    page.wait_for_timeout(100)
    page.screenshot(path=str(OUTPUT / "desktop-top.png"))
    go_section(page, "briefing")
    page.screenshot(path=str(OUTPUT / "desktop-briefing.png"))
    go_section(page, "economics")
    page.screenshot(path=str(OUTPUT / "desktop-economics.png"))
    for section_id in ["financial-views", "dilution-example", "roadmap", "operating-reconciliation", "commitment-overview"]:
        go_section(page, section_id)
        page.screenshot(path=str(OUTPUT / f"r2-desktop-{section_id}.png"))
    for module_id in ["what-changed", "compute-trend", "commercial-evidence", "ownership-map", "entry-comparison"]:
        page.locator(f"#{module_id}").screenshot(path=str(OUTPUT / f"nov4-desktop-{module_id}.png"))
    page.locator("#retail-access").screenshot(path=str(OUTPUT / "retail-desktop-full.png"))
    go_section(page, "drivers")
    page.screenshot(path=str(OUTPUT / "desktop-drivers.png"))
    page.locator('#drivers a[href="#source-a-mda"]').first.click()
    page.screenshot(path=str(OUTPUT / "desktop-source-preview.png"))
    page.locator("#source-preview-close").click()
    go_section(page, "spacex")
    expect(page.locator('[data-section="spacex"]')).to_have_attribute("aria-current", "location")
    record("Active desktop contents tracks the visible section")
    page.screenshot(path=str(OUTPUT / "desktop-spacex.png"))
    page.screenshot(path=str(OUTPUT / "desktop-full.png"), full_page=True)

    page.emulate_media(reduced_motion="reduce")
    assert page.locator("body").evaluate("e => getComputedStyle(e).animationName") == "none"
    record("Reduced-motion mode retains complete content")

    # 200% desktop zoom-equivalent viewport, followed by doubled text sizing.
    page.set_viewport_size({"width": 720, "height": 900})
    page.goto(URL)
    page.add_style_tag(content="html { font-size: 200%; } body { font-size: 36px; }")
    no_overflow(page, "Increased text and narrow viewport reflow")

    nojs_context = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
    nojs = nojs_context.new_page()
    nojs.goto(URL, wait_until="networkidle")
    expect(nojs.locator(".period-control")).not_to_be_visible()
    expect(nojs.locator("#result-amount")).to_have_text("−$567m")
    nojs.locator("#exact-figures > summary").click()
    expect(nojs.locator("#exact-figures")).to_contain_text("11.555")
    expect(nojs.locator("#per100-amount")).to_have_text("$103")
    expect(nojs.locator("#exact-figures")).to_contain_text("16.956")
    expect(nojs.locator("#operating-reconciliation")).to_contain_text("$2,463m")
    expect(nojs.locator("#commitment-overview")).to_contain_text("$900.9bn")
    expect(nojs.locator("#compute-ratio-q2")).to_have_text("48.1%")
    expect(nojs.locator("#compute-ratio-q3")).to_have_text("58.2%")
    expect(nojs.locator('[data-entry-return="offer"]')).to_have_text("+6.6%")
    expect(nojs.locator('[data-entry-return="open"]')).to_have_text("−4.1%")
    expect(nojs.locator('[data-entry-return="earlyClose"]')).to_have_text("−31.9%")
    expect(nojs.locator("#adoption-government")).to_contain_text("No minimum spending commitment")
    expect(nojs.locator("#ownership-map .ownership-lanes > li")).to_have_count(3)
    expect(nojs.locator("#what-changed")).to_be_visible()
    record("All five additions retain complete static evidence and calculations without JavaScript")
    expect(nojs.locator(".retail-table tbody tr")).to_have_count(6)
    expect(nojs.locator(".retail-platforms li")).to_have_count(6)
    nojs.locator("#retail-broker-details > summary").click()
    expect(nojs.locator(".retail-table")).to_be_visible()
    no_overflow(nojs, "390px no-JavaScript expanded retail names reflow")
    nojs.locator("#retail-broker-details > summary").click()
    expect(nojs.locator("#retail-access")).to_contain_text("does not guarantee")
    expect(nojs.locator("#retail-access")).to_contain_text("current platform confirmation")
    nojs.locator('#retail-access a[href="#entry-comparison"]').click()
    assert nojs.evaluate("location.hash") == "#entry-comparison"
    nojs.locator('#entry-comparison a[href="#retail-access"]').click()
    assert nojs.evaluate("location.hash") == "#retail-access"
    record("Retail facts, conditions and both entry-route links remain complete without JavaScript")
    expect(nojs.locator(".dilution-controls")).not_to_be_visible()
    expect(nojs.locator("#dilution-result")).to_have_text("−4.0%")
    expect(nojs.locator("#dilution-formula")).to_contain_text("120 ÷ 125")
    expect(nojs.locator(".mobile-reading")).not_to_be_visible()
    nojs.locator('a[data-term="economic-shares"]').click()
    assert nojs.evaluate("location.hash") == "#glossary"
    nojs.locator("#glossary > summary").click()
    expect(nojs.locator("#definition-economic-shares")).to_be_visible()
    record("No-JavaScript dilution illustration, term anchor and native glossary")
    expect(nojs.locator("#exact-figures")).to_contain_text("8.4%")
    nojs.locator('#briefing a[href="#source-a-mda"]').first.click()
    assert nojs.evaluate("location.hash") == "#source-a-mda"
    expect(nojs.locator("#source-preview")).not_to_be_visible()
    nojs.locator("#spacex-chronology > summary").click()
    expect(nojs.locator(".event")).to_have_count(7)
    record("No-JavaScript citations and newly grouped supporting content")
    no_overflow(nojs, "No-JavaScript baseline reflow")
    record("No-JavaScript figures, native disclosures and hidden non-working switch")
    nojs.screenshot(path=str(OUTPUT / "mobile-nojs.png"))

    fallback_context = browser.new_context(viewport={"width": 390, "height": 844})
    fallback = fallback_context.new_page()
    fallback_html = re.sub(r"@font-face\s*\{[^}]+\}", "", (PROJECT / "index.html").read_text())
    fallback.route(URL, lambda route: route.fulfill(status=200, content_type="text/html", body=fallback_html))
    fallback.goto(URL, wait_until="networkidle")
    no_overflow(fallback, "Embedded fonts unavailable: fallback reflow")
    fallback.screenshot(path=str(OUTPUT / "mobile-font-fallback.png"))

    file_page = browser.new_page(viewport={"width": 390, "height": 844})
    try:
        file_page.goto((PROJECT / "index.html").as_uri(), wait_until="load")
        file_page.get_by_role("radio", name="Second quarter 2026").check()
        expect(file_page.locator("#result-amount")).to_have_text("+$974m")
        record("Direct file:// loading and interaction")
    except Exception as e:
        if "ERR_BLOCKED_BY_ADMINISTRATOR" not in str(e):
            raise
        record("Direct file:// loading", "not verified: browser administrator policy blocks file URLs")

    page.set_viewport_size({"width": 1440, "height": 1000})
    page.goto(URL, wait_until="networkidle")
    page.set_viewport_size({"width": 794, "height": 1123})
    page.emulate_media(media="print")
    print_figure = page.locator("#entry-comparison").bounding_box()
    for label in page.locator(".entry-return").all():
        rect = label.bounding_box()
        assert rect["x"] >= print_figure["x"]
        assert rect["x"] + rect["width"] <= print_figure["x"] + print_figure["width"]
    record("A4 print layout contains all three complete signed SpaceX return labels")
    page.pdf(path=str(PROJECT / "tests" / "print-preview.pdf"), print_background=True, prefer_css_page_size=True)
    record("Print PDF generated for visual/text inspection")
    nojs.set_viewport_size({"width": 794, "height": 1123})
    nojs.pdf(path=str(PROJECT / "tests" / "print-nojs.pdf"), print_background=True, prefer_css_page_size=True)
    record("No-JavaScript print PDF generated")

    assert errors == [], errors
    assert console_errors == [], console_errors
    assert all(r.startswith(URL) or r.startswith("data:") for r in requests), requests
    record("No page/console errors or runtime third-party requests")
    browser.close()

(PROJECT / "tests" / "browser-results.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
