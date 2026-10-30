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
    no_overflow(page, "390px default reflow")
    record("HTTP 200, preliminary terms, H1 default")

    invalid = page.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')]
        .filter(a => !document.getElementById(a.hash.slice(1))).map(a => a.hash)""")
    assert invalid == [], invalid
    record("All internal citation/navigation targets exist")

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
    assert abs(float(page.locator("#revenue-bar").evaluate("e => parseFloat(e.style.width)")) - 11555 / 18000 * 100) < .001
    expect(page.locator("#period-announcement")).to_contain_text("974 million")
    record("Q2 updates values, sign, period, announcement and fixed-scale geometry")
    q2.focus()
    page.keyboard.press("ArrowLeft")
    expect(page.get_by_role("radio", name="First half 2026")).to_be_checked()
    expect(page.locator("#result-amount")).to_have_text("−$693m")
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
    page.locator(".event").nth(4).locator("summary").click()
    expect(page.locator(".event").nth(4)).to_contain_text("911.5m")
    page.screenshot(path=str(OUTPUT / "mobile-spacex.png"))
    page.locator(".event").nth(4).locator("summary").click()

    page.goto(URL, wait_until="networkidle")
    page.screenshot(path=str(OUTPUT / "mobile-top.png"))
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
    go_section(page, "economics")
    page.screenshot(path=str(OUTPUT / "desktop-economics.png"))
    go_section(page, "drivers")
    page.screenshot(path=str(OUTPUT / "desktop-drivers.png"))
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
