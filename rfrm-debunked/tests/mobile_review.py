#!/usr/bin/env python3
"""Real Chromium viewport/touch review; does not substitute for Safari or hardware."""
import json
import functools
import http.server
import threading
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/artifacts/mobile-review'
OUT.mkdir(parents=True, exist_ok=True)
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{server.server_port}/index.html'
report = {'engine': 'Chromium / Playwright', 'cases': [],
          'limitations': ['Viewport and touch emulation; no physical devices or Safari']}
sizes = [('phone320',320,850), ('phone375',375,900), ('phone390',390,900),
         ('phone430',430,932), ('landscape',844,390), ('tablet',768,1024),
         ('desktop',1440,1000)]

with sync_playwright() as pw:
    options = {'headless': True, 'args': ['--no-sandbox']}
    executable = os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('chromium-browser')
    if executable:
        options['executable_path'] = executable
    browser = pw.chromium.launch(**options)
    for name, width, height in sizes:
        result = {'name': name, 'viewport': [width,height], 'checks': [], 'pageErrors': []}
        report['cases'].append(result)
        context = browser.new_context(viewport={'width':width,'height':height},
                                      is_mobile=width<900, has_touch=width<900)
        page = context.new_page()
        page.on('pageerror', lambda error, r=result: r['pageErrors'].append(str(error)))

        def check(label, ok, detail=None):
            result['checks'].append({'label':label,'passed':bool(ok),'detail':detail})
        def activate(selector):
            control = page.locator(selector)
            control.tap() if width<900 else control.click()
        def visible():
            return page.locator('.policy:not([hidden])').evaluate_all('(els)=>els.map(e=>e.id)')
        def shot(label):
            page.screenshot(path=str(OUT / f'{name}-{label}.png'))
        def geometry(label):
            data = page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth})''')
            check(label+' no global overflow', data['scroll']<=data['width'], data)
        try:
            page.goto(URL); page.locator('html.js').wait_for()
            shot('top'); geometry('initial')
            check('All entries available', len(visible())==101)
            activate('#number-index-panel > summary')
            check('Number links have 44px targets', page.locator('.number-grid a').evaluate_all(
                '(els)=>els.every(e=>e.getBoundingClientRect().width>=43.5 && e.getBoundingClientRect().height>=43.5)'))
            activate('#number-index-panel > summary')
            activate('button[data-shortcut="housing"]')
            if width<900: page.locator('#topic-select').select_option('getting-homes-built-in-cities')
            else: activate('.topic-nav a[data-topic="getting-homes-built-in-cities"]')
            page.locator('#query').fill('#12')
            evidence = page.locator('#measure-12 .evidence-label').text_content().strip()
            page.locator('#evidence-select').select_option(evidence)
            check('Four filters combine', visible()==['measure-12'] and page.locator('#active-filters button').count()==4)
            activate('#active-filters button[data-clear-filter="query"]')
            check('Remove query preserves other filters', page.locator('#active-filters button').count()==3 and page.locator('#query').input_value()=='')
            shot('explorer'); geometry('filtered')
            activate('#reset')
            check('Clear all resets evidence and chips', len(visible())==101 and page.locator('#evidence-select').input_value()=='' and page.locator('#active-filters').is_hidden())
            activate('button[data-shortcut="energy"]')
            heading = page.locator('#explorer-heading').bounding_box()
            bar = page.locator('#mobile-tools').bounding_box() if width<900 else None
            check('Heading clears sticky toolbar', heading['y']>=((bar['y']+bar['height']) if bar else 0)-1, {'heading':heading,'toolbar':bar})
            activate('#reset')
            if width<900:
                page.locator('#measure-12').scroll_into_view_if_needed()
                activate('#jump-search')
                q=page.locator('#query').bounding_box(); bar=page.locator('#mobile-tools').bounding_box()
                check('Toolbar Search focuses unobscured input', page.locator('#query').evaluate('(e)=>e===document.activeElement') and q['y']>=bar['y']+bar['height']-1, {'input':q,'toolbar':bar})
                activate('#change-topic')
                check('Toolbar Change topic focuses chooser', page.locator('#topic-select').evaluate('(e)=>e===document.activeElement'))
            page.goto(URL+'#measure-35')
            page.wait_for_function('document.activeElement.id === "measure-35-heading"')
            shot('expanded'); geometry('expanded')
            activate('#measure-35 .route-steps a[href="#measure-34"]')
            page.wait_for_function('document.activeElement.id === "measure-34-heading"')
            check('Guided route opens next analysis', page.locator('#measure-34 details').get_attribute('open') is not None)
            activate('#measure-34 .term-links a[href="#term-ni"]')
            page.wait_for_function('document.activeElement.id === "term-ni"')
            check('Glossary opens from contextual link', page.locator('#term-ni').get_attribute('open') is not None)
            shot('glossary'); geometry('glossary')
            reports = page.locator('a.report-error').evaluate_all('(els)=>els.map(e=>e.href)')
            check('Correction drafts reference the hosted page', len(reports)==102 and all('/issues/new?' in u and 'file%3A' not in u for u in reports))
            for target,label in [('uc-calculation','uc-figure'),('funding-calculation','funding-figure')]:
                page.goto(URL+'#'+target)
                page.wait_for_function('(id)=>document.activeElement.id===id',arg=target)
                shot(label); geometry(label)
            gutters=page.locator('.hero-grid,.headline-section,.layout').evaluate_all(
                '(els)=>els.map(e=>({left:parseFloat(getComputedStyle(e).paddingLeft),right:parseFloat(getComputedStyle(e).paddingRight)}))')
            check('Containers retain 20px gutters', all(g['left']>=19.5 and g['right']>=19.5 for g in gutters),gutters)
        except Exception as error:
            check('Interaction sequence completes',False,str(error)); shot('failure')
        check('No JavaScript errors',not result['pageErrors'],result['pageErrors'])
        context.close()
        print(name+': '+str(sum(not c['passed'] for c in result['checks']))+' failures',flush=True)
    browser.close()

report['failures']=[{'case':c['name'],**v} for c in report['cases'] for v in c['checks'] if not v['passed']]
server.shutdown()
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'cases':len(report['cases']),'failures':report['failures']},indent=2))
raise SystemExit(bool(report['failures']))
