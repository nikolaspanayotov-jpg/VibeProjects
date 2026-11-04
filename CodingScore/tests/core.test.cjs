const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const script = html.match(/<script>([\s\S]+)<\/script>/)[1].split('/* UI */')[0];
const context = vm.createContext({Date,URL,Intl});
vm.runInContext(script,context);
const core = vm.runInContext('Core',context);
const TODAY = core.localDate();
let sequence = 0;
function entry(date,extra={}) {
  const createdAt=new Date().toISOString();
  return {id:`e-${++sequence}`,localDate:date,category:'Build',note:'Used Codex to understand a real work task.',xp:10,useful:true,outcome:'A useful result',createdAt,updatedAt:createdAt,occurredAt:null,minutes:null,reference:'',missionId:null,...extra};
}
const stateWith = entries => ({...core.blank(),entries});

test('local dates use calendar arithmetic across month, leap-year, and year boundaries',()=>{
  assert.equal(core.addDays('2024-02-28',1),'2024-02-29');
  assert.equal(core.addDays('2025-02-28',1),'2025-03-01');
  assert.equal(core.addDays('2025-12-31',1),'2026-01-01');
  assert.equal(core.addDays('2026-01-01',-1),'2025-12-31');
  assert.equal(core.parseDate('2025-02-29'),null);
  assert.equal(core.parseDate('2026-13-01'),null);
  assert.equal(core.parseDate('2026-2-01'),null);
  assert.equal(core.localDate(new Date(2026,0,1,0,5)),'2026-01-01');
});
test('day arithmetic crosses both DST transitions without skipping or duplicating dates',()=>{
  for(const start of ['2026-03-07','2026-10-31']){
    const dates=Array.from({length:5},(_,i)=>core.addDays(start,i));
    assert.equal(new Set(dates).size,5);
    dates.slice(1).forEach((d,i)=>assert.equal(core.addDays(d,-1),dates[i]));
  }
});
test('the documented score examples produce 40, 50, and 85 XP',()=>{
  const state=core.blank(),start=core.addDays(TODAY,-6);
  state.entries.push(entry(start));state.dailyNotes[start]={learning:'A lesson',nextTask:'A next task'};
  assert.equal(core.calculate(state).scores.get(start).total,40);
  const second=core.addDays(start,1);state.entries.push(entry(second),entry(second));state.dailyNotes[second]={learning:'A lesson',nextTask:''};
  assert.equal(core.calculate(state).scores.get(second).total,50);
  for(let i=2;i<7;i++){const d=core.addDays(start,i);state.entries.push(entry(d),entry(d),entry(d));state.dailyNotes[d]={learning:'A lesson',nextTask:'A next task'};}
  assert.equal(core.calculate(state).scores.get(TODAY).total,85);
});
test('multiple same-day entries cap work XP and award daily/learning/streak bonuses once',()=>{
  const state=stateWith(Array.from({length:10},()=>entry(TODAY)));
  state.dailyNotes[TODAY]={learning:'A lesson',nextTask:'A task'};
  const score=core.calculate(state).scores.get(TODAY);
  assert.equal(score.base,20);assert.equal(score.work,30);assert.equal(score.streak,0);assert.equal(score.learning,5);assert.equal(score.next,5);assert.equal(score.total,60);
  const minutes=state.entries.map(e=>({...e,minutes:1440}));assert.equal(core.calculate({...state,entries:minutes}).total,60);
});
test('yesterday keeps the current run open; a missed day breaks it while preserving the best',()=>{
  const dates=[-5,-4,-3,-1].map(n=>core.addDays(TODAY,n));
  const state=stateWith(dates.map(d=>entry(d))),stats=core.calculate(state);
  assert.equal(stats.current,1);assert.equal(stats.best,3);assert.equal(stats.scores.get(dates[3]).streak,0);
  state.entries=state.entries.filter(e=>e.localDate!==dates[3]);assert.equal(core.calculate(state).current,0);assert.equal(core.calculate(state).best,3);
});
test('historical additions and deletions recalculate later streak XP and badges',()=>{
  const first=core.addDays(TODAY,-2),middle=core.addDays(TODAY,-1),state=stateWith([entry(first),entry(TODAY)]);
  assert.equal(core.calculate(state).scores.get(TODAY).streak,0);
  state.entries.push(entry(middle));assert.equal(core.calculate(state).scores.get(TODAY).streak,10);
  assert.equal(core.badges(state).find(b=>b.id==='streak3').earned,true);
  state.entries=state.entries.filter(e=>e.localDate!==middle);assert.equal(core.badges(state).find(b=>b.id==='streak3').earned,false);
  assert.equal(core.calculate(state).scores.get(TODAY).streak,0);
});
test('notes, readings, and offline missions cannot create active days or XP',()=>{
  const state=core.blank();state.dailyNotes[TODAY]={learning:'Offline preparation',nextTask:'Tomorrow'};
  state.entries.push(entry(TODAY,{note:'   '}));
  assert.equal(core.calculate(state).total,0);assert.equal(core.calculate(state).activeDays,0);
});
test('levels preserve thresholds and continue after 3000 XP',()=>{
  for(const [xp,number] of [[0,1],[99,1],[100,2],[300,3],[700,4],[1500,5],[3000,6],[3999,6],[4000,7],[5000,8]]){
    const level=core.level(xp);assert.equal(level.number,number);assert.ok(level.start<=xp&&level.end>xp);
  }
});
test('campaigns use exact half-open timestamps, distinct local dates, and no attribution for unknown time',()=>{
  const c={id:'c',startAt:'2025-01-01T12:00:00Z',endAt:'2025-01-08T12:00:00Z',review:''};
  const state=stateWith([
    entry('2025-01-01',{occurredAt:'2025-01-01T11:59:59Z'}),
    entry('2025-01-01',{occurredAt:c.startAt}),entry('2025-01-01',{occurredAt:'2025-01-01T18:00:00Z'}),
    entry('2025-01-02',{occurredAt:null}),entry('2025-01-03',{occurredAt:'2025-01-03T12:00:00Z',category:'Review'}),
    entry('2025-01-08',{occurredAt:c.endAt})
  ]);
  const p=core.campaignProgress(state,c);assert.equal(p.days,2);assert.equal(p.categories,2);assert.equal(p.entries.length,3);
});
test('a seven-day period crossing eight local date labels caps challenge progress at seven',()=>{
  const c={startAt:'2025-01-01T12:00:00Z',endAt:'2025-01-08T12:00:00Z'};
  const state=stateWith(Array.from({length:8},(_,i)=>entry(`2025-01-0${i+1}`,{occurredAt:`2025-01-0${i+1}T${i===7?'11':'13'}:00:00Z`})));
  assert.equal(core.campaignProgress(state,c).days,7);
});
test('quota expiry never refills either window; weekly zero remains independently exhausted',()=>{
  const state=core.blank(),now=Date.now();
  const short={id:'s',kind:'short',remaining:20,observedAt:new Date(now-10000).toISOString(),resetAt:new Date(now-1000).toISOString()};
  const weekly={id:'w',kind:'weekly',remaining:0,observedAt:new Date(now-9000).toISOString(),resetAt:new Date(now+86400000).toISOString()};
  state.observations=[short,weekly];assert.equal(core.quotaStatus(null,now),'unknown');assert.equal(core.quotaStatus(short,now),'expired');assert.equal(short.remaining,20);assert.equal(core.quotaStatus(weekly,now),'recharge');assert.equal(core.latestObservation(state,'weekly').id,'w');
});
test('mission stamps require one real, timed entry inside their window and are not duplicated',()=>{
  const m={id:'m',title:'A task',startAt:'2025-01-01T12:00:20Z',endAt:'2025-01-01T17:00:00Z'},state=core.blank();
  state.missions=[m];state.entries=[entry('2025-01-01',{missionId:'m',occurredAt:null})];assert.equal(core.missionEntry(state,m),undefined);
  state.entries[0].occurredAt=m.endAt;assert.equal(core.missionEntry(state,m),undefined);
  state.entries[0].occurredAt=m.startAt;assert.equal(core.missionEntry(state,m).id,state.entries[0].id);
  state.entries.push(entry('2025-01-01',{missionId:'m',occurredAt:m.startAt}));assert.equal(state.missions.filter(x=>core.missionEntry(state,x)).length,1);
});
test('backup validation round trips all source records and rejects invalid data before replacement',()=>{
  const state=stateWith([entry(TODAY)]);assert.equal(core.validate(JSON.parse(JSON.stringify(state))).entries[0].note,state.entries[0].note);
  for(const mutate of [s=>s.version=2,s=>s.entries[0].xp=11,s=>s.entries[0].note='',s=>s.entries[0].category='Unknown',s=>s.entries[0].reference='javascript:alert(1)',s=>s.entries.push({...s.entries[0]}),s=>s.entries[0].localDate=core.addDays(TODAY,1),s=>s.settings.weeklyGoal=0,s=>s.dailyNotes.bad={learning:'',nextTask:''},s=>s.entries[0].missionId='missing']){
    const bad=JSON.parse(JSON.stringify(state));mutate(bad);assert.throws(()=>core.validate(bad));
  }
  assert.equal(state.entries.length,1);assert.equal(state.entries[0].xp,10);
});
test('badge results derive from useful outcomes and actual category coverage',()=>{
  const state=stateWith(core.CATEGORIES.map(category=>entry(TODAY,{category,useful:false})));
  assert.equal(core.badges(state).find(b=>b.id==='variety').earned,true);
  assert.equal(core.badges(state).find(b=>b.id==='automation').earned,false);
  state.entries.find(e=>e.category==='Automate').useful=true;assert.equal(core.badges(state).find(b=>b.id==='automation').earned,true);
});
test('travel preserves the original local date and XP of an already recorded use',()=>{
  const originalDate=TODAY,deviceYesterday=core.addDays(TODAY,-1),past=new Date(Date.now()-1000).toISOString();
  const state=stateWith([entry(originalDate,{occurredAt:past})]);state.dailyNotes[originalDate]={learning:'A real lesson',nextTask:''};
  const restored=core.validate(state,deviceYesterday);assert.equal(restored.entries[0].localDate,originalDate);assert.equal(core.calculate(restored,deviceYesterday).total,35);
});
