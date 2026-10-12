/* Bob round 2: melody-aware accompaniment + drums, light video export, multi-image picker, work page from current state */
(()=>{
const css=`.drumrow{display:flex;gap:6px;align-items:center;margin-top:10px}.drumrow .lb{font-size:15px;min-width:30px}.drumrow .seg{flex:1;margin:0}
.litev{display:flex;gap:10px;align-items:flex-start;margin-top:12px;font-size:15px}.litev input{width:22px;height:22px;flex:none;margin-top:1px}.litev small{display:block;font-size:12.5px;color:var(--mute);margin-top:2px}`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

/* ---------- 豆3 accompaniment ---------- */
const SAL='https://tonejs.github.io/audio/salamander/',DR='https://tonejs.github.io/audio/drum-samples/acoustic-kit/';
const PN=['A0','C1','D#1','F#1','A1','C2','D#2','F#2','A2','C3','D#3','F#3','A3','C4','D#4','F#4','A4','C5','D#5','F#5','A5','C6'];
let bank=null;
function loadBank(){if(bank)return bank;bank=(async()=>{const get=u=>Tone.ToneAudioBuffer.fromUrl(u).then(b=>b.get());
 const P={};await Promise.all(PN.map(async n=>{P[n]=await get(SAL+n.replace('#','s')+'.mp3')}));
 const D={};await Promise.all(['kick','snare','hihat'].map(async k=>{try{D[k]=await get(DR+k+'.mp3')}catch(e){console.warn('drum',k,e)}}));return {P,D}})();bank.catch(()=>bank=null);return bank}
S.drums=0;
$('#styles').insertAdjacentHTML('afterend',`<div class="drumrow"><span class="lb">鼓</span><div class="seg" id="drumSeg"><button class="on" data-dr="0">無</button><button data-dr="1">弱</button><button data-dr="2">中</button><button data-dr="3">強</button></div></div>`);
async function renderAuto2(){const r=ACC2.arrange(S.notes,S.style,S.drums),{P,D}=await loadBank(),sh=r.shift,base=r.introStart+sh; // acc time 0 == intro downbeat
 const out=await Tone.Offline(()=>{const rel=S.style==='抒情'?2.2:S.style==='溫暖'?1.2:.8;const smp=new Tone.Sampler({urls:P,release:rel}).toDestination();smp.volume.value=-4;
  for(const x of r.ev)smp.triggerAttackRelease(Tone.Frequency(x.p,'midi').toNote(),x.d,Math.max(0,x.s+sh-base),x.v);
  const dg=new Tone.Gain(.9).toDestination();for(const h of r.hits){if(!D[h.k])continue;const s=new Tone.ToneBufferSource(D[h.k]).connect(new Tone.Gain(h.v).connect(dg));s.start(Math.max(0,h.s+sh-base))}
 },r.end+sh-base+2,2,44100);
 return {buf:out.get(),r,ms:sh-base+0}}
let busy=false,again=false;
async function doAuto(){if(busy){again=true;return}if(!S.notes){toast('要先哼一段，才能配伴奏');return}busy=true;const b=$('#autoIntro'),old='✨ 幫我配伴奏';b.disabled=true;b.textContent='配伴奏中…（第一次要下載鋼琴音色）';
 try{stopAll();const {buf,r}=await renderAuto2();S.acc=buf;S.accName=S.style+'伴奏';S.introMode='auto';S.accMeta=r;
  // vocal enters after the one-bar intro: vocal t=0 sits at acc time (shift - introStart - shift)=-introStart
  S.offset=Math.round((-r.introStart)*1000)/1000;showOff();
  const kn=r.key.endsWith('m')?r.key.slice(0,-1)+' 小調':r.key+' 大調';
  $('#offSrc').textContent=`已加一小節前奏，照你的速度（約 ${r.bpm} BPM）跟著走`;$('#accInfo').textContent=`🎹 ${S.style}伴奏配好了・${kn}・${r.bpm} BPM${S.drums?'・鼓 '+['','弱','中','強'][S.drums]:''}，按下面 ▶ 試聽`;
  toast('伴奏配好了！');$('#accCtl').style.opacity=1;$('#accCtl').style.pointerEvents='auto';S.done[2]=true;syncTabs();credits()}
 catch(e){console.warn(e);toast('鋼琴音色載入不了，請檢查網路再試')}finally{busy=false;if(again){again=false;return doAuto()}b.disabled=false;b.textContent=old}}
$('#autoIntro').onclick=doAuto;
const regen=()=>{if(S.acc&&S.introMode==='auto'){const was=playing==='mix';doAuto().then(()=>{if(was)$('[data-play="mix"]').click()})}};
$$('#styles .sty').forEach(b=>{const o=b.onclick;b.onclick=()=>{const prev=S.style;o();if(S.style!==prev)regen()}});
$$('#drumSeg button').forEach(b=>b.onclick=()=>{$$('#drumSeg button').forEach(x=>x.classList.toggle('on',x===b));S.drums=+b.dataset.dr;toast('鼓：'+b.textContent);regen()});

/* ---------- 豆4 light export ---------- */
$('#makeVid').insertAdjacentHTML('beforebegin',`<label class="litev"><input type="checkbox" id="liteVid" checked><span>輕量分享版<small>檔案約小一半，適合 LINE、IG、抖音、YouTube</small></span></label>`);
$('#liteVid').onchange=e=>toast(e.target.checked?'輕量分享版（720p・約 1.8 Mbps）':'高畫質（720p・約 4 Mbps）');
window.BOBV=()=>$('#liteVid').checked?{v:1.8e6,a:128000}:{v:4e6,a:192000};

/* ---------- 豆4 multi image ---------- */
const fi=$('#imgFile');fi.multiple=true;
fi.onchange=e=>{const fs=[...e.target.files];e.target.value='';if(!fs.length)return;const room=5-S.imgs.length;fs.slice(0,room).forEach(f=>S.imgs.push(URL.createObjectURL(f)));renderThs();
 toast(fs.length>room?`最多 5 張，只加了前 ${Math.max(0,room)} 張`:`加了 ${fs.length} 張圖`)};

/* ---------- work page (預覽分享頁) from current state ---------- */
const L=$('#v-landing');
function fillLanding(){if(!(S.notes||S.raw))return;const t=$('#title').value||'未命名',who=S.name||S.singer||'你';
 L.querySelector('.land-hero').style.backgroundImage=`url(${S.imgs[0]||'img/cover.jpg'})`;
 const h=L.querySelector('.h1');if(h)h.textContent=t;const by=h&&h.previousElementSibling;if(by)by.textContent=`${who} 分享了一首歌`;
 const sub=h&&h.nextElementSibling;if(sub)sub.textContent=creditList().slice(1).filter(c=>/^(唱|詞|伴奏|影片)：/.test(c)).join('・');
 const pp=L.querySelector('.people');if(pp)pp.innerHTML=[['🎤','唱',S.singer||S.name||'你'],['✍️','詞',S.align.length?(S.lyricist||S.name||'你'):'（只有哼）'],['🎹','伴奏',S.acc?(S.accBy||S.name||'你'):'—'],['🎬','影片',S.name||'你']].map(([i,k,v])=>`<div>${i} ${k}：${v}</div>`).join('');
 const mb=$('#moreBtn');if(mb)mb.textContent='更多作品（即將推出）';const ch=L.querySelector('.chip');if(ch)ch.textContent=shortLink();
 const tm=L.querySelector('[data-time="land"]');if(tm)tm.textContent='0:00 / '+fmt(landDur())}
function landDur(){const pl=placement();const v=S.raw?vocalBuf():null;return Math.max(v?pl.vocAt+v.duration:0,S.acc?(pl.accAt+S.acc.duration):0,S.notes?S.notes[S.notes.length-1].end:0)}
const _show=show;show=function(id){const r=_show.apply(this,arguments);if(id==='landing')fillLanding();return r};
$('[data-play="land"]').onclick=()=>{if(playing==='land'){stopAll();return}if(!(S.notes||S.raw)){toast('這是範例頁，做好作品後會換成你的歌');return}
 const pl=placement(),v=S.raw?vocalBuf():null;playScore({key:'land',mel:!v,voice:v,vocAt:S.acc?pl.vocAt:0,acc:S.acc,accAt:pl.accAt,vg:+$('#vocVol').value,ag:+$('#accVol').value,wet:!!v})};
window.BOB2={renderAuto2,fillLanding,loadBank};
})();
