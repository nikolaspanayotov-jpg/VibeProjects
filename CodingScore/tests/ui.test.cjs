/* A deliberately small DOM adapter exercises actual UI handlers without a browser.
 * It does not measure layout, browser-native validation, or accessibility behavior. */
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const script = html.match(/<script>([\s\S]+)<\/script>/)[1];
const attr = (text,name) => text.match(new RegExp(`(?:^|\\s)${name}="([^"]*)"`))?.[1] ?? '';

function app({saved=null,denyStorage=false,reducedMotion=false}={}) {
  const elements=new Map(),store=new Map(),documentHandlers={},downloads=[],intervals=new Map();let timerSequence=0;
  if(saved!==null)store.set('codingScore.v1',saved);
  let clock=Date.parse('2026-11-04T12:00:30Z'),document;
  class Clock extends Date {constructor(...args){super(...(args.length?args:[clock]));}static now(){return clock;}}
  class Element {
    constructor(tag='',attributes=''){
      this.tagName=tag.toUpperCase();this.id=attr(attributes,'id');this.value=attr(attributes,'value');this.defaultValue=this.value;this.checked=false;this.hidden=false;this.open=false;this.dataset={};this.style={};this.attributes={};this.listeners={};this._html='';this.textContent='';const classes=new Set(attr(attributes,'class').split(/\s+/).filter(Boolean));this.classList={add(...values){values.forEach(v=>classes.add(v));},remove(...values){values.forEach(v=>classes.delete(v));},toggle(value,force){const add=force===undefined?!classes.has(value):force;if(add)classes.add(value);else classes.delete(value);return add;},contains:value=>classes.has(value)};
      for(const match of attributes.matchAll(/data-([\w-]+)="([^"]*)"/g))this.dataset[match[1].replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=match[2];
    }
    set innerHTML(value){this._html=value;parse(value);}
    get innerHTML(){return this._html;}
    setAttribute(name,value){this.attributes[name]=String(value);}
    removeAttribute(name){delete this.attributes[name];}
    getAttribute(name){return this.attributes[name]??null;}
    addEventListener(name,handler){(this.listeners[name]??=[]).push(handler);}
    emit(name,event={}){for(const h of this.listeners[name]||[])h({target:this,preventDefault(){},...event});}
    querySelector(){return this.span??=new Element('span');}
    closest(selector){if(selector==='a[href^="#"]'&&this.tagName==='A'&&this.attributes.href?.startsWith('#'))return this;if(selector==='[data-action]'&&this.dataset.action)return this;const match=selector.match(/^\[data-action="([^"]+)"\]$/);if(match&&this.dataset.action===match[1])return this;if(selector==='[data-close]')return null;if(selector==='dialog'&&this.tagName==='DIALOG')return this;return null;}
    focus(){document.activeElement=this;}
    showModal(){this.open=true;this.focus();}
    close(){this.open=false;this.emit('close');}
    scrollIntoView(){}
    getBoundingClientRect(){return {left:0,right:600,top:0,bottom:800};}
    reset(){const content=html.match(new RegExp(`<form[^>]*id="${this.id}"[\\s\\S]*?<\\/form>`))?.[0]||'';for(const match of content.matchAll(/id="([^"]+)"/g)){const e=elements.get(match[1]);if(e&&e!==this){e.value=e.defaultValue;e.checked=false;}}}
    click(){if(this.download)downloads.push(this.download);}
    remove(){}
    get isConnected(){return true;}
  }
  function parse(markup){
    for(const match of markup.matchAll(/<([a-z][a-z0-9]*)\b([^>]*\bid="[^"]+"[^>]*)>/gi)){
      const id=attr(match[2],'id');if(!elements.has(id))elements.set(id,new Element(match[1],match[2]));
    }
    for(const match of markup.matchAll(/<select\b([^>]*)>([\s\S]*?)<\/select>/gi)){
      const e=elements.get(attr(match[1],'id'));if(!e)continue;
      const options=[...match[2].matchAll(/<option\b([^>]*)>([^<]*)<\/option>/g)],selected=options.find(o=>/\bselected\b/.test(o[1]))||options[0];
      if(selected)e.value=e.defaultValue=selected[1].includes('value=')?attr(selected[1],'value'):selected[2];
    }
  }
  parse(html.split('<script>')[0]);
  document={getElementById:id=>elements.get(id)||null,activeElement:null,body:{append(){}},
    querySelectorAll:selector=>selector==='dialog'?[...elements.values()].filter(e=>e.tagName==='DIALOG'):[],
    querySelector:selector=>selector==='dialog[open]'?[...elements.values()].find(e=>e.open)||null:null,
    addEventListener:(name,handler)=>(documentHandlers[name]??=[]).push(handler),
    createElement:tag=>new Element(tag),hidden:false};
  document.activeElement=new Element('body');
  const context=vm.createContext({document,Date:Clock,URL,Blob,Intl,console,crypto:{randomUUID:()=>`id-${Math.random().toString(36).slice(2)}`},navigator:{clipboard:{writeText:async()=>{}}},setTimeout:fn=>{fn();return 1;},setInterval:(fn,delay)=>{const id=++timerSequence;intervals.set(id,{fn,delay});return id;},clearInterval:id=>intervals.delete(id),matchMedia:()=>({matches:reducedMotion}),localStorage:{getItem:key=>{if(denyStorage)throw Error('denied');return store.get(key)??null;},setItem:(key,value)=>{if(denyStorage)throw Error('denied');store.set(key,value);}}});
  vm.runInContext(script,context);
  return {get:id=>elements.get(id),state:()=>JSON.parse(store.get('codingScore.v1')||'null'),store,downloads,active:()=>document.activeElement,
    click(action,data={}){const target=new Element('button');target.dataset={action,...data};for(const handler of documentHandlers.click||[])handler({target});},
    anchor(id){const target=new Element('a');target.attributes.href='#'+id;for(const handler of documentHandlers.click||[])handler({target});},
    submit:id=>elements.get(id).emit('submit'),change:id=>elements.get(id).emit('change'),
    advance:ms=>{clock+=ms;},tick:delay=>{for(const timer of [...intervals.values()])if(timer.delay===delay)timer.fn();},timers:delay=>[...intervals.values()].filter(t=>t.delay===delay).length,key(action,data={},tag='g',key='Enter'){let prevented=false;const target=new Element(tag);target.dataset={action,...data};for(const handler of documentHandlers.keydown||[])handler({target,key,preventDefault(){prevented=true;}});return prevented;},hide(){document.hidden=true;for(const handler of documentHandlers.visibilitychange||[])handler({});},blank:()=>vm.runInContext('Core.blank()',context)};
}
function log(a,note='Codex helped me fix a script.',extra={}){
  a.click('log');a.get('entryNote').value=note;
  for(const [id,value] of Object.entries(extra)){if(['entryUseful','entryStepComplete'].includes(id))a.get(id).checked=value;else a.get(id).value=value;}
  a.submit('entryForm');
}

test('the complete script boots into an honest empty state',()=>{
  const a=app();assert.equal(a.get('xpTotal').textContent,'0 XP');assert.equal(a.get('activeWeek').textContent,'0 of 7 days');assert.match(a.get('shortReading').innerHTML,/Not recorded/);assert.match(a.get('journalList').innerHTML,/Your first win/);assert.equal(a.get('storageNotice').hidden,true);
});
test('actual logging handlers persist once-only daily XP and restore on reload',()=>{
  const a=app();log(a);assert.equal(a.state().entries.length,1);assert.equal(a.get('xpTotal').textContent,'25 XP');assert.equal(a.get('entryDialog').open,false);
  log(a,'A second actual use.',{entryXP:'10',entryLearning:'A useful lesson',entryNext:'Automate tomorrow’s report'});
  assert.equal(a.state().entries.length,2);assert.equal(a.get('xpTotal').textContent,'45 XP');assert.equal(a.get('suggestionText').textContent,'Automate tomorrow’s report');
  const reloaded=app({saved:a.store.get('codingScore.v1')});assert.equal(reloaded.get('xpTotal').textContent,'45 XP');
});
test('editing, deleting, and undoing recalculate from records',()=>{
  const a=app();log(a);const id=a.state().entries[0].id;
  a.click('edit-entry',{id});a.get('entryXP').value='10';a.submit('entryForm');assert.equal(a.state().entries.length,1);assert.equal(a.get('xpTotal').textContent,'30 XP');
  a.click('delete-entry',{id});assert.equal(a.get('xpTotal').textContent,'0 XP');assert.equal(a.get('undoButton').hidden,false);
  a.click('undo');assert.equal(a.get('xpTotal').textContent,'30 XP');assert.equal(a.state().entries.length,1);
});
test('backfilling a day preserves a gap honestly and historical correction joins the streak',()=>{
  const a=app();log(a,'A use two days ago.',{entryDate:'2026-11-02',entryTime:''});log(a);
  assert.match(a.get('streakCount').innerHTML,/^1<span>/);
  log(a,'A use yesterday.',{entryDate:'2026-11-03',entryTime:''});assert.match(a.get('streakCount').innerHTML,/^3<span>/);assert.equal(a.get('xpTotal').textContent,'90 XP');
});
test('invalid XP or a future occurrence leaves current data unchanged and keeps the form open',()=>{
  const a=app();log(a,'A use.',{entryXP:'11'});assert.equal(a.state(),null);assert.match(a.get('entryError').textContent,/work XP/);assert.equal(a.get('entryDialog').open,true);
  a.get('entryXP').value='5';a.get('entryDate').value='2099-01-01';a.submit('entryForm');assert.equal(a.state(),null);assert.match(a.get('entryError').textContent,/dates/);
});
test('a newly created mission can be banked immediately, retaining occurrence seconds',()=>{
  const a=app();a.click('reading',{kind:'short'});a.get('readingPercent').value='75';a.get('readingReset').value='2026-11-04T17:00';a.submit('readingForm');
  a.click('mission');a.get('missionText').value='Fix a small bug';a.submit('missionForm');const id=a.state().missions[0].id;
  a.advance(1000);a.click('log-mission',{id});a.get('entryNote').value='Fixed the bug with Codex.';a.submit('entryForm');
  assert.equal(a.get('entryError').textContent,'');assert.equal(a.state().entries[0].missionId,id);assert.match(a.get('missionTray').innerHTML,/1 mission banked/);
});
test('a weekly zero blocks new missions while leaving real-use logging available',()=>{
  const a=app();for(const [kind,remaining,reset] of [['short','75','2026-11-04T17:00'],['weekly','0','2026-11-10T12:00']]){a.click('reading',{kind});a.get('readingPercent').value=remaining;a.get('readingReset').value=reset;a.submit('readingForm');}
  assert.match(a.get('shortReading').innerHTML,/weekly reading is 0%/);a.click('mission');a.get('missionText').value='A task';a.submit('missionForm');assert.match(a.get('missionError').textContent,/weekly reading is 0%/);assert.equal(a.state().missions.length,0);
  log(a);assert.equal(a.state().entries.length,1);
});
test('campaign setup and review use timed actual activity and persist the review',()=>{
  const a=app();log(a);a.click('campaign');a.get('campaignStart').value='2026-10-29T12:00';a.get('campaignEnd').value='2026-11-05T12:00';a.get('campaignReview').value='Debugging saved me time.';a.submit('campaignForm');
  assert.equal(a.state().campaigns.length,1);assert.match(a.get('campaignProgress').innerHTML,/1 \/ 7 active dates/);assert.match(a.get('campaignProgress').innerHTML,/Debugging saved me time/);
});
test('user content is escaped in journal, day dialog, and next-task surfaces',()=>{
  const a=app();log(a,'<img src=x onerror=alert(1)>',{entryNext:'<script>bad()</script>',entryUseful:true});assert.match(a.get('journalList').innerHTML,/&lt;img/);assert.doesNotMatch(a.get('journalList').innerHTML,/<img/);
  a.click('day',{date:'2026-11-04'});assert.match(a.get('dayRecords').innerHTML,/&lt;img/);assert.equal(a.get('suggestionText').textContent,'<script>bad()</script>');
});
test('denied storage stays usable and clearly identifies session-only changes',()=>{
  const a=app({denyStorage:true});log(a);assert.equal(a.get('xpTotal').textContent,'25 XP');assert.equal(a.get('storageNotice').hidden,false);assert.equal(a.get('saveStatus').textContent,'This visit only');
});
test('corrupt data is retained verbatim while new visit records stay exportable',()=>{
  const a=app({saved:'{unreadable'});log(a);assert.equal(a.store.get('codingScore.v1'),'{unreadable');assert.equal(a.get('recoverButton').hidden,false);assert.equal(a.get('xpTotal').textContent,'25 XP');a.click('export');assert.equal(a.downloads.length,1);
});
test('import validates first, previews replacement, and changes nothing until confirmation',async()=>{
  const a=app();log(a);const original=a.store.get('codingScore.v1');
  a.get('backupFile').files=[{size:20,text:async()=>'{}'}];await a.get('backupFile').listeners.change[0]({target:a.get('backupFile')});assert.equal(a.store.get('codingScore.v1'),original);assert.match(a.get('backupStatus').textContent,/Import stopped/);
  a.get('backupFile').files=[{size:100,text:async()=>JSON.stringify(a.blank())}];await a.get('backupFile').listeners.change[0]({target:a.get('backupFile')});assert.equal(a.get('confirmDialog').open,true);assert.equal(a.store.get('codingScore.v1'),original);
  a.get('confirmButton').emit('click');assert.equal(a.state().entries.length,0);assert.equal(a.get('xpTotal').textContent,'0 XP');
});
test('clear-data requires confirmation and resets personal state',()=>{
  const a=app();log(a);a.click('clear-data');assert.equal(a.state().entries.length,1);a.get('confirmButton').emit('click');assert.equal(a.state().entries.length,0);assert.equal(a.get('xpTotal').textContent,'0 XP');
});
function createQuest(a,title='A useful project') {
  a.click('new-quest');a.get('questName').value=title;a.get('questGoal').value='A small working improvement';a.submit('questForm');return a.state().quests.at(-1);
}
function createWorkflow(a,title='A useful shortcut') {
  a.click('new-workflow');a.get('workflowName').value=title;a.get('workflowKind').value='Review';a.get('workflowPrompt').value='Review [paste change] for edge cases.';a.get('workflowResult').value='Found a missing boundary check';a.submit('workflowForm');return a.state().workflows.at(-1);
}
test('old browser data migrates without losing XP and gains the new sections',()=>{
  const first=app();log(first);const old=first.state();old.version=1;delete old.quests;delete old.workflows;delete old.challenges;
  for(const e of old.entries)for(const key of ['minutesSaved','before','after','prompt','questId','questStepId','stepComplete','workflowId','workflowTitle'])delete e[key];
  const upgraded=app({saved:JSON.stringify(old)});assert.equal(upgraded.get('xpTotal').textContent,'25 XP');assert.match(upgraded.get('workshopCount').textContent,/1 \/ 7/);assert.match(upgraded.get('workflowList').innerHTML,/good prompt/);
  createQuest(upgraded);assert.equal(upgraded.state().version,2);assert.equal(upgraded.state().entries.length,1);
});
test('quest creation adds no XP and actual log handlers complete only explicitly marked steps',()=>{
  const a=app(),q=createQuest(a);assert.equal(a.get('xpTotal').textContent,'0 XP');assert.equal(q.steps.length,4);
  a.click('quest-step',{id:q.id,step:q.steps[0].id});a.get('entryNote').value='Investigated the problem';a.submit('entryForm');assert.equal(a.state().entries[0].stepComplete,false);assert.match(a.get('questList').innerHTML,/0 \/ 4 steps/);
  for(let i=0;i<4;i++){a.click('quest-step',{id:q.id,step:q.steps[i].id});a.get('entryNote').value=`Completed step ${i}`;a.get('entryStepComplete').checked=true;a.submit('entryForm');}
  a.get('questFilter').value='complete';a.change('questFilter');assert.match(a.get('questList').innerHTML,/Quest complete/);assert.match(a.get('workshopItems').innerHTML,/Tools/);assert.equal(a.state().entries.filter(e=>e.stepComplete).length,4);
});
test('quest editing preserves step IDs, archiving preserves linked work, and empty deletion confirms',()=>{
  const a=app(),q=createQuest(a);a.click('edit-quest',{id:q.id});a.get('questStep1').value='Understand the inputs';a.get('questArchived').checked=true;a.submit('questForm');assert.equal(a.state().quests[0].steps[0].id,q.steps[0].id);assert.equal(a.state().quests[0].archived,true);
  a.get('questFilter').value='archived';a.change('questFilter');assert.match(a.get('questList').innerHTML,/Understand the inputs/);
  a.click('delete-quest',{id:q.id});assert.equal(a.state().quests.length,1);a.get('confirmButton').emit('click');assert.equal(a.state().quests.length,0);
  const second=createQuest(a);a.click('log-quest',{id:second.id});a.get('entryNote').value='Real linked work';a.submit('entryForm');a.click('delete-quest',{id:second.id});assert.equal(a.state().quests.length,1);assert.match(a.get('toastText').textContent,/Archive/);
});
test('editing a completed quest log to unfinished removes derived completion',()=>{
  const a=app(),q=createQuest(a);
  for(const step of q.steps){a.click('quest-step',{id:q.id,step:step.id});a.get('entryNote').value='Completed work';a.get('entryStepComplete').checked=true;a.submit('entryForm');}
  const entry=a.state().entries[0];a.click('edit-entry',{id:entry.id});a.get('entryStepComplete').checked=false;a.submit('entryForm');a.get('questFilter').value='active';a.change('questFilter');assert.match(a.get('questList').innerHTML,/3 \/ 4 steps/);
});
test('a personal challenge is accepted once and completes from a matching useful result',()=>{
  const a=app(),id='2026-11-02-Automate';a.click('accept-challenge',{id});a.click('accept-challenge',{id});assert.equal(a.state().challenges.length,1);assert.equal(a.get('xpTotal').textContent,'0 XP');
  a.click('log-challenge',{id});assert.equal(a.get('entryCategory').value,'Automate');a.get('entryNote').value='Automated a small repeated task';a.get('entryUseful').checked=true;a.submit('entryForm');assert.match(a.get('challengeCount').textContent,/1 challenge completed/);assert.equal(a.get('xpTotal').textContent,'25 XP');
});
test('variety challenge counts different categories rather than repeated same-category logs',()=>{
  const a=app();a.click('accept-challenge',{id:'2026-11-02-variety'});log(a,'First', {entryCategory:'Build'});log(a,'Second',{entryCategory:'Build'});assert.match(a.get('challengeCount').textContent,/0 challenges/);
  log(a,'A review',{entryCategory:'Review'});log(a,'Learned a function',{entryCategory:'Learn'});assert.match(a.get('challengeCount').textContent,/1 challenge/);
});
test('payoff and prompt fields persist through edit/reload, remain searchable, and never multiply XP',()=>{
  const a=app();log(a,'A real task',{entryBefore:'Manual spreadsheet work',entryAfter:'One script generates the report',entrySaved:'45',entryPrompt:'Help me automate [sample rows].'});
  assert.equal(a.get('xpTotal').textContent,'25 XP');assert.equal(a.state().entries[0].minutesSaved,45);assert.match(a.get('payoffSummary').textContent,/45 estimated minutes/);assert.match(a.get('journalList').innerHTML,/Before and after/);
  const id=a.state().entries[0].id;a.click('edit-entry',{id});assert.equal(a.get('entrySaved').value,45);a.get('entryNote').value='A corrected task note';a.submit('entryForm');assert.equal(a.state().entries[0].before,'Manual spreadsheet work');
  a.get('journalSearch').value='spreadsheet';a.get('journalSearch').emit('input');assert.match(a.get('journalList').innerHTML,/corrected task/);
  const reloaded=app({saved:a.store.get('codingScore.v1')});assert.equal(reloaded.state().entries[0].prompt,'Help me automate [sample rows].');assert.match(reloaded.get('recapMetrics').innerHTML,/45/);
});
test('invalid payoff estimates preserve the current scorebook and form input',()=>{
  const a=app();log(a,'Valid');const original=a.store.get('codingScore.v1');log(a,'Bad estimate',{entrySaved:'-10'});assert.match(a.get('entryError').textContent,/estimated minutes/);assert.equal(a.store.get('codingScore.v1'),original);assert.equal(a.get('entryNote').value,'Bad estimate');
});
test('weekly recap navigation, summary, and vector fallback export work without changing scores',()=>{
  const a=app();log(a,'A useful result',{entrySaved:'15',entryUseful:true});assert.equal(a.get('recapStatus').textContent,'Week so far');assert.match(a.get('recapMetrics').innerHTML,/15/);
  a.click('recap-previous');assert.equal(a.get('recapStatus').textContent,'Full week');assert.match(a.get('recapHighlight').innerHTML,/next small win/);a.click('recap-current');a.click('export-recap');assert.equal(a.downloads.at(-1),'CodingScore-week-2026-11-02.svg');assert.equal(a.get('xpTotal').textContent,'25 XP');
});
test('workshop controls expose unlock rules and return focus after replacing the illustration',()=>{
  const a=app();a.click('workshop-item',{id:'plant'});assert.match(a.get('workshopItemInfo').textContent,/7 different dates/);assert.equal(a.active().id,'workshop-item-plant');
  log(a);assert.match(a.get('workshopCount').textContent,/1 \/ 7 unlocked/);assert.match(a.get('workshopScene').innerHTML,/room-item unlocked/);
});
test('workflow library supports save, favorite, filters, and actual reuse logging',()=>{
  const a=app(),w=createWorkflow(a);assert.equal(a.get('xpTotal').textContent,'0 XP');a.click('favorite-workflow',{id:w.id});assert.equal(a.state().workflows[0].favorite,true);
  a.get('workflowSearch').value='boundary';a.get('workflowSearch').emit('input');assert.match(a.get('workflowList').innerHTML,/useful shortcut/);
  a.get('workflowCategory').value='Build';a.change('workflowCategory');assert.match(a.get('workflowList').innerHTML,/No matching/);a.click('clear-workflow-filters');
  a.click('log-workflow',{id:w.id});assert.equal(a.get('entryCategory').value,'Review');assert.equal(a.get('entryPrompt').value,w.prompt);a.get('entryNote').value='Used the saved review prompt';a.submit('entryForm');assert.equal(a.state().entries[0].workflowId,w.id);assert.match(a.get('workflowList').innerHTML,/1 actual reuse logged/);assert.match(a.get('recapDiscovery').textContent,/1 saved workflow/);
});
test('saving a workflow from a use prefills the actual prompt, outcome, and context',()=>{
  const a=app();log(a,'Simplified a report',{entryPrompt:'Make [report] simpler.',entryOutcome:'A shorter report',entryBefore:'Too much manual editing'});const id=a.state().entries[0].id;
  a.click('save-entry-workflow',{id});assert.equal(a.get('workflowPrompt').value,'Make [report] simpler.');assert.equal(a.get('workflowResult').value,'A shorter report');a.submit('workflowForm');assert.equal(a.state().workflows[0].sourceEntryId,id);assert.equal(a.get('xpTotal').textContent,'25 XP');
});
test('deleting a workflow keeps historical reuse, prompt, title, and score, including after editing',()=>{
  const a=app(),w=createWorkflow(a);a.click('log-workflow',{id:w.id});a.get('entryNote').value='Used this prompt';a.submit('entryForm');const entry=a.state().entries[0],xp=a.get('xpTotal').textContent;
  a.click('delete-workflow',{id:w.id});assert.equal(a.state().workflows.length,1);a.get('confirmButton').emit('click');assert.equal(a.state().workflows.length,0);assert.equal(a.state().entries[0].workflowId,w.id);assert.equal(a.state().entries[0].workflowTitle,w.title);assert.equal(a.get('xpTotal').textContent,xp);
  a.click('edit-entry',{id:entry.id});a.submit('entryForm');assert.equal(a.state().entries[0].prompt,w.prompt);assert.match(a.get('journalList').innerHTML,/removed from library/);
});
test('new workflow and quest surfaces escape user text, and backups round trip all additions',async()=>{
  const a=app(),q=createQuest(a,'<img onerror=alert(1)>');createWorkflow(a,'<script>unsafe()</script>');assert.match(a.get('questList').innerHTML,/&lt;img/);assert.match(a.get('workflowList').innerHTML,/&lt;script&gt;/);assert.doesNotMatch(a.get('workflowList').innerHTML,/<script>/);
  a.click('accept-challenge',{id:'2026-11-02-Automate'});a.click('log-quest',{id:q.id});a.get('entryNote').value='Real work';a.get('entrySaved').value='10';a.submit('entryForm');const saved=a.store.get('codingScore.v1'),restored=app({saved});assert.equal(restored.state().quests.length,1);assert.equal(restored.state().workflows.length,1);assert.equal(restored.state().challenges.length,1);assert.equal(restored.state().entries[0].minutesSaved,10);
  restored.click('clear-data');restored.get('confirmButton').emit('click');assert.equal(restored.state().quests.length,0);assert.equal(restored.state().workflows.length,0);assert.equal(restored.state().challenges.length,0);
  restored.get('backupFile').files=[{size:saved.length,text:async()=>saved}];await restored.get('backupFile').listeners.change[0]({target:restored.get('backupFile')});assert.match(restored.get('confirmText').textContent,/1 quests, 1 workflows, and 1 challenges/);restored.get('confirmButton').emit('click');assert.equal(restored.state().quests.length,1);assert.equal(restored.state().workflows.length,1);assert.equal(restored.state().challenges.length,1);assert.equal(restored.state().entries[0].minutesSaved,10);
});
test('selecting a quest emblem preserves it across save, edit, and backup reload',()=>{
  const a=app();a.click('new-quest');assert.equal(a.get('questEmblem').value,'compass');a.click('quest-emblem',{id:'robot'});assert.equal(a.active().id,'quest-emblem-robot');a.get('questName').value='A robot helper';a.submit('questForm');const q=a.state().quests[0];assert.equal(q.emblem,'robot');assert.match(a.get('questList').innerHTML,/Robot adventure/);
  a.click('edit-quest',{id:q.id});assert.equal(a.get('questEmblem').value,'robot');a.get('questName').value='A better robot helper';a.submit('questForm');const restored=app({saved:a.store.get('codingScore.v1')});restored.click('edit-quest',{id:q.id});assert.equal(restored.get('questEmblem').value,'robot');assert.equal(restored.get('xpTotal').textContent,'0 XP');
});
test('quest paths show illustrated steps, textual status, and only connect completed neighbors',()=>{
  const a=app(),q=createQuest(a);assert.match(a.get('questList').innerHTML,/Quest journey/);assert.match(a.get('questList').innerHTML,/Your next step/);assert.match(a.get('questList').innerHTML,/Step 1 of 4/);
  a.click('quest-step',{id:q.id,step:q.steps[0].id});a.get('entryNote').value='Finished investigating';a.get('entryStepComplete').checked=true;a.submit('entryForm');assert.doesNotMatch(a.get('questList').innerHTML,/class="complete connected"/);
  a.click('quest-step',{id:q.id,step:q.steps[1].id});a.get('entryNote').value='Finished building';a.get('entryStepComplete').checked=true;a.submit('entryForm');assert.match(a.get('questList').innerHTML,/class="complete connected"/);assert.match(a.get('questList').innerHTML,/step-check/);
});
test('locked achievements retain their reward artwork, requirements, and real progress',()=>{
  const a=app();assert.match(a.get('badgeShelf').innerHTML,/badge-illustration/);assert.match(a.get('badgeShelf').innerHTML,/achievement-ring/);assert.match(a.get('badgeShelf').innerHTML,/Locked · preview reward/);a.click('achievement',{id:'streak7'});assert.equal(a.get('achievementDialog').open,true);assert.equal(a.get('achievementRequirement').textContent,'Use Codex 7 days in a row');assert.match(a.get('achievementDetailProgress').textContent,/0 of 7/);assert.equal(a.get('achievementDayButton').hidden,true);
});
test('earned achievement details explain the date and let users revisit its actual day',()=>{
  const a=app();log(a,'Fixed a real issue');assert.equal(a.get('celebrationView').dataset.id,'first');a.click('achievement',{id:'first'});assert.match(a.get('achievementEarnedDate').textContent,/2026/);assert.match(a.get('achievementProof').textContent,/Fixed a real issue/);assert.equal(a.get('achievementDayButton').hidden,false);
  a.click('achievement-day',{date:a.get('achievementDayButton').dataset.date});assert.equal(a.get('achievementDialog').open,false);assert.equal(a.get('dayDialog').open,true);assert.match(a.get('dayRecords').innerHTML,/Fixed a real issue/);
});
test('achievement collection filters are keyboard-focusable and preserve scores',()=>{
  const a=app();a.click('achievement-filter',{filter:'earned'});assert.match(a.get('badgeShelf').innerHTML,/first collectible/);assert.equal(a.active().id,'achievement-filter-earned');log(a);a.click('achievement-filter',{filter:'earned'});assert.match(a.get('badgeShelf').innerHTML,/First little win/);assert.doesNotMatch(a.get('badgeShelf').innerHTML,/7-day streak/);
  a.click('achievement-filter',{filter:'next'});assert.doesNotMatch(a.get('badgeShelf').innerHTML,/First little win/);assert.equal(a.get('xpTotal').textContent,'25 XP');
});
test('daily focus follows the active quest and moves on when that quest is completed',()=>{
  const a=app();assert.match(a.get('focusQuest').innerHTML,/Pick a project/);const q=createQuest(a,'My current adventure');assert.match(a.get('focusQuest').innerHTML,/My current adventure/);assert.match(a.get('focusAchievement').innerHTML,/Next reward/);
  for(const step of q.steps){a.click('quest-step',{id:q.id,step:step.id});a.get('entryNote').value='Useful quest work';a.get('entryStepComplete').checked=true;a.submit('entryForm');}assert.match(a.get('focusQuest').innerHTML,/Pick a project/);
});
test('badge dates and earned-state details recalculate after deletion',()=>{
  const a=app();log(a);const id=a.state().entries[0].id;a.click('delete-entry',{id});a.click('achievement',{id:'first'});assert.equal(a.get('achievementDetailStatus').textContent,'A reward to work toward');assert.equal(a.get('achievementDayButton').hidden,true);assert.doesNotMatch(a.get('achievementEarnedDate').textContent,/Earned on/);
});
test('turning off celebrations still earns illustrated rewards without an unlock banner',()=>{
  const a=app();a.get('celebrationsToggle').checked=false;a.change('celebrationsToggle');log(a);assert.equal(a.get('celebration').hidden,true);assert.match(a.get('badgeShelf').innerHTML,/Earned · view your story/);assert.equal(a.get('xpTotal').textContent,'25 XP');
});
test('workshop objects expose keyboard shortcuts to actual features even before decoration unlocks',()=>{
  const a=app();assert.equal((a.get('workshopScene').innerHTML.match(/data-action="workshop-open"/g)||[]).length,7);a.click('workshop-open',{id:'books'});assert.equal(a.active().id,'workflowSearch');
  a.click('workshop-open',{id:'plant'});assert.equal(a.active().id,'calendar');a.click('workshop-open',{id:'lamp'});assert.equal(a.get('dailyIdeas').open,true);assert.equal(a.active().id,'taskShuffle');
  a.key('workshop-open',{id:'window'},'g','Enter');assert.equal(a.active().id,'skill-island-Build');a.click('workshop-open',{id:'desk'});assert.equal(a.get('questDialog').open,true);assert.equal(a.get('xpTotal').textContent,'0 XP');
});
test('the desk opens the active quest story and its log control links actual work',()=>{
  const a=app(),q=createQuest(a);a.click('workshop-open',{id:'desk'});assert.equal(a.get('questStoryDialog').open,true);assert.match(a.get('questStoryArt').innerHTML,/data-stage="0"/);
  a.click('story-log',{id:q.id});assert.equal(a.get('questStoryDialog').open,false);assert.equal(a.get('entryQuest').value,q.id);a.get('entryNote').value='Real project progress';a.get('entryStepComplete').checked=true;a.submit('entryForm');assert.match(a.get('questList').innerHTML,/data-stage="1"/);
});
test('win cards flip in place, preserve missing outcomes honestly, and open their real day',()=>{
  const a=app();log(a,'A useful question',{entryUseful:true,entryBefore:'Manual cleanup',entryAfter:'A repeatable script',entrySaved:'15'});const id=a.state().entries[0].id,xp=a.get('xpTotal').textContent;
  assert.match(a.get('winGallery').innerHTML,/Manual cleanup/);assert.match(a.get('winGallery').innerHTML,/A repeatable script/);a.click('flip-win',{id});assert.equal(a.get('win-card-'+id).attributes['aria-pressed'],'true');a.click('flip-win',{id});assert.equal(a.get('win-card-'+id).attributes['aria-pressed'],'false');assert.equal(a.get('xpTotal').textContent,xp);a.click('win-entry',{id});assert.equal(a.get('dayDialog').open,true);
  a.get('dayDialog').close();log(a,'Still in progress',{entryBefore:'A complex function'});assert.match(a.get('winGallery').innerHTML,/Add an after note/);
});
test('win gallery category filters and paging are backed by actual journal records',()=>{
  const a=app();for(let i=0;i<7;i++)log(a,'Useful task '+i,{entryUseful:true,entryCategory:i===6?'Review':'Build'});assert.match(a.get('winGalleryCount').textContent,/1–3 of 7/);a.click('win-page',{direction:'1'});assert.match(a.get('winGalleryCount').textContent,/4–6 of 7/);a.click('win-page',{direction:'1'});assert.match(a.get('winGalleryCount').textContent,/7–7 of 7/);assert.equal(a.get('winNext').disabled,true);
  a.get('winCategory').value='Review';a.change('winCategory');assert.match(a.get('winGalleryCount').textContent,/1–1 of 1/);a.get('winCategory').value='Learn';a.change('winCategory');assert.match(a.get('winGallery').innerHTML,/Your next win/);
});
test('task deck cards reveal prompts, shuffle, and prefill logging without awarding XP',()=>{
  const a=app();assert.match(a.get('taskDeck').innerHTML,/Debug/);assert.equal(a.get('task-copy-1').disabled,true);a.click('flip-task',{id:'1'});assert.equal(a.get('task-copy-1').disabled,false);assert.equal(a.get('task-card-1').attributes['aria-pressed'],'true');a.click('copy-task',{id:'1'});assert.equal(a.state(),null);
  a.click('log-task',{id:'1'});assert.equal(a.get('entryCategory').value,'Debug');assert.equal(a.get('entryNote').value,'');a.get('entryDialog').close();a.click('shuffle-tasks');assert.match(a.get('taskDeck').innerHTML,/Plan/);assert.equal(a.get('xpTotal').textContent,'0 XP');
  a.get('ideaCategory').value='Plan';a.change('ideaCategory');assert.equal(a.get('taskShuffle').disabled,true);assert.match(a.get('taskDeck').innerHTML,/first step/);
});
test('showcase allows three earned pins, prevents unearned pins, and survives reload and historical correction',()=>{
  const a=app();a.click('pin-achievement',{id:'streak100'});assert.equal(a.state(),null);
  const w=createWorkflow(a);a.click('log-workflow',{id:w.id});a.get('entryCategory').value='Automate';a.get('entryNote').value='Reused a useful automation';a.get('entryUseful').checked=true;a.submit('entryForm');
  for(const id of ['first','automation','workflow'])a.click('pin-achievement',{id});assert.equal(a.state().settings.pinnedAchievements.length,3);assert.match(a.get('badgeShowcase').innerHTML,/A shortcut worth keeping/);
  const restored=app({saved:a.store.get('codingScore.v1')});assert.equal(restored.state().settings.pinnedAchievements.length,3);const entry=restored.state().entries[0];restored.click('delete-entry',{id:entry.id});assert.match(restored.get('badgeShowcase').innerHTML,/Requirement no longer met/);restored.click('pin-achievement',{id:'first'});assert.equal(restored.state().settings.pinnedAchievements.length,2);
});
test('showcase refuses a fourth earned badge until another favorite is unpinned',()=>{
  const a=app();log(a,'Earlier use',{entryDate:'2026-11-02',entryTime:'',entryUseful:true,entryCategory:'Automate'});log(a,'Yesterday',{entryDate:'2026-11-03',entryTime:''});log(a,'Today');
  for(const id of ['first','automation','streak3'])a.click('pin-achievement',{id});assert.equal(a.state().settings.pinnedAchievements.length,3);
  const w=createWorkflow(a);a.click('log-workflow',{id:w.id});a.get('entryNote').value='A real workflow reuse';a.submit('entryForm');a.click('pin-achievement',{id:'workflow'});assert.equal(a.state().settings.pinnedAchievements.length,3);assert.match(a.get('toastText').textContent,/three favorites/);
});
test('badge export uses the actual earned date and leaves source records unchanged',()=>{
  const a=app();a.click('export-badge',{id:'streak7'});assert.equal(a.downloads.length,0);log(a);const original=a.store.get('codingScore.v1');a.click('export-badge',{id:'first'});assert.equal(a.downloads.at(-1),'CodingScore-first-2026-11-04.svg');assert.equal(a.store.get('codingScore.v1'),original);
});
test('practice islands show real results, lead to category logs, and filter the journal',()=>{
  const a=app();log(a,'Reviewed a function',{entryCategory:'Review',entryUseful:true});a.click('skill',{category:'Review'});assert.equal(a.get('skillDialog').open,true);assert.match(a.get('skillRecent').innerHTML,/Reviewed a function/);assert.match(a.get('skillMetrics').innerHTML,/useful results/);
  a.click('skill-journal',{category:'Review'});assert.equal(a.get('journalCategory').value,'Review');assert.equal(a.active().id,'journalSearch');a.click('skill',{category:'Learn'});a.click('skill-log',{category:'Learn'});assert.equal(a.get('entryCategory').value,'Learn');assert.equal(a.get('entryNote').value,'');
});
test('quest scenes complete once after actual work and linked journal views remain precise',()=>{
  const a=app(),q=createQuest(a);log(a,'Unrelated work');for(const step of q.steps){a.click('quest-step',{id:q.id,step:step.id});a.get('entryNote').value='Linked quest work';a.get('entryStepComplete').checked=true;a.submit('entryForm');}
  assert.equal(a.get('questCompletion').hidden,false);assert.match(a.get('questCompletionArt').innerHTML,/data-stage="4"/);a.click('quest-journal',{id:q.id});assert.equal(a.get('journalScope').hidden,false);assert.doesNotMatch(a.get('journalList').innerHTML,/Unrelated work/);a.click('clear-filters');assert.match(a.get('journalList').innerHTML,/Unrelated work/);
  a.click('dismiss-quest-completion');assert.equal(a.get('questCompletion').hidden,true);log(a,'Another useful use');assert.equal(a.get('questCompletion').hidden,true);
});
test('replay supports pause, seeking, manual steps, and returns to the actual day without changing XP',()=>{
  const a=app();log(a,'A real win',{entryUseful:true});const original=a.store.get('codingScore.v1');a.click('open-replay');assert.equal(a.get('replayDialog').open,true);assert.match(a.get('replayPosition').textContent,/Moment 1 of/);a.click('replay-play');assert.equal(a.timers(2500),1);a.tick(2500);assert.equal(Number(a.get('replaySeek').value),1);
  a.click('replay-play');assert.equal(a.timers(2500),0);a.get('replaySeek').value='0';a.get('replaySeek').emit('input');assert.equal(Number(a.get('replaySeek').value),0);a.click('replay-next');assert.equal(Number(a.get('replaySeek').value),1);a.click('replay-day',{date:a.get('replayDay').dataset.date});assert.equal(a.get('replayDialog').open,false);assert.equal(a.get('dayDialog').open,true);assert.equal(a.store.get('codingScore.v1'),original);
});
test('replay timers stop on close, hidden tabs, data edits, and the final event',()=>{
  const a=app();log(a);a.click('open-replay');a.click('replay-play');a.get('replayDialog').close();assert.equal(a.timers(2500),0);
  a.click('open-replay');a.click('replay-play');a.hide();assert.equal(a.timers(2500),0);a.click('replay-play');log(a,'A new actual use');assert.equal(a.timers(2500),0);
  a.click('open-replay');a.click('replay-play');for(let i=0;i<30&&a.timers(2500);i++)a.tick(2500);assert.equal(a.timers(2500),0);assert.equal(a.get('replayNext').disabled,true);
});
test('reduced motion uses manual replay and empty weeks never create fake events',()=>{
  const empty=app();empty.click('open-replay');assert.match(empty.get('replayStage').innerHTML,/No actual work/);assert.equal(empty.get('replayPlay').disabled,true);assert.equal(empty.get('replayDay').disabled,true);
  const a=app({reducedMotion:true});log(a);a.click('open-replay');assert.equal(a.get('replayPlay').disabled,true);a.click('replay-play');assert.equal(a.timers(2500),0);a.click('replay-next');assert.equal(Number(a.get('replaySeek').value),1);assert.match(a.get('replayMotionNote').textContent,/Reduced motion/);
});
test('expanded backup retains pinned achievements and clearing removes the showcase preferences',async()=>{
  const a=app();log(a);a.click('pin-achievement',{id:'first'});const saved=a.store.get('codingScore.v1');a.click('clear-data');a.get('confirmButton').emit('click');assert.equal(a.state().settings.pinnedAchievements.length,0);
  a.get('backupFile').files=[{size:saved.length,text:async()=>saved}];await a.get('backupFile').listeners.change[0]({target:a.get('backupFile')});a.get('confirmButton').emit('click');assert.equal(a.state().settings.pinnedAchievements[0],'first');assert.match(a.get('badgeShowcase').innerHTML,/First little win/);
});

function saveCapsule(a){a.click('new-capsule');a.get('capsuleAction').value='Finish the report';a.get('capsuleContext').value='Input rows match';a.get('capsulePrompt').value='Check the output';a.get('capsuleReference').value='https://example.org/report';a.get('capsuleCategory').value='Review';a.submit('capsuleForm');return a.state().personal.capsules.at(-1).id;}
function saveExperiment(a){a.click('new-experiment');a.get('experimentName').value='Sharper code review';a.get('experimentCategory').value='Review';a.get('experimentPrompt').value='Review this function';a.submit('experimentForm');return a.state().personal.experiments.at(-1);}
function saveGift(a,kind='days',target='1'){a.click('new-gift');a.get('giftName').value='Buy a book';a.get('giftKind').value=kind;a.change('giftKind');a.get('giftTarget').value=target;a.submit('giftForm');return a.state().personal.rewards.at(-1).id;}
test('Today and Explore toggles keep their selected state across source changes',()=>{
  const a=app();assert.equal(a.get('viewToday').attributes['aria-pressed'],'true');a.click('view',{id:'explore'});assert.equal(a.get('viewExplore').attributes['aria-pressed'],'true');log(a);assert.equal(a.get('viewExplore').attributes['aria-pressed'],'true');a.click('view',{id:'today'});assert.equal(a.get('viewToday').attributes['aria-pressed'],'true');assert.match(a.get('exploreTiles').innerHTML,/#lab/);
});
test('companions and suggested tasks are cosmetic and persist without XP',()=>{
  const a=app();a.click('choose-companion',{id:'sprig'});assert.equal(a.state().personal.companion,'sprig');assert.equal(a.get('xpTotal').textContent,'0 XP');a.click('companion-idea');assert.equal(a.get('dailyIdeas').open,true);assert.equal(a.state().entries.length,0);const reload=app({saved:a.store.get('codingScore.v1')});assert.equal(reload.state().personal.companion,'sprig');a.click('choose-companion',{id:'none'});assert.equal(a.get('companionAvatar').hidden,true);
});
test('capsules save a next action without logging it and complete only through a checked actual use',()=>{
  const a=app(),id=saveCapsule(a);assert.equal(a.get('xpTotal').textContent,'0 XP');assert.match(a.get('capsuleHome').innerHTML,/Finish the report/);a.click('resume-capsule',{id});assert.equal(a.state().entries.length,0);
  a.click('complete-capsule',{id});assert.equal(a.get('entryNote').value,'');assert.equal(a.get('entryCategory').value,'Review');assert.equal(a.get('entryPrompt').value,'Check the output');a.get('entryNote').value='Codex checked the report';a.get('entryCapsuleComplete').checked=true;a.get('entryOutcome').value='Every row is accounted for';a.submit('entryForm');
  assert.equal(a.state().entries[0].capsuleId,id);assert.match(a.get('capsuleList').innerHTML,/Every row is accounted for/);assert.doesNotMatch(a.get('capsuleHome').innerHTML,/<strong>Finish the report/);assert.match(a.get('journalList').innerHTML,/Next action: Finish the report/);
});
test('correcting a capsule completion returns its next action to Today',()=>{
  const a=app(),id=saveCapsule(a);a.click('complete-capsule',{id});a.get('entryNote').value='A first attempt';a.get('entryCapsuleComplete').checked=true;a.submit('entryForm');const eid=a.state().entries[0].id;a.click('edit-entry',{id:eid});assert.equal(a.get('entryCapsuleComplete').checked,true);a.get('entryCapsuleComplete').checked=false;a.submit('entryForm');assert.match(a.get('capsuleHome').innerHTML,/Finish the report/);assert.equal(a.state().entries[0].capsuleComplete,false);
});
test('capsules can be put aside and restored, and unsafe references preserve the open form',()=>{
  const a=app(),id=saveCapsule(a);a.click('archive-capsule',{id});assert.equal(a.state().personal.capsules[0].archived,true);a.click('archive-capsule',{id});assert.equal(a.state().personal.capsules[0].archived,false);a.click('new-capsule');a.get('capsuleAction').value='Unsafe';a.get('capsuleReference').value='javascript:alert(1)';a.submit('capsuleForm');assert.equal(a.state().personal.capsules.length,1);assert.match(a.get('capsuleError').textContent,/http/);
});
test('mission packs accept once and stamps require useful linked work in the matching category',()=>{
  const a=app();a.click('accept-pack',{id:'detective'});a.click('accept-pack',{id:'detective'});assert.equal(a.state().personal.packs.length,1);assert.equal(a.get('xpTotal').textContent,'0 XP');a.click('pack-task',{id:'detective',task:'trace'});assert.equal(a.get('entryCategory').value,'Debug');a.get('entryNote').value='Traced the failure';a.submit('entryForm');assert.match(a.get('packList').innerHTML,/0 \/ 3 useful/);const eid=a.state().entries[0].id;a.click('edit-entry',{id:eid});a.get('entryUseful').checked=true;a.submit('entryForm');assert.match(a.get('packList').innerHTML,/1 \/ 3 useful/);a.click('edit-entry',{id:eid});a.get('entryCategory').value='Build';a.submit('entryForm');assert.match(a.get('packList').innerHTML,/0 \/ 3 useful/);
});
test('prompt lab versions copy without logging and actual uses keep the exact chosen prompt',()=>{
  const a=app(),x=saveExperiment(a);assert.equal(a.get('xpTotal').textContent,'0 XP');a.click('add-version',{id:x.id});a.get('experimentPrompt').value='Check boundary inputs explicitly';a.submit('experimentForm');const versions=a.state().personal.experiments[0].versions;assert.equal(versions.length,2);assert.equal(versions[0].prompt,'Review this function');a.click('copy-version',{id:x.id,version:versions[1].id});assert.equal(a.state().entries.length,0);a.click('log-version',{id:x.id,version:versions[0].id});assert.equal(a.get('entryPrompt').value,'Review this function');a.get('entryNote').value='Reviewed the parser';a.submit('entryForm');assert.equal(a.state().entries[0].experimentVersion,versions[0].id);a.click('experiment-detail',{id:x.id});assert.match(a.get('experimentVersions').innerHTML,/1 actual uses/);
});
test('prompt observations remain distinct from actual-use counts',()=>{
  const a=app(),x=saveExperiment(a),v=x.versions[0];a.click('observe-version',{id:x.id,version:v.id});a.get('versionResult').value='The instructions are clearer';a.get('versionVerdict').value='Keep this version';a.submit('versionForm');assert.equal(a.state().personal.experiments[0].versions[0].verdict,'Keep this version');assert.match(a.get('experimentVersions').innerHTML,/0 actual uses/);assert.equal(a.state().entries.length,0);
});
test('a saved workflow starts an experiment and version use also records actual workflow reuse',()=>{
  const a=app();a.click('new-workflow');a.get('workflowName').value='Review parser';a.get('workflowPrompt').value='Check every boundary';a.submit('workflowForm');const w=a.state().workflows[0];a.click('experiment-workflow',{id:w.id});assert.equal(a.get('experimentPrompt').value,w.prompt);a.submit('experimentForm');const x=a.state().personal.experiments[0];a.click('log-version',{id:x.id,version:x.versions[0].id});a.get('entryNote').value='Checked a parser boundary';a.submit('entryForm');assert.equal(a.state().entries[0].workflowId,w.id);assert.equal(a.state().entries[0].experimentId,x.id);
});
test('personal records show the source work and reset after deletion',()=>{
  const a=app();a.click('record-detail',{id:'streak'});assert.match(a.get('recordProof').textContent,/0 consecutive/);log(a,'Fixed the parser');a.click('record-detail',{id:'streak'});assert.match(a.get('recordEvidence').innerHTML,/Fixed the parser/);a.click('delete-entry',{id:a.state().entries[0].id});a.click('record-detail',{id:'streak'});assert.match(a.get('recordProof').textContent,/0 consecutive/);
});
test('personal gifts stay wrapped until earned and claiming does not add points',()=>{
  const a=app(),id=saveGift(a);a.click('claim-gift',{id});assert.equal(a.state().personal.rewards[0].claimedAt,null);log(a);const xp=a.get('xpTotal').textContent;assert.match(a.get('giftList').innerHTML,/Unwrapped/);a.click('claim-gift',{id});assert.ok(a.state().personal.rewards[0].claimedAt);assert.equal(a.get('xpTotal').textContent,xp);a.click('delete-entry',{id:a.state().entries[0].id});assert.match(a.get('giftList').innerHTML,/milestone changed after an edit/);
});
test('personal rewards can be removed through confirmation',()=>{
  const a=app(),id=saveGift(a);a.click('delete-gift',{id});assert.equal(a.state().personal.rewards.length,1);a.get('confirmButton').emit('click');assert.equal(a.state().personal.rewards.length,0);
});
test('locked decorations cannot be placed and earned decorations survive reload and correction',()=>{
  const a=app();a.click('decorate');a.get('decorSlot').value='wall';a.click('place-decor',{id:'sprout'});assert.equal(a.state(),null);log(a);a.click('place-decor',{id:'sprout'});assert.equal(a.state().personal.decor.wall,'sprout');assert.match(a.get('workshopDecor').innerHTML,/placed-decor wall/);const reloaded=app({saved:a.store.get('codingScore.v1')});assert.match(reloaded.get('workshopDecor').innerHTML,/placed-decor wall/);a.click('delete-entry',{id:a.state().entries[0].id});assert.equal(a.state().personal.decor.wall,'sprout');assert.equal(a.get('workshopDecor').innerHTML,'');
});
test('new personal content is escaped in every generated card and dialog',()=>{
  const a=app();a.click('new-capsule');a.get('capsuleAction').value='<img src=x onerror=bad()>';a.submit('capsuleForm');assert.match(a.get('capsuleHome').innerHTML,/&lt;img/);assert.doesNotMatch(a.get('capsuleList').innerHTML,/<img/);a.click('new-experiment');a.get('experimentName').value='<img src=x>';a.get('experimentPrompt').value='<script>bad()</script>';a.submit('experimentForm');assert.match(a.get('experimentList').innerHTML,/&lt;img/);assert.match(a.get('experimentVersions').innerHTML,/&lt;script/);a.click('new-gift');a.get('giftName').value='<img src=x>';a.submit('giftForm');assert.match(a.get('giftList').innerHTML,/&lt;img/);
});
test('JSON backup includes personal features and clear removes them all',()=>{
  const a=app();saveCapsule(a);saveExperiment(a);saveGift(a);a.click('choose-companion',{id:'bolt'});a.click('accept-pack',{id:'docs'});a.click('export');assert.match(a.downloads.at(-1),/CodingScore/);const b=app({saved:a.store.get('codingScore.v1')});assert.equal(b.state().personal.capsules.length,1);assert.equal(b.state().personal.experiments.length,1);assert.equal(b.state().personal.rewards.length,1);assert.equal(b.state().personal.packs.length,1);b.click('clear-data');b.get('confirmButton').emit('click');assert.equal(b.state().personal.capsules.length,0);assert.equal(b.state().personal.experiments.length,0);assert.equal(b.state().personal.rewards.length,0);assert.equal(b.state().personal.companion,'orbit');
});
test('all three mission stamps earn a patch and unwrap a linked pack reward',()=>{
  const a=app();a.click('accept-pack',{id:'docs'});a.click('new-gift');a.get('giftName').value='A good book';a.get('giftKind').value='pack';a.change('giftKind');a.get('giftSource').value='docs';a.submit('giftForm');
  for(const task of ['understand','explain','review']){a.click('pack-task',{id:'docs',task});a.get('entryNote').value='Used Codex on this real task';a.get('entryUseful').checked=true;a.submit('entryForm');}
  assert.match(a.get('packList').innerHTML,/✓ Patch earned/);assert.match(a.get('giftList').innerHTML,/Unwrapped/);a.click('delete-entry',{id:a.state().entries[0].id});assert.doesNotMatch(a.get('giftList').innerHTML,/Unwrapped/);
});
test('expanded import previews personal collections and restores links only after confirmation',async()=>{
  const source=app(),id=saveCapsule(source);saveExperiment(source);saveGift(source);source.click('complete-capsule',{id});source.get('entryNote').value='Finished the report';source.get('entryCapsuleComplete').checked=true;source.submit('entryForm');const saved=source.store.get('codingScore.v1'),a=app();
  a.get('backupFile').files=[{size:saved.length,text:async()=>saved}];await a.get('backupFile').listeners.change[0]({target:a.get('backupFile')});assert.equal(a.state(),null);assert.match(a.get('confirmText').textContent,/1 capsules, 1 experiments, and 1 personal rewards/);a.get('confirmButton').emit('click');assert.equal(a.state().entries[0].capsuleId,id);assert.match(a.get('capsuleList').innerHTML,/Finished the report/);
});
test('earned decoration and frame choices retain their focus after redraw',()=>{
  const a=app();for(const date of ['2026-11-02','2026-11-03','2026-11-04'])log(a,'A real use',{entryDate:date,entryTime:''});a.click('decorate');a.click('frame',{id:'peach'});assert.equal(a.active().id,'frame-choice-peach');a.click('place-decor',{id:'poster'});assert.equal(a.active().id,'decor-choice-poster');assert.equal(a.state().personal.decor.wall,'poster');
});
test('section anchors open Explore while the workshop lamp returns to visible Today ideas',()=>{
  const a=app();assert.equal(a.get('main').classList.contains('view-today'),true);a.anchor('achievements');assert.equal(a.get('main').classList.contains('view-explore'),true);a.click('workshop-open',{id:'lamp'});assert.equal(a.get('main').classList.contains('view-today'),true);assert.equal(a.get('dailyIdeas').open,true);a.anchor('lab');assert.equal(a.get('main').classList.contains('view-explore'),true);a.anchor('today');assert.equal(a.get('main').classList.contains('view-today'),true);
});
