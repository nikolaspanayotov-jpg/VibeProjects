/* Generated public-file manifest. Rebuild with tests/build_offline.py. */
'use strict';
const VERSION="2026-11-05-5d8c79d42e80";
const ASSETS=[{"path":"index.html","sha256":"e512034db780b9200331304e5bb420029abfb8d60a827e50e856a2321df0f2d9"},{"path":"curriculum.js?v=20261105-visuals","sha256":"4967f94d432914d0750cfd780f35c26d9809794b336c986d046680b51963881a"},{"path":"gamification.js?v=20261105-habit","sha256":"2c2d49aaa30937c81cf7f65c247dc787ef5aabc02b2dffaaac6d1ada898f09bf"},{"path":"solutions.md","sha256":"c32d53fdeb7714b978ea3f7d8a7688ee3352550e6ab95980ab83d56939d72d31"},{"path":"worked-project.md","sha256":"f1fd66aeb10ca307a66ba7c222e00b18ca9dcd071958bf632409dd002ce82169"},{"path":"design.md","sha256":"2eece7d7cfc3d58b37b7ca6257b4ca6e550ab7e67e991ae22b482076a5c49aa3"},{"path":"learning-activities.json","sha256":"73be814e2c17fe522be6e52729d536d10d8fcdc7a4b62a873a9566f22f70cd41"},{"path":"reasoning-activities.json","sha256":"037bc23a9b64a4aedc81d9b95c2882bef523b1fdc3ecaff21a6350791459b143"},{"path":"rehearsal-activities.json","sha256":"2b5f355c344983717e222575d4a0b676533e144f01bf20efbaab5a520b0078af"},{"path":"ksb-visuals.json","sha256":"c0ef13d59f9b7fd4c3227d4e040e3db17ac25390a216e95469b45f0605ead157"},{"path":"manifest.webmanifest","sha256":"516657ed5ebbfd25fe0982c8dc9be3e57f11583c8b419cd5ecc17fad7ccdc6d2"},{"path":"icon-192.png","sha256":"597046cdbef3ba7fec4edb42e38b9e01eb043e81df662ad95ede5643265969f7"},{"path":"icon-512.png","sha256":"95c8da095060c31f45e1de0d33c3f2f0593f7bd56e12e4732119f8ed6be6f724"}];
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
 if(['curriculum.js','gamification.js'].some(file=>url.pathname===new URL(file,scope).pathname)){event.respondWith((async()=>{
  for(const name of await caches.keys())if(name.startsWith(PREFIX)){const cached=await (await caches.open(name)).match(request);if(cached)return cached;}
  return fetch(request);
 })());}
});
