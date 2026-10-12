/* Bob: transport bars, marks, contour zoom/pan, nudges, drafts, subtitle export (豆1 / 豆2) */
(()=>{
const css=`
.tpbar{display:flex;gap:6px;align-items:center;margin:10px 0}
.tpbar button{flex:1;height:48px;font-size:17px;border-radius:14px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.09);color:#F1F1E6;cursor:pointer;white-space:nowrap}
.tpbar button.pp{flex:1.3;background:rgba(185,229,154,.2);border-color:rgba(185,229,154,.5)}
.tpbar .tpt{min-width:62px;font-size:12.5px;color:var(--mute);text-align:right;font-variant-numeric:tabular-nums}
button.bigbtn,button.mini,button.big,.tpbar button,.zbtn,.ndg button,.mkb{transition:transform .08s,background .08s,filter .08s}
button.bigbtn:active,button.mini:active,button.big:active,.tpbar button:active,.zbtn:active,.ndg button:active,.mkb:active,button.pressed{transform:scale(.95);background:rgba(185,229,154,.35)!important;filter:brightness(1.25)}
.rollz{display:flex;gap:6px;align-items:center;justify-content:flex-end;margin-top:-18px}
.zbtn{width:34px;height:30px;border-radius:10px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#F1F1E6;font-size:17px;cursor:pointer}
#roll{touch-action:none;cursor:grab}
.mkb{background:none;border:0;color:inherit;font:inherit;min-width:34px;min-height:34px;border-radius:8px;cursor:pointer}
.ntab tr.mk{background:rgba(255,159,90,.16)}.ntab tr.mk.cur{background:rgba(255,190,120,.32)}.ntab tr.mk .mkb{color:#FFB07A;font-weight:700}
.ntab.onlymk tr:not(.mk){display:none}
.mkf{font-size:14px;display:flex;align-items:center;gap:6px;margin:6px 0}
.alr{flex-wrap:wrap}.alr.cur{background:rgba(185,229,154,.18);border-radius:10px}.alr.mk{box-shadow:inset 3px 0 0 #FF9F5A}.alr.mk .lmk{color:#FFB07A}
.alr .t{min-width:64px}
.ndg{display:flex;gap:4px;align-items:center;width:100%;padding-left:2px}
.ndg button{height:34px;min-width:44px;border-radius:10px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);color:#E8EDE9;font-size:14px;cursor:pointer}
.ndg button.f{min-width:38px;height:28px;font-size:12px;color:var(--mute)}
.ndg .lmk{margin-left:auto}
.drn{font-size:13px;margin:0 0 8px}`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

const ft=t=>{t=Math.max(0,t||0);return Math.floor(t/60)+':'+(t%60).toFixed(2).padStart(5,'0')};
const r2=x=>Math.round(x*100)/100;
S.marks=new Set();S.lmarks=new Set();
const notes=()=>S.notes||[];

/* press feedback (pointer-based, works even when :active is short on touch) */
document.addEventListener('pointerdown',e=>{const b=e.target.closest('button');if(!b)return;b.classList.add('pressed');setTimeout(()=>b.classList.remove('pressed'),180)},true);

/* ---------- generic transport ---------- */
const now=()=>performance.now()/1000;
function makeTP(o){const T={pos:0,on:false,t0:0,nx:0,raf:0,o};
 const units=()=>o.units();
 T.cur=()=>{const u=units();let k=-1;for(let i=0;i<u.length;i++)if(u[i].start<=T.pos+.02)k=i;return Math.max(0,k)};
 T.end=()=>{const N=notes();return N.length?Math.max(...N.map(n=>n.end)):0};
 function loop(){if(!T.on)return;T.pos=now()-T.t0;const N=notes();
  while(T.nx<N.length&&N[T.nx].start<T.pos+.15){const n=N[T.nx++];if(piano&&n.end>T.pos){try{piano.triggerAttackRelease(Tone.Frequency(n.pitch,'midi').toNote(),Math.max(.06,n.end-Math.max(n.start,T.pos)),Tone.now()+Math.max(0,n.start-T.pos),.75)}catch(e){}}}
  o.onPos(T.pos,T.cur(),true);
  if(T.pos>T.end()+.4){T.pause();T.pos=0;o.onPos(0,T.cur(),false);o.onEnd&&o.onEnd();return}
  T.raf=requestAnimationFrame(loop)}
 T.play=async()=>{if(!notes().length){toast('還沒有旋律');return}TPS.forEach(x=>x!==T&&x.pause());_stopAll();
  if(T.pos>=T.end())T.pos=0;T.on=true;setBtn();
  try{await Tone.start();await loadInst()}catch(e){console.warn(e)}
  if(!T.on)return;const N=notes();T.nx=N.findIndex(n=>n.end>T.pos);if(T.nx<0)T.nx=N.length;
  T.t0=now()-T.pos;loop()};
 T.pause=()=>{if(!T.on)return;T.on=false;cancelAnimationFrame(T.raf);try{piano&&piano.releaseAll()}catch(e){}setBtn();o.onPos(T.pos,T.cur(),false)};
 T.toggle=()=>T.on?T.pause():T.play();
 T.seek=t=>{const was=T.on;if(was){T.on=false;cancelAnimationFrame(T.raf);try{piano&&piano.releaseAll()}catch(e){}}T.pos=Math.max(0,t);o.onPos(T.pos,T.cur(),false);if(was)T.play();else setBtn()};
 T.prev=()=>{const u=units();if(!u.length){T.seek(T.pos-2);return}const i=T.cur();T.seek(T.pos-u[i].start>.6?u[i].start:u[Math.max(0,i-1)].start)};
 T.next=()=>{const u=units();if(!u.length){T.seek(T.pos+2);return}const i=T.cur();if(i+1<u.length)T.seek(u[i+1].start);else toast('已經是最後一個')};
 function setBtn(){const b=$(`#${o.id}Play`);if(b){b.textContent=T.on?'⏸ 暫停':'▶ 播放';b.setAttribute('aria-label',T.on?'暫停':'播放')}const tt=$(`#${o.id}Time`);if(tt)tt.textContent=ft(T.pos)}
 T.setBtn=setBtn;return T}
const tpHtml=id=>`<div class="tpbar" id="${id}"><button id="${id}Prev" aria-label="後退">⏮</button><button class="pp" id="${id}Play" aria-label="播放">▶ 播放</button><button id="${id}Next" aria-label="前進">⏭</button><button id="${id}Mark" aria-label="標記">✱ 標記</button><span class="tpt" id="${id}Time">0:00.00</span></div>`;
function wire(T,id,onMark){$(`#${id}Prev`).onclick=T.prev;$(`#${id}Play`).onclick=T.toggle;$(`#${id}Next`).onclick=T.next;$(`#${id}Mark`).onclick=onMark}
const TPS=[];
const _stopAll=stopAll;stopAll=function(){TPS.forEach(t=>t.pause());return _stopAll.apply(this,arguments)};

/* ---------- 豆1: notes ---------- */
const Z={z:1,x:0};const VW=()=>1000/Z.z;
function clampZ(){Z.z=Math.min(12,Math.max(1,Z.z));Z.x=Math.min(1000-VW(),Math.max(0,Z.x))}
let curI=-1,userScrollT=0;
const span=()=>{const N=notes();const s=Math.min(...N.map(n=>n.start)),e=Math.max(...N.map(n=>n.end));return{s,sp:Math.max(.5,e-s)}};
const _rr=renderRoll;
renderRoll=function(cur){const N=notes();if(!N.length){$('#roll').innerHTML='';return}if(cur==null)cur=curI>=0?curI:undefined;
 const {s,sp}=span(),lo=Math.min(...N.map(n=>n.pitch))-1,hi=Math.max(...N.map(n=>n.pitch))+1,rg=Math.max(1,hi-lo),W=1000,H=160;
 $('#rollLbl').textContent='旋律的高低起伏'+(Z.z>1?`（放大 ${Z.z.toFixed(1)}×，可左右拖）`:'');
 const roll=$('#roll');roll.setAttribute('viewBox',`${Z.x.toFixed(2)} 0 ${VW().toFixed(2)} ${H}`);
 const ph=TP1?((TP1.pos-s)/sp*W):-10;
 roll.innerHTML=[.25,.5,.75].map(m=>`<line x1="0" x2="${W}" y1="${m*H}" y2="${m*H}" stroke="rgba(255,255,255,.08)"/>`).join('')+N.map((n,i)=>{const ed=n.pitch!==S.orig[i],mk=S.marks.has(i),x=(n.start-s)/sp*W,w=Math.max(3/Z.z,(n.end-n.start)/sp*W);
  return (mk?`<rect x="${x.toFixed(1)}" y="0" width="${w.toFixed(1)}" height="${H}" fill="rgba(255,159,90,.18)" pointer-events="none"/>`:'')+`<rect x="${x.toFixed(1)}" y="${((hi-n.pitch)/rg*H).toFixed(1)}" width="${w.toFixed(1)}" height="${Math.max(4,H/rg).toFixed(1)}" rx="2" fill="${i===cur?'#fff':mk?'#FF9F5A':ed?'#FFD479':'#B9E59A'}" ${mk?'stroke="#FFB07A" stroke-width="2" vector-effect="non-scaling-stroke"':''} data-ri="${i}"/>`}).join('')+
  `<line id="rollPh" x1="${ph}" x2="${ph}" y1="0" y2="${H}" stroke="rgba(255,255,255,.55)" stroke-width="1.5" vector-effect="non-scaling-stroke" pointer-events="none"/>`};
function phMove(t){const l=$('#rollPh');if(!l||!notes().length)return;const {s,sp}=span(),x=((t-s)/sp*1000).toFixed(1);l.setAttribute('x1',x);l.setAttribute('x2',x);
 if(TP1.on&&Z.z>1){const v=VW();if(x<Z.x||x>Z.x+v*.85){Z.x=x-v*.15;clampZ();$('#roll').setAttribute('viewBox',`${Z.x} 0 ${v} 160`)}}}
const _row=rowHtml;
rowHtml=function(n,i){return _row(n,i).replace(/^<td>\d+<\/td>/,`<td><button class="mkb" data-mk="${i}" aria-label="標記">${S.marks.has(i)?'✱':''}${i+1}</button></td>`)};
function applyMarks(){$$('#ntab tr').forEach(tr=>{const i=+tr.dataset.i;tr.classList.toggle('mk',S.marks.has(i));tr.classList.toggle('cur',i===curI)})}
const _rn=renderNotes;renderNotes=function(){_rn();applyMarks();updMkCount()};
function updMkCount(){const c=$('#mkCnt');if(c)c.textContent=S.marks.size?`（${S.marks.size}）`:''}
function scrollRow(i,force){const w=$('.ntabw'),r=$(`#ntab tr[data-i="${i}"]`);if(!w||!r||!w.offsetParent)return;if(!force&&now()-userScrollT<3)return;
 const top=r.offsetTop-w.clientHeight/2+r.offsetHeight/2;if(Math.abs(w.scrollTop-top)>r.offsetHeight*.5)w.scrollTo({top,behavior:'smooth'})}
['wheel','touchstart','pointerdown'].forEach(ev=>document.addEventListener(ev,e=>{if(e.target.closest&&e.target.closest('.ntabw'))userScrollT=now()},{passive:true}));
function setCur(i,scroll){const rr=$(`#ntab tr[data-i="${i}"]`);if(i===curI&&(!rr||rr.classList.contains('cur')))return;curI=i;$$('#ntab tr.cur').forEach(r=>r.classList.remove('cur'));const r=$(`#ntab tr[data-i="${i}"]`);if(r)r.classList.add('cur');renderRoll(i);if(scroll)scrollRow(i)}
var TP1=makeTP({id:'tp1',units:()=>notes(),onPos:(t,i,on)=>{setCur(i,on);phMove(t);TP1.setBtn()}});TPS.push(TP1);
hl=function(i){curI=-1;setCur(i,false);if(!TP1.on){TP1.pos=notes()[i]?notes()[i].start:0;TP1.setBtn();phMove(TP1.pos)}};
function toggleMark(i){if(!notes()[i])return;if(S.marks.has(i)){S.marks.delete(i);toast(`取消標記第 ${i+1} 個音`)}else{S.marks.add(i);toast(`已標記第 ${i+1} 個音 ✱`)}
 const tr=$(`#ntab tr[data-i="${i}"]`);if(tr){tr.innerHTML=rowHtml(notes()[i],i)}applyMarks();renderRoll();updMkCount()}
// UI insertion
$('#roll').insertAdjacentHTML('afterend',`<div class="rollz" style="margin-top:6px"><span style="font-size:12px;color:var(--mute);margin-right:auto">點音條可跳到那個音</span><button class="zbtn" id="zOut" aria-label="縮小">−</button><button class="zbtn" id="zIn" aria-label="放大">+</button></div>`+tpHtml('tp1'));
wire(TP1,'tp1',()=>{if(!notes().length){toast('還沒有旋律');return}toggleMark(TP1.cur())});
$('#ntab').closest('.ntabw').insertAdjacentHTML('beforebegin',`<label class="mkf"><input type="checkbox" id="onlyMk" style="width:22px;height:22px">只看標記<span id="mkCnt"></span></label>`);
$('#onlyMk').onchange=e=>{$('.ntab').classList.toggle('onlymk',e.target.checked);if(e.target.checked&&!S.marks.size)toast('還沒有標記，播放時按 ✱ 標記')};
$('#dlMid1').insertAdjacentHTML('afterend','<button class="mini" id="saveDraft1">💾 儲存草稿</button>');
$('#replayAll').onclick=()=>{if(!notes().length){toast('還沒有旋律');return}TP1.seek(0);TP1.play()};
const _nc=$('#ntab').onclick;$('#ntab').onclick=e=>{const m=e.target.closest('[data-mk]');if(m){toggleMark(+m.dataset.mk);return}_nc(e);const tr=e.target.closest('tr');if(tr&&!e.target.closest('button'))TP1.seek(notes()[+tr.dataset.i].start)};
$('#undoBtn').addEventListener('click',()=>{applyMarks()});
const _rs=$('#resetBtn').onclick;$('#resetBtn').onclick=()=>{if(!S.notes){toast('還沒有旋律');return}_rs();toast('已重設，回到原本的音')};
const _ud=$('#undoBtn').onclick;$('#undoBtn').onclick=()=>{const had=S.hist.length;_ud();if(had)toast('已復原');applyMarks()};
function zoom(f,cx){const v=VW(),c=cx==null?Z.x+v/2:cx;Z.z*=f;clampZ();Z.x=c-(c-Z.x)*(v/Z.z/v)*1;Z.x=c-(c-Z.x)/f;clampZ();renderRoll()}
$('#zIn').onclick=()=>zoom(1.5);$('#zOut').onclick=()=>{zoom(1/1.5);if(Z.z===1)toast('已縮到最小')};
(()=>{const R=$('#roll'),P=new Map();let g=null;
 const sx=e=>{const b=R.getBoundingClientRect();return{px:e.clientX-b.left,w:b.width}};
 R.addEventListener('pointerdown',e=>{R.setPointerCapture(e.pointerId);P.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(P.size===1)g={mode:'tap',x0:e.clientX,zx:Z.x,t:e.target};else if(P.size===2){const [a,b]=[...P.values()];g={mode:'pinch',d0:Math.abs(a.x-b.x)+1,z0:Z.z,zx:Z.x,mid:(a.x+b.x)/2}}});
 R.addEventListener('pointermove',e=>{if(!P.has(e.pointerId)||!g)return;P.set(e.pointerId,{x:e.clientX,y:e.clientY});const {w}=sx(e);
  if(g.mode!=='pinch'&&P.size===1){const dx=e.clientX-g.x0;if(Math.abs(dx)>6)g.mode='pan';if(g.mode==='pan'){Z.x=g.zx-dx*VW()/w;clampZ();R.setAttribute('viewBox',`${Z.x} 0 ${VW()} 160`)}}
  else if(g.mode==='pinch'&&P.size===2){const [a,b]=[...P.values()],d=Math.abs(a.x-b.x)+1,bb=R.getBoundingClientRect(),c=g.zx+(g.mid-bb.left)/bb.width*(1000/g.z0);
   Z.z=g.z0*d/g.d0;clampZ();Z.x=c-(g.mid-bb.left)/bb.width*VW();clampZ();R.setAttribute('viewBox',`${Z.x} 0 ${VW()} 160`)}});
 const up=e=>{if(!P.has(e.pointerId))return;P.delete(e.pointerId);if(!g)return;
  if(g.mode==='tap'&&P.size===0){const {px,w}=sx(e),vx=Z.x+px/w*VW(),N=notes();if(N.length){const {s,sp}=span(),t=s+vx/1000*sp;
    let i=g.t&&g.t.dataset&&g.t.dataset.ri!=null?+g.t.dataset.ri:-1;if(i<0){let bd=1e9;N.forEach((n,k)=>{const d=t<n.start?n.start-t:t>n.end?t-n.end:0;if(d<bd){bd=d;i=k}})}
    jumpTo(i)}}
  if(P.size===0){if(g.mode!=='tap')renderRoll();g=null}};
 R.addEventListener('pointerup',up);R.addEventListener('pointercancel',up);
 R.addEventListener('wheel',e=>{if(!e.ctrlKey)return;e.preventDefault();zoom(e.deltaY<0?1.2:1/1.2)},{passive:false})})();
function jumpTo(i){const d=$('#ntab').closest('details');if(d&&!d.open)d.open=true;if($('#onlyMk').checked&&!S.marks.has(i)){$('#onlyMk').checked=false;$('.ntab').classList.remove('onlymk')}
 TP1.seek(notes()[i].start);curI=-1;setCur(i,false);requestAnimationFrame(()=>scrollRow(i,true));if(!TP1.on)audition(notes()[i].pitch,.5)}

/* ---------- 豆2: lyrics ---------- */
const lunits=()=>S.align.filter(a=>a.start!=null);
let curL=-1;
var TP2=makeTP({id:'tp2',units:lunits,onPos:(t,i,on)=>{const u=lunits(),a=u[i];const k=a?S.align.indexOf(a):-1;
  if(k!==curL){curL=k;$$('#alignOut .alr').forEach(r=>r.classList.toggle('cur',+r.dataset.li===k));const el=$(`#alignOut .alr[data-li="${k}"]`);if(on&&el&&now()-userPageT>3){const b=el.getBoundingClientRect();if(b.top<80||b.bottom>innerHeight-140)el.scrollIntoView({block:'center',behavior:'smooth'})}}
  $('#lyrNow').textContent=a&&(t>=a.start-.05||!on)?a.text:'';TP2.setBtn()},onEnd:()=>{$('#lyrNow').textContent=''}});TPS.push(TP2);
let userPageT=0;['wheel','touchstart'].forEach(ev=>addEventListener(ev,()=>userPageT=now(),{passive:true}));
$('#alignOut').insertAdjacentHTML('beforebegin',`<div id="tp2wrap" class="hidden"><div class="sub" style="font-size:13.5px;margin:10px 0 0">用 ◀ ▶ 讓字幕早／晚 0.1 秒，下排是 0.01 秒細調。✱ 標記要再改的句子。</div>${tpHtml('tp2')}<label class="mkf"><input type="checkbox" id="onlyLMk" style="width:22px;height:22px">只看標記<span id="lmkCnt"></span></label></div>`);
$('#alignOut').insertAdjacentHTML('afterend',`<div class="row hidden" id="b2dl" style="flex-wrap:wrap;gap:8px;margin-top:10px"><button class="mini" id="saveDraft2">💾 儲存草稿</button><button class="mini" id="dlSrt">⬇ 下載字幕 .srt</button><button class="mini" id="dlLrc2">⬇ 下載字幕 .lrc</button></div>`);
function toggleLMark(k){if(k<0||!S.align[k])return;S.lmarks.has(k)?(S.lmarks.delete(k),toast(`取消標記第 ${k+1} 句`)):(S.lmarks.add(k),toast(`已標記第 ${k+1} 句 ✱`));renderAlign()}
wire(TP2,'tp2',()=>{if(!lunits().length){toast('先把歌詞配到旋律上');return}toggleLMark(S.align.indexOf(lunits()[TP2.cur()]))});
$('#onlyLMk').onchange=e=>{renderAlign();if(e.target.checked&&!S.lmarks.size)toast('還沒有標記的句子')};
const _ra=renderAlign;
renderAlign=function(){_ra();const has=S.align.length>0;$('#tp2wrap').classList.toggle('hidden',!has);$('#b2dl').classList.toggle('hidden',!has);
 const only=$('#onlyLMk').checked;$$('#alignOut .alr').forEach((r,k)=>{const a=S.align[k];r.dataset.li=k;r.classList.toggle('mk',S.lmarks.has(k));r.classList.toggle('cur',k===curL);if(only&&!S.lmarks.has(k))r.style.display='none';
  const t=r.querySelector('.t');if(t)t.textContent=a.start!=null?ft(a.start):'—';
  if(a.start!=null)r.insertAdjacentHTML('beforeend',`<div class="ndg"><button data-nd="-0.1" aria-label="提早 0.1 秒">◀ 0.1</button><button data-nd="0.1" aria-label="延後 0.1 秒">0.1 ▶</button><button class="f" data-nd="-0.01">◀.01</button><button class="f" data-nd="0.01">.01▶</button><button class="lmk" data-lmk="${k}" aria-label="標記這句">${S.lmarks.has(k)?'✱ 已標記':'✱'}</button></div>`)});
 const c=$('#lmkCnt');if(c)c.textContent=S.lmarks.size?`（${S.lmarks.size}）`:''};
const _ac=$('#alignOut').onclick;
$('#alignOut').onclick=e=>{const nd=e.target.closest('[data-nd]'),lm=e.target.closest('[data-lmk]');
 if(lm){toggleLMark(+lm.dataset.lmk);return}
 if(nd){const r=nd.closest('.alr'),k=+r.dataset.li,a=S.align[k],d=+nd.dataset.nd;const prev=S.align.slice(0,k).filter(x=>x.start!=null).pop();
  a.start=r2(Math.min(a.end-.05,Math.max(prev?prev.start+.05:0,a.start+d)));r.querySelector('.t').textContent=ft(a.start);toast(`第 ${k+1} 句 ${ft(a.start)}`,900);return}
 const b=e.target.closest('[data-al]');if(b){const a=S.align[+b.dataset.al];if(a&&a.start!=null){TP2.pos=a.start;TP2.setBtn()}}
 _ac(e)};
// hold a fine-nudge button to repeat
(()=>{let tm=0,iv=0;const clr=()=>{clearTimeout(tm);clearInterval(iv)};$('#alignOut').addEventListener('pointerdown',e=>{const b=e.target.closest('[data-nd]');if(!b)return;clr();tm=setTimeout(()=>{iv=setInterval(()=>b.click(),110)},450)});['pointerup','pointercancel','pointerleave'].forEach(ev=>$('#alignOut').addEventListener(ev,clr))})();
const LEAD=0; // no subtitle-lead setting exists in this app; exported times are exactly what is shown
function srt(){const L=S.align.filter(a=>a.start!=null),f=t=>{t=Math.max(0,t);const h=Math.floor(t/3600),m=Math.floor(t/60)%60,s=Math.floor(t%60),ms=Math.round((t-Math.floor(t))*1000)%1000;return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')},${String(ms).padStart(3,'0')}`};
 return L.map((a,i)=>{const e=Math.max(a.start+.3,Math.min(a.end+.5,L[i+1]?L[i+1].start:a.end+.5));return `${i+1}\n${f(a.start-LEAD)} --> ${f(e-LEAD)}\n${a.text}\n`}).join('\n')}
const nm=()=>($('#title').value||'lyrics');
$('#dlSrt').onclick=()=>{if(!S.align.length){toast('先把歌詞配到旋律上');return}dlBlob(new Blob([srt()],{type:'text/plain'}),nm()+'.srt');toast('已下載字幕 .srt')};
$('#dlLrc2').onclick=()=>{if(!S.align.length){toast('先把歌詞配到旋律上');return}dlBlob(new Blob([ALIGN.toLRC(S.align,-LEAD)],{type:'text/plain'}),nm()+'.lrc');toast('已下載字幕 .lrc')};
$('#lyrics').addEventListener('input',()=>{if(!S.align.length){S.lmarks.clear();$('#tp2wrap').classList.add('hidden');$('#b2dl').classList.add('hidden');TP2.pause()}});

/* ---------- drafts ---------- */
const key=()=>'doujia.draft.'+(S.pod||'local');
function saveDraft(){if(!notes().length&&!S.align.length){toast('還沒有可以存的內容');return}
 const d={v:1,t:Date.now(),n:notes().length,pitches:notes().map(n=>n.pitch),marks:[...S.marks],align:S.align.map(a=>({...a})),lmarks:[...S.lmarks],lyrics:$('#lyrics').value};
 try{localStorage.setItem(key(),JSON.stringify(d));toast('草稿已儲存在這支手機')}catch(e){toast('存不了草稿（瀏覽器空間不足）')}}
$('#saveDraft1').onclick=saveDraft;$('#saveDraft2').onclick=saveDraft;
function restoreDraft(){let d;try{d=JSON.parse(localStorage.getItem(key())||'null')}catch(e){}if(!d)return false;let ok=false;
 if(d.pitches&&d.n===notes().length&&notes().length){S.notes.forEach((n,i)=>n.pitch=d.pitches[i]);S.marks=new Set(d.marks||[]);renderNotes();ok=true}
 if(d.align&&d.align.length){S.align=d.align;$('#lyrics').value=d.lyrics||d.align.map(a=>a.text).join('\n');S.lmarks=new Set(d.lmarks||[]);S.done[1]=true;S.noLyrics=false;renderAlign();try{syncTabs()}catch(e){}ok=true}
 if(!ok)return false;const dt=new Date(d.t),when=`${dt.getMonth()+1}/${dt.getDate()} ${String(dt.getHours()).padStart(2,'0')}:${String(dt.getMinutes()).padStart(2,'0')}`;
 const msg=`已載入你 ${when} 存的草稿`;$$('.drn').forEach(x=>x.remove());
 [$('#ncount').closest('.card'),$('#alignOut').closest('.card')].forEach(c=>c&&c.insertAdjacentHTML('afterbegin',`<div class="banner drn">${msg}・<button class="link" data-drop style="font-size:12.5px">捨棄草稿</button></div>`));
 $$('[data-drop]').forEach(b=>b.onclick=()=>{localStorage.removeItem(key());$$('.drn').forEach(x=>x.remove());toast('已捨棄草稿，重新整理後回到原本的版本')});
 setTimeout(()=>toast(msg),2600);return true}
let tries=0;const iv=setInterval(()=>{tries++;if(S._loading===false&&(S.pod||notes().length)){clearInterval(iv);restoreDraft()}else if(tries>120)clearInterval(iv)},250);
window.BOB={TP1,TP2,restoreDraft,saveDraft,srt,Z};
})();
