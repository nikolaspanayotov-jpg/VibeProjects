"""Authoring-only: create the atomic public-file cache manifest in sw.js.

Run after changing any cached public asset. The shipped website needs no build.
"""
from pathlib import Path
import argparse,hashlib,json
parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();root=args.root
assets=['index.html','assessment.js?v=20261107-assessment','assessment.css?v=20261107-assessment','assessment-criteria.json','preparation.css?v=20261105-prep','preparation-data.js?v=20261105-prep','preparation.js?v=20261107-assessment','sql-LICENSE.txt','curriculum.js?v=20261107-assessment','gamification.js?v=20261105-quests','solutions.md','worked-project.md','design.md','learning-activities.json','reasoning-activities.json','rehearsal-activities.json','ksb-visuals.json','manifest.webmanifest','icon-192.png','icon-512.png']
assets += [f'vendor/sql-asm-{i:02d}.js?v=1.13.0' for i in range(1,23)] + ['vendor/sql-manifest.json']
entries=[dict(path=name,sha256=hashlib.sha256((root/name.split('?')[0]).read_bytes()).hexdigest()) for name in assets]
version='2026-11-07-'+hashlib.sha256(json.dumps(entries).encode()).hexdigest()[:12]
script='''/* Generated public-file manifest. Rebuild with tests/build_offline.py. */
'use strict';
const VERSION=__VERSION__;
const ASSETS=__ASSETS__;
const PREFIX='l4-fellowship-offline:'+new URL(self.registration.scope).pathname+':';
const CACHE=PREFIX+VERSION;
const urls=new Map(ASSETS.map(a=>[new URL(a.path,self.registration.scope).href,a]));
const indexURL=new URL('index.html',self.registration.scope).href;
self.addEventListener('install',event=>event.waitUntil((async()=>{
 // Validate the entire release before writing a cache or making it active.
 const fetched=await Promise.all(ASSETS.map(async asset=>{
  const url=new URL(asset.path,self.registration.scope).href;
  const response=await fetch(url,{cache:'reload'});
  if(!response.ok)throw new Error('Offline file unavailable: '+asset.path);
  const bytes=await response.clone().arrayBuffer();
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(b=>b.toString(16).padStart(2,'0')).join('');
  if(hash!==asset.sha256)throw new Error('Offline release mismatch: '+asset.path);
  return [url,response];
 }));
 const cache=await caches.open(CACHE);
 await Promise.all(fetched.map(([url,response])=>cache.put(url,response)));
})()));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('message',event=>{
 if(event.data?.type==='ACTIVATE')event.waitUntil(self.skipWaiting());
 if(event.data?.type==='STATUS')event.waitUntil((async()=>{
  const cache=await caches.open(CACHE);
  const ready=(await Promise.all([...urls.keys()].map(url=>cache.match(url)))).every(Boolean);
  event.ports[0]?.postMessage({version:VERSION,ready});
 })());
});
self.addEventListener('fetch',event=>{
 const request=event.request,url=new URL(request.url),scope=new URL(self.registration.scope);
 if(request.method!=='GET'||url.origin!==scope.origin||!url.pathname.startsWith(scope.pathname))return;
 const isIndex=url.pathname===scope.pathname||url.pathname===new URL(indexURL).pathname;
 const exact=urls.has(url.href)?url.href:null;
 if(isIndex||exact){event.respondWith((async()=>{
  const cache=await caches.open(CACHE),cached=await cache.match(isIndex?indexURL:exact);
  return cached||fetch(request);
 })());return;}
 // An older open tab may request its own versioned curriculum. Keep versions paired.
 if(['curriculum.js','gamification.js','preparation.js','preparation-data.js','preparation.css','assessment.js','assessment.css',...Array.from({length:22},(_,i)=>'vendor/sql-asm-'+String(i+1).padStart(2,'0')+'.js')].some(file=>url.pathname===new URL(file,scope).pathname)){event.respondWith((async()=>{
  for(const name of await caches.keys())if(name.startsWith(PREFIX)){const cached=await (await caches.open(name)).match(request);if(cached)return cached;}
  return fetch(request);
 })());}
});
'''.replace('__VERSION__',json.dumps(version)).replace('__ASSETS__',json.dumps(entries,separators=(',',':')))
(root/'sw.js').write_text(script);print('Built verified offline release '+version)
