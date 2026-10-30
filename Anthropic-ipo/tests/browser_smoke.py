"""Browser checks for the standalone IPO guide. Requires installed Playwright/Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import json
import re

PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / "tests" / "screenshots"
OUTPUT.mkdir(parents=True, exist_ok=True)
URL = "http://127.0.0.1:8765/"
results = []


def record(name, detail="passed"):
    results.append({"check": name, "result": detail})


def no_overflow(page, name):
    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), name
    record(name)


def go_section(page, section_id):
    page.evaluate("""id => {
        const top = document.getElementById(id).getBoundingClientRect().top + scrollY;
        scrollTo(0, top - (innerWidth >= 1100 ? 24 : 92));
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
    expect(page.locator("#result-amount")).to_have_text("−$693m")
    expect(page.get_by_text("Not specified in this filing", exact=True)).to_have_count(2)
    expect(page.locator("#briefing h3")).to_have_count(3)
    expect(page.locator("#briefing")).to_contain_text("Terms incomplete")
    expect(page.locator("#per100-amount")).to_have_text("$104")
    expect(page.locator("#margin-amount")).to_have_text("−4.3%")
    record("60-second briefing and default per-$100 explanation")
    no_overflow(page, "390px default reflow")
    record("HTTP 200, preliminary terms, H1 default")

    invalid = page.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')]
        .filter(a => !document.getElementById(a.hash.slice(1))).map(a => a.hash)""")
    assert invalid == [], invalid
    record("All internal citation/navigation targets exist")
    ids = page.locator("[id]").evaluate_all("es => es.map(e => e.id)")
    assert len(ids) == len(set(ids)), "Duplicate IDs"
    record("Unique document and source identifiers")

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

    dialog = page.get_by_role("dialog", name="Financial results, compute and financing")
    trigger = page.locator('#economics .sources-inline a[href="#source-a-mda"]').first
    trigger.scroll_into_view_if_needed()
    before_scroll = page.evaluate("scrollY")
    trigger.focus()
    page.keyboard.press("Enter")
    expect(dialog).to_be_visible()
    expect(page.locator("#source-preview-kind")).to_have_text("Filing")
    expect(page.locator("#source-preview-date")).to_have_text("26 October 2026")
    expect(page.locator("#source-preview-excerpt")).to_contain_text("Revenue for the six months")
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
    expect(page.locator("#source-preview-excerpt")).to_contain_text("11,900 customers")
    page.locator("#source-preview-close").click()
    page.locator('#commitments a[href="#source-a-mda"]').first.click()
    expect(page.locator("#source-preview-excerpt")).to_contain_text("up to $120.5 billion")
    page.locator("#source-preview-close").click()
    record("Source excerpts follow customer, financial and compute citation context")

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
    record("All 20 source previews have provenance, dates, notes and original links")

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
    record("Integer financial reconciliation for both periods")

    q2 = page.get_by_role("radio", name="Second quarter 2026")
    q2.check()
    expect(page.locator("#result-amount")).to_have_text("+$974m")
    expect(page.locator("#ledger-title")).to_have_text("Second quarter 2026")
    expect(page.locator("#revenue-amount")).to_have_text("$11.56bn")
    expect(page.locator("#expense-amount")).to_have_text("$10.58bn")
    expect(page.locator("#per100-amount")).to_have_text("$92")
    expect(page.locator("#per100-period")).to_have_text("Q2 2026")
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

    page.locator("#exact-figures > summary").click()
    expect(page.locator("#exact-figures")).to_have_attribute("open", "")
    expect(page.locator("#exact-figures")).to_contain_text("16.286")
    expect(page.locator("#exact-figures")).to_contain_text("11.555")
    no_overflow(page, "390px exact figures confined to table region")
    page.locator("#exact-figures > summary").click()

    menu = page.locator("#mobile-contents")
    menu.locator("summary").click()
    menu.get_by_role("link", name="Lessons from SpaceX").click()
    expect(menu).not_to_have_attribute("open", "")
    page.wait_for_timeout(100)
    top = page.locator("#spacex-title").bounding_box()["y"]
    assert top >= 68 and top <= 140, top
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
    page.evaluate("scrollTo(0,0)")
    page.wait_for_timeout(100)
    page.screenshot(path=str(OUTPUT / "desktop-top.png"))
    go_section(page, "briefing")
    page.screenshot(path=str(OUTPUT / "desktop-briefing.png"))
    go_section(page, "economics")
    page.screenshot(path=str(OUTPUT / "desktop-economics.png"))
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
    expect(nojs.locator("#result-amount")).to_have_text("−$693m")
    nojs.locator("#exact-figures > summary").click()
    expect(nojs.locator("#exact-figures")).to_contain_text("11.555")
    expect(nojs.locator("#per100-amount")).to_have_text("$104")
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
    page.pdf(path=str(PROJECT / "tests" / "print-preview.pdf"), print_background=True, prefer_css_page_size=True)
    record("Print PDF generated for visual/text inspection")
    nojs.pdf(path=str(PROJECT / "tests" / "print-nojs.pdf"), print_background=True, prefer_css_page_size=True)
    record("No-JavaScript print PDF generated")

    assert errors == [], errors
    assert console_errors == [], console_errors
    assert all(r.startswith("http://127.0.0.1:8765") or r.startswith("data:") for r in requests), requests
    record("No page/console errors or runtime third-party requests")
    browser.close()

(PROJECT / "tests" / "browser-results.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
