// Fast interaction regression check; this does not verify browser layout.
import {parseHTML} from 'linkedom';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const file=fileURLToPath(new URL('../index.html',import.meta.url));
const html=fs.readFileSync(file,'utf8');
const {document, window:domWindow}=parseHTML(html);
let focused='',scrolled=0,printed=false,focusCount=0;
domWindow.HTMLElement.prototype.focus=function(){focused=this.id;focusCount++;};
domWindow.HTMLElement.prototype.scrollIntoView=function(){scrolled++;};
const window={matchMedia:()=>({matches:true}),print(){printed=true}};
const navigator={clipboard:{async writeText(text){navigator.copied=text}}};
const $=id=>document.getElementById(id);
const select=(id,value)=>{for(const option of $(id).querySelectorAll('option'))option.removeAttribute('selected');$(id).querySelector('option[value="'+value+'"]').setAttribute('selected','');$(id).onchange()};
const click=id=>{assert(!$(id).disabled,`${id} unexpectedly disabled`);assert(!$(id).hidden,`${id} unexpectedly hidden`);$(id).click()};
assert($('storyLab').hidden);assert($('quizPanel').hidden);assert($('copyActions').hidden);assert(!$('interactiveNotice').hidden);
for(const sel of document.querySelectorAll('select'))sel.querySelector('option').selected=true;
vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],{document,window,navigator});
assert(!$('storyLab').hidden);assert(!$('quizPanel').hidden);assert(!$('copyActions').hidden);assert($('interactiveNotice').hidden);
for(const story of ['oom','stale']){
 click(story);assert($('back').disabled);assert.equal($(story).getAttribute('aria-pressed'),'true');
 const other=story==='oom'?'stale':'oom';assert.equal($(other).getAttribute('aria-pressed'),'false');
 for(let step=1;step<=3;step++){let before=$('workspace').innerHTML;click('next');assert.notEqual($('workspace').innerHTML,before);assert.match($('counter').textContent,new RegExp(`STEP ${step+1} OF 4`));}
 assert($('next').hidden);assert.equal(focused,'stepTitle');assert.match($('outcome').className,/danger/);
 click('back');assert(!$('next').hidden);assert($('compare').hidden);click('next');click('patch');
 assert.equal($('badge').textContent,'Repaired PHP');
 for(let i=0;i<3;i++)click('next');assert.match($('outcome').className,/safe/);
 assert.match($('workspace').textContent,story==='oom'?/No invalid cleanup/:/Fresh, valid state/);
 click('patch');assert.equal($('badge').textContent,'Original PHP');click('next');click('reset');assert.match($('counter').textContent,/STEP 1 OF 4/);
}
assert(scrolled>0);
for(const [v,t] of Object.entries({visitor:'server operator',owner:'hosting provider',admin:'Inventory, update'})){select('role',v);assert($('roleResult').textContent.includes(t))}
for(const [v,t] of Object.entries({'8.5':'8.5.12','8.4':'8.4.27','8.3':'8.3.36','8.2':'8.2.35'})){select('branch',v);for(const level of ['before','fixed']){select('level',level);assert($('versionResult').textContent.includes(t));assert($('versionResult').textContent.includes(level==='before'?'need the repair':'Verify deployment'))}}
for(const v of ['old','unknown']){select('branch',v);assert($('level').disabled)}select('branch','8.5');assert(!$('level').disabled);
for(const answers of [[0,0,0],[1,1,1],[2,2,2],[1,0,2]]){let score=0;assert($('quizNext').disabled);for(const [i,a] of answers.entries()){if(a===[1,0,2][i])score++;$('answers').children[a].click();assert([...$('answers').children].every(e=>e.disabled));assert($('feedback').textContent.length>40);click('quizNext');assert.equal(focused,'question')};assert($('question').textContent.includes(`${score} out of 3`));assert($('quizNext').hidden);const beforeReset=focusCount;click('quizReset');assert.equal(focusCount-beforeReset,1);assert.equal($('answers').children.length,3);assert.equal($('progress').value,0)}
await $('copy').onclick();assert.equal(navigator.copied,$('explanation').textContent);assert.equal($('copyStatus').textContent,'Explanation copied.');navigator.clipboard.writeText=async()=>{throw Error('Denied')};await $('copy').onclick();assert.match($('copyStatus').textContent,/Select the explanation text/);click('print');assert(printed);
for(const a of document.querySelectorAll('a[href^="#"]')){const id=a.getAttribute('href').slice(1);if(id)assert($(id),`Missing anchor ${id}`)}
const ids=[...document.querySelectorAll('[id]')].map(el=>el.id);assert.equal(new Set(ids).size,ids.length);
console.log('PASS: parsed HTML with LinkeDOM; every story/replay/back/restart, all audience/version choices, all nine answers, scoring/reset, copy success/denial, print dispatch, anchors and JS-disabled initial state. Focus and scroll APIs instrumented; no layout or visual browser claims.');
