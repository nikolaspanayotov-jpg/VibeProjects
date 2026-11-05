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
import subprocess
import re
from urllib.parse import urlparse, parse_qs

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



def check_personal_tools(browser, page, url, checks, errors):
    page.goto(url)
    page.emulate_media(reduced_motion="reduce")
    expect(page.locator("#station-tools")).to_be_visible()
    assert page.locator("#compare-first option").count() == 97
    page.locator("#compare-first").select_option("glossop")
    page.locator("#compare-second").select_option("stockport")
    profiles = page.locator(".comparison-result")
    assert profiles.count() == 2
    expect(profiles.first).to_contain_text("December 2026")
    expect(profiles.last).to_contain_text("By December 2028")
    expect(page.locator("#comparison-count-note")).to_contain_text("published list names 42")
    expect(page.locator("#comparison-message")).to_contain_text("does not confirm a direct service or through-ticket validity")
    page.locator("#compare-first").select_option("flowery-field")
    page.locator("#compare-second").select_option("salford-central")
    expect(profiles.first).to_contain_text("category C")
    expect(profiles.first).to_contain_text("2027–2028")
    expect(profiles.last).to_contain_text("Current step-free access is not confirmed")
    page.locator("#compare-second").select_option("flowery-field")
    expect(page.locator("#comparison-message")).to_contain_text("different second station")
    assert profiles.count() == 1
    page.locator("#clear-comparison").click()
    expect(page.locator("#compare-first")).to_be_focused()
    assert profiles.count() == 0
    checks.append("Comparison derives all 96 options and dated facts from station records, handles duplicates and clearing, and retains 2028/source qualifications")

    assert page.locator(".journey-story").count() == 3
    for index,pair in enumerate((("rose-hill-marple","manchester-piccadilly"),("rochdale","manchester-victoria"),("flowery-field","manchester-piccadilly"))):
        story = page.locator(".journey-story").nth(index)
        story.locator("summary").focus(); page.keyboard.press("Enter")
        assert story.locator("details").evaluate("el => el.open")
        story.locator("[data-compare-pair]").click()
        expect(page.locator("#compare-first")).to_have_value(pair[0])
        expect(page.locator("#compare-second")).to_have_value(pair[1])
        expect(page.locator("#comparison-title")).to_be_focused()
    expect(page.locator(".journey-story").nth(1)).to_contain_text("does not confirm a later last train")
    expect(page.locator(".journey-story").nth(2)).to_contain_text("does not confirm a step-free journey")
    for width in (320,390,768,1440):
        page.set_viewport_size({"width":width,"height":1000})
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"),width
        if width in (390,1440):
            page.locator("#your-stations").screenshot(style=".masthead,.skip-link,.station-context{visibility:hidden!important}",path=str(ARTIFACTS / f"station-tools-{width}.png"))
            page.locator("#journey-stories").screenshot(style=".masthead,.skip-link,.station-context{visibility:hidden!important}",path=str(ARTIFACTS / f"journey-stories-{width}.png"))
    checks.append("Three qualified journey stories expand by keyboard and open the matching comparison; station tools and stories reflow at four widths")

    page.goto(url+"?station=glossop")
    page.locator("#compare-station").click()
    expect(page.locator("#compare-first")).to_have_value("glossop")
    page.locator("#comparison-results [data-select-station='glossop']").click()
    expect(page.locator("#station-detail-title")).to_be_focused()
    page.locator("#save-station").click()
    expect(page.locator("#save-station")).to_have_attribute("aria-pressed","true")
    page.reload()
    expect(page.locator("#saved-stations-list")).to_contain_text("Glossop")
    expect(page.locator("#saved-stations-list")).to_contain_text("Planned: December 2026")
    page.locator("#saved-stations-list [data-select-station='glossop']").click()
    expect(page.locator("#station-detail-title")).to_have_text("Glossop")
    page.locator(".remove-saved").click()
    expect(page.locator("#saved-empty")).to_be_visible()
    expect(page.locator("#saved-title")).to_be_focused()
    for station in ("glossop","flowery-field","stockport","rose-hill-marple","salford-central","rochdale"):
        page.goto(url+f"?station={station}")
        page.locator("#save-station").click()
    assert page.locator("#saved-stations-list li").count() == 6
    page.goto(url+"?station=stalybridge")
    page.locator("#save-station").click()
    expect(page.locator("#save-status")).to_contain_text("shortlist has six stations")
    assert page.locator("#saved-stations-list li").count() == 6
    state = page.evaluate("JSON.parse(localStorage.getItem('beetrains.reader.v1'))")
    assert set(state) == {"version","stationIds"} and state["version"] == 1
    page.locator("#clear-saved").click()
    page.reload()
    expect(page.locator("#saved-empty")).to_be_visible()
    checks.append("My stations persists only a versioned shortlist of IDs, restores links and dates, limits saves to six, removes individual/all entries and preserves useful focus")

    for kind,script,expected in (
        ("blocked-read","Storage.prototype.getItem = () => { throw new DOMException('Blocked','SecurityError'); }","visit only"),
        ("blocked-write","Storage.prototype.setItem = () => { throw new DOMException('Full','QuotaExceededError'); }","visit only"),
        ("malformed","localStorage.setItem('beetrains.reader.v1','{broken')","visit only"),
        ("unknown-version","localStorage.setItem('beetrains.reader.v1',JSON.stringify({version:999,stationIds:['stockport']}))","visit only"),
    ):
        special = browser.new_context(viewport={"width":390,"height":844})
        special.add_init_script(script)
        probe = special.new_page(); probe.on("pageerror",lambda error: errors.append(str(error)))
        probe.goto(url+"?station=glossop")
        probe.locator("#save-station").click()
        expect(probe.locator("#saved-stations-list")).to_contain_text("Glossop")
        expect(probe.locator("#saved-storage-note")).to_contain_text(expected)
        if kind == "unknown-version":
            assert probe.evaluate("JSON.parse(localStorage.getItem('beetrains.reader.v1')).version") == 999
        special.close()
    special = browser.new_context()
    special.add_init_script("localStorage.setItem('beetrains.reader.v1',JSON.stringify({version:1,stationIds:['glossop','glossop','obsolete','<img onerror=alert(1)>','stockport']}))")
    probe = special.new_page(); probe.goto(url)
    assert probe.locator("#saved-stations-list li").count() == 2
    assert probe.locator("#saved-stations-list img").count() == 0
    special.close()
    checks.append("Blocked reads/writes, malformed data and unsupported storage versions fall back to this visit; invalid and duplicate saved IDs are filtered safely")

    page.goto(url)
    expect(page.locator("#checklist-count")).to_contain_text("0 of 5")
    for need in ("access","assistance","late"):
        choice = page.locator(f'[data-check-need="{need}"]')
        choice.focus(); page.keyboard.press("Space")
        expect(choice).to_be_checked()
    assert page.locator("[data-check-group]:visible").count() == 10
    page.locator("#check-journey").check(); page.locator("#check-available").check()
    expect(page.locator("#checklist-count")).to_contain_text("2 of 10")
    page.locator('[data-check-need="tickets"]').uncheck()
    expect(page.locator("#checklist-count")).to_contain_text("1 of 7")
    expect(page.locator("#check-available")).to_be_hidden()
    page.locator("#reset-checklist").click()
    expect(page.locator("#checklist-count")).to_contain_text("0 of 7")
    expect(page.locator('[data-check-need="access"]')).to_be_checked()
    expect(page.locator("#travel-checklist")).to_contain_text("do not confirm a service, ticket or accessible route")
    for width in (320,390,768,1440):
        page.set_viewport_size({"width":width,"height":1000})
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"),width
        if width in (390,1440): page.locator("#travel-checklist").screenshot(style=".masthead,.skip-link,.station-context{visibility:hidden!important}",path=str(ARTIFACTS / f"travel-checklist-{width}.png"))
    checks.append("The personal checklist filters four topics, counts only selected checks, supports keyboard ticks and resets without implying operational confirmation")

    page.evaluate("scrollTo({top:0,behavior:'instant'})")
    page.wait_for_function("parseFloat(document.querySelector('.masthead').style.getPropertyValue('--reading-progress')) < .01")
    page.locator("#checklist-title").evaluate("el => el.scrollIntoView({block:'start',behavior:'instant'})")
    expect(page.locator('.desktop-nav a[href="#travel-checklist"]')).to_have_attribute("aria-current","location")
    expect(page.locator('.mobile-nav nav a[href="#travel-checklist"]')).to_have_attribute("aria-current","location")
    assert page.locator('.desktop-nav [aria-current="location"]').count() == 1
    assert page.locator('.mobile-nav nav [aria-current="location"]').count() == 1
    page.locator("#reset-checklist").focus()
    page.evaluate("scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    expect(page.locator('.desktop-nav a[href="#sources"]')).to_have_attribute("aria-current","location")
    expect(page.locator("#reset-checklist")).to_be_focused()
    page.wait_for_function("parseFloat(document.querySelector('.masthead').style.getPropertyValue('--reading-progress')) === 1")
    page.set_viewport_size({"width":390,"height":844})
    page.locator(".mobile-nav > summary").click()
    menu = page.locator(".mobile-nav nav").bounding_box()
    assert menu["y"] + menu["height"] <= 844
    page.locator('.mobile-nav a[href="#your-stations"]').click()
    assert not page.locator(".mobile-nav").evaluate("el => el.open")
    expect(page.locator('.mobile-nav a[href="#your-stations"]')).to_have_attribute("aria-current","location")
    page.screenshot(path=str(ARTIFACTS / "reading-navigation-mobile.png"))
    checks.append("Contents and desktop navigation follow scroll with one active link, progress reaches both endpoints, mobile Contents stays in view and scroll does not steal focus")


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

            # Reader choices keep the search prominent and link to real page sections.
            assert page.locator(".quick-start a").count() == 3
            for target in ("explore", "tickets", "piccadilly-transfer"):
                page.locator(f'.quick-start a[href="#{target}"]').click()
                assert page.url.endswith(f"#{target}")
                expect(page.locator(f"#{target}")).to_be_visible()
            page.goto(url)
            for term_id in ("integration", "rail-contactless", "fare-cap", "stopping-service"):
                disclosure = page.locator(f"#meaning-{term_id}")
                summary = disclosure.locator("summary")
                summary.focus(); page.keyboard.press("Enter")
                assert disclosure.evaluate("el => el.open")
                expect(disclosure.locator("p")).to_be_visible()
                expect(summary).to_be_focused()
                assert summary.bounding_box()["height"] >= 44
                page.keyboard.press("Space")
                assert not disclosure.evaluate("el => el.open")
            role_summary = page.locator("#rail-responsibilities > summary")
            expect(page.locator(".role-list")).to_be_hidden()
            role_summary.focus(); page.keyboard.press("Enter")
            expect(page.locator(".role-list")).to_be_visible()
            checks.append("Quick start reaches three reader tasks; four contextual definitions and background responsibilities expand by keyboard")

            for phase in ("2026", "2027", "services", "2028", "2030"):
                page.locator(f'[data-phase="{phase}"]').click()
                disclosure = page.locator(f'[data-panel="{phase}"] > .evidence')
                before = page.url
                disclosure.locator("summary").focus(); page.keyboard.press("Enter")
                expect(disclosure.locator(".evidence-body")).to_be_visible()
                expect(disclosure).to_contain_text("reviewed 31 October 2026")
                expect(disclosure).to_contain_text("Still uncertain")
                assert disclosure.locator('a[href^="https://"]').count() >= 1
                assert page.url == before
            expect(page.locator("#station-count-note")).to_have_count(1)
            page.locator("#payment-evidence > summary").click()
            expect(page.locator("#payment-evidence")).to_contain_text("secondary reporting")
            expect(page.locator("#payment-evidence")).to_contain_text("26 October 2026")
            expect(page.locator("#payment-evidence")).to_contain_text("cross-boundary ticket validity remain unconfirmed")
            page.locator("#boundary-evidence > summary").click()
            expect(page.locator("#boundary-journeys")).to_contain_text("Derbyshire")
            expect(page.locator(".boundary-warning")).to_contain_text("remain unconfirmed")
            expect(page.locator("#boundary-evidence")).to_contain_text("fresh retrieval on 2 November returned HTTP 403")
            for width in (320,390,768,1440):
                page.set_viewport_size({"width":width,"height":1000})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"),width
                if width in (390,1440):
                    page.locator("#boundary-journeys").scroll_into_view_if_needed()
                    page.screenshot(path=str(ARTIFACTS / f"boundary-evidence-{width}.png"))
                    page.locator("#payment-evidence").scroll_into_view_if_needed()
                    page.screenshot(path=str(ARTIFACTS / f"payment-evidence-{width}.png"))
            checks.append("Local evidence panels retain publisher, dates, claims, uncertainty and original URLs; the cross-boundary explanation reflows at four widths")

            # Only inspect issue drafts: the browser never submits or opens GitHub.
            for link in page.locator("[data-correction-section]").all():
                issue_url = urlparse(link.get_attribute("href"))
                assert issue_url.netloc == "github.com"
                assert issue_url.path == "/nikolaspanayotov-jpg/VibeProjects/issues/new"
                fields = parse_qs(issue_url.query)
                assert link.get_attribute("data-correction-section") in fields["title"][0]
                assert "Supporting source URL and publication date:" in fields["body"][0]
            for station_id, name in (("glossop","Glossop"),("rose-hill-marple","Rose Hill Marple")):
                page.goto(url+f"?station={station_id}")
                expect(page.locator("#station-detail-title")).to_have_text(name)
                fields = parse_qs(urlparse(page.locator("#station-correction-link").get_attribute("href")).query)
                assert name in fields["title"][0]
                assert f"Record ID: {station_id}" in fields["body"][0]
                assert "Research snapshot: 31 October 2026" in fields["body"][0]
                assert "127.0.0.1" not in fields["body"][0]
                expect(page.locator("#station-date-evidence-context")).to_contain_text(name)
            checks.append("Correction links create reviewable GitHub drafts with section or current station context, without submitting issues")
            page.goto(url)

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

            page.set_viewport_size({"width":390,"height":844})
            page.goto(url)
            assert not page.locator("#roadmap-details").evaluate("el => el.open")
            roadmap_summary = page.locator("#roadmap-details > summary")
            roadmap_summary.focus(); page.keyboard.press("Enter")
            expect(page.locator(".roadmap-table")).to_be_visible()
            assert page.locator(".roadmap-table tbody tr").count() == 5
            expect(page.locator('[data-milestone="2028"]')).to_contain_text("published list names 42")
            expect(page.locator('[data-milestone="2028"]')).to_contain_text("Eligible journeys and conditions remain unconfirmed")
            for width in (320,390,768,1440):
                page.set_viewport_size({"width":width,"height":1000})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"),width
            page.locator(".roadmap-table").screenshot(path=str(ARTIFACTS / "roadmap-desktop.png"))
            page.locator('[data-jump-phase="services"]').click()
            expect(page.locator('[data-panel="services"]')).to_be_visible()
            expect(page.locator("#diagram-view")).to_be_hidden()
            checks.append("Roadmap compares five qualified milestones, reflows at four widths and links to the correct explorer state")

            expect(page.locator('#piccadilly-transfer a[href$="Manchester-Piccadilly-Station-Map.pdf"]')).to_have_count(1)
            expect(page.locator('#piccadilly-transfer a[href="https://www.nationalrail.co.uk/help-and-assistance/passenger-assist/"]')).to_have_count(1)
            expect(page.locator("#piccadilly-transfer .source-note")).to_contain_text("not live lift availability")
            assert page.locator("#updates .update-list li").count() == 5
            expect(page.locator(".updates-intro")).to_contain_text("does not confirm")
            assert page.locator('#updates time[datetime="2026-11-01"]').count() == 2
            page.set_viewport_size({"width":390,"height":844})
            page.locator("#piccadilly-transfer").screenshot(path=str(ARTIFACTS / "transfer-mobile.png"))
            checks.append("Piccadilly transfer and dated update notes retain official sources and distinguish facilities from live conditions")

            page.emulate_media(reduced_motion="reduce")
            page.goto(url + "?station=glossop#explore")
            expect(page.locator("#station-context")).to_be_hidden()
            page.locator("#sources").scroll_into_view_if_needed()
            expect(page.locator("#station-context")).to_be_visible()
            expect(page.locator("#context-name")).to_have_text("Glossop")
            expect(page.locator("#context-date")).to_contain_text("Planned to join: December 2026")
            summary = page.locator("#station-context-details > summary")
            summary.focus(); page.keyboard.press("Enter")
            expect(page.locator("#context-return")).to_be_visible()
            expect(summary).to_be_focused()
            page.screenshot(path=str(ARTIFACTS / "station-context-mobile.png"))
            page.locator("#context-return").click()
            expect(page.locator("#station-detail-title")).to_be_focused()
            expect(page.locator("#station-context")).to_be_hidden()
            assert page.locator("#station-detail-title").bounding_box()["y"] >= page.locator(".masthead").bounding_box()["height"]
            page.locator("#station-search").fill("Rose Hill")
            page.locator('#search-results [data-select-station="rose-hill-marple"]').click()
            page.locator("#sources").scroll_into_view_if_needed()
            expect(page.locator("#context-name")).to_have_text("Rose Hill Marple")
            expect(page.locator("#context-date")).to_contain_text("March 2027")
            page.locator('[data-phase="2030"]').click()
            expect(page.locator("#station-context")).to_be_hidden()
            expect(page.locator("#station-brief")).to_be_empty()
            checks.append("Selected-station bar appears only after the result, supports keyboard expansion, restores focus and clears stale selection")

            for station_id in ("glossop","flowery-field","stockport","salford-central"):
                page.goto(url + f"?station={station_id}#explore")
                expect(page.locator("#station-detail")).to_be_visible()
                page.evaluate("window.print = () => { window.printWasRequested = true; }")
                page.locator("#print-station-brief").click()
                assert page.evaluate("window.printWasRequested")
                expect(page.locator("#station-brief")).to_be_hidden()
                page.emulate_media(media="print")
                expect(page.locator("#station-brief")).to_be_visible()
                expect(page.locator("#main")).to_be_hidden()
                expect(page.locator("#station-brief")).to_contain_text("Research snapshot: 31 October 2026")
                expect(page.locator("#station-brief")).to_contain_text("Eligible journeys, fares and ticket conditions remain to be confirmed")
                if station_id == "stockport":
                    expect(page.locator("#station-brief")).to_contain_text("heading says 43")
                pdf_path = ARTIFACTS / f"brief-{station_id}.pdf"
                page.pdf(path=str(pdf_path),prefer_css_page_size=True)
                if shutil.which("pdfinfo"):
                    info = subprocess.check_output([shutil.which("pdfinfo"),str(pdf_path)],text=True)
                    assert re.search(r"Pages:\s+1\s",info), (station_id,info)
                page.emulate_media(media="screen")
                page.evaluate("window.dispatchEvent(new Event('afterprint'))")
                expect(page.locator("#main")).to_be_visible()
                assert not page.evaluate("document.documentElement.dataset.printMode")
            page.goto(url + "?station=glossop#explore")
            with page.expect_download() as captured:
                page.locator("#download-station-brief").click()
            download = captured.value
            assert download.suggested_filename == "beetrains-glossop-brief.html"
            saved = ARTIFACTS / download.suggested_filename
            download.save_as(saved)
            exported = saved.read_text()
            assert "<script" not in exported.lower()
            offline_brief = browser.new_context(offline=True,java_script_enabled=False).new_page()
            offline_brief.set_content(exported)
            expect(offline_brief.get_by_role("heading",name="Glossop",exact=True)).to_be_visible()
            expect(offline_brief.locator(".station-brief")).to_contain_text("December 2026")
            expect(offline_brief.locator(".station-brief")).to_contain_text("Research snapshot: 31 October 2026")
            checks.append("Station briefs print as one-page A4 PDFs for four representative records; standalone downloads retain dated facts, sources and uncertainty offline")

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
            page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
            assert page.locator("[data-panel]:visible").count() == 5
            assert page.locator(".phase-stations:visible").count() == 4
            expect(page.locator(".roadmap-table")).to_be_visible()
            expect(page.locator("#payment-evidence .evidence-body")).to_be_visible()
            expect(page.locator("#meaning-fare-cap p")).to_be_visible()
            page.pdf(path=str(ARTIFACTS / "print.pdf"))
            page.emulate_media(media="screen")
            page.evaluate("window.dispatchEvent(new Event('afterprint'))")
            page.set_viewport_size({"width": 390,"height": 844})
            page.evaluate("document.documentElement.style.fontSize='200%'; document.body.style.fontSize='36px'")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            checks.append("Reduced motion disables scrolling animation; print exposes all phases; enlarged text reflows")

            check_personal_tools(browser,page,url,checks,errors)

            offline = browser.new_context(offline=True,viewport={"width":390,"height":844})
            offline_page = offline.new_page()
            # A browser-local document verifies runtime independence from servers and external assets.
            offline_page.set_content((PROJECT / "index.html").read_text())
            expect(offline_page.locator("#finder")).to_be_visible()
            offline_page.locator("#station-search").fill("Glossop")
            expect(offline_page.locator("#search-results")).to_contain_text("Glossop")
            offline_page.locator("#compare-first").select_option("glossop")
            offline_page.locator("#compare-second").select_option("stockport")
            assert offline_page.locator(".comparison-result").count() == 2
            checks.append("Browser-local content, station search and comparison work with network offline")

            no_js = browser.new_context(java_script_enabled=False,viewport={"width":390,"height":844})
            fallback = no_js.new_page()
            fallback.goto(url)
            assert fallback.locator("[data-panel]:visible").count() == 5
            assert fallback.locator("[data-station-group] li:visible").count() == 96
            assert fallback.locator("[data-payment-panel]:visible").count() == 3
            expect(fallback.locator("#station-count-note")).to_be_visible()
            expect(fallback.locator(".roadmap-table")).to_be_visible()
            expect(fallback.locator("#piccadilly-transfer")).to_be_visible()
            expect(fallback.locator("#updates")).to_be_visible()
            expect(fallback.locator("#boundary-journeys")).to_be_visible()
            fallback.locator("#payment-evidence > summary").click()
            expect(fallback.locator("#payment-evidence .evidence-body")).to_be_visible()
            fallback.locator("#meaning-rail-contactless > summary").focus(); fallback.keyboard.press("Enter")
            expect(fallback.locator("#meaning-rail-contactless p")).to_be_visible()
            assert "title=" in fallback.locator('[data-correction-section="Tickets and payments"]').get_attribute("href")
            expect(fallback.locator("#station-tools")).to_be_hidden()
            assert fallback.locator(".journey-story").count() == 3
            fallback.locator(".journey-story summary").first.focus(); fallback.keyboard.press("Enter")
            expect(fallback.locator(".journey-story details").first).to_be_visible()
            assert fallback.locator("[data-check-group]:visible").count() == 10
            fallback.locator("#check-journey").focus(); fallback.keyboard.press("Space")
            expect(fallback.locator("#check-journey")).to_be_checked()
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
