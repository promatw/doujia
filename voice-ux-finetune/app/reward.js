/* 陽光獎勵（示範資料，UX 用；不接後端） */
(function(){
const LV=[['豆子',0],['豆苗',120],['豆藤',300],['豆莢',800],['天空之藤',2000]];
const R=window.REWARD={sun:+(localStorage.getItem('hum.sun')||100),
 level(s=R.sun){let l=0;LV.forEach((x,i)=>{if(s>=x[1])l=i});return l},
 levels:LV};
const css=`.sunb{position:absolute;top:52px;right:16px;z-index:60;height:30px;padding:0 11px;border-radius:15px;border:1px solid rgba(255,214,120,.45);background:rgba(40,36,16,.75);color:#FFE7A0;font-size:14px;font-weight:700;display:flex;align-items:center;gap:4px;cursor:pointer;font-family:inherit;backdrop-filter:blur(8px)}
.sunb.fixed{position:fixed}
.rmask{position:fixed;inset:0;z-index:200;background:rgba(0,0,0,.55);display:none;align-items:center;justify-content:center;padding:20px}
.rmask.on{display:flex}
.rcard{width:100%;max-width:340px;background:linear-gradient(170deg,#183326,#0B1411);border:1px solid rgba(185,229,154,.3);border-radius:22px;padding:20px;color:#F1F1E6;font-size:14.5px;line-height:1.7;position:relative;box-shadow:0 20px 50px rgba(0,0,0,.5)}
.rcard h3{margin:0 0 6px;font-size:20px;font-family:"Noto Serif TC",serif}
.rcard ul{margin:6px 0;padding-left:20px}.rcard .x{position:absolute;top:10px;right:12px;background:none;border:0;color:#F1F1E6;font-size:22px;cursor:pointer}
.rlv{display:flex;gap:4px;margin-top:8px}.rlv span{flex:1;text-align:center;font-size:11.5px;padding:6px 2px;border-radius:10px;background:rgba(255,255,255,.05);color:#9AA8A1}.rlv span.on{background:rgba(255,214,120,.2);color:#FFE7A0;font-weight:700}
.plus{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%) scale(.6);opacity:0;z-index:210;background:linear-gradient(160deg,#FFE9A8,#F6C85F);color:#3a2a05;border-radius:22px;padding:16px 26px;font-size:22px;font-weight:800;text-align:center;box-shadow:0 0 50px rgba(255,214,120,.5);transition:.35s cubic-bezier(.3,1.6,.5,1);pointer-events:none}
.plus small{display:block;font-size:13px;font-weight:600}.plus.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
.cert{text-align:center;border:2px solid rgba(255,214,120,.55);background:radial-gradient(120% 80% at 50% 0%,#2a4a33,#0B1411)}
.cert .big{font-size:56px;line-height:1.1}.cert .lv{font-family:"Noto Serif TC",serif;font-size:30px;color:#FFE7A0;letter-spacing:4px;margin:4px 0}
.rbtn{display:block;width:100%;margin-top:12px;height:46px;border-radius:23px;border:0;background:#B9E59A;color:#13261B;font-weight:700;font-size:16px;cursor:pointer;font-family:inherit}`;
document.head.insertAdjacentHTML('beforeend',`<style>${css}</style>`);
const mask=document.createElement('div');mask.className='rmask';mask.id='rmask';document.body.appendChild(mask);
mask.onclick=e=>{if(e.target===mask||e.target.closest('.x'))R.close()};
const plus=document.createElement('div');plus.className='plus';plus.id='rplus';document.body.appendChild(plus);
R.close=()=>mask.classList.remove('on');
R.open=html=>{mask.innerHTML=`<div class="rcard">${html}<button class="x" aria-label="關閉">×</button></div>`;mask.classList.add('on')};
R.lvBar=()=>`<div class="rlv">${LV.map((x,i)=>`<span class="${i===R.level()?'on':''}">${x[0]}</span>`).join('')}</div>`;
R.info=()=>R.open(`<h3>☀️ 陽光</h3>陽光是照在豆芽上的光，讓你的豆子慢慢長大。
<ul><li>完成一個步驟</li><li>幫別人接歌</li><li>作品被按 ❤️、你被訂閱 🔔</li><li>別人送你 👏</li></ul>都會得到陽光。
陽光可以送給別人，<b>不能買，也不能換成現金</b>。<div style="margin-top:8px">你現在有 <b style="color:#FFE7A0">${R.sun}</b> 點・<b>${LV[R.level()][0]}</b></div>${R.lvBar()}
<div style="font-size:12px;color:#9AA8A1;margin-top:4px">${LV.slice(1).map(x=>x[0]+' '+x[1]).join('・')}</div>`);
R.sync=()=>{document.querySelectorAll('.sunv').forEach(e=>e.textContent=R.sun);localStorage.setItem('hum.sun',R.sun);R.onChange&&R.onChange()};
R.cert=(i)=>R.open(`<div class="cert" style="margin:-20px;padding:24px 20px;border-radius:22px"><div style="font-size:13px;color:#B9E59A;letter-spacing:3px">哼哼・豆莢浪歌　升級證書</div><div class="big">🌱</div><div>恭喜 <b>${(window.S&&S.name)||'你'}</b> 成為</div><div class="lv">${LV[i][0]}</div><div style="font-size:13px;color:#C9D0CB">累積 ${R.sun} 點陽光・${new Date().toLocaleDateString('zh-TW',{timeZone:'Asia/Taipei'})}</div>
<button class="rbtn" id="certShare">📤 分享證書</button></div>`);
R.add=(n,why)=>{const before=R.level();R.sun+=n;R.sync();plus.innerHTML=`+${n} ☀️ 陽光<small>${why||''}</small>`;plus.classList.add('on');clearTimeout(plus._t);
 plus._t=setTimeout(()=>{plus.classList.remove('on');const after=R.level();if(after>before)R.cert(after)},1500)};
document.addEventListener('click',e=>{if(e.target.closest('[data-sun]'))R.info();if(e.target.id==='certShare'){const t='我在哼哼・豆莢浪歌升級了！';if(navigator.share)navigator.share({text:t}).catch(()=>{});else{navigator.clipboard&&navigator.clipboard.writeText(t).catch(()=>{});e.target.textContent='✓ 已複製，可以貼到社群'}}});
R.badge=(parent,fixed)=>{const b=document.createElement('button');b.className='sunb'+(fixed?' fixed':'');b.dataset.sun='';if(!document.getElementById('sunBadge'))b.id='sunBadge';b.innerHTML='☀️ <b class="sunv"></b>';parent.appendChild(b);R.sync();return b};
})();
