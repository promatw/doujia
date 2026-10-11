from gen import *
CSS=r'''
:root{--bg:#0A0A0B;--bg2:#141416;--fg:#EDEBE6;--mute:#77757C;--line:rgba(237,235,230,.13);--lime:#D4FF3A;--vio:#7B5CFF;
--sans:"Geist","Noto Sans CJK TC",sans-serif;--serif:"Noto Serif CJK TC",serif;--mono:"Geist Mono","Noto Sans Mono CJK TC",monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1400px;background:#050506;color:var(--fg);font-family:var(--sans)}
.page{padding:54px 70px 70px;position:relative;overflow:hidden}
.pglow{position:absolute;pointer-events:none}
.head{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:58px;position:relative}
.wm{display:flex;align-items:center;gap:18px}
.wm h1{font-family:var(--serif);font-weight:700;font-size:44px;letter-spacing:4px}
.wm .sl{font-size:14px;color:var(--mute);letter-spacing:3px;margin-top:6px}
.kick{font-family:var(--mono);font-size:12px;letter-spacing:3px;color:var(--lime);margin-bottom:14px}
.meta{display:flex;gap:44px;align-items:flex-end}
.pal{display:flex;gap:6px}.pal i{width:26px;height:26px;border-radius:50%;border:1px solid var(--line)}
.iconset{display:flex;gap:22px;color:var(--fg)}
.iconset figure{font-family:var(--mono);font-size:10px;color:var(--mute);text-align:center;letter-spacing:1px}
.iconset svg{width:34px;height:34px;display:block;margin:0 auto 6px;stroke-width:1.4}
.row{display:flex;gap:45px;justify-content:center;position:relative}
.wrap{position:relative}
.cap{position:absolute;top:-30px;left:2px;font-family:var(--mono);font-size:11px;letter-spacing:2px;color:var(--mute)}
.cap b{color:var(--fg);font-weight:500}
.phone{width:390px;height:844px;border-radius:52px;background:var(--bg);position:relative;overflow:hidden;
 box-shadow:0 0 0 1px #2B2B30,0 0 0 9px #111113,0 0 0 10px #2E2E33,0 40px 80px rgba(0,0,0,.6)}
.grain{position:absolute;inset:0;width:100%;height:100%;opacity:.13;mix-blend-mode:screen;pointer-events:none;z-index:9}
.island{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:118px;height:34px;border-radius:20px;background:#000;z-index:10}
.status{height:54px;display:flex;justify-content:space-between;align-items:center;padding:6px 32px 0 38px;font-weight:600;font-size:15px;font-family:var(--sans)}
.status i{display:inline-block;width:24px;height:11px;border:1.3px solid currentColor;border-radius:4px;position:relative;opacity:.9}
.status i:after{content:"";position:absolute;inset:1.5px 6px 1.5px 1.5px;background:currentColor;border-radius:1px}
.homebar{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:var(--fg);opacity:.85;z-index:11}
.topline{display:flex;justify-content:space-between;align-items:center;padding:14px 28px 0;font-family:var(--mono);font-size:11px;letter-spacing:2px;color:var(--mute)}
.topline b{color:var(--fg);font-weight:500}
.ser{font-family:var(--serif);font-weight:700}
.btn{height:58px;border-radius:29px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;font-size:18px;font-weight:700;letter-spacing:4px}
.btn.lime{background:var(--lime);color:#0A0A0B}
.btn.white{background:var(--fg);color:#0A0A0B}
.btn .ar{font-family:var(--mono);font-weight:400;letter-spacing:0}
.prog{position:relative;width:300px;margin:0 auto}
.prog svg{width:300px;height:56px;display:block}
.prog .lbl{position:relative;height:16px}
.prog .lbl span{position:absolute;transform:translateX(-50%);font-size:11px;color:var(--mute);letter-spacing:1px;white-space:nowrap}
.prog .lbl span.on{color:var(--lime)}
.tabbar{position:absolute;left:22px;right:22px;bottom:28px;height:68px;border-radius:34px;background:rgba(26,26,29,.82);border:1px solid var(--line);
 display:flex;justify-content:space-around;align-items:center;backdrop-filter:blur(20px);z-index:8}
.tab{width:60px;height:60px;display:flex;align-items:center;justify-content:center;color:#A9A6AD;position:relative}
.tab svg{width:30px;height:30px;stroke-width:1.5}
.tab.on{color:var(--lime)}
.tab.on:after{content:"";position:absolute;bottom:4px;width:4px;height:4px;border-radius:50%;background:var(--lime)}
.pill{display:inline-flex;align-items:center;gap:10px;padding:9px 16px;border-radius:99px;font-size:13px;letter-spacing:1px;border:1px solid var(--line);background:rgba(26,26,29,.8)}
.pulse{width:7px;height:7px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 4px rgba(212,255,58,.18),0 0 12px var(--lime)}
.foot{margin-top:70px;display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;color:var(--mute);letter-spacing:2px;border-top:1px solid var(--line);padding-top:18px}
'''
G='<svg class="grain"><rect width="100%" height="100%" filter="url(#grainF)"/></svg>'
ST='<div class="island"></div><div class="status"><span>9:41</span><i></i></div>'
def logo(w=110):
    return f'''<svg width="{w}" height="{w*0.42}" viewBox="0 0 110 46">
<ellipse cx="60" cy="24" rx="40" ry="14" fill="#7B5CFF" opacity=".8" filter="url(#sprayM)"/>
<path d="M10 27C24 9 80 6 102 17 92 38 32 42 10 27z" fill="none" stroke="#EDEBE6" stroke-width="1.3" stroke-linejoin="round"/>
<path d="M10 27c-4 0-6-2.5-6-6" fill="none" stroke="#EDEBE6" stroke-width="1.3" stroke-linecap="round"/>
<circle cx="35" cy="24.5" r="5.5" fill="none" stroke="#EDEBE6" stroke-width="1.2"/><circle cx="52" cy="22.5" r="5.5" fill="none" stroke="#EDEBE6" stroke-width="1.2"/>
<circle cx="69" cy="21.5" r="5.5" fill="none" stroke="#EDEBE6" stroke-width="1.2"/><circle cx="86" cy="21" r="5.5" fill="#D4FF3A"/></svg>'''

# --- A
A=f'''<div class="phone">{ST}
<div class="topline"><span><b>豆莢浪歌</b> / DOUJIA</span><span>Nº 001</span></div>
<svg width="390" height="380" viewBox="0 0 390 380" style="display:block;margin-top:4px">
 <ellipse cx="230" cy="175" rx="150" ry="135" fill="#7B5CFF" opacity=".95" filter="url(#sprayL)"/>
 <ellipse cx="135" cy="250" rx="85" ry="70" fill="#D4FF3A" opacity=".55" filter="url(#sprayL)"/>
 <g transform="rotate(-28 195 190)">
  <path d="M60 205C110 120 300 105 340 165 300 250 120 270 60 205z" fill="none" stroke="#EDEBE6" stroke-width="1.4" stroke-linejoin="round"/>
  <path d="M60 205c-16 2-28-8-28-24" fill="none" stroke="#EDEBE6" stroke-width="1.4" stroke-linecap="round"/>
  <path d="M90 196C150 150 270 140 320 168" fill="none" stroke="#EDEBE6" stroke-width=".8" stroke-dasharray="2 5" opacity=".6"/>
  <circle cx="125" cy="196" r="22" fill="none" stroke="#EDEBE6" stroke-width="1.2"/>
  <circle cx="180" cy="186" r="23" fill="none" stroke="#EDEBE6" stroke-width="1.2"/>
  <circle cx="236" cy="180" r="23" fill="none" stroke="#EDEBE6" stroke-width="1.2"/>
  <circle cx="290" cy="178" r="21" fill="#D4FF3A"/>
 </g>
 <g fill="#EDEBE6" filter="url(#soft)"><circle cx="330" cy="72" r="3"/><circle cx="345" cy="92" r="4"/><circle cx="330" cy="112" r="2.4"/></g>
 <g font-family="Geist Mono" font-size="10" fill="#EDEBE6" letter-spacing="1.5" opacity=".75">
  <line x1="300" y1="250" x2="352" y2="300" stroke="#EDEBE6" stroke-width=".7"/><text x="290" y="316">VOICE ONLY</text>
  <line x1="58" y1="92" x2="98" y2="128" stroke="#EDEBE6" stroke-width=".7"/><text x="28" y="84">4 BEANS / 4 STEPS</text>
 </g>
</svg>
<div style="padding:0 30px;margin-top:-8px">
 <div class="ser" style="font-size:34px;line-height:1.32;letter-spacing:2px">隨口唱一首，<br>短短幾秒<span style="color:var(--lime)">天下行</span></div>
 <div style="font-size:14px;color:var(--mute);margin-top:12px;letter-spacing:2px">不用露臉。讓聲音先出道。</div>
 <div style="margin-top:36px;font-family:var(--mono);font-size:10px;letter-spacing:2px;color:var(--mute)">01 — NAME</div>
 <div style="display:flex;align-items:center;height:52px;border-bottom:1px solid rgba(237,235,230,.35);font-size:20px;color:#5E5C63;letter-spacing:2px">
   <span style="width:2px;height:24px;background:var(--lime);margin-right:10px"></span>取個名字</div>
 <div class="btn lime" style="margin-top:26px"><span>開始唱</span><span class="ar">→</span></div>
</div>
<div class="homebar"></div>{G}</div>'''

# --- B
B=f'''<div class="phone">{ST}
<div class="topline"><span><b>01</b> / 04 · SING</span><span style="display:flex;align-items:center;gap:8px">@yuki_00 <svg width="26" height="26" style="color:#EDEBE6;stroke-width:1.3"><use href="#pod"/></svg></span></div>
<div style="margin-top:18px">{prog(0,'#EDEBE6','#4A484F','#D4FF3A')}</div>
<div class="ser" style="font-size:30px;line-height:1.35;letter-spacing:2px;padding:30px 30px 0">今天，<br>想唱點什麼？</div>
<svg width="390" height="330" viewBox="0 0 390 330" style="display:block;margin-top:-6px">
 <circle cx="195" cy="168" r="120" fill="#7B5CFF" opacity=".95" filter="url(#sprayL)"/>
 <circle cx="230" cy="210" r="60" fill="#D4FF3A" opacity=".45" filter="url(#sprayL)"/>
 <circle cx="195" cy="168" r="134" fill="none" stroke="#EDEBE6" stroke-width="5" stroke-dasharray="1 9.5" opacity=".28"/>
 <circle cx="195" cy="168" r="96" fill="#0A0A0B"/>
 <circle cx="195" cy="168" r="96" fill="none" stroke="#D4FF3A" stroke-width="1.5"/>
 <use href="#headO" x="148" y="122" width="88" height="88" style="color:#D4FF3A;stroke-width:1.6"/>
 <g fill="#D4FF3A"><circle cx="242" cy="148" r="3.2"/><circle cx="252" cy="168" r="4.2"/><circle cx="242" cy="189" r="2.6"/></g>
</svg>
<div style="text-align:center;font-family:var(--mono);font-size:15px;letter-spacing:3px;margin-top:-4px">00:00 <span style="color:var(--mute)">/ 15s</span></div>
<div style="text-align:center;margin-top:16px"><span class="pill" style="color:#BDBAC0">
 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#BDBAC0" stroke-width="1.6" stroke-linecap="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/></svg>
 安靜的地方 ・ 手機離嘴約20公分</span></div>
{tabbar(0)}<div class="homebar"></div>{G}</div>'''

# --- C : dot matrix
cols,rows=34,14; cw=9.6; ox=16; oy=18
seq,tot=notes_seq()
lit={}
for t,d,p in seq:
    c0=round(t/tot*cols); c1=max(c0+1,round((t+d)/tot*cols))
    r=rows-1-p
    for c in range(c0,c1): lit[(c,r)]=t
phc=round(sum(D[:PH])/tot*cols)
dm=''
for c in range(cols):
    for r in range(rows):
        x=ox+c*cw; y=oy+r*13.2
        if (c,r) in lit:
            if c<phc: dm+=f'<circle cx="{x}" cy="{y}" r="3.2" fill="#D4FF3A"/>'
            elif c==phc: dm+=f'<circle cx="{x}" cy="{y}" r="3.8" fill="#FFFFFF"/>'
            else: dm+=f'<circle cx="{x}" cy="{y}" r="3" fill="#EDEBE6" opacity=".85"/>'
        else: dm+=f'<circle cx="{x}" cy="{y}" r="1.1" fill="#3A383F"/>'
pr=[r for (c,r) in lit if c==phc]; py=oy+(pr[0] if pr else 6)*13.2
glow=f'<circle cx="{ox+phc*cw}" cy="{py}" r="30" fill="#7B5CFF" filter="url(#sprayM)"/>'
glow+=f'<line x1="{ox+phc*cw}" y1="8" x2="{ox+phc*cw}" y2="200" stroke="#EDEBE6" stroke-width="1" opacity=".5"/>'
C=f'''<div class="phone">{ST}
<div style="text-align:center;margin-top:6px"><span class="pill"><span class="pulse"></span>換聲處理中 · 好了通知你</span></div>
<div style="margin-top:16px">{prog(1,'#EDEBE6','#4A484F','#D4FF3A')}</div>
<div style="padding:24px 30px 0;display:flex;justify-content:space-between;align-items:flex-end">
 <div><div style="font-family:var(--mono);font-size:10px;letter-spacing:2px;color:var(--lime)">02 — MELODY</div>
 <div class="ser" style="font-size:30px;letter-spacing:2px;margin-top:4px">你的旋律</div></div>
 <div style="font-family:var(--mono);font-size:11px;color:var(--mute);text-align:right;line-height:1.7;letter-spacing:1px">12.4s<br>C MAJ · 96 BPM</div>
</div>
<div style="margin:16px 20px 0;height:222px;border-radius:26px;background:#121214;border:1px solid var(--line);overflow:hidden;position:relative">
 <svg width="350" height="222" viewBox="0 0 350 222">{glow}{dm}
 <text x="18" y="212" font-family="Geist Mono" font-size="10" fill="#77757C" letter-spacing="1">00:05</text><text x="300" y="212" font-family="Geist Mono" font-size="10" fill="#77757C" letter-spacing="1">00:12</text></svg>
</div>
<div style="display:flex;justify-content:center;align-items:center;gap:30px;margin-top:22px">
 <div style="width:52px;height:52px;border-radius:50%;border:1px solid rgba(237,235,230,.25);display:flex;align-items:center;justify-content:center">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#EDEBE6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M5 2.5V7h4.5"/></svg></div>
 <div style="width:82px;height:82px;border-radius:50%;background:var(--lime);display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(212,255,58,.25)">
  <svg width="30" height="30" viewBox="0 0 30 30"><path d="M9 5.5v19c0 1 1 1.6 1.9 1.1l15-9.5c.8-.5.8-1.7 0-2.2l-15-9.5C10 3.9 9 4.5 9 5.5z" fill="#0A0A0B"/></svg></div>
 <div style="width:52px;height:52px;border-radius:50%;border:1px solid rgba(237,235,230,.25);display:flex;align-items:center;justify-content:center">
  <svg width="26" height="26" style="color:#EDEBE6;stroke-width:1.4"><use href="#i-sing"/></svg></div>
</div>
<div class="btn white" style="margin:24px 30px 0"><span>下一顆豆</span><span class="ar">→</span></div>
{tabbar(1)}<div class="homebar"></div>{G}</div>'''

body=f'''<div class="page">
<svg class="pglow" style="left:-500px;top:-560px" width="1500" height="1300"><ellipse cx="750" cy="650" rx="300" ry="200" fill="#7B5CFF" opacity=".25" filter="url(#sprayL)"/></svg>
<div class="head"><div><div class="kick">V1 — DARK EDITORIAL</div>
<div class="wm">{logo(120)}<div><h1>豆莢浪歌</h1><div class="sl">隨口唱一首，短短幾秒天下行</div></div></div></div>
<div class="meta"><div class="pal"><i style="background:#0A0A0B"></i><i style="background:#EDEBE6"></i><i style="background:#D4FF3A"></i><i style="background:#7B5CFF"></i></div>
<div class="iconset"><figure><svg style="color:#D4FF3A"><use href="#i-sing"/></svg>唱</figure><figure><svg><use href="#i-melody"/></svg>旋律</figure><figure><svg><use href="#i-voice"/></svg>配樂</figure><figure><svg><use href="#i-share"/></svg>分享</figure></div></div></div>
<div class="row">
<div class="wrap"><div class="cap"><b>A</b> &nbsp;首次啟動 / ONBOARDING</div>{A}</div>
<div class="wrap"><div class="cap"><b>B</b> &nbsp;唱 / SING HOME</div>{B}</div>
<div class="wrap"><div class="cap"><b>C</b> &nbsp;旋律結果 / MELODY</div>{C}</div>
</div>
<div class="foot"><span>NEAR-BLACK · LIME #D4FF3A · VIOLET AIRBRUSH #7B5CFF</span><span>SERIF HEADLINE / MONO META / 1.5PX LINE ICONS</span><span>STYLE EXPLORATION 2026</span></div>
</div>'''
page(CSS,body,'/workspace/doujia/mockup/src/v1.html')
