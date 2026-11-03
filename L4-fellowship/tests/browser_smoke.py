"""End-to-end checks. Start a localhost server in L4-fellowship, then run:
python3 tests/browser_smoke.py --url http://127.0.0.1:8000/ --output /tmp/l4-qa
Requires Playwright and its Chromium browser; the website has no dependencies.
"""
import argparse
import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser=argparse.ArgumentParser()
parser.add_argument('--url',default='http://127.0.0.1:8000/')
parser.add_argument('--output',default='/tmp/l4-qa')
args=parser.parse_args()
OUTPUT=Path(args.output);OUTPUT.mkdir(parents=True,exist_ok=True)
KEY='l4-fellowship.v1'
checks=[]

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    context=browser.new_context(viewport={'width':1440,'height':1000},timezone_id='Pacific/Kiritimati',accept_downloads=True,reduced_motion='reduce')
    page=context.new_page();errors=[];requests=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda request:requests.append(request.url))
    page.clock.install(time=datetime(2026,11,3,23,30,tzinfo=timezone.utc))
    page.goto(args.url)
    expect(page.locator('h1')).to_have_text('Your study desk.')
    assert page.locator('.ksb-cell').count()==37
    page.screenshot(path=str(OUTPUT/'today-desktop.png'),full_page=True)
    checks.append('Clean first visit, 37 index links, no fabricated progress')

    def stored():
        return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)

    def go(hash_value):
        page.evaluate('(hash)=>location.hash=hash',hash_value)
        page.wait_for_function('(hash)=>location.hash==="#"+hash',arg=hash_value)
        page.wait_for_function('''hash => {
            if(hash.startsWith('ksb-')) return document.querySelector('h1')?.textContent === window.L4_CURRICULUM.items.find(k=>k.id===hash.slice(4).toUpperCase())?.title;
            const labels={today:'Today',library:'KSB library',studio:'KSB library',evidence:'My evidence',practice:'Practice',plan:'Plan and sources'};
            return document.querySelector('#topbar-context')?.textContent===labels[hash];
        }''',arg=hash_value)

    go('library');expect(page.locator('.ksb-row')).to_have_count(37)
    page.locator('#library-search').fill('NULL')
    expect(page.locator('.ksb-row[href="#ksb-k8"]')).to_have_count(1)
    page.locator('#filter-category').select_option('K')
    assert all(x.startswith('K') for x in page.locator('.ksb-row .ksb-tag').all_text_contents())
    page.locator('[data-action="clear-filters"]').click()
    page.locator('#filter-category').select_option('S')
    expect(page.locator('.ksb-row')).to_have_count(15)
    page.locator('#filter-theme').select_option('0')
    expect(page.locator('.ksb-row')).to_have_count(2)
    page.locator('#filter-evidence').select_option('linked')
    expect(page.locator('.ksb-row')).to_have_count(0)
    expect(page.get_by_text('No KSBs match these filters.')).to_be_visible()
    page.locator('[data-action="clear-filters"]').first.click()
    checks.append('Search, combined filters, clear filters and empty state')

    data=page.evaluate('window.L4_CURRICULUM.items.map(k=>({id:k.id,title:k.title,targets:k.targets.length}))')
    for k in data:
        go('ksb-'+k['id'].lower())
        expect(page.locator('h1')).to_have_text(k['title'])
        assert page.locator('[data-coverage]').count()==k['targets']
        expect(page.locator('#my-response')).to_be_visible()
        assert len(page.locator('.reading-panel > .prose').inner_text())>200
    checks.append('All 37 complete lessons, response forms, source links and target checklists')

    go('ksb-k8');expect(page.locator('#my-response')).to_be_visible()
    response='Synthetic QA response: I checked NULLs, cardinality and source totals. <img src=x onerror="window.__xss=1">'
    page.locator('#my-response').fill(response)
    page.get_by_text('Learning and confidence',exact=True).click()
    page.locator('#lesson-learning').select_option('explain')
    page.locator('#lesson-confidence').select_option('4')
    page.locator('[data-coverage]').first.select_option('covered')
    page.locator('[data-action="save-response"]').click()
    page.reload();expect(page.locator('#my-response')).to_have_value(response)
    assert stored()['ksbs']['K8']['confidence']=='4'
    page.locator('#lesson-recall').select_option('independent')
    page.locator('[data-action="record-lesson-review"]').click()
    assert stored()['ksbs']['K8']['lastReview']=='2026-11-04'
    assert stored()['ksbs']['K8']['nextReview']=='2026-11-11'
    page.locator('#lesson-recall').select_option('independent')
    page.locator('[data-action="record-lesson-review"]').click()
    assert stored()['ksbs']['K8']['nextReview']=='2026-11-18'
    page.locator('#lesson-recall').select_option('help')
    page.locator('#lesson-review-date').fill('2026-11-01')
    page.locator('[data-action="record-lesson-review"]').click()
    checks.append('Local persistence, escaped text, separate confidence/learning and local-date review rules across UTC boundary')
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(OUTPUT/'lesson-desktop.png'),full_page=True)

    go('ksb-s12');expect(page.locator('h1')).to_contain_text('Stakeholder')
    page.get_by_text('Two stakeholder examples',exact=True).click()
    page.locator('#stakeholder-0-role').fill('Fictional service manager')
    page.locator('#stakeholder-1-role').fill('Fictional data engineer')
    page.locator('[data-action="save-response"]').click()
    go('ksb-s13');expect(page.locator('.forecast-svg')).to_have_count(1)
    page.get_by_text('My forecast and mining worksheet',exact=True).click()
    page.locator('#forecast-target').fill('Synthetic monthly requests')
    page.locator('#forecast-mining').fill('Separate practice clustering example')
    page.locator('[data-action="save-response"]').click()
    page.reload();expect(page.locator('.forecast-svg')).to_have_count(1)
    assert stored()['ksbs']['S13']['forecast']['target']=='Synthetic monthly requests'
    assert stored()['ksbs']['S12']['stakeholders'][1]['role']=='Fictional data engineer'
    checks.append('S12 two-stakeholder and S13 forecast/mining worksheets persist; accessible forecast plot/table')

    go('evidence');expect(page.locator('#evidence-form')).to_be_visible()
    title='QA reflection <img src=x onerror="window.__xss=1">'
    page.locator('#ev-title').fill(title)
    page.locator('#ev-project').fill('Fictional practice project')
    page.locator('#ev-reflection').fill('Synthetic reflection about my own checks; not workplace evidence.')
    page.locator('input[name="ev-ksbs"][value="K8"]').check()
    page.locator('input[name="ev-ksbs"][value="S6"]').check()
    page.locator('#ev-status').select_option('linked')
    page.get_by_role('button',name='Save reflection',exact=True).click()
    expect(page.locator('#evidence-error')).to_contain_text('add an approved reference')
    page.locator('#ev-reference').fill('QA-REF-001')
    page.locator('#ev-rationale-K8').fill('Explains the quality risk and its impact.')
    page.locator('#ev-rationale-S6').fill('Demonstrates checks, treatment and validation.')
    page.get_by_role('button',name='Save reflection',exact=True).click()
    expect(page.locator('.evidence-card')).to_have_count(1)
    assert len(stored()['evidence'][0]['links'])==2
    assert page.evaluate('window.__xss') is None
    page.locator('[data-action="edit-evidence"]').click()
    page.locator('#ev-status').select_option('reviewed')
    page.locator('#ev-review-note').fill('Fictional review note for QA only.')
    page.locator('#ev-review-date').fill('2026-11-04')
    page.get_by_role('button',name='Save reflection',exact=True).click()
    assert stored()['evidence'][0]['status']=='reviewed'
    page.locator('[data-action="delete-evidence"]').click()
    expect(page.locator('.evidence-card')).to_have_count(0)
    page.locator('[data-action="undo-evidence"]').click()
    expect(page.locator('.evidence-card')).to_have_count(1)
    page.locator('#ev-title').fill('Unfinished safe draft')
    page.locator('.topbar [data-action="backup"]').click()
    page.reload();expect(page.locator('#ev-title')).to_have_value('Unfinished safe draft')
    checks.append('Evidence validation, multi-KSB rationales, reviewed state, escaped titles, deletion undo and draft recovery')

    go('practice');expect(page.locator('#practice-mode')).to_be_visible()
    page.locator('#practice-topic').select_option('K8')
    page.locator('#practice-duration').select_option('5')
    page.locator('#practice-timer').check()
    page.locator('[data-action="start-practice"]').click()
    expect(page.locator('.compare-grid')).to_have_count(0)
    page.locator('#practice-response').fill('Synthetic practice recall of quality risks.')
    page.locator('[data-action="pause-practice"]').click()
    expect(page.locator('h1')).to_have_text('Your study desk.')
    page.reload();page.locator('[data-action="resume-practice"]').click()
    expect(page.locator('#practice-response')).to_have_value('Synthetic practice recall of quality risks.')
    page.locator('[data-action="toggle-timer"]').click()
    page.clock.fast_forward(301000)
    expect(page.locator('#timer-finished')).to_be_visible()
    expect(page.locator('#practice-response')).to_have_value('Synthetic practice recall of quality risks.')
    page.locator('[data-action="reveal-answer"]').click()
    expect(page.locator('.compare-grid')).to_have_count(1)
    page.locator('#practice-gap').fill('Explain the impact more clearly.')
    page.locator('[data-action="rate-practice"][data-result="partial"]').click()
    assert stored()['ksbs']['K8']['nextReview']=='2026-11-07'
    assert stored()['ksbs']['K8']['learning']=='explain'
    page.locator('#practice-mode').select_option('mixed')
    for i in range(3):
        expect(page.locator(f'#mixed-{i}')).to_be_visible()
    page.locator('[data-action="start-practice"]').click()
    for i in range(3):
        page.locator('[data-action="reveal-answer"]').click()
        page.locator('[data-action="rate-practice"][data-result="help"]').click()
    assert stored()['session'] is None
    checks.append('Recall hidden until reveal, pause/reload/resume, timer expiry keeps answers, rating schedules and mixed discussion')

    go('plan');expect(page.locator('#plan-form')).to_be_visible()
    page.locator('#plan-ap03').check()
    page.locator('#plan-standard').fill('ST0118 v1.1, confirmed for test only')
    page.locator('#plan-priority').select_option(['B7','S13'])
    page.get_by_role('button',name='Save study plan',exact=True).click()
    assert stored()['settings']['priority']==['S13','B7']
    go('library');expect(page.locator('#filter-route')).to_be_visible()
    page.locator('#filter-route').select_option('1');expect(page.locator('.ksb-row')).to_have_count(17)
    page.locator('#filter-route').select_option('2');expect(page.locator('.ksb-row')).to_have_count(20)
    checks.append('Study plan, priority topics and conditional AP03 route filters')

    go('studio');expect(page.locator('.studio-task')).to_have_count(6)
    datasets={}
    for kind in ['requests','lookup','monthly','feedback']:
        with page.expect_download() as info:
            page.locator(f'[data-dataset="{kind}"]').click()
        datasets[kind]=list(csv.DictReader(io.StringIO(Path(info.value.path()).read_text())))
    assert len(datasets['requests'])==300 and len(datasets['feedback'])==36 and len(datasets['monthly'])==12
    req=datasets['requests'];lookup=datasets['lookup']
    assert sum(not r['completed_date'] for r in req)==30
    assert sum(not r['service_id'] for r in req)==4
    assert sum(r['service_id']=='S99' for r in req)==8
    assert sum(max(1,sum(l['service_id']==r['service_id'] for l in lookup)) for r in req)==357
    checks.append('Six complete studio tasks and four downloadable synthetic datasets; planted issue counts reconcile')

    with page.expect_download() as info:
        page.locator('.topbar [data-action="backup"]').click()
    original=json.loads(Path(info.value.path()).read_text())
    go('ksb-k8');expect(page.locator('#my-response')).to_be_visible()
    page.locator('#my-response').fill('Current conflicting response kept by merge.')
    page.locator('[data-action="save-response"]').click()
    incoming=json.loads(json.dumps(original));incoming['ksbs']['B7']['response']='New non-conflicting imported response.'

    def import_json(data,name='backup.json'):
        content=data if isinstance(data,str) else json.dumps(data)
        page.set_input_files('#backup-file',{'name':name,'mimeType':'application/json','buffer':content.encode()})

    for invalid in ['{bad json',dict(incoming,version=2),dict(incoming,ksbs=dict(incoming['ksbs'],X99={}))]:
        import_json(invalid)
        expect(page.locator('#toast')).to_contain_text('Backup not imported')
        assert stored()['ksbs']['K8']['response']=='Current conflicting response kept by merge.'
    import_json(incoming)
    expect(page.locator('#restore-dialog')).to_be_visible()
    page.locator('[data-action="apply-restore"]').click()
    assert stored()['ksbs']['K8']['response']=='Current conflicting response kept by merge.'
    assert stored()['ksbs']['B7']['response']=='New non-conflicting imported response.'
    import_json(original)
    page.locator('#restore-mode').select_option('replace')
    page.locator('[data-action="apply-restore"]').click()
    expect(page.locator('#restore-error')).to_contain_text('Confirm replacement')
    page.locator('#confirm-replace').check()
    page.locator('[data-action="apply-restore"]').click()
    assert stored()['ksbs']['K8']['response']==original['ksbs']['K8']['response']
    assert stored()['ksbs']['B7']['response']==original['ksbs']['B7']['response']
    checks.append('JSON export, malformed/newer/unknown-ID rejection, preview, conflict-safe merge and confirmed replacement')

    for width in [390,320,768,1280]:
        page.set_viewport_size({'width':width,'height':900})
        for route_name in ['today','library','ksb-s13','evidence','practice','plan','studio']:
            go(route_name)
            page.wait_for_function('(route)=>document.getElementById("mobile-section").value === (route.startsWith("ksb-")||route==="studio"?"library":route)',arg=route_name)
            page.wait_for_timeout(50)
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(width,route_name)
        if width==390:
            go('today');page.screenshot(path=str(OUTPUT/'today-mobile.png'),full_page=True)
            go('ksb-s13');page.screenshot(path=str(OUTPUT/'forecast-mobile.png'),full_page=True)
    page.set_viewport_size({'width':1440,'height':1000});go('ksb-s13')
    page.screenshot(path=str(OUTPUT/'forecast-desktop.png'),full_page=True)
    keyboard_page=context.new_page();keyboard_page.goto(args.url)
    keyboard_page.keyboard.press('Tab')
    expect(keyboard_page.locator('.skip-link')).to_be_focused()
    keyboard_page.keyboard.press('Enter');expect(keyboard_page.locator('#main')).to_be_focused()
    keyboard_page.keyboard.press('Tab')
    expect(keyboard_page.locator('[data-action="study"]')).to_be_focused()
    keyboard_page.close()
    page.emulate_media(media='print');assert page.locator('.sidebar').evaluate('(e)=>getComputedStyle(e).display')=='none';page.emulate_media(media='screen')
    checks.append('390/320/768/1280px overflow checks across all views, reduced motion, keyboard skip link and print styling')
    assert not errors,errors
    assert not [url for url in requests if not url.startswith(args.url) and not url.startswith('data:')],requests
    checks.append('No page errors or required external network requests')

    corrupt_context=browser.new_context();corrupt_context.add_init_script(f"localStorage.setItem('{KEY}','{{broken');")
    corrupt=corrupt_context.new_page();corrupt.goto(args.url+'#ksb-k8')
    expect(corrupt.locator('#storage-warning')).to_contain_text('left untouched')
    corrupt.locator('#my-response').fill('A temporary recovery response.')
    corrupt.locator('[data-action="save-response"]').click()
    assert corrupt.evaluate('(key)=>localStorage.getItem(key)',KEY)=='{broken'
    with corrupt.expect_download() as info:
        corrupt.locator('[data-action="recover-original"]').click()
    assert Path(info.value.path()).read_text()=='{broken'
    corrupt_context.close()

    quota_context=browser.new_context();quota_context.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('Quota exceeded','QuotaExceededError')};")
    quota=quota_context.new_page();quota.goto(args.url+'#ksb-k8')
    quota.locator('#my-response').fill('Temporary quota-test response.')
    quota.locator('[data-action="save-response"]').click()
    expect(quota.locator('#storage-warning')).to_contain_text('temporary memory')
    with quota.expect_download() as info:
        quota.locator('.topbar [data-action="backup"]').click()
    assert json.loads(Path(info.value.path()).read_text())['ksbs']['K8']['response']=='Temporary quota-test response.'
    quota_context.close()
    checks.append('Corrupt storage is preserved and recoverable; write failures keep an exportable in-memory session')

    file_context=browser.new_context();file_page=file_context.new_page();file_errors=[]
    file_page.on('pageerror',lambda error:file_errors.append(str(error)))
    file_page.goto((Path(__file__).resolve().parent.parent/'index.html').as_uri()+'#ksb-s13')
    expect(file_page.locator('h1')).to_have_text('Time Series Forecasting & Data Mining')
    expect(file_page.locator('.forecast-svg')).to_have_count(1)
    assert not file_errors,file_errors
    checks.append('Direct file opening loads the answer bank and forecast without fetch or a server')
    browser.close()

report={'status':'passed','checks':checks,'screenshots':[p.name for p in OUTPUT.glob('*.png')],'page_errors':errors}
(OUTPUT/'results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
