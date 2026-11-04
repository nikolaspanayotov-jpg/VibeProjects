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

function app({saved=null,denyStorage=false}={}) {
  const elements=new Map(),store=new Map(),documentHandlers={},downloads=[];
  if(saved!==null)store.set('codingScore.v1',saved);
  let clock=Date.parse('2026-11-04T12:00:30Z'),document;
  class Clock extends Date {constructor(...args){super(...(args.length?args:[clock]));}static now(){return clock;}}
  class Element {
    constructor(tag='',attributes=''){
      this.tagName=tag.toUpperCase();this.id=attr(attributes,'id');this.value=attr(attributes,'value');this.defaultValue=this.value;this.checked=false;this.hidden=false;this.open=false;this.dataset={};this.style={};this.attributes={};this.listeners={};this._html='';this.textContent='';this.classList={add(){},remove(){},toggle(){}};
      for(const match of attributes.matchAll(/data-([\w-]+)="([^"]*)"/g))this.dataset[match[1].replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=match[2];
    }
    set innerHTML(value){this._html=value;parse(value);}
    get innerHTML(){return this._html;}
    setAttribute(name,value){this.attributes[name]=String(value);}
    removeAttribute(name){delete this.attributes[name];}
    addEventListener(name,handler){(this.listeners[name]??=[]).push(handler);}
    emit(name,event={}){for(const h of this.listeners[name]||[])h({target:this,preventDefault(){},...event});}
    querySelector(){return this.span??=new Element('span');}
    closest(selector){if(selector==='[data-action]'&&this.dataset.action)return this;if(selector==='[data-close]')return null;if(selector==='dialog'&&this.tagName==='DIALOG')return this;return null;}
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
    createElement:tag=>new Element(tag)};
  document.activeElement=new Element('body');
  const context=vm.createContext({document,Date:Clock,URL,Blob,Intl,console,crypto:{randomUUID:()=>`id-${Math.random().toString(36).slice(2)}`},navigator:{clipboard:{writeText:async()=>{}}},setTimeout:fn=>{fn();return 1;},setInterval:()=>1,localStorage:{getItem:key=>{if(denyStorage)throw Error('denied');return store.get(key)??null;},setItem:(key,value)=>{if(denyStorage)throw Error('denied');store.set(key,value);}}});
  vm.runInContext(script,context);
  return {get:id=>elements.get(id),state:()=>JSON.parse(store.get('codingScore.v1')||'null'),store,downloads,
    click(action,data={}){const target=new Element('button');target.dataset={action,...data};for(const handler of documentHandlers.click||[])handler({target});},
    submit:id=>elements.get(id).emit('submit'),change:id=>elements.get(id).emit('change'),
    advance:ms=>{clock+=ms;},blank:()=>vm.runInContext('Core.blank()',context)};
}
function log(a,note='Codex helped me fix a script.',extra={}){
  a.click('log');a.get('entryNote').value=note;
  for(const [id,value] of Object.entries(extra)){if(id==='entryUseful')a.get(id).checked=value;else a.get(id).value=value;}
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
