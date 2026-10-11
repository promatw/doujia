from gen import *
CSS=r'''
:root{--paper:#EDEAE2;--ink:#0F0F10;--mute:#77736C;--cob:#2142FF;--line:rgba(15,15,16,.85);
--sans:"Noto Sans CJK TC",sans-serif;--disp:"Archivo Black","Noto Sans CJK TC",sans-serif;--mono:"Space Mono","Noto Sans Mono CJK TC",monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1400px;background:#D8D4CA;color:var(--ink);font-family:var(--sans)}
.page{padding:50px 70px 60px;position:relative;overflow:hidden}
.pgrain{position:absolute;inset:0;width:100%;height:100%;opacity:.22;mix-blend-mode:multiply;pointer-events:none}
.head{display:grid;grid-template-columns:auto 1fr auto;gap:40px;align-items:end;margin-bottom:58px;position:relative;border-bottom:2px solid var(--ink);padding-bottom:22px}
.big{font-weight:700;font-size:64px;letter-spacing:-1px;line-height:.95}
.kick{font-family:var(--mono);font-size:12px;letter-spacing:2px;margin-bottom:12px}
.kick b{background:var(--cob);color:#fff;padding:2px 8px;font-weight:700}
.sl{font-size:15px;letter-spacing:4px;font-weight:700}
.iconset{display:flex;gap:22px}
.iconset figure{font-family:var(--mono);font-size:10px;text-align:center}
.iconset svg{width:36px;height:36px;display:block;margin:0 auto 6px;stroke-width:1.6}
.pal{display:flex;gap:0;margin-bottom:14px;justify-content:flex-end}.pal i{width:40px;height:22px;border:1.5px solid var(--ink);margin-left:-1.5px}
.row{display:flex;gap:45px;justify-content:center;position:relative}
.wrap{position:relative}
.cap{position:absolute;top:-30px;left:0;right:0;display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;letter-spacing:1px}
.phone{width:390px;height:844px;border-radius:50px;background:var(--paper);position:relative;overflow:hidden;
 box-shadow:0 0 0 8px var(--ink),0 30px 60px rgba(0,0,0,.18)}
.grain{position:absolute;inset:0;width:100%;height:100%;opacity:.28;mix-blend-mode:multiply;pointer-events:none;z-index:9}
.island{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:118px;height:34px;border-radius:20px;background:#000;z-index:10}
.status{height:54px;display:flex;justify-content:space-between;align-items:center;padding:6px 32px 0 38px;font-weight:700;font-size:15px;font-family:"Inter",sans-serif}
.status i{display:inline-block;width:24px;height:11px;border:1.5px solid currentColor;border-radius:4px;position:relative}
.status i:after{content:"";position:absolute;inset:1.5px 6px 1.5px 1.5px;background:currentColor;border-radius:1px}
.homebar{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:var(--ink);z-index:11}
.mast{display:flex;justify-content:space-between;align-items:center;margin:10px 24px 0;padding-bottom:8px;border-bottom:1.5px solid var(--ink);font-family:var(--mono);font-size:10.5px;letter-spacing:1px}
.mono{font-family:var(--mono)}
.btn{height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;font-size:19px;font-weight:700;letter-spacing:6px;border-radius:3px}
.btn.ink{background:var(--ink);color:var(--paper)}
.btn.cob{background:var(--cob);color:#fff}
.btn .ar{font-family:var(--mono);letter-spacing:0;font-weight:400;font-size:20px}
.prog{position:relative;width:300px;margin:0 auto}
.prog svg{width:300px;height:56px;display:block}
.prog .lbl{position:relative;height:16px}
.prog .lbl span{position:absolute;transform:translateX(-50%);font-size:11px;font-weight:700;letter-spacing:1px;white-space:nowrap;color:var(--mute)}
.prog .lbl span.on{color:var(--cob)}
.tabbar{position:absolute;left:0;right:0;bottom:0;height:96px;border-top:1.5px solid var(--ink);background:var(--paper);display:flex;justify-content:space-around;padding:12px 18px 0;z-index:8}
.tab{width:64px;height:52px;display:flex;align-items:center;justify-content:center;position:relative;color:var(--ink)}
.tab svg{width:32px;height:32px;stroke-width:1.6}
.tab.on{color:var(--cob)}
.tab.on:after{content:"";position:absolute;top:-13px;width:28px;height:4px;background:var(--cob)}
.pill{display:inline-flex;align-items:center;gap:10px;padding:8px 16px 8px 12px;border-radius:99px;background:var(--ink);color:var(--paper);font-size:13px;font-weight:700;letter-spacing:1px}
.pill i{width:8px;height:8px;border-radius:50%;background:var(--cob);box-shadow:0 0 0 3px rgba(33,66,255,.35)}
.reg{position:absolute;width:14px;height:14px}
.foot{margin-top:56px;display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;letter-spacing:1px;border-top:2px solid var(--ink);padding-top:14px;position:relative}
'''
G='<svg class="grain"><rect width="100%" height="100%" filter="url(#grainF)"/></svg>'
ST='<div class="island"></div><div class="status"><span>9:41</span><i></i></div>'
def reg(x,y):
    return f'<svg class="reg" style="left:{x}px;top:{y}px" viewBox="0 0 14 14"><circle cx="7" cy="7" r="4" fill="none" stroke="#0F0F10" stroke-width="1"/><path d="M7 0v14M0 7h14" stroke="#0F0F10" stroke-width="1"/></svg>'
def barcode(x,y,h=26):
    import random; random.seed(7); s=''; cx=x
    for i in range(34):
        w=random.choice([1,1,1.5,2,3]); s+=f'<rect x="{cx}" y="{y}" width="{w}" height="{h}" fill="#0F0F10"/>'; cx+=w+random.choice([1,1.5,2])
    return s
def logo(w=120):
    return f'''<svg width="{w}" height="{w*0.42}" viewBox="0 0 110 46">
<path d="M10 27C24 9 80 6 102 17 92 38 32 42 10 27z" fill="none" stroke="#0F0F10" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M10 27c-4 0-6-2.5-6-6" fill="none" stroke="#0F0F10" stroke-width="1.6" stroke-linecap="round"/>
<circle cx="35" cy="24.5" r="5.5" fill="#0F0F10"/><circle cx="52" cy="22.5" r="5.5" fill="#0F0F10"/>
<circle cx="69" cy="21.5" r="5.5" fill="#0F0F10"/><circle cx="86" cy="21" r="9" fill="#2142FF" filter="url(#sprayS)"/><circle cx="86" cy="21" r="5.5" fill="#2142FF"/></svg>'''

# ---------- A
A=f'''<div class="phone">{ST}
<div class="mast"><span>DOUJIA LANGE®</span><span>ISSUE Nº001 — 2026</span></div>
<div style="position:relative;height:392px">
 <svg width="390" height="392" viewBox="0 0 390 392" style="position:absolute;inset:0">
  <text x="22" y="318" font-family="Noto Sans CJK TC" font-weight="700" font-size="318" fill="#2142FF" opacity=".75" filter="url(#sprayM)">唱</text>
  <text x="22" y="318" font-family="Noto Sans CJK TC" font-weight="700" font-size="318" fill="#2142FF">唱</text>
  <rect x="0" y="150" width="390" height="5" fill="#EDEAE2"/><rect x="118" y="0" width="5" height="392" fill="#EDEAE2"/><rect x="0" y="246" width="390" height="5" fill="#EDEAE2"/>
  <g transform="rotate(-18 200 220)">
   <path d="M70 250C120 190 300 175 345 215 305 280 125 300 70 250z" fill="none" stroke="#0F0F10" stroke-width="1.6" stroke-linejoin="round"/>
   <path d="M70 250c-14 1-24-8-24-22" fill="none" stroke="#0F0F10" stroke-width="1.6" stroke-linecap="round"/>
   <circle cx="130" cy="244" r="15" fill="#0F0F10"/><circle cx="176" cy="236" r="16" fill="#0F0F10"/><circle cx="224" cy="231" r="16" fill="#0F0F10"/><circle cx="272" cy="229" r="15" fill="none" stroke="#0F0F10" stroke-width="1.6"/>
  </g>
  <g fill="#2142FF"><circle cx="348" cy="70" r="3.4"/><circle cx="360" cy="90" r="4.6"/><circle cx="348" cy="110" r="2.8"/></g>
  <g fill="#0F0F10" opacity=".6"><circle cx="300" cy="40" r="1.2"/><circle cx="310" cy="52" r="0.8"/><circle cx="60" cy="350" r="1.1"/><circle cx="74" cy="360" r=".8"/></g>
  <text x="24" y="378" font-family="Space Mono" font-size="10" letter-spacing="1" fill="#0F0F10">FIG.01 — 你的聲音，就是你的臉。</text>
 </svg>
 <div style="position:absolute;right:20px;top:120px;writing-mode:vertical-rl;font-size:13px;font-weight:700;letter-spacing:6px">隨口唱一首，短短幾秒天下行</div>
</div>
<div style="padding:0 24px">
 <div style="font-size:34px;font-weight:700;line-height:1.2;letter-spacing:1px">只要聲音，<br>不用露臉。</div>
 <div class="mono" style="font-size:10.5px;letter-spacing:1px;margin-top:10px;color:var(--mute)">SING → MELODY → MIX → SHARE</div>
 <div style="margin-top:26px;border:1.5px solid var(--ink);height:62px;border-radius:3px;padding:8px 14px;position:relative">
  <div class="mono" style="font-size:9.5px;letter-spacing:1px">NAME / 名字</div>
  <div style="font-size:19px;color:#9A968E;font-weight:700;margin-top:1px;display:flex;align-items:center;letter-spacing:2px"><span style="width:2px;height:20px;background:var(--cob);margin-right:8px"></span>取個名字</div>
 </div>
 <div class="btn ink" style="margin-top:12px"><span style="display:flex;align-items:center;gap:12px"><i style="width:10px;height:10px;border-radius:50%;background:var(--cob);display:inline-block"></i>開始唱</span><span class="ar">→</span></div>
</div>
<div class="homebar"></div>{G}</div>'''

# ---------- B
ring="TAP TO SING ✳ 點一下開始唱 ✳ TAP TO SING ✳ 點一下開始唱 ✳ TAP TO SING ✳ 點一下開始唱 ✳ "
B=f'''<div class="phone">{ST}
<div class="mast"><span>VOL.01 / SING</span><span>01 — 04</span></div>
<div style="display:flex;align-items:flex-end;justify-content:space-between;padding:18px 24px 0">
 <div style="display:flex;align-items:baseline;gap:10px"><span style="font-size:52px;font-weight:700;line-height:1">唱</span><span style="font-family:var(--disp);font-size:30px;letter-spacing:-.5px">SING</span></div>
 <div class="mono" style="font-size:10px;text-align:right;line-height:1.5">HI, @YUKI_00<br>今日第 3 顆豆</div>
</div>
<div style="margin-top:16px">{prog(0,'#0F0F10','#9A968E','#2142FF')}</div>
<svg width="390" height="350" viewBox="0 0 390 350" style="display:block;margin-top:2px">
 <defs><path id="ringp" d="M195 175 m-140 0 a140 140 0 1 1 280 0 a140 140 0 1 1 -280 0"/></defs>
 <circle cx="195" cy="175" r="118" fill="#2142FF" opacity=".7" filter="url(#sprayL)"/>
 <text font-family="Space Mono" font-size="11" letter-spacing="0" fill="#0F0F10" font-weight="700"><textPath href="#ringp" textLength="872" lengthAdjust="spacing">{ring}</textPath></text>
 <circle cx="195" cy="175" r="104" fill="#2142FF"/>
 <use href="#headO" x="150" y="128" width="86" height="86" style="color:#EDEAE2;stroke-width:2"/>
 <g fill="#EDEAE2"><circle cx="241" cy="153" r="3.4"/><circle cx="251" cy="174" r="4.5"/><circle cx="241" cy="195" r="2.8"/></g>
</svg>
<div style="text-align:center;margin-top:-8px"><span style="font-family:var(--disp);font-size:34px">00:00</span><span class="mono" style="font-size:12px;margin-left:8px">/ 15 SEC</span></div>
<div style="margin:14px 46px 0;border:1.5px dashed var(--ink);padding:9px 0;text-align:center;font-size:13px;font-weight:700;letter-spacing:1px">安靜的地方・手機離嘴約20公分</div>
{tabbar(0)}<div class="homebar"></div>{G}</div>'''

# ---------- C : printed score
seq,tot=notes_seq(); W=322; x0=34; base=170; sp=13
staff=''.join(f'<line x1="18" x2="332" y1="{base-i*2*sp+0}" y2="{base-i*2*sp}" stroke="#0F0F10" stroke-width=".9"/>' for i in range(5))
nt=''; phx=0; phy=0
for i,(t,d,p) in enumerate(seq):
    x=x0+(t+d/2)/tot*W*0.93; y=base+8-p*sp
    r=5+d*1.3
    if i<PH: nt+=f'<ellipse cx="{x:.1f}" cy="{y}" rx="{r+1:.1f}" ry="{r-0.6:.1f}" fill="#0F0F10" transform="rotate(-18 {x:.1f} {y})"/>'
    elif i==PH: phx,phy=x,y
    else: nt+=f'<ellipse cx="{x:.1f}" cy="{y}" rx="{r+1:.1f}" ry="{r-0.6:.1f}" fill="none" stroke="#0F0F10" stroke-width="1.5" transform="rotate(-18 {x:.1f} {y})"/>'
cur=f'<circle cx="{phx:.1f}" cy="{phy}" r="24" fill="#2142FF" opacity=".8" filter="url(#sprayM)"/><line x1="{phx:.1f}" x2="{phx:.1f}" y1="30" y2="198" stroke="#2142FF" stroke-width="1.5"/><circle cx="{phx:.1f}" cy="{phy}" r="7.5" fill="#2142FF"/>'
C=f'''<div class="phone">{ST}
<div style="text-align:center;margin-top:6px"><span class="pill"><i></i>換聲處理中 · 好了通知你</span></div>
<div style="margin-top:12px">{prog(1,'#0F0F10','#9A968E','#2142FF')}</div>
<div style="display:flex;align-items:flex-end;justify-content:space-between;padding:18px 24px 10px;border-bottom:1.5px solid var(--ink);margin:0 0 0">
 <div style="display:flex;align-items:baseline;gap:10px"><span style="font-size:40px;font-weight:700;line-height:1">旋律</span><span style="font-family:var(--disp);font-size:22px">MELODY</span></div>
 <div class="mono" style="font-size:10px;text-align:right;line-height:1.5">12.4 SEC<br>C MAJ · 96 BPM</div>
</div>
<svg width="390" height="222" viewBox="0 0 350 222" style="display:block;margin:0 auto">
 <text x="18" y="22" font-family="Space Mono" font-size="9.5" letter-spacing="1" fill="#0F0F10">FIG.02 — 你的旋律</text>
 {staff}{cur}{nt}
 <text x="18" y="214" font-family="Space Mono" font-size="9.5" fill="#77736C">00:05</text>
 <g>{barcode(250,198,16)}</g>
</svg>
<div style="display:flex;justify-content:center;align-items:center;gap:30px;margin-top:6px">
 <div style="width:54px;height:54px;border-radius:50%;border:1.5px solid var(--ink);display:flex;align-items:center;justify-content:center">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F0F10" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M5 2.5V7h4.5"/></svg></div>
 <div style="width:84px;height:84px;border-radius:50%;background:var(--ink);display:flex;align-items:center;justify-content:center">
  <svg width="30" height="30" viewBox="0 0 30 30"><path d="M9 5.5v19c0 1 1 1.6 1.9 1.1l15-9.5c.8-.5.8-1.7 0-2.2l-15-9.5C10 3.9 9 4.5 9 5.5z" fill="#EDEAE2"/></svg></div>
 <div style="width:54px;height:54px;border-radius:50%;border:1.5px solid var(--ink);display:flex;align-items:center;justify-content:center">
  <svg width="27" height="27" style="color:#0F0F10;stroke-width:1.6"><use href="#i-sing"/></svg></div>
</div>
<div class="btn cob" style="margin:22px 24px 0"><span>下一顆豆</span><span class="ar">→</span></div>
{tabbar(1)}<div class="homebar"></div>{G}</div>'''

body=f'''<div class="page"><svg class="pgrain"><rect width="100%" height="100%" filter="url(#grainF)"/></svg>
<svg style="position:absolute;left:-330px;bottom:-360px" width="700" height="600"><circle cx="350" cy="300" r="120" fill="#2142FF" opacity=".55" filter="url(#sprayL)"/></svg>
<div class="head">
 <div><div class="kick"><b>V2</b> &nbsp;LIGHT ZINE / STREETWEAR</div><div style="display:flex;align-items:center;gap:18px">{logo(130)}<div class="big">豆莢浪歌</div></div></div>
 <div class="sl" style="align-self:end;padding-bottom:6px">隨口唱一首，<br>短短幾秒天下行</div>
 <div><div class="pal"><i style="background:#EDEAE2"></i><i style="background:#0F0F10"></i><i style="background:#2142FF"></i></div>
 <div class="iconset"><figure><svg style="color:#2142FF"><use href="#i-sing"/></svg>唱</figure><figure><svg><use href="#i-melody"/></svg>旋律</figure><figure><svg><use href="#i-voice"/></svg>配樂</figure><figure><svg><use href="#i-share"/></svg>分享</figure></div></div>
</div>
<div class="row">
<div class="wrap"><div class="cap"><span>A — 首次啟動 ONBOARDING</span><span>P.01</span></div>{A}</div>
<div class="wrap"><div class="cap"><span>B — 唱 SING HOME</span><span>P.02</span></div>{B}</div>
<div class="wrap"><div class="cap"><span>C — 旋律 MELODY RESULT</span><span>P.03</span></div>{C}</div>
</div>
<div class="foot"><span>PAPER #EDEAE2 · INK #0F0F10 · COBALT #2142FF</span><span>STENCIL CUT / SPRAY OVERSPRAY / PRINTED SCORE</span><span>DOUJIA LANGE® STYLE EXPLORATION</span></div>
</div>'''
page(CSS,body,'/workspace/doujia/mockup/src/v2.html')
