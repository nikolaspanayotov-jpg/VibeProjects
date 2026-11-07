/* Pure v1 preparation validation and merge invariants; no browser state. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),context={window:{},URL,structuredClone};vm.createContext(context);
for(const file of ['preparation-data.js','preparation.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),context);
const P=context.window.L4_PREP,D=context.window.L4_PREP_DATA,ids=[...Array.from({length:15},(_,i)=>'K'+(i+1)),...Array.from({length:15},(_,i)=>'S'+(i+1)),...Array.from({length:7},(_,i)=>'B'+(i+1))];
const plain=v=>JSON.parse(JSON.stringify(v)),validate=s=>plain(P.validate(s,ids));
assert.deepEqual(validate(undefined),plain(P.blank()));assert.equal(D.sql.length,6);assert.equal(D.comparisons.length,6);assert.equal(D.glossary.length,16);
const resource={id:'r-synthetic',title:'Synthetic note',url:'https://example.org/course',notes:'<script>inert</script>',ksbs:['K1','S1']};
let s=plain(P.blank());s.resources[resource.id]=resource;assert.deepEqual(validate(s),s);
for(const url of ['javascript:alert(1)','data:text/html,hello','file:///tmp/private','https://user:pass@example.org']){const bad=structuredClone(s);bad.resources[resource.id].url=url;assert.throws(()=>validate(bad));}
s.resourceDraft={...resource,id:'r-draft',url:'https://'};assert.equal(validate(s).resourceDraft.url,'https://');
for(const mutation of [x=>x.resources[resource.id].ksbs.push('K99'),x=>x.resources[resource.id].ksbs.push('K1'),x=>x.resources[resource.id].title='x'.repeat(201),x=>x.resources[resource.id].notes=33,x=>x.sql.unknown={query:'SELECT 1',hint:0,runs:0},x=>x.comparisons.identity={variant:0,choice:1,reason:'',revealed:true},x=>x.extra='unsupported',x=>x.resources=JSON.parse('{"__proto__":{}}')]){const bad=structuredClone(s);mutation(bad);assert.throws(()=>validate(bad));}
const incoming=structuredClone(s);incoming.resources[resource.id].title='Incoming note';let result=P.merge(s,incoming,{});assert.equal(result.merged.resources[resource.id].title,'Synthetic note');assert.equal(result.conflicts.length,1);result=P.merge(s,incoming,{['prep-resources-'+resource.id]:'import'});assert.equal(result.merged.resources[resource.id].title,'Incoming note');assert.deepEqual(validate(P.merge(s,P.blank(),{}).merged),s);
const removed=plain(P.blank());removed.deleted=['resources:'+resource.id];incoming.resourceDraft=resource;result=P.merge(removed,incoming,{});assert.equal(result.merged.resources[resource.id],undefined);assert.equal(result.merged.resourceDraft,null);assert.equal(result.merged.deleted.length,1);
const mock={id:'r-mock',date:'2026-11-05',started:1793865600000,minutes:10,index:0,queue:['K1','S1','B1'],answers:Array.from({length:3},()=>({response:'Synthetic answer',checks:[false,false,false,false],next:''})),finished:''};s=plain(P.blank());s.activeMock=mock;assert.deepEqual(validate(s),s);
for(const mutation of [m=>m.queue=['K1','S1','K1'],m=>m.queue=['K1','K2','K3'],m=>m.answers.pop(),m=>m.answers[0].checks=[true],m=>m.started=Infinity,m=>m.date='2026-02-30',m=>m.index=3,m=>m.finished='2026-11-05']){const bad=structuredClone(s);mutation(bad.activeMock);assert.throws(()=>validate(bad));}
for(const collection of [D.sql,D.comparisons,D.glossary]){assert.equal(new Set(collection.map(x=>x.id)).size,collection.length);for(const item of collection)for(const id of item.ksbs)assert(ids.includes(id));}
for(const c of D.comparisons){assert.equal(c.questions.length,2);for(const q of c.questions)assert([0,1].includes(q.answer));}
console.log('Preparation v1 defaults, bounded validation, safe saved links, recoverable URL drafts, record conflicts, deletion tombstones, mock invariants and authored IDs passed.');

// Packaging must reproduce the exact pinned engine, including direct-file loader order.
const crypto=require('node:crypto'),vendorContext={};vm.createContext(vendorContext);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'vendor/sql-manifest.json'),'utf8'));
for(let i=1;i<=manifest.parts;i++)vm.runInContext(fs.readFileSync(path.join(root,'vendor/sql-asm-'+String(i).padStart(2,'0')+'.js'),'utf8'),vendorContext);
const source=vendorContext.L4_SQL_PARTS.join('');assert.equal(Buffer.byteLength(source),manifest.bytes);assert.equal(crypto.createHash('sha256').update(source).digest('hex'),manifest.source_sha256);assert.equal(manifest.source_sha256,'c83beac167ae9c1af075449555b1db68b24b5280d0fc65c1f7ac4d1cd103459d');
new vm.Script(source);console.log('All 22 vendor chunks reconstruct the pinned SQLite engine byte-for-byte.');
