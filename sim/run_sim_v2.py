#!/usr/bin/env python3
"""豆莢浪歌 relay simulation v2 — new naming: <serial>-<豆1 user>-<豆2 user>-<豆3 user>-<豆4 user>, e.g. K08-003-011-015-015.
Skipped step = '000'. Same user, same step, same parent again = '#2' (folder/URL: 'n2').
Rebuilds ../pods/ (K07 = migrated old Bob1–6 tree, K08 = 愛到濃烈), pods/users.json, pods/counters.json, pods/index.json."""
import os, json, shutil, subprocess, threading, datetime, secrets, hashlib, re
import numpy as np, pretty_midi as pm
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); PODS=os.path.join(ROOT,'pods'); V60='/workspace/v60'
AAC='/home/box/agent-data/agents/1b6a3197-e02c-4822-9d2a-7c445d678ca3/attachments/8c5d6d403e8e2b644f28cb652a6bf35fd7ebfeee3cdb1a36e89d433618cf7b13.aac'
IMG=os.path.join(ROOT,'ux','img'); IR=os.path.join(ROOT,'app','assets','ir_openair_patrington.wav'); SF2='/usr/share/sounds/sf2/FluidR3_GM.sf2'
CRED_PIANO='Salamander Grand Piano by Alexander Holm (CC BY 3.0)'
CRED_IR="Impulse response: OpenAIR Library (openair.hosted.york.ac.uk), St Patrick's Church Patrington, CC BY 4.0"
CRED_V60='旋律轉譜：v60 哼唱轉 MIDI（pYIN）'
SKIP='000'; LOG=[]; TZ=datetime.timezone(datetime.timedelta(hours=8)); T0=datetime.datetime(2026,10,11,20,30,tzinfo=TZ); clock=[0]; LOCK=threading.Lock()
def now():
    with LOCK: clock[0]+=3; return (T0+datetime.timedelta(minutes=clock[0])).isoformat()
def sh(*a): subprocess.run(a,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def ff(*a): sh('ffmpeg','-y','-loglevel','error',*a)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
def log(m): LOG.append(m); print(m)

# ---------- users (model of the future Firebase 'users' collection) ----------
USERS={}
def make_user(code,name,device):
    tc=secrets.token_hex(4).upper()  # shown once to the user; only the hash is stored
    USERS[code]=dict(code=code,displayName=name,nameLocked=True,devices=[device],created=now(),
                     transfer=dict(codeHash=hashlib.sha256(tc.encode()).hexdigest(),expires=None,used=False))
    return tc
def set_name(code,name):
    if USERS[code]['nameLocked']: return False
def transfer(code,tc,new_device):
    t=USERS[code]['transfer']
    if t['used'] or hashlib.sha256(tc.encode()).hexdigest()!=t['codeHash']: return False
    USERS[code]['devices']=[new_device]; t['used']=True; return True
def dn(code): return SKIP if code==SKIP else USERS[code]['displayName']

# ---------- ids ----------
def disp(pid): return re.sub(r'n(\d+)',r'#\1',pid)   # folder/URL 'K08-003-011-015n2' -> display 'K08-003-011-015#2'
def next_serial():
    """atomic counter (Firebase: transaction on counters/songs)."""
    while True:
        c=json.load(open(os.path.join(PODS,'counters.json'))); n=c['songs']+1
        try: os.mkdir(os.path.join(PODS,f'K{n:02d}'))
        except FileExistsError: c['songs']=n; json.dump(c,open(os.path.join(PODS,'counters.json'),'w')); continue
        c['songs']=n; json.dump(c,open(os.path.join(PODS,'counters.json'),'w')); return f'K{n:02d}'
def alloc(parent,step,user):
    """id = parent + '-' + user code (plus '000' for every skipped step); mkdir is atomic -> second version gets n2, n3…"""
    if step==1: base=next_serial(); pid=f'{base}-{user}'; os.mkdir(os.path.join(PODS,pid)); return pid
    pstep=load(parent)['step']; base=parent+''.join(f'-{SKIP}' for _ in range(step-pstep-1))+f'-{user}'
    for k in range(1,100):
        pid=base if k==1 else f'{base}n{k}'
        try: os.mkdir(os.path.join(PODS,pid)); return pid
        except FileExistsError: continue
    raise RuntimeError('too many versions')
def write_pod(pid,parent,step,author,files,notes,credits,**extra):
    d=os.path.join(PODS,pid); C=(chain(parent) if parent else [])
    pod=dict(id=pid,display=disp(pid),song=pid.split('-')[0],parent=parent,step=step,author=author,authorName=dn(author),created=now(),files=files,notes=notes,credits=credits,**extra)
    tmp=os.path.join(d,'.pod.json.tmp'); json.dump(pod,open(tmp,'w',encoding='utf8'),ensure_ascii=False,indent=1); os.replace(tmp,os.path.join(d,'pod.json')); return pod
def load(pid): return json.load(open(os.path.join(PODS,pid,'pod.json'),encoding='utf8'))
def chain(pid):
    c=[]
    while pid: p=load(pid); c.insert(0,p); pid=p['parent']
    return c
def can_publish(pid):
    C=chain(pid); have={p['step'] for p in C}; nolyr=any(p.get('noLyrics') for p in C)
    miss=[s for s in (1,3) if s not in have]+([] if (2 in have or nolyr) else [2]); return not miss,miss

# ---------- 豆1 ----------
def bean1(user,title,audio,wav,mid):
    pid=alloc(None,1,user); d=os.path.join(PODS,pid)
    shutil.copy(audio,os.path.join(d,'hum'+os.path.splitext(audio)[1]))
    ff('-i',wav,'-b:a','160k',os.path.join(d,'denoised.mp3')); shutil.copy(wav,os.path.join(d,'denoised.wav'))
    shutil.copy(mid,os.path.join(d,'melody.mid'))
    n=sorted(pm.PrettyMIDI(mid).instruments[0].notes,key=lambda x:x.start)
    json.dump([dict(pitch=x.pitch,start=round(x.start,4),end=round(x.end,4)) for x in n],open(os.path.join(d,'notes.json'),'w'))
    write_pod(pid,None,1,user,dict(audio='hum'+os.path.splitext(audio)[1],denoised='denoised.mp3',midi='melody.mid',notes='notes.json'),
      f'哼唱 {dur(audio):.1f} 秒；降噪；v60 轉出 {len(n)} 個音。',[f'{dn(user)}：哼唱',CRED_V60],title=title)
    os.remove(os.path.join(d,'denoised.wav')); log(f'{dn(user)}({user}) → {disp(pid)}（豆1，{len(n)} 音）'); return pid

# ---------- 豆2 ----------
def bean2(parent,user,lyr,title):
    pid=alloc(parent,2,user); d=os.path.join(PODS,pid); root=chain(parent)[0]['id']
    shutil.copy(lyr,os.path.join(d,'lyrics.txt'))
    al=json.loads(subprocess.check_output(['node',os.path.join(HERE,'align_cli.js'),os.path.join(PODS,root,'notes.json'),lyr,'sections']))
    json.dump(al,open(os.path.join(d,'aligned.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    def ts(t): m=int(t//60); return f'[{m:02d}:{t-60*m:05.2f}]'
    open(os.path.join(d,'lyrics.lrc'),'w',encoding='utf8').write(''.join(f"{ts(a['start'])}{a['text']}\n" for a in al if a['start'] is not None))
    nph=len(json.loads(subprocess.check_output(['node','-e',f"const A=require('{ROOT}/app/align.js');console.log(JSON.stringify(A.phrases(require('{PODS}/{root}/notes.json'))))"])))
    warn=[f"第{i+1}行 {a['chars']}字/{a['notes']}音" for i,a in enumerate(al) if a['chars']>a['notes']*1.6+1]
    write_pod(pid,parent,2,user,dict(lyrics='lyrics.txt',aligned='aligned.json',lrc='lyrics.lrc'),
      f'{len(al)} 行歌詞 ↔ {nph} 句旋律'+('（重複段落：分兩段各自對齊）' if any('section' in a for a in al) else '')+('；字數偏多：'+'、'.join(warn) if warn else ''),[f'{dn(user)}：作詞'],title=title)
    log(f'{dn(user)}({user}) → {disp(pid)}（豆2，{len(al)} 行 / {nph} 句）'); return pid

# ---------- 豆3 ----------
def nudge(auto,true):
    """listener starts at the auto estimate and presses ±1 / ±0.1 until it sounds right: best reachable value on that grid."""
    base=round(auto,2); steps=round((true-base)/0.1); v=round(base+steps*0.1,2); return v,steps
def bean3_upload(parent,user,src,label,true_ms):
    pid=alloc(parent,3,user); d=os.path.join(PODS,pid); root=chain(parent)[0]['id']
    shutil.copy(src,os.path.join(d,'accompaniment.mp3'))
    ff('-i',src,'-ac','1','-ar','22050','-f','f32le','/tmp/acc.f32')
    auto=float(subprocess.check_output(['node',os.path.join(HERE,'autooff_cli.js'),os.path.join(PODS,root,'notes.json'),'/tmp/acc.f32']).decode())
    ms,steps=nudge(auto,true_ms); preview(d,root,ms)
    write_pod(pid,parent,3,user,dict(accompaniment='accompaniment.mp3',preview='preview_mix.mp3'),
      f'上傳伴奏「{label}」({dur(src):.1f}s，含前奏)。自動估 {auto:.2f}s → 試聽微調 {steps:+d}×0.1s → melody_start={ms:.2f}s（實際 {true_ms:.4f}s，誤差 {abs(ms-true_ms)*1000:.0f} ms）。',
      [f'{dn(user)}：配樂（{label}，使用者上傳）',CRED_PIANO],melody_start=ms,
      intro=dict(mode='upload',auto_estimate=round(auto,3),nudges=steps,truth=round(true_ms,4),unit='秒；豆1 時間軸要延後多少秒才對上伴奏'))
    log(f'{dn(user)}({user}) → {disp(pid)}（豆3 上傳 {label}；auto {auto:.2f} → melody_start {ms:.2f}，真值 {true_ms:.4f}）'); return pid
def bean3_auto(parent,user):
    """mode (a): generated accompaniment (ACC.arrange) + one 92-BPM bar intro of the first chord, ending exactly on the first melody note."""
    pid=alloc(parent,3,user); d=os.path.join(PODS,pid); root=chain(parent)[0]['id']
    r=json.loads(subprocess.check_output(['node',os.path.join(HERE,'acc_cli.js'),os.path.join(PODS,root,'notes.json')]))
    ms=r['melody_start']; m=pm.PrettyMIDI(initial_tempo=92); bass=pm.Instrument(32,name='bass'); pno=pm.Instrument(0,name='piano')
    for a in r['acc']: (bass if a['ch']==1 else pno).notes.append(pm.Note(a['vel']+20,a['pitch'],a['start']+ms,a['end']+ms))
    NAMES=['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']; fc=r['firstChord']; root_pc=NAMES.index(fc['root']); minor=fc['name'].endswith('m')
    pcs=[root_pc,(root_pc+(3 if minor else 4))%12,(root_pc+7)%12]; tones=[p for p in range(46,62) if p%12 in pcs]
    I=r['introStart']; beat=60/92
    bass.notes.append(pm.Note(64,34+((root_pc-10)%12),I,I+4*beat))
    for k in range(8): pno.notes.append(pm.Note(60 if k==0 else 50,tones[[0,2,1,3,2,1,3,2][k]%len(tones)],I+k*beat/2,I+4*beat))
    m.instruments+= [bass,pno]; m.write(os.path.join(d,'accompaniment.mid'))
    sh('fluidsynth','-ni','-g','0.8','-F','/tmp/auto.wav','-r','44100',SF2,os.path.join(d,'accompaniment.mid'))
    ff('-i','/tmp/auto.wav','-b:a','160k',os.path.join(d,'accompaniment.mp3')); preview(d,root,ms)
    write_pod(pid,parent,3,user,dict(accompaniment='accompaniment.mp3',midi='accompaniment.mid',preview='preview_mix.mp3'),
      f'自動伴奏（{r["keyName"]}）＋自動前奏：第一個和弦 {fc["name"]} 一小節（92 BPM = {r["bar"]:.3f}s），在 {I:.3f}s 開始、剛好結束在第一個音 → melody_start={ms:.3f}s（精確，不用猜）。',
      [f'{dn(user)}：配樂（自動伴奏）',CRED_PIANO,'GM 音色：FluidR3_GM'],melody_start=round(ms,4),
      intro=dict(mode='auto',bar_sec=round(r['bar'],4),intro_start=round(I,4),first_chord=fc['name'],bpm=92))
    log(f'{dn(user)}({user}) → {disp(pid)}（豆3 自動前奏；melody_start {ms:.3f}，前奏 {I:.3f}→{I+r["bar"]:.3f}s）'); return pid
def preview(d,root,ms):
    ff('-i',os.path.join(PODS,root,'denoised.mp3'),'-i',os.path.join(d,'accompaniment.mp3'),'-filter_complex',
       f'[0:a]adelay={int(round(ms*1000))}|{int(round(ms*1000))}[v];[1:a]volume=0.8[a];[v][a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95','-ac','2','-b:a','160k',os.path.join(d,'preview_mix.mp3'))

# ---------- 豆4 ----------
LEAD=0.5   # subtitle appears this many seconds before the phrase
def ass_time(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f'{h}:{m:02d}:{s:05.2f}'
def sub_events(al,ms):
    ev=[]
    for i,a in enumerate(al):
        if a['start'] is None: continue
        s=max(0,a['start']+ms-LEAD); nxt=al[i+1]['start']+ms-LEAD if i+1<len(al) and al[i+1]['start'] is not None else 1e9
        e=min(nxt-0.05,a['end']+ms+1.2); ev.append((s,e,a['text']))
    return ev
def bean4(parent,user,vertical=True):
    ok,miss=can_publish(parent)
    if not ok: log(f'{dn(user)}({user}) 想在 {disp(parent)} 做豆4 → 被擋下（缺豆 {miss}）'); return None
    pid=alloc(parent,4,user); d=os.path.join(PODS,pid); C=chain(parent); root=C[0]; lyr=[p for p in C if p['step']==2]; acc=[p for p in C if p['step']==3][-1]
    ms=acc['melody_start']   # reuse; never re-estimate
    accf=os.path.join(PODS,acc['id'],'accompaniment.mp3'); voc=os.path.join(PODS,root['id'],'denoised.mp3'); os.makedirs(os.path.join(d,'images'))
    imgs=['th1.jpg','th2.jpg','th3.jpg','cover.jpg','p2-bg.jpg']
    for i in imgs: shutil.copy(os.path.join(IMG,i),os.path.join(d,'images',i))
    md=int(round(ms*1000))
    ff('-i',voc,'-i',accf,'-i',IR,'-filter_complex',
       f'[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay={md}|{md},asplit[v1][v2];[v2][2:a]afir=dry=0:wet=1[rv];[rv]volume=0.22[rw];'
       f'[1:a]aresample=44100,volume=0.75[a];[v1][rw][a]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11','-ar','44100','-b:a','192k',os.path.join(d,'final_mix.mp3'))
    D=dur(os.path.join(d,'final_mix.mp3')); al=json.load(open(os.path.join(PODS,lyr[-1]['id'],'aligned.json'),encoding='utf8')) if lyr else []
    title=(lyr[-1].get('title') if lyr else None) or root.get('title','')
    head='[Script Info]\nScriptType: v4.00+\nPlayResX: 720\nPlayResY: 1280\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
    head+='Style: Lyr,Noto Sans CJK TC,50,&H00FFFFFF,&H00FFFFFF,&H99000000,&H00000000,1,0,0,0,100,100,0,0,1,4,1,2,50,50,200,1\nStyle: Ttl,Noto Serif CJK TC,40,&H00E9F5D4,&H00FFFFFF,&H99000000,&H00000000,1,0,0,0,100,100,2,0,1,3,0,8,40,40,90,1\nStyle: Id,Noto Sans CJK TC,24,&H00C0D0C8,&H00FFFFFF,&H99000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,8,40,40,150,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    names='・'.join(f"豆{p['step']} {dn(p['author'])}" for p in C)+f'・豆4 {dn(user)}'
    ev=[f'Dialogue: 0,{ass_time(0)},{ass_time(D)},Ttl,,0,0,0,,豆莢浪歌・{title}',f'Dialogue: 0,{ass_time(0)},{ass_time(D)},Id,,0,0,0,,{disp(pid)}　{names}']
    subs=sub_events(al,ms)
    for s,e,t in subs: ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Lyr,,0,0,0,,{t.replace('　','\\N') if len(t)>9 else t}")
    open(os.path.join(d,'subtitles.ass'),'w',encoding='utf8').write(head+'\n'.join(ev)+'\n')
    seg=D/len(imgs); xf=1.0; inputs=[]; fl=[]
    for k,i in enumerate(imgs):
        inputs+=['-loop','1','-t',f'{seg+xf:.3f}','-i',os.path.join(d,'images',i)]
        fl.append(f'[{k}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,scale=in_range=full:out_range=tv,format=yuv420p[i{k}]')
    last='i0'
    for k in range(1,len(imgs)): fl.append(f'[{last}][i{k}]xfade=transition=fade:duration={xf}:offset={k*seg:.3f}[x{k}]'); last=f'x{k}'
    fl.append(f"[{last}]subtitles={os.path.join(d,'subtitles.ass')}:fontsdir=/usr/share/fonts/opentype/noto,format=yuv420p[vout]")
    ff(*inputs,'-i',os.path.join(d,'final_mix.mp3'),'-filter_complex',';'.join(fl),'-map','[vout]','-map',f'{len(imgs)}:a','-c:v','libx264','-profile:v','high','-level','4.0','-preset','medium','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','44100','-shortest','-movflags','+faststart',os.path.join(d,'video.mp4'))
    ff('-ss','20','-i',os.path.join(d,'video.mp4'),'-frames:v','1','-vf','scale=360:-1',os.path.join(d,'poster.jpg'))
    write_pod(pid,parent,4,user,dict(mix='final_mix.mp3',video='video.mp4',subtitles='subtitles.ass',poster='poster.jpg',images=[f'images/{i}' for i in imgs]),
      f'用 {disp(acc["id"])} 的伴奏，melody_start={ms}s（沿用豆3，不重估）；原唱＋伴奏＋OpenAIR 殘響，−14 LUFS；720×1280 H.264/AAC {D:.1f}s，{len(subs)} 行字幕。接力：{names}',
      sorted({c for p in C for c in p['credits']})+[f'{dn(user)}：成品',CRED_IR,'圖片：豆莢浪歌 UX 素材','用 豆莢浪歌 製作'],published=True,title=title,melody_start=ms)
    log(f'{dn(user)}({user}) → {disp(pid)}（豆4 發布，{D:.1f}s，melody_start {ms}）'); return pid

# ---------- subtitle timing quality ----------
def measure(pid,true_ms):
    p=load(pid); C=chain(pid); root=C[0]; lyr=[c for c in C if c['step']==2][-1]; ms=p['melody_start']
    al=json.load(open(os.path.join(PODS,lyr['id'],'aligned.json'),encoding='utf8')); notes=json.load(open(os.path.join(PODS,root['id'],'notes.json')))
    sr=22050; y=np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i','/workspace/v60/v2/denoised.wav','-ac','1','-ar',str(sr),'-f','f32le','-']),np.float32).astype(float); h=sr//100
    rms=20*np.log10(np.sqrt(np.convolve(y**2,np.ones(h)/h,'same')[::h])+1e-9); thr=rms.max()-35
    ass=[l for l in open(os.path.join(PODS,pid,'subtitles.ass'),encoding='utf8') if ',Lyr,' in l]
    def t(s): hh,mm,ss=s.split(':'); return int(hh)*3600+int(mm)*60+float(ss)
    rows=[]
    for a,l in zip([x for x in al if x['start'] is not None],ass):
        f=l.split(','); s,e=t(f[1]),t(f[2])
        k0=int((a['start']-0.4)*100); k=next((k for k in range(max(0,k0),k0+90) if rms[k]>thr),k0+40)
        sung=k/100+true_ms   # actual vocal onset on the video timeline (true offset)
        sung_end=a['end']+true_ms
        inner=[notes[i+1]['start']-notes[i]['end'] for i in range(len(notes)-1) if notes[i]['start']>=a['start']-1e-3 and notes[i+1]['end']<=a['end']+1e-3]
        rows.append(dict(text=a['text'],sub_start=round(s,2),sub_end=round(e,2),shown=round(e-s,2),sung_start=round(sung,2),sung_len=round(sung_end-sung,2),
                         lead=round(sung-s,2),tail=round(e-sung_end,2),chars=a['chars'],notes=a['notes'],max_inner_gap=round(max(inner,default=0),2),
                         check_uses_melody_start=abs(s-max(0,a['start']+ms-LEAD))<0.011))
    return dict(id=disp(pid),melody_start=ms,truth=true_ms,rows=rows)

def main():
    shutil.rmtree(PODS,ignore_errors=True); os.makedirs(PODS); json.dump(dict(songs=6),open(os.path.join(PODS,'counters.json'),'w'))
    TC={}
    for code,name in [('001','Bob1'),('002','Bob2'),('003','HM'),('011','Amy'),('012','Bob3'),('014','Bob4'),('015','Bob5'),('016','Bob6')]: TC[code]=make_user(code,name,f'dev-{code}-a')
    log(f"用戶：{', '.join(f'{c}={u['displayName']}' for c,u in USERS.items())}")
    log(f"改名測試：Amy 想把顯示名稱改成『小艾』→ {'成功' if set_name('011','小艾') else '拒絕（名稱一次決定、不能改）'}")
    log(f"換手機：Bob5 在新手機輸入轉移碼 → {'成功' if transfer('015',TC['015'],'dev-015-b') else '失敗'}；再用一次同一組碼 → {'成功' if transfer('015',TC['015'],'dev-015-c') else '失敗（一次性）'}")
    # ===== K07: migrated old Bob1–6 tree =====
    r=bean1('001','月台',AAC,os.path.join(V60,'v2/denoised.wav'),os.path.join(V60,'user_v60.mid'))
    l=bean2(r,'002',os.path.join(HERE,'lyrics.txt'),'月台')
    a=bean3_upload(l,'012',os.path.join(V60,'v4/accomp_only.mp3'),'極簡鋼琴＋貝斯（v4）',2.8179)
    bean3_upload(l,'012',os.path.join(V60,'v3/accomp_only.mp3'),'鋼琴＋弦樂（v3）',2.8179)
    bean4(a,'014')
    s=bean3_upload(r,'012',os.path.join(V60,'v4/accomp_only.mp3'),'極簡鋼琴＋貝斯（v4，跳過豆2）',2.8179); bean4(s,'014')
    bean3_upload(l,'002',os.path.join(V60,'v3/accomp_only.mp3'),'鋼琴＋弦樂（v3，Bob2 自己配）',2.8179)
    out=[]; th=[threading.Thread(target=lambda w,f:out.append(bean2(r,w,os.path.join(HERE,f),'月台')),args=a_) for a_ in (('015','lyrics_bob5.txt'),('016','lyrics_bob6.txt'),('016','lyrics_bob6.txt'))]
    [t.start() for t in th]; [t.join() for t in th]; log(f'同時接手（Bob5＋Bob6 兩支手機同一秒）：{sorted(map(disp,out))}（沒有覆蓋）')
    # ===== K08: 愛到濃烈 =====
    TRUE=json.load(open(os.path.join(V60,'v4/v4_arrangement_info.json')))['PRE_sec']; log(f'v4 info PRE_sec = {TRUE:.6f}s（伴奏第一個旋律音 5.5435s − 哼唱第一音 2.7255s）')
    r=bean1('003','愛到濃烈',AAC,os.path.join(V60,'v2/denoised.wav'),os.path.join(V60,'user_v60.mid'))
    l=bean2(r,'011',os.path.join(HERE,'lyrics_amy.txt'),'愛到濃烈')
    a=bean3_upload(l,'015',os.path.join(V60,'v4/accomp_only.mp3'),'極簡鋼琴＋貝斯（v4）',TRUE)
    f1=bean4(a,'015'); f2=bean4(a,'003')
    b=bean3_upload(l,'015',os.path.join(V60,'v3/accomp_only.mp3'),'鋼琴＋弦樂（v3，第二版）',TRUE)
    f3=bean4(b,'015')
    c=bean3_auto(l,'003'); f4=bean4(c,'003')
    Q=[measure(f1,TRUE),measure(f3,TRUE),measure(f4,load(c)['melody_start'])]
    json.dump(Q,open(os.path.join(HERE,'subtitle_timing.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    idx=[]
    for pid in sorted(os.listdir(PODS),key=lambda s:(s.split('-')[0],s.count('-'),s)):
        if not os.path.isdir(os.path.join(PODS,pid)) or not os.path.exists(os.path.join(PODS,pid,'pod.json')): continue
        p=load(pid); idx.append({k:p.get(k) for k in ('id','display','song','parent','step','author','authorName','created','title','notes','published','melody_start')})
    json.dump(dict(generated=now(),naming='K<serial>-<豆1>-<豆2>-<豆3>-<豆4>（用戶代碼；000=跳過；第二版 n2 顯示 #2）',songs=sorted({p['song'] for p in idx}),pods=idx),open(os.path.join(PODS,'index.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    pub={c:{k:u[k] for k in ('code','displayName','created')} for c,u in USERS.items()}
    json.dump(dict(note='模擬：正式版放 Firebase；轉移碼只存 hash，這裡也不公開',users=pub),open(os.path.join(PODS,'users.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    json.dump(USERS,open(os.path.join(HERE,'users_private_sim.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    for d_ in os.listdir(PODS):
        if re.fullmatch(r'K\d+',d_): os.rmdir(os.path.join(PODS,d_))  # serial lock dirs
    open(os.path.join(HERE,'sim_log_v2.txt'),'w',encoding='utf8').write('\n'.join(LOG)+'\n')
main()
