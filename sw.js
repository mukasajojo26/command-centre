/* Command Centre service worker — offline shell */
const V='csrm-shell-1.3.0',LIB='csrm-lib';
const SHELL=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','icon-maskable-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V&&k!==LIB).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
 const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
 if(u.origin===location.origin){
  if(r.mode==='navigate'||u.pathname.endsWith('/')||u.pathname.endsWith('/index.html')){
   e.respondWith(fetch(r).then(res=>{if(res&&res.ok){const c=res.clone();caches.open(V).then(x=>x.put('index.html',c))}return res}).catch(()=>caches.match('index.html').then(m=>m||caches.match('./'))));return}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res&&res.ok){const c=res.clone();caches.open(V).then(x=>x.put(r,c))}return res})));return}
 if(u.hostname==='cdnjs.cloudflare.com'){
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{const c=res.clone();caches.open(LIB).then(x=>x.put(r,c));return res}).catch(()=>m)))}
});
