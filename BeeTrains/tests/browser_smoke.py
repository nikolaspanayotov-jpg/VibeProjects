"""Browser acceptance checks. Requires Python Playwright and a Chromium executable.

Run: python3 BeeTrains/tests/browser_smoke.py
Optional: CHROMIUM_PATH=/path/to/chromium
The script serves the repository on an ephemeral loopback port and saves QA
screenshots in tests/artifacts/, which is intentionally ignored by Git.
"""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from html.parser import HTMLParser
from collections import Counter
import json
import os
import shutil

from playwright.sync_api import sync_playwright, expect

PROJECT = Path(__file__).resolve().parents[1]
ARTIFACTS = PROJECT / "tests" / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


class StaticAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.anchors = []
        self.stations = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if "data-station" in attrs:
            self.stations.append(attrs["data-station"])


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    audit = StaticAudit()
    audit.feed((PROJECT / "index.html").read_text())
    assert not [key for key, value in Counter(audit.ids).items() if value > 1]
    assert set(audit.anchors) - {""} <= set(audit.ids)
    assert len(audit.stations) == len(set(audit.stations)) == 96

    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(PROJECT.parent)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/BeeTrains/"
    executable = os.environ.get("CHROMIUM_PATH") or shutil.which("chromium") or shutil.which("google-chrome")
    checks = []
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=executable, headless=True, args=["--no-sandbox"])
            context = browser.new_context(viewport={"width": 1440, "height": 1000})
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            response = page.goto(url)
            assert response.status == 200
            page.evaluate("document.fonts.ready")
            expect(page.locator("#finder")).to_be_visible()
            expect(page.locator('[data-panel="2026"]')).to_be_visible()
            assert page.locator("[data-panel]:visible").count() == 1
            assert page.evaluate("document.fonts.check('600 30px \"Barlow Condensed\"')")
            checks.append("Page loads with embedded fonts and December 2026 selected")

            for width in (320, 390, 768, 1440):
                page.set_viewport_size({"width": width, "height": 1000 if width > 759 else 844})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
                page.screenshot(path=str(ARTIFACTS / f"page-{width}.png"), full_page=True)
                if width in (390, 1440):
                    page.screenshot(path=str(ARTIFACTS / f"opening-{width}.png"))
            checks.append("No horizontal overflow at 320, 390, 768 and 1440px; screenshots saved")

            page.locator("#station-search").fill("glossop")
            expect(page.locator("#search-results")).to_contain_text("1 match")
            page.locator('#search-results [data-select-station="glossop"]').click()
            expect(page.locator("#station-detail-title")).to_have_text("Glossop")
            expect(page.locator("#station-detail-date")).to_have_text("December 2026")
            expect(page.locator("#station-detail-title")).to_be_focused()
            assert "station=glossop" in page.url
            page.locator("#station-search").fill("Rose Hill")
            page.locator('#search-results [data-select-station="rose-hill-marple"]').click()
            expect(page.locator("#station-detail-date")).to_have_text("March 2027")
            expect(page.locator('[data-phase="2027"]')).to_have_attribute("aria-pressed", "true")
            page.locator("#clear-search").click()
            expect(page.locator("#station-search")).to_have_value("")
            expect(page.locator('[data-phase="2027"]')).to_have_attribute("aria-pressed", "true")
            checks.append("Search selects Glossop and Rose Hill Marple, synchronises dates and focus, and clears safely")

            page.locator("#station-search").fill("<img onerror=alert(1)>")
            expect(page.locator("#search-results")).to_contain_text("No stations match")
            assert page.locator("#search-results img").count() == 0
            page.locator("#station-search").fill("HALL I TH WOOD")
            expect(page.locator("#search-results")).to_contain_text("Hall-i'-th'-Wood")
            page.locator("#station-search").fill("Manchester")
            assert page.locator("#search-results button").count() <= 6
            page.locator("#clear-search").click()
            checks.append("Search handles empty matches, punctuation, bounded results and markup as plain text")

            page.locator('[data-phase="services"]').click()
            expect(page.locator("#station-detail")).to_be_hidden()
            expect(page.locator('[data-panel="services"]')).to_contain_text("does not add a separate station group")
            assert "station=" not in page.url
            page.locator('[data-view="list"]').click()
            expect(page.locator("#station-list-view")).to_contain_text("no separate station group")
            for phase, count in (("2026",14), ("2027",15), ("2028",42), ("2030",25)):
                page.locator(f'[data-phase="{phase}"]').click()
                assert page.locator("#station-list-view button").count() == count
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator('[data-phase="2028"]').click()
            expect(page.locator('[data-panel="2028"]')).to_contain_text("separate milestones")
            checks.append("Every phase and complete station list works, including service-only and 2028 payment distinctions")

            page.goto(url + "?station=rose-hill-marple#explore")
            expect(page.locator("#station-detail-title")).to_have_text("Rose Hill Marple")
            page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true,value:{writeText:()=>Promise.reject(new Error('Denied'))}})")
            page.locator("#copy-station-link").click()
            expect(page.locator("#share-fallback")).to_be_visible()
            expect(page.locator("#share-fallback")).to_have_value(url + "?station=rose-hill-marple#explore")
            page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true,value:{writeText:()=>Promise.resolve()}})")
            page.locator("#copy-station-link").click()
            expect(page.locator("#copy-status")).to_have_text("Link copied")
            page.goto(url + "?station=missing-station#explore")
            expect(page.locator("#explore-note")).to_contain_text("not recognised")
            checks.append("Shared URLs restore selection; copying succeeds or offers a fallback; invalid IDs have a useful message")

            page.goto(url)
            page.keyboard.press("Tab")
            expect(page.get_by_role("link", name="Skip to content")).to_be_focused()
            phase = page.locator('[data-phase="2027"]')
            phase.focus()
            page.keyboard.press("Enter")
            expect(phase).to_have_attribute("aria-pressed","true")
            expect(phase).to_be_focused()
            summary = page.locator(".faq-list summary").first
            summary.focus()
            page.keyboard.press("Enter")
            expect(page.locator(".faq-list details").first).to_have_attribute("open", "")
            checks.append("Keyboard activates timeline and questions, preserves phase focus and reaches the skip link")

            page.emulate_media(reduced_motion="reduce")
            assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"
            page.emulate_media(media="print")
            assert page.locator("[data-panel]:visible").count() == 5
            assert page.locator(".phase-stations:visible").count() == 4
            page.pdf(path=str(ARTIFACTS / "print.pdf"))
            page.emulate_media(media="screen")
            page.set_viewport_size({"width": 390,"height": 844})
            page.evaluate("document.documentElement.style.fontSize='200%'; document.body.style.fontSize='36px'")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            checks.append("Reduced motion disables scrolling animation; print exposes all phases; enlarged text reflows")

            offline = browser.new_context(offline=True,viewport={"width":390,"height":844})
            offline_page = offline.new_page()
            # A browser-local document verifies runtime independence from servers and external assets.
            offline_page.set_content((PROJECT / "index.html").read_text())
            expect(offline_page.locator("#finder")).to_be_visible()
            offline_page.locator("#station-search").fill("Glossop")
            expect(offline_page.locator("#search-results")).to_contain_text("Glossop")
            checks.append("Browser-local content and station search work with network offline")

            no_js = browser.new_context(java_script_enabled=False,viewport={"width":390,"height":844})
            fallback = no_js.new_page()
            fallback.goto(url)
            assert fallback.locator("[data-panel]:visible").count() == 5
            assert fallback.locator("[data-station-group] li:visible").count() == 96
            expect(fallback.locator("#finder")).to_be_hidden()
            assert fallback.evaluate("document.documentElement.scrollWidth <= innerWidth")
            fallback.screenshot(path=str(ARTIFACTS / "no-javascript.png"),full_page=True)
            checks.append("Without JavaScript, all milestone text and 96 station entries remain readable")
            assert not errors, errors
            checks.append("No page JavaScript errors")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    report = {"checks":checks,"page_errors":errors,"screenshots":str(ARTIFACTS)}
    (ARTIFACTS / "results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
