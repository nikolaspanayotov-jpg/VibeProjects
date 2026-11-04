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
  for(const mutate of [s=>s.version=99,s=>s.entries[0].xp=11,s=>s.entries[0].note='',s=>s.entries[0].category='Unknown',s=>s.entries[0].reference='javascript:alert(1)',s=>s.entries.push({...s.entries[0]}),s=>s.entries[0].localDate=core.addDays(TODAY,1),s=>s.settings.weeklyGoal=0,s=>s.dailyNotes.bad={learning:'',nextTask:''},s=>s.entries[0].missionId='missing']){
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
function quest() {
  const now=new Date().toISOString();return {id:'quest',title:'Automate a report',goal:'One command produces a checked report',archived:false,createdAt:now,updatedAt:now,steps:['Investigate','Build','Test','Finish'].map((title,i)=>({id:'step'+i,title}))};
}
function workflow() {
  const now=new Date().toISOString();return {id:'workflow',title:'Review a change',category:'Review',prompt:'Review [paste code] for edge cases.',result:'Caught a boundary bug',notes:'Use before merging',favorite:true,sourceEntryId:null,createdAt:now,updatedAt:now};
}
test('v1 migration preserves existing source data and XP while adding optional collections',()=>{
  const legacy=stateWith([entry(TODAY)]);legacy.version=1;delete legacy.quests;delete legacy.workflows;delete legacy.challenges;
  const before=core.calculate(legacy).total,migrated=core.validate(JSON.parse(JSON.stringify(legacy)));
  assert.equal(migrated.version,2);assert.equal(migrated.entries[0].note,legacy.entries[0].note);assert.equal(core.calculate(migrated).total,before);
  assert.equal(migrated.entries[0].minutesSaved,null);assert.equal(migrated.quests.length,0);assert.equal(migrated.workflows.length,0);assert.equal(migrated.challenges.length,0);assert.equal(core.KEY,'codingScore.v1');
});
test('quest completion requires four distinct steps explicitly completed by actual logs',()=>{
  const q=quest(),state=stateWith([entry(TODAY,{questId:q.id,questStepId:'step0',stepComplete:false})]);state.quests=[q];
  assert.equal(core.questProgress(state,q).completed,0);
  state.entries[0].stepComplete=true;state.entries.push(entry(TODAY,{questId:q.id,questStepId:'step0',stepComplete:true}));assert.equal(core.questProgress(state,q).completed,1);
  for(let i=1;i<4;i++)state.entries.push(entry(TODAY,{questId:q.id,questStepId:'step'+i,stepComplete:true}));
  assert.equal(core.questProgress(state,q).complete,true);assert.equal(core.badges(state).find(b=>b.id==='quest').earned,true);assert.equal(core.workshop(state).find(i=>i.id==='tools').earned,true);
  state.entries=state.entries.filter(e=>e.questStepId!=='step2');assert.equal(core.questProgress(state,q).complete,false);assert.equal(core.badges(state).find(b=>b.id==='quest').earned,false);assert.equal(core.workshop(state).find(i=>i.id==='tools').earned,false);
});
test('v2 round trips payoff, prompts, quests, workflow reuse, and accepted challenges',()=>{
  const state=stateWith([entry(TODAY,{minutesSaved:0,before:'Manual rows',after:'A checked script',prompt:'Help automate this.',questId:'quest',questStepId:'step1',stepComplete:true,workflowId:'workflow'})]);state.quests=[quest()];state.workflows=[workflow()];state.challenges=[{...core.recommendations(state,TODAY)[0],createdAt:new Date().toISOString()}];
  const restored=core.validate(JSON.parse(JSON.stringify(state)));
  assert.equal(restored.entries[0].minutesSaved,0);assert.equal(restored.entries[0].prompt,'Help automate this.');assert.equal(restored.entries[0].workflowTitle,'Review a change');assert.equal(restored.entries[0].questStepId,'step1');assert.equal(restored.challenges.length,1);assert.equal(restored.workflows[0].favorite,true);
});
test('invalid new fields and orphaned quest links are rejected without normalizing away valid data',()=>{
  const good=stateWith([entry(TODAY)]);
  for(const mutate of [s=>s.entries[0].minutesSaved=-1,s=>s.entries[0].minutesSaved=1.2,s=>s.entries[0].minutesSaved=10081,s=>s.entries[0].questId='missing',s=>s.entries[0].stepComplete=true,s=>s.entries[0].workflowId='missing',s=>s.workflows=[{...workflow(),prompt:''}],s=>s.quests=[{...quest(),steps:[]}],s=>s.quests=[{...quest(),steps:Array(4).fill({id:'duplicate',title:'Step'})}],s=>s.challenges=[{...core.recommendations(s,TODAY)[0],weekStart:core.addDays(core.weekStart(TODAY),1),createdAt:new Date().toISOString()}]]){
    const bad=JSON.parse(JSON.stringify(good));mutate(bad);assert.throws(()=>core.validate(bad));
  }
});
test('workflow history survives library deletion using a title snapshot',()=>{
  const state=stateWith([entry(TODAY,{workflowId:'workflow',workflowTitle:'A saved shortcut',prompt:'The original prompt'})]);
  const restored=core.validate(state);assert.equal(restored.workflows.length,0);assert.equal(restored.entries[0].workflowId,'workflow');assert.equal(core.badges(restored).find(b=>b.id==='workflow').earned,true);assert.equal(restored.entries[0].prompt,'The original prompt');
});
test('personal recommendations choose less-used categories and remain stable during the week',()=>{
  const start=core.weekStart(TODAY),state=stateWith([entry(core.addDays(start,-1),{category:'Automate'}),entry(core.addDays(start,-2),{category:'Build'}),entry(core.addDays(start,-3),{category:'Debug'})]);
  const recommended=core.recommendations(state,TODAY);assert.equal(recommended[0].category,'Review');assert.equal(recommended[1].category,'Learn');
  state.entries.push(entry(TODAY,{category:'Review'}));assert.equal(core.recommendations(state,TODAY)[0].id,recommended[0].id);
});
test('personal challenges use local-week boundaries and distinct actual activity',()=>{
  const start=core.weekStart(TODAY),category={id:'c',weekStart:start,kind:'category',category:'Automate',target:1},variety={id:'v',weekStart:start,kind:'variety',category:null,target:3};
  const state=stateWith([entry(core.addDays(start,-1),{category:'Automate',useful:true}),entry(start,{category:'Automate',useful:false}),entry(start,{category:'Build'}),entry(start,{category:'Build'})]);
  assert.equal(core.challengeProgress(state,category).complete,false);assert.equal(core.challengeProgress(state,variety).value,2);
  state.entries.push(entry(start,{category:'Review'}),entry(start,{category:'Automate',useful:true}));assert.equal(core.challengeProgress(state,category).complete,true);assert.equal(core.challengeProgress(state,variety).complete,true);
  state.entries=state.entries.filter(e=>e.category!=='Review');assert.equal(core.challengeProgress(state,variety).complete,false);
});
test('midweek recaps compare the same elapsed weekdays instead of a full previous week',()=>{
  const monday='2026-10-26',wednesday='2026-10-28',state=core.blank();
  for(let i=0;i<3;i++)state.entries.push(entry(core.addDays(monday,i)));
  for(let i=0;i<5;i++)state.entries.push(entry(core.addDays(monday,i-7)));
  const recap=core.weeklyRecap(state,wednesday,wednesday);assert.equal(recap.current,true);assert.equal(recap.activeDays,3);assert.equal(recap.previous.activeDays,3);assert.equal(recap.daysDelta,0);assert.equal(recap.through,wednesday);
  const completed=core.weeklyRecap(state,core.addDays(monday,-7),wednesday);assert.equal(completed.current,false);assert.equal(completed.activeDays,5);
});
test('recaps distinguish missing estimates from zero and identify first-time categories and workflows',()=>{
  const start=core.weekStart(TODAY),state=stateWith([entry(core.addDays(start,-1),{category:'Build',workflowId:'old',workflowTitle:'Old workflow'}),entry(start,{category:'Automate',minutesSaved:0,workflowId:'new',workflowTitle:'New workflow'}),entry(start,{category:'Review',minutesSaved:30,outcome:'Saved half an hour'}),entry(start,{category:'Build',minutesSaved:null,workflowId:'old',workflowTitle:'Old workflow'})]);
  const recap=core.weeklyRecap(state,TODAY);assert.equal(recap.minutesSaved,30);assert.equal(recap.estimatedUses,2);assert.equal(recap.newWorkflows.length,1);assert.equal(recap.newWorkflows[0],'new');assert.equal(recap.newCategories.includes('Automate'),true);assert.equal(recap.newCategories.includes('Build'),false);assert.equal(recap.highlight.outcome,'Saved half an hour');assert.match(core.recapText(recap),/my estimate/);
  const total=core.calculate(state).total;state.entries.forEach(e=>e.minutesSaved=1000);assert.equal(core.calculate(state).total,total);
});
test('workshop grows on distinct active dates and retains cumulative items across streak gaps',()=>{
  const state=stateWith(Array.from({length:10},()=>entry(TODAY)));assert.equal(core.workshop(state).find(i=>i.id==='desk').earned,true);assert.equal(core.workshop(state).find(i=>i.id==='lamp').earned,false);
  state.entries.push(entry(core.addDays(TODAY,-3)),entry(core.addDays(TODAY,-6)));assert.equal(core.workshop(state).find(i=>i.id==='lamp').earned,true);assert.equal(core.calculate(state).current,1);assert.equal(core.workshop(state).find(i=>i.id==='trophy').earned,false);
});
test('recap export escapes user text and stays a self-contained bounded SVG',()=>{
  const state=stateWith([entry(TODAY,{outcome:'<script>alert("x")</script> & a useful result',minutesSaved:20})]),svg=core.recapSvg(core.weeklyRecap(state,TODAY));
  assert.match(svg,/width="1080" height="1350"/);assert.doesNotMatch(svg,/<script>/);assert.match(svg,/&lt;script&gt;/);assert.match(svg,/my estimate/);assert.doesNotMatch(svg,/<foreignObject|<image|<script\b/);assert.ok(svg.endsWith('</svg>'));
});
test('old quests receive a safe default emblem and every selectable emblem round trips',()=>{
  const state=core.blank();state.quests=[quest()];assert.equal(core.validate(state).quests[0].emblem,'compass');
  for(const emblem of core.EMBLEMS){state.quests[0].emblem=emblem;assert.equal(core.validate(JSON.parse(JSON.stringify(state))).quests[0].emblem,emblem);}
  state.quests[0].emblem='<img onerror=alert(1)>';assert.throws(()=>core.validate(state),/six quest emblems/);
});
test('locked quest reward reports actual partial steps rather than zero completed projects',()=>{
  const state=core.blank(),q=quest();state.quests=[q];state.entries=[0,1,2].map(i=>entry(TODAY,{questId:q.id,questStepId:'step'+i,stepComplete:true}));
  const badge=core.badges(state).find(b=>b.id==='quest');assert.equal(badge.earned,false);assert.equal(badge.progress,.75);assert.match(badge.progressText,/3 of 4/);
});
test('achievement details identify the actual first use and first completed streak dates',()=>{
  const first=core.addDays(TODAY,-4),state=stateWith(Array.from({length:5},(_,i)=>entry(core.addDays(first,i))));
  assert.equal(core.achievementDetails(state,'first').earnedOn,first);const streak=core.achievementDetails(state,'streak3');assert.equal(streak.earnedOn,core.addDays(first,2));assert.match(streak.proof,/3 consecutive local dates/);
  const locked=core.achievementDetails(state,'streak7');assert.equal(locked.earnedOn,null);assert.equal(locked.earned,false);assert.match(locked.progressText,/5 of 7/);assert.equal(core.achievementDetails(state,'unknown'),null);
});
test('result and category achievements use the first date the requirement was met',()=>{
  const first=core.addDays(TODAY,-5),state=stateWith(Array.from({length:12},(_,i)=>entry(core.addDays(first,Math.floor(i/2)),{category:core.CATEGORIES[i%6]})));
  assert.equal(core.achievementDetails(state,'wins').earnedOn,core.addDays(first,4));assert.equal(core.achievementDetails(state,'variety').earnedOn,core.addDays(first,2));
  state.entries[2].category='Automate';state.entries[2].useful=true;assert.equal(core.achievementDetails(state,'automation').earnedOn,core.addDays(first,1));
});
test('project badge date follows the last first-completed step and corrections revoke it',()=>{
  const state=core.blank(),q=quest(),first=core.addDays(TODAY,-5);state.quests=[q];state.entries=[0,1,2,3].map(i=>entry(core.addDays(first,i),{questId:q.id,questStepId:'step'+i,stepComplete:true}));state.entries.push(entry(TODAY,{questId:q.id,questStepId:'step0',stepComplete:true}));
  const earned=core.achievementDetails(state,'quest');assert.equal(earned.earnedOn,core.addDays(first,3));assert.match(earned.proof,/Automate a report/);
  state.entries=state.entries.filter(e=>e.questStepId!=='step2');assert.equal(core.achievementDetails(state,'quest').earnedOn,null);
});
test('challenge and removed-workflow details retain evidence from actual dated activity',()=>{
  const start=core.weekStart(TODAY),state=stateWith([entry(start,{category:'Automate',useful:true,workflowId:'removed',workflowTitle:'My good shortcut'})]);
  state.challenges=[{id:'challenge',title:'Try an automation',kind:'category',category:'Automate',target:1,weekStart:start,createdAt:new Date().toISOString()}];
  assert.equal(core.achievementDetails(state,'challenge').earnedOn,start);assert.match(core.achievementDetails(state,'challenge').proof,/Try an automation/);assert.match(core.achievementDetails(state,'workflow').proof,/My good shortcut/);
});
test('daily focus chooses an unfinished active project and the nearest partial reward',()=>{
  const q=quest(),other={...quest(),id:'archived',archived:true,updatedAt:new Date().toISOString()},state=core.blank();state.quests=[other,q];state.entries=[0,1,2].map(i=>entry(TODAY,{questId:q.id,questStepId:'step'+i,stepComplete:true}));
  const focus=core.dailyFocus(state);assert.equal(focus.quest.id,q.id);assert.equal(focus.nextAchievement.id,'quest');assert.equal(focus.nextAchievement.progress,.75);
  state.entries.push(entry(TODAY,{questId:q.id,questStepId:'step3',stepComplete:true}));assert.equal(core.dailyFocus(state).quest,null);
});
test('illustrations are distinct, self-contained, and reject untrusted artwork keys',()=>{
  const art=vm.runInContext('Art',context),emblems=core.EMBLEMS.map(key=>art.emblem(key)),badges=core.badges(core.blank()).map(b=>art.badge(b.id));
  assert.equal(new Set(emblems).size,6);assert.equal(new Set(badges).size,12);for(const svg of [...emblems,...badges]){assert.match(svg,/viewBox="0 0 96 96"/);assert.doesNotMatch(svg,/<script|<image|<foreignObject/);assert.ok(svg.endsWith('</svg>'));}
  assert.equal(art.emblem('<script>'),art.emblem('compass'));assert.equal(art.badge('invalid'),art.badge('first'));
});
test('a complete collection has no invented next reward and every earned badge has a real date',()=>{
  const state=core.blank(),q=quest(),start=core.addDays(TODAY,-99);state.quests=[q];
  state.entries=Array.from({length:100},(_,i)=>entry(core.addDays(start,i),{category:core.CATEGORIES[i%6],useful:true,workflowId:i===0?'old-workflow':null,workflowTitle:i===0?'A good old workflow':'',questId:i>=96?q.id:null,questStepId:i>=96?'step'+(i-96):null,stepComplete:i>=96}));
  const recent=state.entries.find(e=>e.localDate>=core.weekStart(TODAY));state.challenges=[{id:'complete-challenge',title:'A useful result this week',kind:'category',category:recent.category,target:1,weekStart:core.weekStart(TODAY),createdAt:new Date().toISOString()}];
  assert.equal(core.badges(state).every(b=>b.earned),true);assert.equal(core.dailyFocus(state).nextAchievement,null);
  for(const badge of core.badges(state))assert.ok(core.parseDate(core.achievementDetails(state,badge.id).earnedOn),badge.id);
});
test('old settings gain empty showcase pins and valid pins survive backup migration',()=>{
  const state=stateWith([entry(TODAY)]);delete state.settings.pinnedAchievements;
  assert.equal(core.validate(state).settings.pinnedAchievements.length,0);
  state.settings.pinnedAchievements=['first','wins','quest'];assert.equal(core.validate(JSON.parse(JSON.stringify(state))).settings.pinnedAchievements.join(','),'first,wins,quest');
  for(const pins of [['first','first'],['first','wins','quest','workflow'],['unknown'],'first']){const bad={...state,settings:{...state.settings,pinnedAchievements:pins}};assert.throws(()=>core.validate(bad),/three different known achievements/);}
});
test('historical corrections preserve a pin preference while its earned state becomes locked',()=>{
  const state=core.blank();state.settings.pinnedAchievements=['first'];const restored=core.validate(state);assert.equal(restored.settings.pinnedAchievements[0],'first');assert.equal(core.badges(restored).find(b=>b.id==='first').earned,false);
});
test('win cards use actual outcome metadata, category filters, and reverse local dates',()=>{
  const state=stateWith([entry(TODAY,{useful:false,outcome:'',before:'',after:''}),entry(core.addDays(TODAY,-1),{category:'Review',useful:false,outcome:'',before:'A slow manual step'}),entry(TODAY,{category:'Automate',useful:true})]);
  const cards=core.winCards(state);assert.equal(cards.length,2);assert.equal(cards[0].category,'Automate');assert.equal(core.winCards(state,'Review').length,1);assert.equal(core.winCards(state,'Learn').length,0);
});
test('practice islands count real uses, useful outcomes, and distinct dates at the 1/5/15/30 milestones',()=>{
  const state=stateWith(Array.from({length:15},(_,i)=>entry(core.addDays(TODAY,-(i%3)),{category:'Review',useful:i<4})));
  const review=core.skillMap(state).find(s=>s.category==='Review'),empty=core.skillMap(state).find(s=>s.category==='Learn');
  assert.equal(review.uses,15);assert.equal(review.wins,4);assert.equal(review.days,3);assert.equal(review.level,3);assert.equal(review.next,30);assert.equal(review.progress,0);assert.equal(empty.level,0);assert.equal(empty.next,1);
  state.entries.push(...Array.from({length:15},()=>entry(TODAY,{category:'Review'})));assert.equal(core.skillMap(state).find(s=>s.category==='Review').next,null);
});
test('quest moments use first step completion dates and do not duplicate repeated logs',()=>{
  const state=core.blank(),q=quest(),start=core.addDays(TODAY,-3);state.quests=[q];state.entries=q.steps.map((s,i)=>entry(core.addDays(start,i),{questId:q.id,questStepId:s.id,stepComplete:true}));state.entries.push(entry(TODAY,{questId:q.id,questStepId:q.steps[0].id,stepComplete:true}));
  const moments=core.questMoments(state,q);assert.equal(moments.steps[0].date,start);assert.equal(moments.completeOn,TODAY);
  state.entries=state.entries.filter(e=>e.questStepId!==q.steps[2].id);assert.equal(core.questMoments(state,q).completeOn,null);
});
test('weekly replay includes actual work, quest steps, first-earned badges, and workshop unlocks in date order',()=>{
  const start=core.weekStart(TODAY),state=core.blank(),q=quest();state.quests=[q];state.entries=Array.from({length:7},(_,i)=>entry(core.addDays(start,i-6),{category:'Automate',questId:i>=3?q.id:null,questStepId:i>=3?q.steps[i-3].id:null,stepComplete:i>=3}));
  const replay=core.weekReplay(state,TODAY,TODAY);assert.equal(replay.start,start);assert.equal(replay.events.some(e=>e.type==='day'),true);assert.equal(replay.events.some(e=>e.type==='step'),true);assert.equal(replay.events.some(e=>e.type==='quest'),true);assert.equal(replay.events.some(e=>e.type==='badge'&&e.badgeId==='quest'),true);assert.equal(replay.events.some(e=>e.type==='workshop'&&e.itemId==='tools'),true);
  replay.events.forEach(e=>assert.ok(e.date>=start&&e.date<=TODAY));for(let i=1;i<replay.events.length;i++)assert.ok(replay.events[i].date>=replay.events[i-1].date);
});
test('replays include first unlocks once, respect week boundaries, and remove corrected milestones',()=>{
  const start=core.weekStart(TODAY),state=stateWith([entry(core.addDays(start,-1)),entry(start),entry(start)]);
  const replay=core.weekReplay(state,TODAY);assert.equal(replay.events.some(e=>e.badgeId==='first'),false);assert.equal(replay.events.some(e=>e.itemId==='desk'),false);assert.equal(replay.events.filter(e=>e.type==='day').length,1);
  state.entries.push(entry(core.addDays(start,7)));assert.equal(core.weekReplay(state,TODAY).events.some(e=>e.date===core.addDays(start,7)),false);
  assert.equal(core.weekReplay(core.blank(),TODAY).events.length,0);
});
test('quest scenes progress across all six themes without changing source records',()=>{
  const art=vm.runInContext('Art',context),state=stateWith([entry(TODAY)]),before=JSON.stringify(state);
  for(const emblem of core.EMBLEMS){const versions=[0,1,2,3,4].map(n=>art.questScene(emblem,n));assert.equal(new Set(versions).size,5);assert.match(versions[0],/data-stage="0"/);assert.match(versions[4],/data-stage="4"/);assert.doesNotMatch(versions[4],/<script|<image|<foreignObject/);}
  assert.equal(art.questScene('<script>',99),art.questScene('compass',4));assert.equal(JSON.stringify(state),before);
});
test('individual badge cards are available only for earned rewards and escape their evidence',()=>{
  const art=vm.runInContext('Art',context),state=stateWith([entry(TODAY,{note:'Fixed <script>alert(1)</script> & checked the output'})]);
  assert.equal(art.badgeCard(core.achievementDetails(state,'streak100')),null);const card=art.badgeCard(core.achievementDetails(state,'first'));
  assert.match(card,/width="1080" height="1080"/);assert.match(card,/&lt;script&gt;/);assert.doesNotMatch(card,/<script|<foreignObject|<image/);assert.match(card,new RegExp(TODAY));
});
