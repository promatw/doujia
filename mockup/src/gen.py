import math
P=[5,5,6,8,8,7,5,4,4,5,7,9,10,9,7,6,5,3,4,5]
D=[1,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,3]
PH=9

DEFS = r'''
<svg width="0" height="0" style="position:absolute"><defs>
 <filter id="grainF" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
 <filter id="sprayL" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="22" result="b"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3.6 0 0 0 -1.3" result="m"/>
  <feComposite in="b" in2="m" operator="in" result="g"/>
  <feComponentTransfer in="b" result="b3"><feFuncA type="linear" slope=".55"/></feComponentTransfer>
  <feMerge><feMergeNode in="b3"/><feMergeNode in="g"/></feMerge></filter>
 <filter id="sprayM" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="b"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="9" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3.8 0 0 0 -1.4" result="m"/>
  <feComposite in="b" in2="m" operator="in" result="g"/>
  <feComponentTransfer in="b" result="b3"><feFuncA type="linear" slope=".4"/></feComponentTransfer>
  <feMerge><feMergeNode in="b3"/><feMergeNode in="g"/></feMerge></filter>
 <filter id="sprayS" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="b"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.8" numOctaves="1" seed="2" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3.8 0 0 0 -1.3" result="m"/>
  <feComposite in="b" in2="m" operator="in" result="g"/>
  <feComponentTransfer in="b" result="b3"><feFuncA type="linear" slope=".5"/></feComponentTransfer>
  <feMerge><feMergeNode in="b3"/><feMergeNode in="g"/></feMerge></filter>
 <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation=".6"/></filter>

 <symbol id="pod" viewBox="0 0 32 32" overflow="visible">
  <path vector-effect="non-scaling-stroke" d="M16 4.5c5.8 0 9 3.9 9 9.2v5.4c0 5.7-4 9.6-9 9.6s-9-3.9-9-9.6v-5.4c0-5.3 3.2-9.2 9-9.2z" fill="none" stroke="currentColor" stroke-linejoin="round"/>
  <path vector-effect="non-scaling-stroke" d="M16 4.5c0-1.9 1.1-3.1 3.2-3.3" fill="none" stroke="currentColor" stroke-linecap="round"/>
 </symbol>
 <symbol id="headO" viewBox="0 0 48 48" overflow="visible">
  <path vector-effect="non-scaling-stroke" d="M13 44v-8C8 33 6 28 6 22 6 12.5 13.5 6 22.5 6 30.5 6 36 11 37 18l3.8 6.2c.6 1-.1 1.8-1 1.8H37.4v1.6l-5.6 2.2 5.6 1.7v3.1c0 2.5-1.9 4.2-4.4 4.1L28 38.2V44" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-linecap="round"/>
 </symbol>
 <symbol id="i-sing" viewBox="0 0 32 32" overflow="visible">
  <use href="#headO" x="1" y="3" width="25" height="25"/>
  <circle cx="26.6" cy="11" r="1.25" fill="currentColor"/><circle cx="29.2" cy="16.6" r="1.6" fill="currentColor"/><circle cx="26.6" cy="22.2" r="1.05" fill="currentColor"/>
 </symbol>
 <symbol id="i-melody" viewBox="0 0 32 32" overflow="visible">
  <use href="#pod" width="32" height="32"/>
  <path vector-effect="non-scaling-stroke" d="M14.4 22v-9.2l6-1.6v8.4" fill="none" stroke="currentColor" stroke-linejoin="round"/>
  <circle cx="12.7" cy="22" r="2.1" fill="currentColor"/><circle cx="18.7" cy="19.6" r="2.1" fill="currentColor"/>
 </symbol>
 <symbol id="i-voice" viewBox="0 0 32 32" overflow="visible">
  <use href="#pod" width="32" height="32"/>
  <path vector-effect="non-scaling-stroke" d="M10.8 21v-2.6a5.2 5.2 0 0 1 10.4 0V21" fill="none" stroke="currentColor" stroke-linecap="round"/>
  <rect x="9.6" y="19.4" width="3.2" height="5.4" rx="1.4" fill="currentColor"/><rect x="19.2" y="19.4" width="3.2" height="5.4" rx="1.4" fill="currentColor"/>
 </symbol>
 <symbol id="i-share" viewBox="0 0 32 32" overflow="visible">
  <use href="#pod" width="32" height="32"/>
  <path vector-effect="non-scaling-stroke" d="M16 24v-7.2" fill="none" stroke="currentColor" stroke-linecap="round"/>
  <path vector-effect="non-scaling-stroke" d="M16 19c-.4-2.6-2.4-3.8-4.6-3.5.1 2.5 2 3.8 4.6 3.5zM16 17.4c.4-2.8 2.6-4.3 5-4-.2 2.8-2.4 4.3-5 4z" fill="none" stroke="currentColor" stroke-linejoin="round"/>
 </symbol>
</defs></svg>'''

def tabbar(active):
    ids=['i-sing','i-melody','i-voice','i-share']
    return '<div class="tabbar">'+''.join(f'<div class="tab{" on" if i==active else ""}"><svg><use href="#{x}"/></svg></div>' for i,x in enumerate(ids))+'</div>'

def prog(step, fg, mute, acc, glow=True):
    xs=[72,125,178,231]; ys=[29,27.5,26.5,26]
    s=f'<svg viewBox="0 0 300 56"><path d="M12 31C36 9 262 6 290 23 272 47 46 53 12 31z" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linejoin="round"/>'
    s+=f'<path d="M12 31c-5 0-8-3-8-7" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>'
    for i,(x,y) in enumerate(zip(xs,ys)):
        if i<step: s+=f'<circle cx="{x}" cy="{y}" r="8" fill="{fg}"/>'
        elif i==step:
            if glow: s+=f'<circle cx="{x}" cy="{y}" r="16" fill="{acc}" opacity=".9" filter="url(#sprayS)"/>'
            s+=f'<circle cx="{x}" cy="{y}" r="8.5" fill="{acc}"/>'
        else: s+=f'<circle cx="{x}" cy="{y}" r="7.5" fill="none" stroke="{mute}" stroke-width="1.2"/>'
    s+='</svg>'
    names=['唱','旋律','配樂','分享']
    lb=''.join(f'<span style="left:{xs[i]}px" class="{"on" if i==step else ""}">{n}</span>' for i,n in enumerate(names))
    return f'<div class="prog">{s}<div class="lbl">{lb}</div></div>'

def notes_seq():
    tot=sum(D); out=[]; t=0
    for p,d in zip(P,D):
        out.append((t,d,p)); t+=d
    return out,tot

def page(css, body, out):
    html=f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><style>{css}</style></head><body>{DEFS}{body}<script>document.documentElement.setAttribute("data-h",document.querySelector(".page").getBoundingClientRect().height)</script></body></html>'
    open(out,'w').write(html)
