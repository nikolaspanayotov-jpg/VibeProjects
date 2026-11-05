/* Independent expected outcomes for scoring, date boundaries and source-derived rewards. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const sandbox={window:{}};vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../gamification.js'),'utf8'),sandbox);const G=sandbox.window.L4_GAME;
const plain=x=>JSON.parse(JSON.stringify(x));let seq=0;const questions=Object.fromEntries(Array.from({length:30},(_,i)=>['Q'+String(i+1).padStart(2,'0'),{answer:i%2===0}]));
function event(kind,target,date='2026-11-02',hour=9,facts={reviewed:true},window=0){return {id:'test-'+(++seq),kind,target,date,at:Date.parse(date+'T'+String(hour).padStart(2,'0')+':00:00Z'),offset:0,window,reflection:'Synthetic learning reflection.',facts};}
const game=()=>({events:[],deleted:[]});let state=game();const metric=(g=state,today='2026-11-02')=>G.metrics(g,questions,today);
state.events.push(event('recall','K8',undefined,9,{result:'help'}));assert.equal(metric().total,20);
state.events.push(event('repair','duplicate-join',undefined,13,{reviewed:true},1));assert.equal(metric().total,40);
state.events.push(event('retrieval','B5',undefined,19,{reviewed:true},2));let m=metric();assert.equal(m.total,100);assert.equal(m.counts.trios,1);assert.equal(m.counts.checkins,1);assert.equal(m.counts.quests,1);assert.equal(m.earned.quest.date,'2026-11-02');assert.equal(m.earned.trio.date,'2026-11-02');
state.events.push(event('repair','chart-scale',undefined,20,{reviewed:true},2));assert.equal(metric().total,100);assert.equal(metric().counts.blocks,4);
state.deleted.push(state.events[2].id);m=metric();assert.equal(m.total,40);assert.equal(m.counts.quests,0);assert.equal(m.earned.trio,undefined);state.deleted=[];assert.equal(metric().total,100);
// Current run survives an unfinished today, then resets after a missed date. Best and earned past milestones remain.
state=game();for(let i=0;i<7;i++)state.events.push(event('recall','K1',G.dayAdd('2026-10-20',i),9,{result:'independent'}));
m=metric(state,'2026-10-27');assert.equal(m.current,7);assert.equal(m.counts.best,7);assert.equal(m.earned.rhythm.date,'2026-10-26');m=metric(state,'2026-10-28');assert.equal(m.current,0);assert.equal(m.counts.best,7);assert.ok(m.earned.rhythm);
state.events.push(event('recall','S1','2026-10-28',9,{result:'partial'}));assert.equal(metric(state,'2026-10-28').current,1);
// Local labels use the recorded offset, including both sides of the DST fallback.
assert.deepEqual(plain(G.stamp(Date.parse('2026-10-25T00:30:00Z'),-60)),{date:'2026-10-25',minute:90});assert.deepEqual(plain(G.stamp(Date.parse('2026-10-25T01:30:00Z'),0)),{date:'2026-10-25',minute:90});assert.equal(G.stamp(Date.parse('2026-06-01T23:30:00Z'),-120).date,'2026-06-02');
assert.equal(G.windowAt(719,[720,1020]),0);assert.equal(G.windowAt(720,[720,1020]),1);assert.equal(G.windowAt(1020,[720,1020]),2);assert.equal(G.timeValue('24:00'),null);assert.equal(G.timeValue('08:30'),510);assert.equal(G.weekOf('2026-11-08'),'2026-11-02');
// Five reviewed questions support one block. Missing supporting history removes block XP.
state=game();const answers=Array.from({length:5},(_,i)=>event('quiz-answer','Q'+String(i+1).padStart(2,'0'),undefined,9,{choice:false,answeredOn:'2026-11-02',session:'set-a'}));state.events.push(...answers,event('quiz','set',undefined,10,{answerIds:answers.map(e=>e.id)}));assert.equal(metric().total,20);assert.equal(metric().counts.topics,0);state.deleted.push(answers[0].id);assert.equal(metric().total,0);
// Same-day correction is excluded; different questions corrected on later answer dates count once each.
state=game();for(let i=0;i<5;i++){const q='Q'+String(i+1).padStart(2,'0');state.events.push(event('quiz-answer',q,'2026-11-01',9,{choice:!questions[q].answer,answeredOn:'2026-11-01',session:'wrong'}),event('quiz-answer',q,'2026-11-01',10,{choice:questions[q].answer,answeredOn:'2026-11-01',session:'same-day'}));}
assert.equal(metric().counts.recoveries,0);for(let i=0;i<5;i++){const q='Q'+String(i+1).padStart(2,'0');state.events.push(event('quiz-answer',q,'2026-11-02',9,{choice:questions[q].answer,answeredOn:'2026-11-02',session:'later'}));}assert.equal(metric().counts.recoveries,5);assert.equal(metric().earned.detective.date,'2026-11-02');
// Coverage requires explicit topic practice, rather than question mappings or connection visits.
state=game();const ids=[...Array.from({length:15},(_,i)=>'K'+(i+1)),...Array.from({length:15},(_,i)=>'S'+(i+1)),...Array.from({length:7},(_,i)=>'B'+(i+1))];for(const id of ids)state.events.push(event('workshop',id));assert.equal(metric().counts.topics,37);assert.ok(metric().earned.standard);assert.equal(metric().total,20);
state.events.push(event('briefing','capacity-lead'),event('briefing','quality-technical'));assert.equal(metric().counts.audiences,0);state.events.push(event('briefing','capacity-technical'));assert.equal(metric().counts.audiences,1);
const refs=['K1','S1','B1'].map(id=>event('recall',id));state.events.push(...refs,event('challenge','mixed',undefined,10,{attemptIds:refs.map(e=>e.id)}));assert.equal(metric().counts.challenges,1);state.deleted.push(refs[0].id);assert.equal(metric().counts.challenges,0);
console.log('Passed: XP cap, trio/quest receipts, deletion recalculation, streaks, local dates/DST, windows, quiz prerequisites, later-day recovery, explicit 37-KSB coverage, audiences and mixed rehearsal.');
