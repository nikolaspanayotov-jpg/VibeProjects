// Independent numerical acceptance checks; no browser or external packages.
import { readFileSync, writeFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const page=readFileSync(new URL('../index.html',import.meta.url),'utf8');
const data=id=>JSON.parse(page.match(new RegExp('<script[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)</script>'))[1]);
const context=vm.createContext({});vm.runInContext(page.match(/<script id="position-engine">([\s\S]*?)<\/script>/)[1],context);
const {calculatePosition,calculateForward}=context.AnthropicPlanning;
const fresh=()=>structuredClone(data('position-default-data'));
const close=(actual,expected,tolerance=1e-8)=>assert.ok(Math.abs(actual-expected)<tolerance,`${actual} != ${expected}`);
const run=plan=>{const r=calculatePosition(plan);assert.equal(r.valid,true,JSON.stringify(r.errors));return r;};
const fees=plan=>{plan.costMode='included';[plan.initial,...plan.buys,...plan.sells].forEach(lot=>{lot.usdFee=0;lot.gbpFee=0;});plan.holding={usd:0,gbp:0};return plan;};
const results=[];const check=(name,fn)=>{fn();results.push({check:name,result:'passed'});};

check('Default initial purchase, unknown costs, reserve and unrealised mark remain separate',()=>{
 const r=run(fresh());close(r.purchaseUSD,1480);close(r.purchaseGBP,1184);close(r.reserve,592);close(r.realizedUSD,0);close(r.unrealizedUSD,360);close(r.combinedGBP,288);assert.equal(r.quantity,20);assert.equal(r.costsIncluded,false);
});
check('Full sale at $92 produces $360 gross profit; a $100 entry produces $160 loss',()=>{
 const p=fresh();p.sells[0]={...p.sells[0],enabled:true,qty:20,price:92};let r=run(p);close(r.realizedUSD,360);close(r.combinedUSD,360);close((92/74-1)*100,24.324324324324323);
 p.initial.price=100;r=run(p);close(r.combinedUSD,-160);close((92/100-1)*100,-8);assert.equal(r.averageUSD,null);assert.equal(r.breakEvenUSD,null);
});
check('One and two finite additions reconcile quantity, cash, average and larger downside',()=>{
 const p=fresh();p.buys[0].enabled=true;let r=run(p);assert.equal(r.quantity,25);close(r.purchaseUSD,1794.5);close(r.averageUSD,71.78);
 p.buys[1].enabled=true;r=run(p);assert.equal(r.quantity,30);close(r.purchaseUSD,2053.5);close(r.averageUSD,68.45);close(r.reserve,18.5);close(r.comparison[0].lossUSD,-680);close(r.comparison[1].valueUSD,1200);close(r.comparison[1].lossUSD,-853.5);
});
check('Two staged sales allocate acquisition cost once and leave ten shares at risk',()=>{
 const p=fresh();p.sells[0].enabled=true;p.sells[1].enabled=true;const r=run(p);close(r.saleUSD,1017.5);close(r.realizedUSD,277.5);assert.equal(r.quantity,10);close(r.remainingBasisUSD,740);close(r.combinedUSD,457.5);close(r.combinedUSD,r.saleUSD+r.markedUSD-r.purchaseUSD);
});
check('Lot-specific sale FX reduces GBP profit without changing the USD price gain',()=>{
 const p=fresh();p.sells[0]={...p.sells[0],enabled:true,qty:20,price:92,fx:1.4};const r=run(p);close(r.purchaseGBP,1184);close(r.saleGBP,1314.2857142857142);close(r.combinedGBP,130.28571428571422);close(r.combinedUSD,360);
});
check('USD/GBP purchase, sale and unallocated holding costs are counted once',()=>{
 const p=fees(fresh());p.initial.usdFee=2;p.initial.gbpFee=1;p.sells[0]={...p.sells[0],enabled:true,qty:20,price:92,fx:1.4,usdFee:1,gbpFee:2};p.holding={usd:3,gbp:4};p.markFx=1.4;const r=run(p);close(r.purchaseUSD,1483.25);close(r.purchaseGBP,1186.6);close(r.realizedUSD,352.95);close(r.combinedUSD,344.35);close(r.combinedGBP,118.82857142857142);assert.equal(r.averageGBP,null);
});
check('Several small sales incur their own supplied minimum commissions',()=>{
 const p=fees(fresh());p.sells[0].enabled=true;p.sells[1].enabled=true;p.sells[0].usdFee=1;p.sells[1].usdFee=1;const r=run(p);close(r.saleUSD,1015.5);close(r.realizedUSD,275.5);close(r.combinedUSD,455.5);
});
check('Transaction costs can exceed the small reserve; caps flag the breach without hiding exposure',()=>{
 const p=fees(fresh());p.buys.forEach(b=>b.enabled=true);p.initial.usdFee=19;let r=run(p);close(r.reserve,-.5);assert.ok(r.breaches.some(x=>x.includes('cap exceeded')));p.maxShares=25;r=run(p);assert.equal(r.breaches.length,2);assert.equal(r.quantity,30);
});
check('A sterling cap uses each lot FX; sales never replenish the contribution reserve',()=>{
 const p=fresh();p.cap={currency:'GBP',amount:1500};p.buys[0].enabled=true;p.buys[0].fx=1.4;let r=run(p);close(r.capUsed,1184+314.5/1.4);close(r.reserve,1500-1184-314.5/1.4);
 p.sells[0].enabled=true;r=run(p);close(r.capUsed,1184+314.5/1.4);p.mark=200;r=run(p);assert.ok(r.markedUSD>p.cap.amount);assert.equal(r.breaches.length,0);
});
check('Partial and zero allocation have finite outputs; additions scale down and short sales are rejected',()=>{
 const p=fresh();p.initial.qty=0;let r=run(p);assert.equal(r.quantity,0);assert.equal(r.averageUSD,null);close(r.combinedUSD,0);close(r.reserve,2072);
 p.sells[0].enabled=true;assert.equal(calculatePosition(p).valid,false);p.sells[0].enabled=false;p.initial.qty=8;p.buys[0].enabled=true;assert.equal(calculatePosition(p).valid,false);p.buys[0].qty=2;r=run(p);assert.equal(r.quantity,10);
});
check('Price gaps never activate additions; two additions require distinct evidence reviews',()=>{
 const p=fresh();p.mark=40;p.buys.forEach(b=>b.price=40);let r=run(p);assert.equal(r.quantity,20);p.buys.forEach(b=>b.enabled=true);p.buys[1].review=1;assert.equal(calculatePosition(p).valid,false);p.buys[1].review=2;r=run(p);assert.equal(r.quantity,30);
});
check('Unknown supplied fees and invalid/empty/non-finite/fractional inputs fail without fabricated net results',()=>{
 const p=fresh();p.costMode='included';assert.equal(calculatePosition(p).valid,false);
 for(const value of [null,NaN,Infinity,-1,21,1.5]){const q=fresh();q.initial.qty=value;assert.equal(calculatePosition(q).valid,false);}
 for(const value of [null,0,-1,Infinity]){const q=fresh();q.markFx=value;assert.equal(calculatePosition(q).valid,false);}
 const q=fees(fresh());q.initial.usdFee=-1;assert.equal(calculatePosition(q).valid,false);
});
check('Fees exceeding sale proceeds create a cash shortfall and never a short position',()=>{
 const p=fees(fresh());p.sells[0]={...p.sells[0],enabled:true,qty:20,price:.01,usdFee:10};const r=run(p);close(r.saleUSD,-9.8);close(r.contributedUSD,1489.8);close(r.combinedUSD,-1489.8);assert.equal(r.quantity,0);
});
check('Forward arithmetic, dilution and all nine cross-combinations use equity rather than EV',()=>{
 const input=data('forward-assumption-data');let r=calculateForward(input);assert.equal(r.valid,true);close(r.price,91.6005450659,.0001);close(r.cases[1].moreSharesPrice,83.2732227872,.0001);assert.equal(r.matrix.length,3);r.matrix.forEach(row=>assert.equal(row.cells.length,3));close(r.matrix[0].cells[2].price,84.3835393337,.0001);
 input.dilution=10;r=calculateForward(input);close(r.price,83.2732227872,.0001);close(r.equity,1650);close(74*18.012993379/136,9.801187574,.0001);
});
check('Forward zero shares/FX-like denominators, non-finite values and mismatched years are rejected',()=>{
 for(const [key,value] of [['baseShares',0],['baseShares',null],['revenue',Infinity],['multiple',-1],['entry',0],['dilution',201],['forecastYear',2029]]){const p=data('forward-assumption-data');p[key]=value;assert.equal(calculateForward(p).valid,false);}
});
writeFileSync(new URL('./position-math-results.json',import.meta.url),JSON.stringify(results,null,2)+'\n');
console.log(JSON.stringify(results,null,2));
