const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)],RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
/* intro: animated logo splash, once per visit; the site reveals itself when it ends */
(()=>{const el=$('#intro'),root=document.documentElement;if(!el)return;
if(!root.classList.contains('intro')){el.remove();return}
const v=$('#iv',el),hv=$('#lv'),SHOW=3400,HARD=7000;let done=0,started=0,t1,t2;
try{sessionStorage.setItem('azi','1')}catch(e){}
if(hv)hv.pause();
const end=()=>{if(done)return;done=1;clearTimeout(t1);clearTimeout(t2);removeEventListener('keydown',key);
 el.classList.add('out');root.classList.remove('intro');
 if(hv){hv.currentTime=0;const p=hv.play();if(p&&p.catch)p.catch(()=>{})}
 $$('.rv:not(.in)').forEach(n=>{io.unobserve(n);io.observe(n)});
 setTimeout(()=>el.remove(),900)},
key=e=>{if(e.key==='Escape')end()},
go=()=>{if(started||done)return;started=1;clearTimeout(t2);el.style.setProperty('--it',SHOW+'ms');el.classList.add('go');t1=setTimeout(end,SHOW)};
v.addEventListener('playing',go,{once:true});v.addEventListener('error',()=>{started=0;go()},{once:true});
t2=setTimeout(go,1500);setTimeout(end,HARD);
$('.is',el).addEventListener('click',end);el.addEventListener('click',end);addEventListener('keydown',key)})();
/* ambient particles */
(()=>{const c=$('#sp');if(!c)return;if(matchMedia('(max-width:900px),(hover:none)').matches){c.remove();return}const x=c.getContext('2d');let W,H,P=[],raf,last=0;
function init(){const d=Math.min(devicePixelRatio||1,1.5);W=innerWidth;H=innerHeight;c.width=W*d;c.height=H*d;x.setTransform(d,0,0,d,0,0);
const n=Math.min(Math.floor(W*H/1e4*.5),90);P=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,s:.8+Math.random()*1.5,a:.12+Math.random()*.35,vx:(Math.random()-.5)*.1,vy:.08+Math.random()*.16,g:Math.random()<.18}))}
function draw(){x.clearRect(0,0,W,H);for(const p of P){x.beginPath();x.arc(p.x,p.y,p.s,0,6.2832);x.fillStyle=p.g?`rgba(200,150,12,${p.a})`:`rgba(11,31,77,${p.a*.7})`;x.fill()}}
function tick(t){raf=requestAnimationFrame(tick);if(t-last<33)return;const dt=Math.min((t-last)/16.67,3);last=t;for(const p of P){p.x+=p.vx*dt;p.y+=p.vy*dt;if(p.y>H+4)p.y=-4;if(p.x<-4)p.x=W+4;if(p.x>W+4)p.x=-4}draw()}
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{init();draw()},150)});
document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelAnimationFrame(raf);else if(!RM){last=performance.now();raf=requestAnimationFrame(tick)}});
init();draw();if(!RM)raf=requestAnimationFrame(tick)})();
/* nav, progress bar */
const nav=$('#nav'),pb=$('#pb');
function sc(){nav.classList.toggle('s',scrollY>40);const h=document.documentElement.scrollHeight-innerHeight;pb.style.transform=`scaleX(${h>0?scrollY/h:0})`}
addEventListener('scroll',sc,{passive:true});sc();
$('#bg').onclick=()=>{const o=$('#ln').classList.toggle('o');$('#bg').setAttribute('aria-expanded',o)};
$$('#ln a').forEach(a=>a.addEventListener('click',()=>{$('#ln').classList.remove('o');$('#bg').setAttribute('aria-expanded','false')}));
addEventListener('keydown',e=>{if(e.key==='Escape'){$('#ln').classList.remove('o');$('#bg').setAttribute('aria-expanded','false')}});
/* nav hover indicator */
const ln=$('#ln');if(ln&&matchMedia('(min-width:1081px)').matches){const ind=document.createElement('span');ind.className='ind';ln.prepend(ind);const L=$$('#ln>a');
const mv=a=>{ind.style.width=a.offsetWidth+'px';ind.style.transform=`translateX(${a.offsetLeft}px)`;ind.style.opacity=1};
L.forEach(a=>{a.addEventListener('mouseenter',()=>mv(a));a.addEventListener('focus',()=>mv(a))});ln.addEventListener('mouseleave',()=>ind.style.opacity=0);ln.addEventListener('focusout',()=>ind.style.opacity=0)}
/* glass sheen follows pointer */
document.addEventListener('pointermove',e=>{const g=e.target.closest&&e.target.closest('.gl');if(!g)return;const r=g.getBoundingClientRect();g.style.setProperty('--mx',e.clientX-r.left+'px');g.style.setProperty('--my',e.clientY-r.top+'px')},{passive:true});
/* counters + reveal */
function cnt(el){const n=+el.dataset.n;if(RM)return el.textContent=n.toLocaleString('en-GB');let t0;const f=t=>{t0=t0||t;const p=Math.min((t-t0)/1600,1);el.textContent=Math.round(n*(1-(1-p)**3)).toLocaleString('en-GB');p<1&&requestAnimationFrame(f)};requestAnimationFrame(f)}
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting&&!document.documentElement.classList.contains('intro')){const i=[...e.target.parentNode.children].indexOf(e.target);e.target.style.transitionDelay=Math.min(i,6)*70+'ms';setTimeout(()=>e.target.style.transitionDelay='',1200);e.target.classList.add('in');$$('[data-n]',e.target).forEach(cnt);io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -40px 0px'});
$$('.rv').forEach(e=>io.observe(e));
/* pricing tabs (also opens #gl / #st) */
const tabs=$$('.seg button');
if(tabs.length){const show=k=>{tabs.forEach(b=>{const on=b.dataset.t===k;b.classList.toggle('on',on);b.setAttribute('aria-selected',on)});$$('.pg').forEach(g=>g.hidden=g.id!==k)};
tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));const h=location.hash.slice(1);show(['gl','st'].includes(h)?h:'gl')}
/* quiz */
const QZ=[['What should you do when a pedestrian is waiting at a crossing?',['Slow down and be ready to stop','Sound your horn','Speed up'],0,'Be ready to stop and give them time to cross safely.'],
['A red circular sign usually means…',['Information','A prohibition or order','Parking'],1,'Circular signs with a red border generally prohibit something.'],
['When may you hold a mobile phone while driving?',['In slow traffic','At red lights','Only to call 999 in a genuine emergency when unsafe to stop'],2,'Holding a phone while driving is illegal apart from a genuine emergency when it is unsafe to stop.'],
['What is the typical overall stopping distance at 30 mph?',['12 metres (40 feet)','23 metres (75 feet)','36 metres (118 feet)'],1,'At 30 mph, thinking plus braking distance is about 23 metres, or 75 feet.'],
['What does a triangular sign with a red border usually do?',['Warns of a hazard ahead','Gives an order','Shows parking'],0,'Triangular signs warn you about hazards ahead.'],
['What is the legal minimum tread depth for car tyres across the central three-quarters?',['0.6 mm','1.0 mm','1.6 mm'],2,'The legal minimum is 1.6 mm across the central three-quarters of the tread.']];
const qz=$('#qz');if(qz){let done={};const qs=$('#qs');
qz.innerHTML=QZ.map((q,i)=>`<div class="gl q rv"><h3>${q[0]}</h3>${q[1].map((o,j)=>`<button class="btn" data-i="${i}" data-j="${j}">${o}</button>`).join('')}<p class="ex" role="status"></p></div>`).join('');
$$('.q.rv',qz).forEach(e=>io.observe(e));
$$('.q .btn',qz).forEach(b=>b.onclick=()=>{const i=+b.dataset.i,ok=+b.dataset.j===QZ[i][2],bx=b.parentNode;$$('.btn',bx).forEach(x=>x.classList.remove('ok','bad'));b.classList.add(ok?'ok':'bad');
$('.ex',bx).textContent=ok?'Correct! '+QZ[i][3]:'Not quite. Try again.';if(ok)done[i]=1;const n=Object.keys(done).length;qs.textContent=n+' of '+QZ.length+' answered correctly'+(n===QZ.length?'. Well done!':'.')})}
/* contact form */
const f=$('#f');if(f){const c=new URLSearchParams(location.search).get('course');if(c){const o=$$('#c option').find(x=>x.textContent.toLowerCase()===c.toLowerCase());if(o)o.selected=true}
f.onsubmit=async e=>{e.preventDefault();let bad=0;const S=(id,m)=>{const el=$('#'+id);el.nextElementSibling.textContent=m||'';el.setAttribute('aria-invalid',!!m);if(m)bad++},v=id=>$('#'+id).value.trim();
S('n',v('n').length<2?'Please enter your name.':'');S('p',!/^[+\d][\d\s()-]{7,}$/.test(v('p'))?'Enter a valid phone number.':'');S('e',!/^\S+@\S+\.\S+$/.test(v('e'))?'Enter a valid email.':'');S('e2',v('e2')!==v('e')?'Emails do not match.':'');
const st=$('#st'),btn=$('button[type=submit]',f);st.className='fine';if(bad)return st.textContent='Please fix the highlighted fields.';
const label=btn.textContent;btn.disabled=true;btn.textContent='Sending…';st.textContent='Sending your enquiry…';
try{const r=await fetch('/api/contact/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:v('n'),phone:v('p'),email:v('e'),course:$('#c').value,location:$('#l').value,method:$('#m').value,message:v('g'),website:v('web')})});
const j=await r.json().catch(()=>({}));if(!r.ok||!j.ok)throw new Error(j.error||'send_failed');
const nm=v('n').split(' ')[0],how=$('#m').value;
f.innerHTML='<div class="ok" role="status"><span class="okc" aria-hidden="true">✓</span><h2>Thank you, <span class="nm"></span>!</h2><p>Your enquiry has been sent to AZ Driving School. We will get back to you by <b class="hw"></b> as soon as we can.</p><button class="btn" type="button">Send another enquiry</button></div>';
$('.nm',f).textContent=nm;$('.hw',f).textContent=how.toLowerCase();$('.ok .btn',f).onclick=()=>location.reload();f.scrollIntoView({behavior:RM?'auto':'smooth',block:'center'})}
catch(err){btn.disabled=false;btn.textContent=label;st.className='fine bad';
st.innerHTML='Sorry, we could not send your enquiry just now. Please call <a href="tel:+447380323268">+44 7380 323268</a>, message us on <a href="https://wa.me/447380323268" target="_blank" rel="noopener">WhatsApp</a> or email <a href="mailto:info@azdriving.co.uk">info@azdriving.co.uk</a>.'}}}
/* 3D gallery */
const cf=$('#cf');if(cf){const cs=$$('.cc',cf),S=cs.length;let a=0,lk=0;cf.classList.add('on');
function lay(){const cw=Math.min(330,cf.clientWidth*.7);cf.style.height=cw*1.33+70+'px';cs.forEach((c,i)=>{let r=i-a;if(r>S/2)r-=S;if(r<-S/2)r+=S;const x=Math.abs(r);c.style.width=cw+'px';c.style.height=cw*1.33+'px';c.style.zIndex=9-x;c.style.opacity=x>2?0:1;c.style.pointerEvents=x>2?'none':'auto';c.classList.toggle('ac',!r);c.setAttribute('aria-hidden',x>0?'true':'false');c.style.transform=`translate(-50%,-50%) translateX(${r*cw*.6}px) translateZ(${-x*220}px) rotateY(${-r*14}deg) scale(${1-x*.1})`})}
function go(i){const n=Date.now();if(n-lk<450)return;lk=n;a=((i%S)+S)%S;lay()}
cs.forEach((c,i)=>c.onclick=()=>go(i));$('#cp').onclick=()=>go(a-1);$('#cn').onclick=()=>go(a+1);
cf.tabIndex=0;cf.onkeydown=e=>{if(e.key==='ArrowRight')go(a+1);if(e.key==='ArrowLeft')go(a-1)};
let sx=0;cf.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});cf.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>40)go(a+(d<0?1:-1))});
addEventListener('resize',lay);lay();if(!RM){setInterval(()=>{if(!document.hidden&&!cf.matches(':hover,:focus-within'))go(a+1)},5000)}}
const lv=$('#lv');if(lv&&RM){lv.pause();lv.removeAttribute('autoplay')}
/* ===== Lightning cursor (port of Originkit Lightning Cursor) ===== */
(()=>{
if(RM||!matchMedia('(hover:hover) and (pointer:fine)').matches)return;
const OPT={color:'#F2B705',thickness:1.2,glow:5,trail:4,intensity:22},
CRACKLE=20,FADE=15,MAXSPREAD=40,SEG=5,MAXSUB=64,MINSTEP=8,SMOOTH=.7,GT=2,BCH=.02,BMIN=15,
GLYPH=[[0,0],[0,18],[5,14],[9,23],[12,21],[8,12],[15,12],[0,0]];
const cv=document.createElement('canvas');cv.setAttribute('aria-hidden','true');
cv.style.cssText='position:fixed;inset:0;width:100%;height:100%;z-index:9999;pointer-events:none;opacity:0;display:block';
document.body.appendChild(cv);const ctx=cv.getContext('2d');if(!ctx)return;
const root=document.documentElement;let hidden=false;
const hide=h=>{if(h===hidden)return;hidden=h;root.classList.toggle('lc',h)};
let w=1,h=1;
function resize(){const d=Math.min(devicePixelRatio||1,2);w=Math.max(1,innerWidth);h=Math.max(1,innerHeight);cv.width=Math.floor(w*d);cv.height=Math.floor(h*d);ctx.setTransform(d,0,0,d,0,0)}
resize();addEventListener('resize',resize);
const mk=()=>{const o=[],b=[];for(let i=0;i<MAXSUB;i++){o.push(Math.random()-.5);if(Math.random()<BCH)b.push({t:i/MAXSUB,a:(Math.random()-.5)*(Math.PI/1.5),l:5+Math.random()*15})}return{o,b}};
let mx=-9999,my=-9999,seen=false,inside=false,lastMove=0,trail=[],bolts=[],gb=[],jit=0,fade=0;
const push=(x,y)=>{const hd=trail[0];if(!hd||Math.hypot(x-hd.x,y-hd.y)>=MINSTEP)trail.unshift({x,y})};
addEventListener('pointermove',e=>{
const t=e.target,field=t&&t.closest&&t.closest('input,textarea,select');
if(field){hide(false);inside=false;return}
hide(true);
if(!inside)trail=[{x:e.clientX,y:e.clientY}];
const batch=e.getCoalescedEvents?e.getCoalescedEvents():null;
if(batch&&batch.length){for(const ev of batch){mx=ev.clientX;my=ev.clientY;push(mx,my)}}else{mx=e.clientX;my=e.clientY;push(mx,my)}
seen=inside=true;lastMove=performance.now();cv.style.opacity='1'},{passive:true});
root.addEventListener('pointerleave',()=>{inside=false;hide(false)});
document.addEventListener('visibilitychange',()=>{if(document.hidden){inside=false;trail=[]}});
const scr=()=>{bolts=Array.from({length:Math.max(2,OPT.trail)},mk);gb=Array.from({length:GLYPH.length-1},mk)};scr();
function stroke(a,b,bolt,width,spread,smooth,prev,next){
const dx=b.x-a.x,dy=b.y-a.y,dist=Math.hypot(dx,dy);if(dist<1||width<.1)return;
const sub=Math.max(3,Math.min(MAXSUB,Math.ceil(dist/SEG))),amp=Math.min(dist*.3,spread),p0=prev||a,p3=next||b,cx=[],cy=[];
for(let i=0;i<=sub;i++){const t=i/sub,t2=t*t,t3=t2*t;
const rx=.5*(2*a.x+(-p0.x+b.x)*t+(2*p0.x-5*a.x+4*b.x-p3.x)*t2+(-p0.x+3*a.x-3*b.x+p3.x)*t3);
const ry=.5*(2*a.y+(-p0.y+b.y)*t+(2*p0.y-5*a.y+4*b.y-p3.y)*t2+(-p0.y+3*a.y-3*b.y+p3.y)*t3);
cx.push(a.x+dx*t+(rx-(a.x+dx*t))*smooth);cy.push(a.y+dy*t+(ry-(a.y+dy*t))*smooth)}
const nrm=i=>{const lo=Math.max(0,i-1),hi=Math.min(sub,i+1),tx=cx[hi]-cx[lo],ty=cy[hi]-cy[lo],l=Math.hypot(tx,ty);return l<1e-4?[-dy/dist,dx/dist]:[-ty/l,tx/l]};
ctx.beginPath();ctx.moveTo(cx[0],cy[0]);
for(let i=1;i<sub;i++){const[nx,ny]=nrm(i),o=bolt.o[i]*amp;ctx.lineTo(cx[i]+nx*o,cy[i]+ny*o)}
ctx.lineTo(cx[sub],cy[sub]);ctx.lineWidth=width;ctx.stroke();
if(dist<BMIN)return;
const bw=Math.max(1,width*.5),al=ctx.globalAlpha;ctx.globalAlpha=al*.8;
for(const br of bolt.b){const i=Math.min(sub,Math.floor(br.t*sub)),[nx,ny]=nrm(i),o=bolt.o[i]*amp,sx=cx[i]+nx*o,sy=cy[i]+ny*o,ex=sx+Math.cos(br.a)*br.l,ey=sy+Math.sin(br.a)*br.l;
ctx.beginPath();ctx.moveTo(sx,sy);ctx.lineTo((sx+ex)/2,(sy+ey)/2);ctx.lineTo(ex,ey);ctx.lineWidth=bw;ctx.stroke()}
ctx.globalAlpha=al}
function drawBolt(a,b,bolt,width,sp,glow,smooth,prev,next){
ctx.shadowBlur=glow*.6;ctx.strokeStyle=OPT.color;stroke(a,b,bolt,width*2.5,sp,smooth,prev,next);
ctx.strokeStyle='#FFFFFF';stroke(a,b,bolt,width,sp,smooth,prev,next);
ctx.shadowBlur=glow*.3;stroke(a,b,bolt,width,sp,smooth,prev,next)}
let last=performance.now();
function frame(now){requestAnimationFrame(frame);
if(document.hidden){last=now;return}
const dt=Math.min(.05,Math.max(0,(now-last)/1000));last=now;const maxLen=Math.max(2,OPT.trail);
jit+=dt;if(jit>=1/(CRACKLE*2)){jit=0;scr()}
ctx.clearRect(0,0,w,h);if(!seen)return;
if(!trail.length){if(!inside)return;trail=[{x:mx,y:my}]}
else if(!inside||now-lastMove>50){fade+=dt*FADE*6;while(fade>=1&&trail.length>1){fade-=1;trail.pop()}}else fade=0;
if(trail.length>maxLen)trail.length=maxLen;
const spread=Math.max(0,Math.min(100,OPT.intensity))/100*MAXSPREAD;
ctx.lineCap='round';ctx.lineJoin='round';ctx.shadowColor=OPT.color;
const hd=trail[0];
for(let i=0;i<trail.length-1;i++){const f=1-i/Math.max(1,trail.length-1);if(f<=.02)continue;ctx.globalAlpha=f;
drawBolt(trail[i],trail[i+1],bolts[i]||bolts[0],OPT.thickness*f,spread,OPT.glow*f,SMOOTH,trail[i-1],trail[i+2])}
if(!inside){ctx.globalAlpha=1;ctx.shadowBlur=0;if(trail.length<=1){trail=[];cv.style.opacity='0'}return}
ctx.globalAlpha=1;
/* solid dark body so the arrow stays visible on gold, white and glass buttons */
ctx.shadowBlur=0;ctx.beginPath();GLYPH.forEach((g,i)=>i?ctx.lineTo(hd.x+g[0],hd.y+g[1]):ctx.moveTo(hd.x+g[0],hd.y+g[1]));ctx.closePath();ctx.lineWidth=5;ctx.strokeStyle='rgba(255,255,255,.95)';ctx.stroke();ctx.fillStyle='#0b1f4d';ctx.fill();
for(let i=0;i<GLYPH.length-1;i++){drawBolt({x:hd.x+GLYPH[i][0],y:hd.y+GLYPH[i][1]},{x:hd.x+GLYPH[i+1][0],y:hd.y+GLYPH[i+1][1]},gb[i]||gb[0],1.4,spread*.05,OPT.glow,0)}
ctx.globalAlpha=1;ctx.shadowBlur=0}
requestAnimationFrame(frame)})();

/* WhatsApp side button */
(()=>{const wa=$('#wa');if(!wa)return;const b=$('#wf'),p=$('#wp'),x=$('#wx');
const set=o=>{p.hidden=!o;wa.classList.toggle('open',o);b.setAttribute('aria-expanded',o)};
b.onclick=()=>set(p.hidden);x.onclick=()=>{set(false);b.focus()};
document.addEventListener('click',e=>{if(!p.hidden&&!wa.contains(e.target))set(false)});
addEventListener('keydown',e=>{if(e.key==='Escape'&&!p.hidden){set(false);b.focus()}})})();

/* ===== PREMIUM MOTION LAYER (v22) ===== */
(()=>{if(RM)return;const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
/* price count-up when a card scrolls into view */
const pio=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;pio.unobserve(e.target);const el=e.target,m=el.textContent.match(/^(\D*)([\d,.]+)(.*)$/);if(!m)return;
const end=parseFloat(m[2].replace(/,/g,'')),t0=performance.now(),d=1100;el.setAttribute('aria-label',el.textContent);
const f=t=>{const p=Math.min((t-t0)/d,1),v=end*(1-Math.pow(1-p,4));el.textContent=m[1]+Math.round(v).toLocaleString('en-GB')+m[3];if(p<1)requestAnimationFrame(f);else el.textContent=m[1]+m[2]+m[3]};requestAnimationFrame(f)}),{threshold:.6});
$$('.pr').forEach(e=>pio.observe(e));
if(!fine)return;
/* 3D tilt on glass cards */
$$('.pe').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',(x*9).toFixed(2)+'deg');c.style.setProperty('--rx',(-y*9).toFixed(2)+'deg')});
c.addEventListener('pointerleave',()=>{c.style.setProperty('--rx','0deg');c.style.setProperty('--ry','0deg')})});
/* magnetic buttons */
$$('.btn.p').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.setProperty('--bx',((e.clientX-r.left-r.width/2)*.18).toFixed(1)+'px');b.style.setProperty('--by',((e.clientY-r.top-r.height/2)*.28).toFixed(1)+'px')});
b.addEventListener('pointerleave',()=>{b.style.setProperty('--bx','0px');b.style.setProperty('--by','0px')})})})();

/* ===== Blob Text Reveal (vanilla port of Originkit Blob Text Reveal) ===== */
(()=>{const els=$$('.brv');if(!els.length||RM||!('IntersectionObserver'in window))return;
const seg=window.Intl&&Intl.Segmenter?new Intl.Segmenter('en',{granularity:'grapheme'}):null,
split=t=>seg?[...seg.segment(t)].map(s=>s.segment):[...t],
sleep=ms=>new Promise(r=>setTimeout(r,ms)),frame=()=>new Promise(r=>requestAnimationFrame(()=>r())),
clamp=(v,a,b)=>Math.min(b,Math.max(a,v)),
tw=(dur,fn)=>new Promise(res=>{const t0=performance.now(),f=t=>{const p=Math.min((t-t0)/(dur*1000),1);fn(p);p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)}),
GOLD='#e9b93a',NAVY='#0b1f4d',ST=18,BLUR=matchMedia('(max-width:900px)').matches?5:12;
els.forEach(el=>{
const full=[el.textContent.trim(),...(el.dataset.words||'').split('|').filter(Boolean)];if(full.length<2)return;
/* a trailing full stop is drawn by the blob itself, so strip it from the animated letters */
const words=full.map(w=>w.replace(/\.$/,'')),size=+el.dataset.blob||12,gap=Math.max(6,Math.round(size*.45)),half0=size/2;
const sr=document.createElement('span');sr.className='brv-s';sr.textContent=full[0];
const tx=document.createElement('span');tx.className='brv-t';tx.setAttribute('aria-hidden','true');
const bl=document.createElement('span');bl.className='brv-b';bl.setAttribute('aria-hidden','true');
el.textContent='';el.append(sr,tx,bl);el.classList.add('on');el.style.paddingRight=(gap+size)+'px';
bl.style.height=size+'px';bl.style.marginBottom=(Math.round(size*.55)-2)+'px';bl.style.backgroundColor=GOLD;bl.style.opacity='0';
let seen=false;new IntersectionObserver(e=>seen=e[0].isIntersecting,{threshold:.35}).observe(el);
const ready=async()=>{while(!seen||document.hidden)await sleep(200)};
const setWord=w=>tx.replaceChildren(...split(w).map(ch=>{const s=document.createElement('span');s.className='brv-c';s.textContent=ch===' '?'\u00A0':ch;return s}));
const measure=()=>{const ns=[...tx.children],m=ns.map(n=>({l:n.offsetLeft,r:n.offsetLeft+n.offsetWidth})),inset=half0+gap;
return{ns,m,home:m[m.length-1].r+inset,left:Math.max(half0,m[0].l-inset)}};
const show=ns=>ns.forEach(n=>{n.getAnimations().forEach(a=>a.cancel());n.style.opacity='1';n.style.filter='blur(0px)';n.style.transform='translateY(0)'});
const hide=n=>{n.style.opacity='0';n.style.filter=`blur(${BLUR}px)`;n.style.transform=`translateY(${ST}px)`};
const reveal=n=>n.animate([{opacity:0,transform:`translateY(${ST}px)`,filter:`blur(${BLUR}px)`},{opacity:1,transform:'translateY(0)',filter:'blur(0px)'}],{duration:500,easing:'cubic-bezier(.215,.61,.355,1)',fill:'forwards'});
(async()=>{let i=0,bw=size,x=0,L;
const R=()=>{bl.style.width=bw+'px';bl.style.transform=`translateX(${x-bw/2}px)`};
const deform=to=>{const a=bw;return tw(.15,p=>{bw=a+(to-a)*p;R()})};
const sweepIn=async()=>{const done=new Set(),d=Math.abs(L.home-L.left);bl.style.backgroundColor=GOLD;
await tw(clamp(d/740,.35,.75),p=>{x=L.left+(L.home-L.left)*p;R();const lead=x+bw/2;L.ns.forEach((n,k)=>{if(!done.has(k)&&lead>=L.m[k].l){done.add(k);reveal(n)}})});
L.ns.forEach((n,k)=>{if(!done.has(k)){done.add(k);reveal(n)}});await sleep(700);show(L.ns);x=L.home;R()};
/* start hidden; the first reveal plays when the heading scrolls into view */
setWord(words[0]);await frame();await frame();L=measure();L.ns.forEach(hide);x=L.left;R();
await ready();L=measure();L.ns.forEach(hide);x=L.left;R();bl.style.opacity='1';await sweepIn();
for(;;){await sleep(2600);await ready();
L=measure();show(L.ns);bl.style.backgroundColor=NAVY;deform(size*1.75);
const dist=Math.abs(L.home-L.left);let shr=false;
await tw(clamp(dist/720,.35,.55),p=>{x=L.home+(L.left-L.home)*p;R();const lead=x-bw/2;L.ns.forEach((n,k)=>{if(lead<=L.m[k].r)hide(n)});if(!shr&&p>=.82){shr=true;deform(size);bl.style.backgroundColor=GOLD}});
if(!shr){deform(size);bl.style.backgroundColor=GOLD}
i=(i+1)%words.length;setWord(words[i]);await frame();L=measure();L.ns.forEach(hide);x=L.left;bw=size;R();await frame();
await sweepIn()}})()})})();

/* footer: staggered entrance when it scrolls into view */
(()=>{const ft=$('footer');if(!ft)return;let n=0;$$('.fqk a,.fg>div>a:not(.fc),.fc',ft).forEach(a=>a.style.setProperty('--i',n++));
if(RM||!('IntersectionObserver'in window))return ft.classList.add('in');
new IntersectionObserver((e,o)=>{if(e[0].isIntersecting){ft.classList.add('in');setTimeout(()=>ft.classList.add('done'),1800);o.disconnect()}},{threshold:.15}).observe(ft)})();
