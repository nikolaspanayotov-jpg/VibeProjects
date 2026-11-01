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
            expect(page.locator("#diagram-view")).to_be_hidden()
            expect(page.locator("#station-list-view")).to_be_hidden()
            expect(page.locator("#view-controls")).to_be_hidden()
            expect(page.locator("#service-visual-note")).to_be_visible()
            expect(page.locator("#service-visual-note")).to_contain_text("No service routes are drawn here")
            assert page.locator('[data-route~="services"]').count() == 0
            assert page.locator('.route.is-active,.route-edge.is-active').count() == 0
            for width in (390,1440):
                page.set_viewport_size({"width":width,"height":1000})
                page.locator("#service-visual-note").scroll_into_view_if_needed()
                page.screenshot(path=str(ARTIFACTS / f"service-text-only-{width}.png"))
            page.locator('[data-phase="2026"]').click()
            page.locator('[data-view="list"]').click()
            for phase, count in (("2026",14), ("2027",15), ("2028",42), ("2030",25)):
                page.locator(f'[data-phase="{phase}"]').click()
                assert page.locator("#station-list-view button").count() == count
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator('[data-phase="2028"]').click()
            expect(page.locator('[data-panel="2028"]')).to_contain_text("rail-only contactless at all Greater Manchester stations by end-2028")
            expect(page.locator('[data-panel="2028"]')).to_contain_text("separate from station integration through 2030")
            expect(page.locator('[data-panel="2028"]')).to_contain_text("Eligible journeys and ticket conditions remain to be confirmed")
            discrepancy="TfGM’s heading says 43 stations; its published list names 42. We reproduce the named entries pending clarification."
            expect(page.locator("#station-list-view")).to_contain_text(discrepancy)
            expect(page.locator("#station-count-note")).to_have_text(discrepancy)
            assert page.locator('[data-panel="2028"] a[href="#source-october"]').count() >= 1
            page.locator('[data-phase="services"]').click()
            expect(page.locator("#diagram-view")).to_be_hidden()
            page.locator('[data-phase="2028"]').click()
            expect(page.locator("#station-list-view")).to_be_visible()
            page.screenshot(path=str(ARTIFACTS / "2028-list-source-note.png"))
            checks.append("Service milestone is text-only with zero route overlays; station groups retain their named entries and view selection")
            checks.append("2028 coverage and the 43-versus-42 discrepancy are visible beside the list with secondary-source attribution")

            expect(page.locator("#tickets .section-copy")).to_contain_text("rail-only contactless at all Greater Manchester stations by end-2028")
            expect(page.locator(".change-item").first).to_contain_text("Rail contactless and a separate daily paper ticket are planned from December 2026")
            expect(page.locator(".ticket-steps li").first).to_contain_text("Planned from December 2026")
            expect(page.locator(".source-context")).to_contain_text("TfGM material was reviewed through indexed copies; external destinations were not all live-verified")
            checks.append("Ticket copy labels the shared planned launch period; source context distinguishes indexed review from live checks")

            page.goto(url)
            page.set_viewport_size({"width":390,"height":844})
            assert page.locator(".phase-controls").bounding_box()["height"] <= 160
            phase_box = page.locator(".phase-copy").bounding_box()
            assert phase_box["y"] + phase_box["height"] <= page.locator("#atlas").bounding_box()["y"]
            assert page.locator("#station-search").bounding_box()["y"] < 700
            checks.append("Mobile controls fit two compact rows; the selected milestone explanation precedes the diagram")

            page.goto(url + "?station=glossop#explore")
            expect(page.locator("#station-facilities-link")).to_have_attribute("href","https://www.nationalrail.co.uk/stations/glossop/")
            expect(page.locator("#station-access")).to_contain_text("category A")
            expect(page.locator("#station-services")).to_contain_text("No station-specific timetable enhancement")
            expect(page.locator("#selected-station-halo")).to_be_visible()
            expect(page.locator("#corridor-list")).to_contain_text("Hadfield")
            page.wait_for_function("(() => { const r=document.querySelector('#station-detail-title').getBoundingClientRect(); return r.top >= 70 && r.bottom < innerHeight; })()")
            page.screenshot(path=str(ARTIFACTS / "station-glossop-mobile.png"))
            page.goto(url + "?station=flowery-field#explore")
            expect(page.locator("#station-access")).to_contain_text("category C")
            expect(page.locator("#station-access-work-row")).to_be_visible()
            expect(page.locator("#station-access-work")).to_contain_text("2027–2028")
            expect(page.locator("#map-omission")).to_contain_text("not drawn")
            expect(page.locator("#selected-station-halo")).to_be_hidden()
            page.locator("#show-omitted-station").click()
            expect(page.locator('#station-list-view [data-select-station="flowery-field"]')).to_be_focused()
            expect(page.locator('#station-list-view [data-select-station="flowery-field"]')).to_have_attribute("aria-pressed","true")
            page.goto(url + "?station=manchester-piccadilly#explore")
            expect(page.locator("#selected-station-halo")).to_be_visible()
            page.goto(url + "?station=salford-central#explore")
            expect(page.locator("#station-facilities-link")).to_have_attribute("href","https://tfgm.com/travel-updates/live-departures/train/salford-central-rail")
            expect(page.locator("#station-access")).to_contain_text("not confirmed")
            assert page.locator('[data-information^="https://www.nationalrail.co.uk/stations/"]').count() == 95
            checks.append("Station results have direct facilities links, sourced current access and separate planned work; omissions and map halos are explicit")

            page.goto(url)
            for option, phrase in (("rail","Complete each part"),("paper","different modes"),("caps","Joined-up capping")):
                page.locator(f'[data-payment="{option}"]').click()
                assert page.locator("[data-payment-panel]:visible").count() == 1
                expect(page.locator(f'[data-payment-panel="{option}"]')).to_contain_text(phrase)
                expect(page.locator(f'[data-payment="{option}"]')).to_have_attribute("aria-pressed","true")
            expect(page.locator(".fare-note")).to_contain_text("awaiting confirmed rules")
            image = page.locator(".place-story img")
            image.scroll_into_view_if_needed()
            image.evaluate("el => el.decode()")
            assert image.evaluate("el => el.naturalWidth") == 1280
            expect(page.locator(".place-story figcaption")).to_contain_text("archive photograph")
            expect(page.locator('.place-story a[href="https://creativecommons.org/licenses/by-sa/3.0/"]')).to_be_visible()
            page.screenshot(path=str(ARTIFACTS / "photo-mobile.png"))
            checks.append("All three journey walkthrough options work; the local archive photograph loads with its visible credit and licence")

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
            assert fallback.locator("[data-payment-panel]:visible").count() == 3
            expect(fallback.locator("#station-count-note")).to_be_visible()
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
