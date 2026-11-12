const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),c={window:{},structuredClone};vm.createContext(c);vm.runInContext(fs.readFileSync(path.join(root,'multiple-choice-data.js'),'utf8'),c);for(let i=1;i<=4;i++)vm.runInContext(fs.readFileSync(path.join(root,'test-packs/additional-'+i+'.js'),'utf8'),c);for(let i=1;i<=4;i++)vm.runInContext(fs.readFileSync(path.join(root,'test-packs/revised-'+i+'.js'),'utf8'),c);vm.runInContext(fs.readFileSync(path.join(root,'multiple-choice.js'),'utf8'),c);const M=c.window.L4_TESTS,D=c.window.L4_TEST_DATA,plain=x=>JSON.parse(JSON.stringify(x));
assert.equal(D.tests.length,50);assert.equal(D.tests.flatMap(t=>t.questions).length,500);assert.equal(new Set(D.tests.flatMap(t=>t.questions.map(q=>q.ksb))).size,37);assert.deepEqual(plain(M.validate(undefined)),plain(M.blank()));
const answers=t=>plain(Object.fromEntries(t.questions.map(q=>[q.id,q.options.filter(o=>o.correct).map(o=>o.id)])));
function attempt(t,id='r-core'){return {id,testId:t.id,revision:D.revision,started:1,finished:1794484800000,offset:0,date:'2026-11-12',answers:answers(t)};}
for(const [revision,tests] of Object.entries(D.editions))for(const t of tests){let a={...attempt(t),revision};assert.equal(M.score(a).total,10);for(const q of t.questions){const required=q.options.filter(o=>o.correct),wrong=q.options.filter(o=>!o.correct);assert([3,4].includes(required.length));for(const o of required){let bad=structuredClone(a);bad.answers[q.id]=bad.answers[q.id].filter(id=>id!==o.id);assert.equal(M.score(bad).total,9);}for(const o of wrong){let bad=structuredClone(a);bad.answers[q.id].push(o.id);assert.equal(M.score(bad).total,9);}let all=structuredClone(a);all.answers[q.id]=q.options.map(o=>o.id);assert.equal(M.score(all).total,9);}for(const key of Object.keys(a.answers))a.answers[key].reverse();assert.equal(M.score(a).total,10);}
const state=plain(M.blank()),t=D.tests[0];state.drafts[t.id]={id:'r-draft',revision:D.revision,index:2,started:1,answers:{[t.questions[0].id]:['A','D']}};const a=attempt(t);state.attempts[a.id]=a;assert.deepEqual(plain(M.validate(state)),state);
for(const change of [s=>s.drafts.T01.answers.bad=['A'],s=>s.drafts.T01.answers[t.questions[0].id]=['Z'],s=>s.drafts.T01.answers[t.questions[0].id]=['A','A'],s=>s.drafts.T01.index=10,s=>s.drafts.T01.revision='unknown',s=>s.attempts['r-core'].score=10,s=>s.attempts['r-core'].date='2026-02-30',s=>s.attempts['r-core'].answers[t.questions[0].id]=[],s=>s.attempts['r-core'].testId='constructor',s=>s.attempts['r-core'].offset=9999,s=>s.drafts=JSON.parse('{"__proto__":{}}'),s=>s.removed=['constructor'],s=>s.unexpected=true,s=>s.drafts.T02={id:s.drafts.T01.id,revision:D.revision,index:0,started:1,answers:{}}]){const bad=structuredClone(state);change(bad);assert.throws(()=>M.validate(bad));}
let incoming=structuredClone(state);incoming.drafts.T01.index=4;let m=M.merge(state,incoming,{});assert.equal(m.merged.drafts.T01.index,2);assert(m.conflicts.some(x=>x.key==='multiple-choice-drafts-T01'));m=M.merge(state,incoming,{'multiple-choice-drafts-T01':'import'});assert.equal(m.merged.drafts.T01.index,4);assert.deepEqual(plain(M.merge(state,M.blank(),{}).merged),state);
const gone=plain(M.blank());gone.removed=[a.id];assert.equal(M.merge(gone,state,{}).merged.attempts[a.id],undefined);
const stale=plain(M.blank());stale.drafts.T01={id:a.id,revision:D.revision,index:1,started:1,answers:{}};assert.equal(M.merge(state,stale,{'multiple-choice-drafts-T01':'import'}).merged.drafts.T01,undefined);assert.equal(M.merge(gone,stale,{}).merged.drafts.T01,undefined);
const capacity=plain(M.blank());for(let i=0;i<500;i++){const r=attempt(t,'r-cap-'+i);capacity.attempts[r.id]=r;}assert.equal(Object.keys(M.validate(capacity).attempts).length,500);capacity.attempts['r-cap-500']=attempt(t,'r-cap-500');assert.throws(()=>M.validate(capacity));
const legacy=JSON.parse(fs.readFileSync(path.join(root,'tests/multiple_choice_legacy_state.json'),'utf8'));assert.deepEqual(plain(M.validate(legacy)),legacy);assert.equal(M.score(legacy.attempts['r-legacy-result']).total,9);const allDrafts=plain(M.blank());for(const test of D.tests)allDrafts.drafts[test.id]={id:'r-draft-'+test.id,revision:D.revision,index:0,started:1,answers:{}};assert.equal(Object.keys(M.validate(allDrafts).drafts).length,50);
const exported=M.summary(state).join('\n');assert(exported.includes('10/10'));assert(exported.includes(t.questions[0].prompt));assert(exported.includes('solutions.md#ksb-k1'));

// Both immutable editions must survive validation, scoring, review and merge.
const oldRevision='2026-11-12-tests-1', oldTests=D.editions[oldRevision];
assert.equal(oldTests.length,50);assert.equal(D.revision,'2026-11-12-tests-2');
assert.deepEqual(plain(D.tests.slice(0,10)),plain(oldTests.slice(0,10)));
const oldAttempt={...attempt(oldTests[49],'r-old-50'),revision:oldRevision};
const editions=plain(M.blank());editions.attempts[oldAttempt.id]=oldAttempt;
editions.drafts.T11={id:'r-old-draft-11',revision:oldRevision,index:3,started:1,answers:answers(oldTests[10])};
assert.deepEqual(plain(M.validate(editions)),editions);assert.equal(M.score(oldAttempt).total,10);
for(const wrongRevision of [oldRevision,D.revision]){const bad=plain(M.blank());const t=wrongRevision===oldRevision?D.tests[49]:oldTests[49];const a={...attempt(t),revision:wrongRevision};bad.attempts[a.id]=a;assert.throws(()=>M.validate(bad));}
const current=plain(M.blank());current.drafts.T11={id:'r-new-draft-11',revision:D.revision,index:1,started:1,answers:answers(D.tests[10])};
assert.deepEqual(plain(M.merge(current,editions,{}).merged.drafts.T11),current.drafts.T11);
assert.deepEqual(plain(M.merge(current,editions,{'multiple-choice-drafts-T11':'import'}).merged.drafts.T11),editions.drafts.T11);
const removed=plain(M.blank());removed.removed=[oldAttempt.id,editions.drafts.T11.id];const merged=M.merge(removed,editions,{}).merged;assert.equal(merged.attempts[oldAttempt.id],undefined);assert.equal(merged.drafts.T11,undefined);
// Golden permutation pins historical display, including Markdown export letters.
const q=D.tests[10].questions[0], idOrder=(q,a)=>plain(M.optionsFor(q,a).map(o=>o.id));
const a1={id:'r-shuffle-one',revision:D.revision},a2={id:'r-shuffle-two',revision:D.revision};
assert.deepEqual(idOrder(q,a1),['F','B','C','G','H','E','A','D']);
for(const t of D.tests){const one=[],two=[];for(const q of t.questions){const original=plain(q.options);const order=idOrder(q,a1);assert.deepEqual([...order].sort(),['A','B','C','D','E','F','G','H']);assert.deepEqual(idOrder(q,structuredClone(a1)),order);assert.deepEqual(plain(q.options),original);one.push(order);two.push(idOrder(q,a2));}assert.notDeepEqual(one,two);}
for(const t of oldTests)for(const q of t.questions)assert.deepEqual(idOrder(q,{...a1,revision:oldRevision}),plain(q.options.map(o=>o.id)));
const summary=M.summary(editions).join('\n');assert(summary.includes(oldTests[49].questions[0].prompt));assert(!summary.includes(D.tests[49].questions[0].prompt));
const shuffled={...attempt(D.tests[10],a1.id)},exportState=plain(M.blank());exportState.attempts[shuffled.id]=shuffled;
const output=M.summary(exportState).join('\n');M.optionsFor(q,a1).forEach((o,i)=>assert(output.includes(String.fromCharCode(65+i)+'. '+o.text)));
console.log('1,000 edition-specific exact-set keys and every missing/extra variant; stable shuffled presentation, immutable legacy order, strict state, cross-edition validation/conflicts/tombstones and exports passed.');

