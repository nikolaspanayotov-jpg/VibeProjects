// Execute the real inline script. Browser-only APIs below are explicitly modelled.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';

const dependency = process.env.BUDGET26_LINKEDOM_PATH;
const {parseHTML} = await import(dependency ? pathToFileURL(dependency).href : 'linkedom');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html = fs.readFileSync(path.join(root,'index.html'),'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const {window:domWindow,document} = parseHTML(html);
const window={document,HTMLElement:domWindow.HTMLElement,HTMLInputElement:domWindow.HTMLInputElement,HTMLSelectElement:domWindow.HTMLSelectElement,Event:domWindow.Event,
  addEventListener:(...args)=>domWindow.addEventListener(...args),dispatchEvent:(...args)=>domWindow.dispatchEvent(...args)};
window.window=window;
let focused = document.body;
Object.defineProperty(document,'activeElement',{configurable:true,get:()=>focused});
window.HTMLElement.prototype.focus=function(){focused=this;};
window.HTMLElement.prototype.scrollIntoView=function(){};
window.HTMLInputElement.prototype.select=function(){this.selectionStart=0;this.selectionEnd=this.value.length;};
Object.defineProperty(window.HTMLElement.prototype,'clientWidth',{configurable:true,get:()=>920});
Object.defineProperty(window.HTMLElement.prototype,'open',{configurable:true,get(){return this.hasAttribute('open');},set(v){this.toggleAttribute('open',Boolean(v));}});
Object.defineProperty(window.HTMLSelectElement.prototype,'value',{configurable:true,get(){return this.querySelector('option[selected]')?.value ?? this.querySelector('option')?.value ?? '';},set(v){this.querySelectorAll('option').forEach(o=>o.toggleAttribute('selected',o.value===v));}});
window.location = new URL('https://example.test/budget26/');
window.requestAnimationFrame=callback=>callback();
window.getComputedStyle=()=>({paddingLeft:'28px',paddingRight:'28px'});
Object.defineProperty(window,'navigator',{configurable:true,value:{clipboard:{writeText:async()=>{throw new Error('Denied');}}}});
window.print=()=>{};
window.URL=URL;
vm.runInContext(script,vm.createContext(window));
const $=selector=>document.querySelector(selector);
const $$=selector=>Array.from(document.querySelectorAll(selector));
const visible=()=>$$('.policy').filter(e=>!e.hidden);
const send=(el,type)=>{
  const event=new window.Event(type,{bubbles:true,cancelable:true});
  if(type==='click') Object.defineProperty(event,'button',{value:0});
  return el.dispatchEvent(event);
};
const tick=()=>new Promise(resolve=>setTimeout(resolve,0));
const checks=[];
function pass(s){checks.push(s);console.log('PASS:',s);}
function search(text){$('#policy-query').value=text;send($('#policy-query'),'input');}
function topic(value){$('#topic-select').value=value;send($('#topic-select'),'change');}
function hash(id){window.location.hash=id;window.dispatchEvent(new window.Event('hashchange'));}
// LinkeDOM does not perform native anchor navigation or emit hashchange.
function follow(link){send(link,'click');hash(link.getAttribute('href').slice(1));}

assert.equal(visible().length,48);
assert.equal($('#forecast-panel').hidden,false);
assert.equal($('#result-count').textContent,'48 of 48 policies shown');
pass('Actual inline runtime initialises all controls, 48 policies and default forecast');

search('CASEY pension');
assert.deepEqual(visible().map(e=>e.id),['policy-state-pension']);
assert.equal($('#policy-state-pension details').open,false);
topic('business');assert.equal(visible().length,0);assert.equal($('#no-results').hidden,false);
send($('#empty-reset'),'click');assert.equal(visible().length,48);assert.equal(document.activeElement,$('#policy-query'));
pass('Multi-word closed-detail search, AND topic, empty state and reset');

for (const [name,count] of Object.entries({bills:8,tax:8,work:8,business:11,funding:8,spending:5,all:48})) {
  send($(`button[data-topic="${name}"]`),'click');
  assert.equal(visible().length,count);
  assert.equal($('#topic-select').value,name);
  assert.equal($(`button[data-topic="${name}"]`).getAttribute('aria-pressed'),'true');
}
pass('All six topic filters, result counts and selection synchronisation');

topic('business');search('unmatchableqzx');hash('policy-household-energy-payment');
assert.equal(visible().length,48);assert.equal($('#policy-query').value,'');
assert.equal($('#policy-household-energy-payment details').open,true);
assert.equal(document.activeElement,$('#policy-household-energy-payment h3'));
topic('tax');hash('policy-household-energy-payment');assert.equal(visible().length,48);
hash('economy-table');assert.equal($('#forecast-data').open,true);
hash('%E0%A4%A');hash('unknown-target');
pass('Filtered and repeated hash recovery, target focus, nested disclosure and invalid fragments');

const routeLinks=$$('.route-grid a');
assert.equal(routeLinks.length,12);
for(const link of routeLinks){
  topic('funding');search('unmatchableqzx');
  assert.equal(visible().length,0);
  follow(link);
  const target=$(link.getAttribute('href'));
  assert.equal(visible().length,48);
  assert.equal($('#policy-query').value,'');
  assert.equal($('#topic-select').value,'all');
  assert.equal(target.querySelector('details').open,true);
  assert.equal(document.activeElement,target.querySelector('h3'));
}
pass('All 12 audience-route links reveal filtered policies, open their details and focus their headings');

$('#policy-business-mileage details').open=false;
search('£6,200');
assert.deepEqual(visible().map(e=>e.id),['policy-business-mileage']);
assert.equal($('#policy-business-mileage details').open,false);
assert.ok(!$('#policy-cash-isa .policy-summary').textContent.includes('£20,000'));
search('£20,000');
assert.ok(visible().includes($('#policy-cash-isa')));
assert.equal($$('#policy-cash-isa .policy-comparison dd')[0].textContent,'£20,000');
for(const id of ['example-business-mileage','example-lifetime-isa']){
  const example=$('#'+id),article=example.closest('.policy');
  article.querySelector('details').open=false;topic('spending');search('unmatchableqzx');
  hash(id);
  assert.equal(article.hidden,false);
  assert.equal(article.querySelector('details').open,true);
  assert.equal(document.activeElement,example);
}
pass('Search indexes comparison values and closed worked examples; example fragments recover filters and disclosures');

assert.equal($('#glossary-return').hidden,true);
const termLinks=$$('.term-link');
assert.equal(termLinks.length,6);
for(const link of termLinks){
  hash(link.id);
  follow(link);
  const definition=$(link.getAttribute('href'));
  assert.equal(document.activeElement,definition);
  assert.equal($('#glossary-return').hidden,false);
  const article=link.closest('.policy');
  if(article){
    article.querySelector('details').open=false;
    topic('funding');search('unmatchableqzx');
  }
  send($('#glossary-return'),'click');
  window.dispatchEvent(new window.Event('hashchange'));
  assert.equal(window.location.hash,'#'+link.id);
  assert.equal(document.activeElement,link);
  if(article){
    assert.equal(article.hidden,false);
    assert.equal(article.querySelector('details').open,true);
    assert.equal($('#policy-query').value,'');
    assert.equal($('#topic-select').value,'all');
  }
  send($('#glossary-return'),'click');
  assert.equal(document.activeElement,link);
}
pass('All six glossary links focus definitions and return to the originating text, recovering closed or filtered policies');

for (const key of ['gdp','cpi','unemployment','borrowing','borrowing-share','debt']) {
  $('#forecast-metric').value=key;send($('#forecast-metric'),'change');
  assert.equal($$('#forecast-chart circle').length,6);
  const tableValues=$$(`tr[data-metric="${key}"] td`).map(e=>e.textContent);
  const labels=$$('#forecast-chart text').slice(5).filter((_,i)=>i%2===0).map(e=>e.textContent);
  assert.deepEqual(labels,tableValues);
  const fiscal=['borrowing','borrowing-share','debt'].includes(key);
  assert.ok($('#chart-desc').textContent.includes(fiscal?'financial years':'calendar years'));
}
pass('Every chart reads six exact values from its HTML table and uses the right year type');

const first=$('#policy-household-energy-payment');send(first.querySelector('.copy-link'),'click');await tick();
const fallback=first.querySelector('.copy-fallback');
assert.equal(fallback.hidden,false);
assert.ok(fallback.querySelector('input').value.endsWith('#policy-household-energy-payment'));
assert.equal(fallback.querySelector('input').selectionEnd,fallback.querySelector('input').value.length);
let copied='';window.navigator.clipboard.writeText=async value=>{copied=value;};
for (const article of $$('.policy')) {
  send(article.querySelector('.copy-link'),'click');await tick();
  assert.ok(copied.endsWith('#'+article.id));
  assert.ok($('#copy-status').textContent.includes('Link copied for '+article.querySelector('h3').textContent));
}
assert.equal(fallback.hidden,true);
pass('Clipboard denial fallback, recovery and correct URL/feedback for all 48 copy buttons');

search('ISA');topic('tax');$('#policy-cash-isa details').open=true;
const states=$$('details').map(e=>e.open),count=visible().length;
window.dispatchEvent(new window.Event('beforeprint'));
assert.equal(visible().length,48);assert.ok($$('details').every(e=>e.open));
window.dispatchEvent(new window.Event('afterprint'));
assert.equal($('#policy-query').value,'ISA');assert.equal($('#topic-select').value,'tax');
assert.equal(visible().length,count);assert.deepEqual($$('details').map(e=>e.open),states);
window.print=()=>{throw new Error('Blocked');};send($('#print-guide'),'click');
assert.equal($('#print-status').hidden,false);assert.equal(visible().length,count);
assert.deepEqual($$('details').map(e=>e.open),states);
pass('Print reveals everything, restores exact state and recovers from print failure');

$('#contents-menu').open=true;
const keyEvent=new window.Event('keydown');Object.defineProperty(keyEvent,'key',{value:'Escape'});document.dispatchEvent(keyEvent);
assert.equal($('#contents-menu').open,false);
assert.equal(document.activeElement,$('#contents-menu summary'));
pass('Mobile Contents Escape closes and returns focus');

console.log(`All ${checks.length} modelled-DOM scenarios passed. Layout, native controls, clipboard permissions and screenshots require browser verification.`);
