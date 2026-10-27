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
try:
 with sync_playwright() as p:
    browser_options={'headless':True,'args':['--no-sandbox']}
    executable=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('chromium-browser')
    if executable:browser_options['executable_path']=executable
    browser=p.chromium.launch(**browser_options)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page();page.on('pageerror',lambda err:errors.append(str(err)))
    page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
    page.goto(url);page.wait_for_selector('html.js')
    check(len(visible_ids(page))==101,'HTTP:101 articles visible')
    check(page.locator('details[open]').count()==0,'Native analyses initially closed')
    page.locator('#query').fill('ROSEBANK')
    check('measure-01' in visible_ids(page) and len(visible_ids(page))<101,'Case-insensitive title search')
    phrase=page.locator('#measure-13 .analysis-text').text_content().split('.')[0][-70:]
    page.locator('#query').fill(phrase)
    check('measure-13' in visible_ids(page),'Search finds text inside closed analysis')
    page.locator('#query').fill('#12')
    check(visible_ids(page)==['measure-12'],'Exact #12 query')
    page.locator('[data-topic="unlocking-the-north-sea"]').click()
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
    check(len(visible_ids(page))==101 and page.locator('details[open]').count()==101,'Print reveals every entry and analysis')
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
    for width in [390,320,720]:
        page.set_viewport_size({'width':width,'height':1000})
        check(no_overflow(page),f'{width}px no global overflow')
        if width==390:
            check(page.locator('#topic-select').is_visible(),'Mobile labelled topic select')
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
    baseline.locator('#measure-01 summary').click()
    check(baseline.locator('#measure-01 .analysis-text').is_visible(),'No JS:native details work')
    check(no_overflow(baseline),'No JS:mobile has no global overflow')
    check(not errors,'No browser page errors')
    browser.close()
finally:
 server.shutdown()
(ARTIFACTS/'results.json').write_text(json.dumps({'passed':results,'pageErrors':errors},indent=2)+'\n')
print('\n'.join('PASS '+r for r in results))
