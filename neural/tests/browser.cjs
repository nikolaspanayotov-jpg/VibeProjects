// Run with Playwright available: node neural/tests/browser.cjs
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs=require('node:fs');
(async () => {
 const browser = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless:true,args:['--no-sandbox','--disable-crashpad-for-testing']});
 const page = await browser.newPage({viewport:{width:1440,height:1100}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 try {
  const root=path.join(__dirname,'..');
  const source=fs.readFileSync(path.join(root,'index.html'),'utf8').replace('<link rel="stylesheet" href="./style.css">',()=>'<style>'+fs.readFileSync(path.join(root,'style.css'),'utf8')+'</style>').replace('<script src="./app.js"></script>',()=>'<script>'+fs.readFileSync(path.join(root,'app.js'),'utf8')+'</script>');
  await page.setContent(source);
  await page.waitForFunction(()=>document.querySelector('#beforeError').textContent!=='Error —');
  assert.equal(await page.locator('#task').inputValue(),'and');
  const initial=await page.evaluate(()=>({model:copyModel(),scores:baseline.scores,error:baseline.error}));
  await page.locator('#heroSwitch0').click();
  assert.deepEqual(await page.evaluate(()=>copyModel()),initial.model,'asking must not train');
  await page.locator('#roundStart').click();assert.equal(await page.evaluate(()=>epoch),0);
  await page.locator('#roundNext').click();assert.equal(await page.evaluate(()=>epoch),0,'compare does not update');
  await page.locator('#roundNext').click();assert.equal(await page.evaluate(()=>epoch),1,'adjust updates exactly once');
  assert.notDeepEqual(await page.evaluate(()=>copyModel()),initial.model);
  assert.equal(await page.locator('#train').isDisabled(),true);
  assert(await page.locator('#weightChange').textContent());
  await page.locator('#roundLab').evaluate(el=>el.scrollIntoView({block:'start',behavior:'instant'}));await page.screenshot({path:'/tmp/neural-round-desktop.png'});
  await page.locator('#roundNext').click();assert.equal(await page.evaluate(()=>epoch),1);
  await page.locator('#roundNext').click();assert.equal(await page.evaluate(()=>epoch),1);
  await page.locator('#replay').click();assert.equal(await page.evaluate(()=>epoch),0);
  assert.deepEqual(await page.evaluate(()=>copyModel()),initial.model,'replay restores exact start');
  assert.deepEqual(await page.evaluate(()=>baseline.scores),initial.scores);
  await page.locator('#challengeOptions button').nth(0).click();
  assert.match(await page.locator('#challengeFeedback').textContent(),/Try the idea again/);
  await page.locator('#challengeOptions button').nth(1).click();
  assert.match(await page.locator('#challengeFeedback').textContent(),/That’s right/);
  assert.equal(await page.locator('#challengeOptions button').nth(1).evaluate(el=>el===document.activeElement),true);
  await page.locator('#input0').fill('0.5');await page.locator('#input1').fill('0.5');
  assert.match(await page.locator('#pointReadout').textContent(),/not supplied/);
  // Teach all three rules using the same real training implementation.
  for(const task of ['and','or','xor']){
   await page.selectOption('#task',task);
   const before=await page.evaluate(()=>baseline.error);
   await page.evaluate(()=>{for(let i=0;i<30000;i++)trainEpoch();render()});
   const error=await page.evaluate(()=>loss());assert(error<before,task+' learning');
   assert.equal(await page.locator('#beforeError').textContent(),'Error '+before.toFixed(4));
  }
  await page.selectOption('#task','and');
  await page.locator('#train').click();await page.waitForFunction(()=>epoch>0);
  await page.locator('#train').click();const paused=await page.evaluate(()=>epoch);
  await page.waitForTimeout(100);assert.equal(await page.evaluate(()=>epoch),paused);
  await page.locator('#examples button').nth(0).focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#examples button').nth(0).evaluate(el=>el===document.activeElement),true);
  // Next lesson stays visible alongside its target on desktop.
  await page.evaluate(()=>{guideStep=0;showGuide()});await page.locator('#guideNext').click();await page.locator('#guideAction').click();
  assert.equal(await page.locator('#roundNext').isVisible(),true);const roundEpoch=await page.evaluate(()=>epoch);await page.locator('#guideAction').click();assert.equal(await page.evaluate(()=>roundDemo.phase),1);assert.equal(await page.evaluate(()=>epoch),roundEpoch);await page.locator('#guideAction').click();assert.equal(await page.evaluate(()=>roundDemo.phase),2);assert.equal(await page.evaluate(()=>epoch),roundEpoch+1);await page.locator('#roundExit').click();
  for(const [name,width,height] of [['desktop',1440,1100],['mobile',390,844],['narrow',320,740]]){
   await page.setViewportSize({width,height});
   if(width<760)assert.equal(await page.locator('#lessonDetails').evaluate(el=>el.open),false);
   await page.locator('#walkthrough').scrollIntoViewIfNeeded();
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,name+' horizontal overflow');
   await page.screenshot({path:'/tmp/neural-learning-'+name+'.png',fullPage:true});
   if(name==='mobile'){await page.locator('#roundStart').click();await page.locator('#roundNext').click();await page.locator('#roundNext').click();await page.locator('#roundLab').evaluate(el=>el.scrollIntoView({block:'start',behavior:'instant'}));await page.screenshot({path:'/tmp/neural-round-mobile.png'});await page.locator('#roundExit').click();await page.locator('#lessonDetails summary').click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'expanded lesson overflow');await page.locator('#lessonDetails summary').click()}
  }
  await page.emulateMedia({reducedMotion:'reduce'});await page.waitForFunction(()=>reduced===true);
  assert.equal(errors.length,0,errors.join('\n'));
  console.log('PASS: slow-round sequencing, exact replay, baseline preservation, questions, all rule training, controls, keyboard focus, responsive overflow, and no page errors.');
 } finally {await browser.close()}
})().catch(error=>{console.error(error);process.exit(1)});
