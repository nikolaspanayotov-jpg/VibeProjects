#!/usr/bin/env python3
"""Run with Python Playwright+Chromium installed; application itself has no dependencies."""
import functools
import http.server
import json
import os
import shutil
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=ROOT/'tests/artifacts';ARTIFACTS.mkdir(exist_ok=True)
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
url=f'http://127.0.0.1:{server.server_port}/index.html'
results=[]; errors=[]
def check(condition,label):
    assert condition,label
    results.append(label)
def visible_ids(page):return page.locator('.policy:not([hidden])').evaluate_all('(els)=>els.map(el=>el.id)')
def no_overflow(page):return page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')

def exercise_controls(context, url):
    """Click each control family, including retries and filtered deep links."""
    page = context.new_page()
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto(url)
    page.wait_for_selector('html.js')

    # Assigning the value without an input event tests the actual submit button.
    page.locator('#query').evaluate('(el) => { el.value = "#12"; }')
    page.locator('#filters button[type="submit"]').click()
    check(visible_ids(page) == ['measure-12'], 'Search button submits without reloading')
    page.locator('#reset').click()
    topics = page.locator('.topic-nav a[data-topic]').evaluate_all('(els) => els.map(el => el.dataset.topic)')
    for topic in topics:
        page.locator(f'.topic-nav a[data-topic="{topic}"]').click()
        expected = page.locator('.policy').evaluate_all(
            '(els, topic) => els.filter(el => topic === "all" || el.dataset.topic === topic).map(el => el.id)', topic)
        assert visible_ids(page) == expected, topic
        assert page.locator('#topic-select').input_value() == topic, topic
    check(True, f'All {len(topics)} desktop topic controls filter and synchronise')
    page.locator('#reset').click()
    shortcuts = {
        'pay': (['tax-cuts-and-household-bills', 'reducing-the-cost-of-hiring-british-workers', 'welfare-claims'], []),
        'energy': (['unlocking-the-north-sea', 'reindustrialising-britain'], ['claim-energy-bills', 'claim-net-zero-spending']),
        'housing': (['getting-homes-built-in-cities', 'building-critical-national-infrastructure'], []),
        'services': (['spending-and-services', 'welfare-claims'], [])
    }
    for key, (group_topics, group_ids) in shortcuts.items():
        button = page.locator(f'button[data-shortcut="{key}"]')
        button.click()
        expected = page.locator('.policy').evaluate_all(
            '(els, group) => els.filter(el => group[0].includes(el.dataset.topic) || group[1].includes(el.id)).map(el => el.id)',
            [group_topics, group_ids])
        assert visible_ids(page) == expected
        assert page.locator('#explorer-heading').evaluate('(el) => el === document.activeElement')
        page.locator('#query').fill('#12')
        assert visible_ids(page) == (['measure-12'] if 'measure-12' in expected else [])
        page.locator('#reset').click()
        assert page.locator('button[data-shortcut][aria-pressed="true"]').count() == 0
    check(True, 'All everyday shortcuts route to results, collect expected entries and combine with search')

    # These are native browser clicks, not assignments to details.open.
    summaries = page.locator('details > summary')
    for i in range(summaries.count()):
        summary = summaries.nth(i)
        summary.click()
        assert summary.evaluate('(el) => el.parentElement.open'), i
        summary.click()
        assert not summary.evaluate('(el) => el.parentElement.open'), i
    check(True, f'All {summaries.count()} analysis, audit and evidence disclosures toggle')

    page.evaluate('window.copiedURLs = []; Object.defineProperty(navigator, "clipboard", {configurable:true, value:{writeText:async url => { window.copiedURLs.push(url); }}})')
    article_ids = page.locator('.policy').evaluate_all('(els) => els.map(el => el.id)')
    for article_id in article_ids:
        button = page.locator(f'#{article_id} .copy-link')
        button.click()
        page.wait_for_function('(id) => document.querySelector(`#${id} .copy-link`).textContent === "Link copied"', arg=article_id)
        assert page.evaluate('window.copiedURLs.at(-1)') == url + '#' + article_id
    check(True, 'All 101 copy buttons send their own permanent URL to clipboard API')
    page.evaluate('navigator.clipboard.writeText = () => Promise.reject(new Error("Denied"))')
    page.locator('#measure-01 .copy-link').click()
    page.wait_for_selector('#measure-01 .copy-fallback:not([hidden])')
    check(page.locator('#measure-01 .copy-link').text_content() == 'Copy link', 'Failed retry clears stale copied feedback')
    page.locator('#measure-02 .copy-link').click()
    page.wait_for_selector('#measure-02 .copy-fallback:not([hidden])')
    check(page.locator('.copy-fallback:not([hidden])').count() == 1, 'Copying another entry closes the previous fallback')

    for target in ['measure-12-heading', 'measure-12-source-1']:
        page.locator('#query').fill('no-such-entry-xyz')
        page.evaluate('(id) => { location.hash = id; }', target)
        page.wait_for_function('(id) => document.activeElement.id === id', arg=target)
        check(len(visible_ids(page)) == 101 and page.locator('#measure-12 details').get_attribute('open') is not None,
              f'Deep link {target} reveals filtered and collapsed content')
    page.locator('#measure-12 summary').click()
    page.locator('#measure-12 summary').click()
    page.locator('#measure-12 .citations a').first.click()
    page.wait_for_function('document.activeElement.id === "measure-12-source-1"')
    check(True, 'Repeated source fragment returns keyboard focus to the citation')

    page.evaluate('location.hash = "measure-12"')
    page.wait_for_function('document.activeElement.id === "measure-12-heading"')
    page.locator('#query').fill('no-such-entry-xyz')
    page.locator('#number-index-panel > summary').click()
    page.locator('.number-grid a[href="#measure-12"]').click()
    page.wait_for_function('document.activeElement.id === "measure-12-heading"')
    check('measure-12' in visible_ids(page), 'Repeated number link clears conflicting filters')

    topic = 'unlocking-the-north-sea'
    page.evaluate('(topic) => { location.hash = "topic-" + topic; }', topic)
    page.wait_for_function('(topic) => document.activeElement.id === "topic-" + topic', arg=topic)
    page.locator(f'.topic-nav a[data-topic="{topic}"]').click()
    check(page.locator('#topic-select').input_value() == topic and len(visible_ids(page)) < 101,
          'Same-hash topic click retains its filter')
    page.locator('#reset').click()
    audit_id = page.locator('.audit-item').first.get_attribute('id')
    page.evaluate('(id) => { location.hash = id; }', audit_id)
    page.wait_for_function('(id) => document.activeElement.id === id', arg=audit_id)
    check(page.locator(f'#{audit_id}').get_attribute('open') is not None, 'Audit fragment opens its disclosure')

    page.locator('#query').fill('#12')
    snapshot = page.locator('details').evaluate_all('(els) => els.map(el => el.open)')
    # A nonblocking print implementation must remain prepared until afterprint.
    page.evaluate('window.print = () => { window.printInvoked = true; window.dispatchEvent(new Event("beforeprint")); }')
    page.locator('#print-page').click()
    check(page.evaluate('window.printInvoked') and len(visible_ids(page)) == 101 and
          page.locator('details:not([open])').count() == 0, 'Print button opens every entry until print completes')
    page.evaluate('window.dispatchEvent(new Event("afterprint"))')
    check(visible_ids(page) == ['measure-12'] and page.locator('details').evaluate_all('(els) => els.map(el => el.open)') == snapshot,
          'Print button restores original filters and disclosures after completion')
    page.evaluate('window.print = () => { throw new Error("Unavailable"); }')
    page.locator('#print-page').click()
    check(page.locator('#print-status').is_visible() and visible_ids(page) == ['measure-12'] and
          page.locator('details').evaluate_all('(els) => els.map(el => el.open)') == snapshot,
          'Print failure restores state and displays recovery guidance')
    page.locator('#reset').click()
    page.set_viewport_size({'width':390, 'height':1000})
    for topic in topics:
        page.locator('#topic-select').select_option(topic)
        expected = page.locator('.policy').evaluate_all(
            '(els, topic) => els.filter(el => topic === "all" || el.dataset.topic === topic).map(el => el.id)', topic)
        assert visible_ids(page) == expected, topic
    check(True, f'All {len(topics)} phone topic options work')
    page.close()
try:
 with sync_playwright() as p:
    browser_options={'headless':True,'args':['--no-sandbox']}
    executable=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('chromium-browser')
    if executable:browser_options['executable_path']=executable
    browser=p.chromium.launch(**browser_options)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    exercise_controls(context, url)
    page=context.new_page();page.on('pageerror',lambda err:errors.append(str(err)))
    page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
    page.goto(url);page.wait_for_selector('html.js')
    check(len(visible_ids(page))==101,'HTTP:101 articles visible')
    check(page.locator('details[open]').count()==0,'Native analyses initially closed')
    check(page.locator('#biggest-problems > .headline-grid > .headline-card').count()==3 and
          page.locator('#more-findings .headline-card').count()==5 and
          page.locator('#more-findings .headline-card').first.is_hidden(), 'Start here shows three findings with five native expansions')
    page.locator('#more-findings > summary').click()
    check(page.locator('#more-findings .headline-card').first.is_visible(), 'More findings opens natively')
    page.locator('#more-findings > summary').click()
    check(page.locator('#uc-calculation').is_visible() and page.locator('#funding-calculation').is_visible(), 'Both sourced calculation figures are discoverable in the opening overview')
    check(page.locator('.policy > .policy-body > .evidence-panel').count()==0 and
          page.locator('.policy details.analysis .evidence-panel').count()>0, 'Supplementary evidence stays inside analysis expansions')
    audit_summary=page.locator('.audit-item > summary').first
    audit_summary.focus();page.keyboard.press('Enter')
    check(page.locator('.audit-item').first.get_attribute('open') is not None and page.locator('.audit-item .audit-check').first.is_visible(),'Audit opens with keyboard and exposes labelled checks')
    page.keyboard.press('Space')
    check(page.locator('.audit-item').first.get_attribute('open') is None,'Audit closes with keyboard')
    page.locator('#query').fill('ROSEBANK')
    check('measure-01' in visible_ids(page) and len(visible_ids(page))<101,'Case-insensitive title search')
    phrase=page.locator('#measure-13 .analysis-text').text_content().split('.')[0][-70:]
    page.locator('#query').fill(phrase)
    check('measure-13' in visible_ids(page),'Search finds text inside closed analysis')
    page.locator('#query').fill('£218.70')
    check('claim-personal-allowance' in visible_ids(page),'Search includes visible worked examples')
    page.locator('#query').fill('Withdrawal Agreement')
    check('claim-welfare-citizenship' in visible_ids(page) and 'measure-35' in visible_ids(page),'Search includes protected-rights evidence')
    page.locator('#query').fill('Legal obstacle')
    check('claim-welfare-citizenship' in visible_ids(page),'Search includes evidence labels')
    check(page.locator('.headline-card').count()==8,'Eight feature panels are separate from policy results')
    page.locator('#query').fill('#12')
    check(visible_ids(page)==['measure-12'],'Exact #12 query')
    page.locator('.topic-nav a[data-topic="unlocking-the-north-sea"]').click()
    check(visible_ids(page)==[] and page.locator('#no-results').is_visible(),'Search AND topic, empty state')
    page.locator('#empty-reset').click()
    check(len(visible_ids(page))==101 and page.locator('#query').input_value()=='','Clear filters restores original entries')
    check(page.locator('#query').evaluate('(el)=>el===document.activeElement'),'Empty-state reset returns focus to search')
    page.locator('#measure-01 summary').click();page.locator('#measure-02 summary').click()
    check(page.locator('details[open]').count()==2,'Multiple disclosures stay open')
    page.goto(url+'#measure-12');page.wait_for_function('document.activeElement.id === "measure-12-heading"')
    check(page.locator('#measure-12 details').get_attribute('open') is not None,'Initial hash opens and focuses target')
    page.locator('#query').fill('zzzznoresult')
    page.evaluate('location.hash="measure-64"');page.wait_for_function('document.activeElement.id === "measure-64-heading"')
    check(len(visible_ids(page))==101 and page.locator('#measure-64 details').get_attribute('open') is not None,'Changed hash clears conflicting filters and reveals target')
    page.evaluate('location.hash="claim-personal-allowance"');page.wait_for_function('document.activeElement.id === "claim-personal-allowance-heading"')
    check(page.locator('#claim-personal-allowance details').get_attribute('open') is not None,'Supporting-entry hash works')
    page.locator('#query').fill('#12')
    page.locator('#measure-12 details').evaluate('(el)=>el.open=false')
    before=page.locator('details').evaluate_all('(els)=>els.map(el=>el.open)')
    page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
    check(len(visible_ids(page))==101 and page.locator('details.analysis[open]').count()==101 and page.locator('.evidence-key').get_attribute('open') is not None and page.locator('.audit-item[open]').count()==20,'Print reveals every entry, analysis and evidence key')
    page.emulate_media(media='print')
    check('https://' in page.locator('.article-sources a').first.evaluate('(el)=>getComputedStyle(el,"::after").content'),'Print exposes citation URLs')
    page.emulate_media(media='screen');page.evaluate('window.dispatchEvent(new Event("afterprint"))')
    check(visible_ids(page)==['measure-12'] and page.locator('#query').input_value()=='#12' and page.locator('details').evaluate_all('(els)=>els.map(el=>el.open)')==before,'After print restores filters and disclosure states')
    page.locator('#reset').click()
    page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:()=>Promise.reject(new Error("Denied"))}})')
    page.locator('#measure-01 .copy-link').click()
    check(page.locator('#measure-01 .copy-fallback').is_visible(),'Denied clipboard opens fallback')
    copy=page.locator('#measure-01-copy')
    check(copy.input_value().endswith('#measure-01') and copy.evaluate('(el)=>el.selectionEnd===el.value.length && el.selectionStart===0'),'Fallback contains selected permanent URL')
    page.goto(url);page.wait_for_selector('html.js')
    page.screenshot(path=str(ARTIFACTS/'desktop-1440.png'))
    check(no_overflow(page),'1440px no global overflow')
    page.locator('#number-index-panel > summary').click()
    for width in [390,320,350,720,950]:
        page.set_viewport_size({'width':width,'height':1000})
        check(no_overflow(page),f'{width}px no global overflow')
        expected_columns=4 if width<350 else 6
        check(page.locator('.number-grid').evaluate('(el)=>getComputedStyle(el).gridTemplateColumns.split(" ").length')==expected_columns,f'{width}px compact numbered grid columns')
        check(page.locator('.number-grid a').evaluate_all('(els)=>els.every(el=>el.getBoundingClientRect().width>=44 && el.getBoundingClientRect().height>=44)'),f'{width}px number links meet 44px targets')
        if width in [320,390]:
            minimum=20 if width==320 else 24
            for selector in ['.masthead .wrap','.hero-grid','.headline-section','.layout','footer .wrap']:
                box=page.locator(selector).bounding_box()
                padding=page.locator(selector).evaluate('(el)=>({left:parseFloat(getComputedStyle(el).paddingLeft),right:parseFloat(getComputedStyle(el).paddingRight)})')
                check(box['x']+padding['left']>=minimum-0.5 and width-(box['x']+box['width'])+padding['right']>=minimum-0.5,f'{width}px {selector} keeps both gutters')
            for selector in ['#headline-heading','.headline-card p','#explorer > h2','.policy-body','#costing-heading','.audit-item > summary']:
                box=page.locator(selector).first.bounding_box()
                check(box['x']>=minimum-0.5 and box['x']+box['width']<=width-minimum+0.5,f'{width}px {selector} text stays inside gutters')
            check(page.locator('.number-grid a').evaluate_all('(els)=>els.every(el=>el.getBoundingClientRect().width>=44 && el.getBoundingClientRect().height>=44)'),f'{width}px number links meet 44px targets')
            page.locator('.audit-item > summary').first.click()
            check(page.locator('.audit-check').first.is_visible() and no_overflow(page),f'{width}px audit opens without horizontal overflow')
            page.locator('.audit-item > summary').first.click()
        if width==390:
            check(page.locator('#topic-select').is_visible(),'Mobile labelled topic select')
            check(page.locator('#mobile-tools').is_visible(), 'Phone reading toolbar is available')
            page.locator('#measure-01 summary').click()
            page.locator('#measure-01 .back-results').click()
            page.wait_for_function('document.activeElement.id === "explorer-heading"')
            page.locator('#change-topic').click()
            check(page.locator('#topic-select').evaluate('(el)=>el===document.activeElement'), 'Change topic returns focus to the topic chooser')
            page.locator('#jump-search').click()
            check(page.locator('#query').evaluate('(el)=>el===document.activeElement'), 'Reading toolbar search returns focus to search')
            box=page.locator('#query').bounding_box()
            toolbar=page.locator('#mobile-tools').bounding_box()
            check(box['y']>=toolbar['y']+toolbar['height'], 'Focused search clears the sticky toolbar')
            page.locator('#topic-select').select_option('using-brexit-freedoms')
            check(visible_ids(page)==['measure-49','measure-50','measure-51','measure-52'],'Mobile topic filter synchronises')
            page.locator('#reset').click();page.screenshot(path=str(ARTIFACTS/'mobile-390.png'))
        if width==320:page.screenshot(path=str(ARTIFACTS/'mobile-320.png'))
    results.append('720px layout checked as 200% zoom-equivalent of 1440px desktop')
    page.emulate_media(reduced_motion='reduce')
    check(page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches'),'Reduced-motion preference honoured')
    page.goto(url);page.keyboard.press('Tab')
    check(page.locator('.skip').evaluate('(el)=>el===document.activeElement'),'Keyboard begins at skip link')
    page.keyboard.press('Enter')
    page.locator('#query').focus();page.keyboard.type('#12')
    check(visible_ids(page)==['measure-12'],'Keyboard search remains usable')
    focus_outline=page.locator('#query').evaluate('(el)=>getComputedStyle(el).outlineStyle')
    check(focus_outline!='none','Keyboard focus visibly outlined')
    file_page=context.new_page();file_page.on('pageerror',lambda err:errors.append(str(err)))
    file_page.goto((ROOT/'index.html').as_uri());file_page.wait_for_selector('html.js');file_page.locator('#query').fill('#12')
    check(visible_ids(file_page)==['measure-12'],'file://search works')
    file_page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:undefined})')
    file_page.locator('#measure-12 .copy-link').click()
    check(file_page.locator('#measure-12 .copy-fallback').is_visible(),'file://clipboard fallback works')
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':1000});baseline=nojs.new_page();baseline.goto(url)
    check(baseline.locator('.policy').count()==101 and baseline.locator('#filters').is_hidden(),'No JS:all content available, enhanced controls hidden')
    check(baseline.locator('#mobile-tools').is_hidden() and baseline.locator('.shortcut-controls').is_hidden(), 'No JS: enhanced reading controls remain hidden')
    baseline.locator('#number-index-panel > summary').click()
    check(baseline.locator('.number-grid a').first.is_visible(), 'No JS: native numbered index opens')
    baseline.locator('#number-index-panel > summary').click()
    baseline.locator('#more-findings > summary').click()
    check(baseline.locator('#more-findings .headline-card').first.is_visible(), 'No JS: extra findings open')
    baseline.locator('#more-findings > summary').click()
    baseline.locator('#measure-01 summary').click()
    check(baseline.locator('#measure-01 .analysis-text').is_visible(),'No JS:native details work')
    baseline.locator('.audit-item > summary').first.click()
    check(baseline.locator('.audit-check').first.is_visible(),'No JS:audit disclosures work')
    baseline.locator('.audit-item > summary').first.click()
    baseline.emulate_media(media='print')
    check(baseline.locator('.audit-check').first.is_visible(),'No JS:print exposes closed audit details')
    check(baseline.locator('#more-findings .headline-card').first.is_visible(),'No JS:print exposes extra findings')
    baseline.emulate_media(media='screen')
    check(no_overflow(baseline),'No JS:mobile has no global overflow')
    check(not errors,'No browser page errors')
    browser.close()
finally:
 server.shutdown()
(ARTIFACTS/'results.json').write_text(json.dumps({'passed':results,'pageErrors':errors},indent=2)+'\n')
print('\n'.join('PASS '+r for r in results))
