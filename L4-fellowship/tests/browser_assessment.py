"""Shared criteria, source/evaluation practice, pack evidence and v1 retention."""
import argparse,copy,json,hashlib,re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
pa=argparse.ArgumentParser();pa.add_argument('--url',default='http://127.0.0.1:8000/');pa.add_argument('--output',default='/tmp/l4-assessment-qa');args=pa.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];KEY='l4-fellowship.v1';checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);c=b.new_context(service_workers='block',accept_downloads=True,viewport={'width':1440,'height':1000});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 def go(route):page.goto(args.url+'#'+route);expect(page.locator('h1')).to_be_visible()
 def saved():page.wait_for_timeout(400);return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
 def restore(value,conflict=None):
  page.locator('#backup-file').set_input_files({'name':'synthetic-assessment.json','mimeType':'application/json','buffer':json.dumps(value).encode()});expect(page.locator('#restore-dialog')).to_be_visible()
  if conflict:page.locator('[data-restore-conflict="'+conflict+'"]').select_option('import')
  page.locator('[data-action=apply-restore]').click();expect(page.locator('#restore-dialog')).not_to_be_visible()
 go('assessment');page.locator('[data-action=text-size]').click();page.locator('[data-action=text-size]').click();baseline=saved();data=page.evaluate('L4_CURRICULUM.assessment');expect(page.locator('.as-group')).to_have_count(30);assert len(data['questions'])==254
 page.locator('#as-method').select_option('AM1');expect(page.locator('.as-group')).to_have_count(13);page.locator('#as-distinction').select_option('yes');expect(page.locator('.as-group')).to_have_count(5)
 page.locator('#as-method').select_option('AM2');expect(page.locator('.as-group')).to_have_count(3);page.locator('[data-assess=clear]').first.click();page.locator('#as-group').select_option('K13+S10');page.locator('.as-group>summary').click();expect(page.locator('.as-na')).to_contain_text('No separate distinction');expect(page.locator('.as-criteria-body')).to_contain_text('Exceeds expectations');assert page.locator('.as-distinction').count()==0
 page.locator('[data-as-group-check]').first.check();page.locator('[data-as-group-note]').fill('Synthetic gap: explain the business cost of false positives.');page.reload();page.locator('#as-group').select_option('K13+S10');page.locator('.as-group>summary').click();expect(page.locator('[data-as-group-note]')).to_have_value('Synthetic gap: explain the business cost of false positives.');expect(page.locator('[data-as-group-check]').first).to_be_checked()
 go('library');expect(page.locator('.ksb-row')).to_have_count(2);go('readiness');expect(page.locator('.readiness-row')).to_have_count(2);page.locator('.as-inline-filters>details>summary').click();page.locator('[data-assess=clear]').first.click();expect(page.locator('.readiness-row')).to_have_count(10);assert saved()['ksbs']==baseline['ksbs'] and saved()['game']==baseline['game']
 checks.append('Thirty groups,37KSBs and eight distinction rows are distinct; N/A and provider extensions stay separate; source filters propagate through library/readiness; self-reviews preserve legacy KSB/game state')
 # Exact supplied grading text and source cell provenance all30groups.
 for g in data['groups']:
  go('assessment');page.locator('#as-group').select_option(g['groupId']);page.locator('.as-group>summary').click();expect(page.locator('.as-pass')).to_have_text(g['gradingPass']);assert page.locator('.as-distinction').count()==(1 if g['gradingDistinction'] else 0)
  if g['gradingDistinction']:expect(page.locator('.as-distinction')).to_have_text(g['gradingDistinction'])
  expect(page.locator('.as-criteria-body')).to_contain_text(g['overviewCell'])
 checks.append('All30groups render exact pass/distinction wording and their overview/source cells')
 go('assessment-practice');page.locator('[data-assess=clear]').first.click();page.locator('#as-mode').select_option('source');q0=page.locator('#as-question').input_value();q0group=next(q['groupId'] for q in data['questions'] if q['id']==q0);spoken_ksb=next(g['members'][0] for g in data['groups'] if g['groupId']==q0group);page.locator('#as-response').fill('<script>window.assessmentInjected=1</script> My synthetic answer.');page.locator('[data-assess=reveal]').click();expect(page.locator('.as-feedback')).to_be_visible();page.locator('[data-as-answer-check]').first.check();page.locator('#as-gap').fill('Give the evidence reference.');page.locator('[data-assess=spoken]').click();expect(page.locator('#prep-speak-ksb')).to_have_value(spoken_ksb);expect(page.locator('audio')).to_have_count(0);go('assessment-practice');page.reload();expect(page.locator('#as-response')).to_have_value('<script>window.assessmentInjected=1</script> My synthetic answer.');assert page.evaluate('window.assessmentInjected') is None
 page.locator('#as-mode').select_option('evaluation')
 for e in data['evaluations']:
  page.locator('#as-question').select_option(e['id']);page.locator('#as-response').fill('Synthetic choice with alternative, stakeholder effects and validation.');page.locator('[data-assess=reveal]').click();expect(page.locator('.as-feedback')).to_contain_text(e['rubric'][0]);
  if e['id']=='visuals':
   expect(page.locator('.as-chart-pair svg')).to_have_count(2);assert page.locator('.as-table tbody tr').all_text_contents()==['W11286','W215117','W313169','W4181410']
  if e['id']=='structures':expect(page.locator('.as-artefact')).to_contain_text('101 | Housing')
 page.locator('#as-mode').select_option('quiz')
 for q in data['quiz']:
  page.locator('#as-question').select_option(q['id']);page.locator('input[name=as-quiz-choice][value="'+str(q['answer']).lower()+'"]').check();page.locator('#as-response').fill('Synthetic rationale for this authored misconception.');page.locator('[data-assess=reveal]').click();expect(page.locator('.as-feedback')).to_contain_text('Your answer matches.');expect(page.locator('#celebration')).to_be_visible()
 page.reload();expect(page.locator('#celebration')).not_to_be_visible();expect(page.locator('[data-assess=reveal]')).to_be_disabled();assert saved()['ksbs']==baseline['ksbs'];checks.append('Source snapshots/drafts survive reload with inert markup; all six evaluation rubrics and six authored quiz keys work; only new objective answers celebrate')
 go('assessment-practice');page.locator('#as-method').select_option('AM2');page.locator('[data-assess=mock-start]').click();expect(page.locator('.as-feedback')).to_have_count(0);expect(page.locator('.as-mock-review')).to_have_count(0)
 for n in range(3):
  page.locator('#as-mock-response').fill('Synthetic source mock answer '+str(n));page.reload();expect(page.locator('#as-mock-response')).to_have_value('Synthetic source mock answer '+str(n));page.locator('[data-assess=mock-next]').click()
 expect(page.locator('.as-mock-review')).to_be_visible();page.locator('[data-as-mock-check]').first.check();page.locator('[data-as-mock-next]').first.fill('Use a more specific safe reference.');m=next(iter(saved()['assessmentReview']['mocks'].values()));assert m['method']=='AM2' and all(next(q for q in data['questions'] if q['id']==x['id'])['method']=='AM2' for x in m['questions'])
 with page.expect_download() as dl:page.locator('[data-assess=mock-export]').click()
 dl.value.save_as(str(out/'source-mock.md'));assert 'Use a more specific safe reference.' in (out/'source-mock.md').read_text()
 checks.append('Source mock keeps AM1/AM2 distinct, resumes each answer, gates rubrics until completion and exports actual self-review without replacing existing sessions')
 go('evidence-packs');page.locator('[data-assess=clear]').first.click();expect(page.locator('.as-pack')).to_have_count(4);assert 'K6' in page.locator('.as-pack').nth(1).inner_text();page.locator('[data-assess=pack-draft]').first.click();expect(page.locator('#ev-title')).to_have_value(re.compile('Project Evidence #1'));draft=saved()['evidenceDraft'];assert {x['id'] for x in draft['links']}=={'K1','K2','K5','K15','B1','B5'} and not saved()['evidence']
 page.locator('#ev-reflection').fill('Synthetic genuine-work-shaped reflection, not actual workplace data.');page.locator('#evidence-form button[type=submit]').click();assert len(saved()['evidence'])==1
 go('evidence-packs');page.locator('[data-as-pack-link=pack-1]').check();page.locator('[data-as-evidence][data-field=role]').fill('Synthetic reviewer role');page.locator('[data-as-evidence][data-field=date]').fill('2026-11-07');page.locator('[data-as-evidence][data-field=feedback]').fill('<img src=x onerror=window.assessmentInjected=2> Synthetic feedback, no assessor claim.');page.reload();expect(page.locator('[data-as-pack-link=pack-1]')).to_be_checked();expect(page.locator('[data-as-evidence][data-field=role]')).to_have_value('Synthetic reviewer role');assert page.evaluate('window.assessmentInjected') is None
 checks.append('Four provider packs preserve required/optional mappings; template creates only an unfinished evidence draft; explicit links and safe review metadata persist separately from approval')
 snapshot=saved();old=copy.deepcopy(snapshot);del old['assessmentReview'];restore(old);assert saved()['assessmentReview']==snapshot['assessmentReview']
 changed=copy.deepcopy(snapshot);changed['assessmentReview']['groups']['K13+S10']['notes']='Imported synthetic note';restore(changed);assert saved()['assessmentReview']['groups']['K13+S10']['notes']==snapshot['assessmentReview']['groups']['K13+S10']['notes'];restore(changed,'assessment-groups-K13+S10');assert saved()['assessmentReview']['groups']['K13+S10']['notes']=='Imported synthetic note'
 before=saved()
 for mutation in [lambda s:s['assessmentReview']['groups'].update(K99={'checks':[False]*3,'notes':'','revision':''}),lambda s:s['assessmentReview']['groups']['K13+S10'].update(checks=[True]),lambda s:s['assessmentReview']['sessions'][q0].update(reviewedOn='2026-02-30'),lambda s:s['assessmentReview']['mocks'][m['id']].update(method='AM1')]:
  invalid=copy.deepcopy(before);mutation(invalid);page.locator('#backup-file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':json.dumps(invalid).encode()});expect(page.locator('#toast')).to_contain_text('Backup not imported');assert saved()==before
 go('assessment-practice');page.locator('[data-assess=mock-delete]').click();restore(snapshot);assert m['id'] not in saved()['assessmentReview']['mocks'];assert saved()['ksbs']==snapshot['ksbs']
 checks.append('Old-v1 imports preserve new records, conflicts require explicit choices, malformed group/flag/date/method data fails before mutation, and removed mocks cannot return through old backups')
 # Stale source reviews are retained and visibly request a deliberate recheck.
 stale=saved();stale['assessmentReview']['groups']['K13+S10']['revision']='older-source';restore(stale,'assessment-groups-K13+S10');go('assessment');page.locator('#as-group').select_option('K13+S10');page.locator('.as-group>summary').click();expect(page.locator('.as-review')).to_contain_text('guidance changed');page.locator('[data-as-group-note]').fill('Edited note still needs source recheck.');page.reload();page.locator('#as-group').select_option('K13+S10');page.locator('.as-group>summary').click();expect(page.locator('.as-review')).to_contain_text('guidance changed');page.locator('[data-assess=review-revision]').click();expect(page.locator('.as-review')).not_to_contain_text('guidance changed')
 # Temporary storage failures stay exportable.
 page.evaluate('()=>{Storage.prototype.setItem=function(){throw new Error("Synthetic quota failure")}}');page.locator('[data-as-group-note]').fill('Temporary assessment note');page.wait_for_timeout(500);expect(page.locator('#storage-warning')).to_be_visible()
 with page.expect_download() as dl:page.locator('[data-action=backup]').first.click()
 dl.value.save_as(str(out/'temporary.json'));assert json.loads((out/'temporary.json').read_text())['assessmentReview']['groups']['K13+S10']['notes']=='Temporary assessment note'
 checks.append('Changed-source notes/checks survive and require explicit recheck; failed storage leaves a real exportable assessment backup')
 # New clean context for all responsive and direct-file views.
 phone=b.new_context(service_workers='block');pp=phone.new_page()
 for width in [320,390,768,1440]:
  pp.set_viewport_size({'width':width,'height':1000})
  for route in ['assessment','assessment-practice','evidence-packs','ksb-k13','library','readiness']:
   pp.goto(args.url+'#'+route);expect(pp.locator('h1')).to_be_visible();assert pp.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,route)
   if width in [390,1440] and route in ['assessment','assessment-practice','evidence-packs']:pp.screenshot(path=str(out/f'{route}-{width}.png'),full_page=True)
 pp.goto((root/'index.html').as_uri()+'#assessment');expect(pp.locator('.as-group')).to_have_count(30);pp.goto((root/'index.html').as_uri()+'#assessment-practice');pp.locator('#as-response').fill('Direct-file synthetic explanation');pp.locator('[data-assess=reveal]').click();expect(pp.locator('.as-feedback')).to_be_visible();phone.close()
 checks.append('All new routes and lesson/library/readiness integrations fit320/390/768/1440px; criteria and source practice work by direct file opening')
 assert not errors,errors;c.close();b.close()
(out/'results.json').write_text(json.dumps({'status':'passed','checks':checks,'page_errors':errors},indent=2));print(json.dumps({'status':'passed','checks':checks},indent=2))
