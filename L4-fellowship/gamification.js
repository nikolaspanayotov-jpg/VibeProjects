/* Self-contained practice rewards. Totals are always derived from dated records. */
window.L4_GAME = (() => {
 'use strict';
 const blocks={recall:{name:'Recall',verb:'Retrieve an idea',mark:'01'},apply:{name:'Apply',verb:'Test a decision',mark:'02'},explain:{name:'Explain',verb:'Put it in your words',mark:'03'}};
 const kinds={recall:'recall',quiz:'recall',repair:'apply',method:'apply',scenario:'apply',change:'apply',lab:'apply',workshop:'explain',briefing:'explain',retrieval:'explain',connection:'explain','quiz-answer':null,challenge:null};
 const packs=[
 {id:'quality',name:'Data quality detective',description:'Follow a risk from understanding to investigation and explanation.',steps:[{label:'Rehearse K8',kind:'recall',target:'K8'},{label:'Investigate the duplicate join',kind:'repair',target:'duplicate-join'},{label:'Rehearse evidence or a gap for B5',kind:'retrieval',target:'B5'}]},
 {id:'forecast',name:'Forecast explorer',description:'Experiment, select a method and communicate the limits.',steps:[{label:'Experiment with forecast windows',kind:'lab',target:'forecast'},{label:'Defend a monthly forecasting method',kind:'method',target:'monthly-demand'},{label:'Brief the service lead',kind:'briefing',target:'capacity-lead'}]},
 {id:'discussion',name:'Discussion rehearsal',description:'Strengthen an answer and adapt a consistent finding for two audiences.',steps:[{label:'Review an S12 answer',kind:'workshop',target:'S12'},{label:'Write the decision-maker briefing',kind:'briefing',target:'capacity-lead'},{label:'Write the technical briefing',kind:'briefing',target:'capacity-technical'}]},
 {id:'privacy',name:'Privacy protector',description:'Trace a legal duty into a safe release decision and your own evidence.',steps:[{label:'Recall data protection principles',kind:'recall',target:'K1'},{label:'Investigate a proposed release',kind:'method',target:'privacy-release'},{label:'Explain secure-working evidence or a gap',kind:'retrieval',target:'B1'}]},
 {id:'statistics',name:'Statistical storyteller',description:'Explain variation, calculate a result and communicate its limits.',steps:[{label:'Recall descriptive and inferential statistics',kind:'recall',target:'K13'},{label:'Calculate a weighted mean',kind:'method',target:'weighted-time'},{label:'Brief a decision-maker',kind:'briefing',target:'capacity-lead'}]},
 {id:'accessibility',name:'Accessible analyst',description:'Connect user needs, chart choices and your own application.',steps:[{label:'Recall UX and domain context',kind:'recall',target:'K7'},{label:'Improve an accessible chart',kind:'method',target:'accessible-chart'},{label:'Rehearse design evidence or a gap',kind:'retrieval',target:'S5'}]}
 ];
 const badges=[
 {id:'spark',name:'First spark',description:'Complete one practice block.',metric:'blocks',goal:1,art:'spark'},
 {id:'trio',name:'Triple play',description:'Complete Recall, Apply and Explain on one local date.',metric:'trios',goal:1,art:'trio'},
 {id:'rhythm',name:'Finding a rhythm',description:'Practise on seven consecutive local dates.',metric:'best',goal:7,art:'flame'},
 {id:'month',name:'A steady month',description:'Practise on 30 consecutive local dates.',metric:'best',goal:30,art:'sun'},
 {id:'checkins',name:'Three times stronger',description:'Complete blocks in all three chosen time windows on five dates.',metric:'checkins',goal:5,art:'clock'},
 {id:'detective',name:'Mistake detective',description:'Correct five different previously missed quiz questions on later answer dates.',metric:'recoveries',goal:5,art:'lens'},
 {id:'story',name:'Evidence storyteller',description:'Complete evidence rehearsals or explicit gap reviews for five different KSBs.',metric:'retrievals',goal:5,art:'book'},
 {id:'audience',name:'Audience adapter',description:'Finish both audience briefings for the same scenario.',metric:'audiences',goal:1,art:'voices'},
 {id:'standard',name:'37 KSBs practised',description:'Explicitly practise each KSB through recall, an answer workshop or evidence rehearsal.',metric:'topics',goal:37,art:'nodes'},
 {id:'quest',name:'Case closed',description:'Complete all three steps of a weekly quest pack in the same week.',metric:'quests',goal:1,art:'ribbon'},
 {id:'challenge',name:'Joined-up discussion',description:'Finish the optional Knowledge, Skill and Behaviour rehearsal.',metric:'challenges',goal:1,art:'star'}
 ];
 function stamp(at,offset=new Date(at).getTimezoneOffset()) {const d=new Date(at-offset*60000);return {date:`${d.getUTCFullYear()}-${String(d.getUTCMonth()+1).padStart(2,'0')}-${String(d.getUTCDate()).padStart(2,'0')}`,minute:d.getUTCHours()*60+d.getUTCMinutes()};}
 function dayAdd(date,n) {const [y,m,d]=date.split('-').map(Number),x=new Date(y,m-1,d+n,12);return `${x.getFullYear()}-${String(x.getMonth()+1).padStart(2,'0')}-${String(x.getDate()).padStart(2,'0')}`;}
 function weekOf(date) {const [y,m,d]=date.split('-').map(Number),x=new Date(y,m-1,d,12);return dayAdd(date,-((x.getDay()+6)%7));}
 function timeValue(value) {if(typeof value!=='string'||!/^([01]\d|2[0-3]):[0-5]\d$/.test(value))return null;return Number(value.slice(0,2))*60+Number(value.slice(3));}
 function windowAt(minute,ends) {return minute<ends[0]?0:minute<ends[1]?1:2;}
 function sourceEvents(game) {const removed=new Set(game.deleted);return game.events.filter(e=>!removed.has(e.id)).sort((a,b)=>a.at-b.at);}
 function validBlocks(events) {const byId=new Map(events.map(e=>[e.id,e]));return events.filter(e=>kinds[e.kind]&&(e.kind!=='quiz'||(e.facts.answerIds.length>=5&&e.facts.answerIds.every(id=>byId.get(id)?.kind==='quiz-answer')&&new Set(e.facts.answerIds.map(id=>byId.get(id).target)).size>=5)));}
 function metrics(game,questions,today) {
  const events=sourceEvents(game),activeBlocks=validBlocks(events),byId=new Map(events.map(e=>[e.id,e])),days={},topicSet=new Set(),retrievalSet=new Set(),recoveries=new Set(),wrongDates={},correctDates={},audiences={},questWeeks={},earned={},counts={blocks:0,trios:0,best:0,checkins:0,recoveries:0,retrievals:0,audiences:0,topics:0,quests:0,challenges:0};
  const unlock=(id,date,eventId)=>{if(!earned[id])earned[id]={date,eventId};};
  for(const e of events){
   if(e.kind==='quiz-answer') {const correct=e.facts.choice===questions[e.target].answer,answered=e.facts.answeredOn;if(!correct){if(!wrongDates[e.target]||answered<wrongDates[e.target])wrongDates[e.target]=answered;}else if(!correctDates[e.target]||answered>correctDates[e.target])correctDates[e.target]=answered;if(wrongDates[e.target]&&correctDates[e.target]&&wrongDates[e.target]<correctDates[e.target]){recoveries.add(e.target);if(recoveries.size>=5)unlock('detective',e.date,e.id);}}
   if(e.kind==='challenge'){const refs=e.facts.attemptIds.map(id=>byId.get(id));if(refs.length===3&&refs.every(x=>x?.kind==='recall')&&new Set(refs.map(x=>x.target[0])).size===3){counts.challenges++;unlock('challenge',e.date,e.id);}}
  }
  for(const e of activeBlocks){
   counts.blocks++;unlock('spark',e.date,e.id);
   const day=days[e.date]||(days[e.date]={blocks:[],types:[],windows:[],xp:0});day.blocks.push(e);if(!day.types.includes(kinds[e.kind]))day.types.push(kinds[e.kind]);if(!day.windows.includes(e.window))day.windows.push(e.window);day.xp=day.types.length*20+(day.types.length===3?40:0);
   if(day.types.length===3)unlock('trio',e.date,e.id);
   if(['recall','workshop','retrieval'].includes(e.kind)){topicSet.add(e.target);if(topicSet.size===37)unlock('standard',e.date,e.id);}
   if(e.kind==='retrieval'){retrievalSet.add(e.target);if(retrievalSet.size>=5)unlock('story',e.date,e.id);}
   if(e.kind==='briefing'){const a=e.target.endsWith('-technical')?'technical':'lead',c=e.target.slice(0,-a.length-1);audiences[c] ||= new Set();audiences[c].add(a);if(audiences[c].size===2)unlock('audience',e.date,e.id);}
   const week=weekOf(e.date);questWeeks[week] ||= {};
   for(const pack of packs){const rows=questWeeks[week][pack.id] ||= [null,null,null];const index=pack.steps.findIndex((s,i)=>!rows[i]&&s.kind===e.kind&&s.target===e.target);if(index>=0)rows[index]=e;if(rows.every(Boolean))unlock('quest',e.date,e.id);}
  }
  const dates=Object.keys(days).sort();let run=0,previous='';for(const date of dates){run=previous&&dayAdd(previous,1)===date?run+1:1;previous=date;counts.best=Math.max(counts.best,run);if(run>=7)unlock('rhythm',date,days[date].blocks.at(-1).id);if(run>=30)unlock('month',date,days[date].blocks.at(-1).id);if(days[date].types.length===3)counts.trios++;if(days[date].windows.length===3){counts.checkins++;if(counts.checkins===5)unlock('checkins',date,days[date].blocks.at(-1).id);}}
  let current=0,cursor=days[today]?today:dayAdd(today,-1);while(days[cursor]){current++;cursor=dayAdd(cursor,-1);}
  let trioCurrent=0;cursor=days[today]?.types.length===3?today:dayAdd(today,-1);while(days[cursor]?.types.length===3){trioCurrent++;cursor=dayAdd(cursor,-1);}
  let trioBest=0,trioRun=0;previous='';for(const date of dates){trioRun=days[date].types.length===3?(previous&&dayAdd(previous,1)===date?trioRun+1:1):0;previous=date;trioBest=Math.max(trioBest,trioRun);}
  counts.recoveries=recoveries.size;counts.retrievals=retrievalSet.size;counts.topics=topicSet.size;counts.audiences=Object.values(audiences).filter(s=>s.size===2).length;counts.quests=Object.values(questWeeks).reduce((n,w)=>n+Object.values(w).filter(steps=>steps.every(Boolean)).length,0);
  const total=dates.reduce((n,d)=>n+days[d].xp,0),level=Math.floor(total/300)+1;
  return {events,activeBlocks,days,dates,counts,earned,current,trioCurrent,trioBest,total,level,nextLevel:level*300,questWeeks,topics:[...topicSet]};
 }
 function badgeArt(kind,locked=false) {const shapes={spark:'M32 8l5 16 17 8-17 6-5 18-6-18-16-6 16-8z',trio:'M10 42V28h10v14zM27 42V20h10v22zM44 42V12h10v30z',flame:'M33 9c2 13 17 18 13 32-4 17-29 15-30-1-1-10 10-17 12-26 1 10 5 13 5-5z',sun:'M32 17a15 15 0 1 0 0 30 15 15 0 0 0 0-30M32 5v7m0 40v7M5 32h7m40 0h7M13 13l5 5m28 28 5 5M13 51l5-5m28-28 5-5',clock:'M32 11a21 21 0 1 0 0 42 21 21 0 0 0 0-42m0 9v13l9 6',lens:'M27 10a17 17 0 1 0 0 34 17 17 0 0 0 0-34m12 30 14 14M20 27l5 5 10-11',book:'M10 15h17l5 4 5-4h17v34H37l-5 4-5-4H10zM32 19v34',voices:'M7 12h32v22H22l-8 8v-8H7zM43 24h14v25h-8l-8 7v-7h-8V40',nodes:'M12 13h12v12H12zM40 13h12v12H40zM26 42h12v12H26zM24 19h16M18 25l14 17 14-17',ribbon:'M20 35l-5 21 17-9 17 9-5-21M32 8l7 4 8 1 2 9-2 9-8 2-7 5-7-5-8-2-2-9 2-9 8-1z',star:'M32 7l8 16 18 3-13 13 3 18-16-9-16 9 3-18L6 26l18-3z'};return `<svg class="badge-art${locked?' locked':''}" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="30" fill="${locked?'#F2F5F8':'#EAF0F8'}" stroke="#A8B6C5"/><path d="${shapes[kind]||shapes.star}" fill="none" stroke="${locked?'#6B7E8E':'#174EA6'}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/></svg>`;}
 return {blocks,kinds,packs,badges,stamp,dayAdd,weekOf,timeValue,windowAt,sourceEvents,validBlocks,metrics,badgeArt};
})();
