#!/usr/bin/env python3
"""豆莢浪歌 relay simulation: Bob1..Bob6 create pods under ../pods/<path>/ (pod.json + files) and pods/index.json."""
import os, json, shutil, subprocess, threading, time, datetime, errno
import pretty_midi as pm
# NOTE: MIDI lyric meta is written as latin-1 by mido/pretty_midi; we store UTF-8 bytes (many players will show mojibake)
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); PODS=os.path.join(ROOT,'pods'); V60='/workspace/v60'
AAC='/home/box/agent-data/agents/1b6a3197-e02c-4822-9d2a-7c445d678ca3/attachments/8c5d6d403e8e2b644f28cb652a6bf35fd7ebfeee3cdb1a36e89d433618cf7b13.aac'
IMG=os.path.join(ROOT,'ux','img'); IR=os.path.join(ROOT,'app','assets','ir_openair_patrington.wav')
CRED_PIANO='Salamander Grand Piano by Alexander Holm (CC BY 3.0)'
CRED_IR="Impulse response: OpenAIR Library (openair.hosted.york.ac.uk), St Patrick's Church Patrington, CC BY 4.0"
CRED_V60='旋律轉譜：v60 哼唱轉 MIDI（pYIN）'
LOG=[]
T0=datetime.datetime(2026,10,11,20,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
clock=[0]
def now(): clock[0]+=7; return (T0+datetime.timedelta(minutes=clock[0])).isoformat()
def sh(*a): subprocess.run(a,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def ff(*a): sh('ffmpeg','-y','-loglevel','error',*a)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
def log(m): LOG.append(m); print(m)

def alloc(parent, step):
    """Atomic allocation: mkdir is atomic, so two people taking the same 豆 at once get different branch letters."""
    if step==1:
        n=8
        while True:
            try: os.mkdir(os.path.join(PODS,str(n))); return str(n)
            except FileExistsError: n+=1
    for i,ch in enumerate('abcdefghijklmnopqrstuvwxyz'):
        suf=f'{step}{ch}' if step<4 else ('4' if i==0 else f'4{ch}')
        pid=f'{parent}-{suf}'
        try: os.mkdir(os.path.join(PODS,pid)); return pid
        except FileExistsError: continue
    raise RuntimeError('too many branches')

def write_pod(pid,parent,step,author,files,notes,credits,**extra):
    d=os.path.join(PODS,pid); pod=dict(id=pid,parent=parent,step=step,author=author,created=now(),files=files,notes=notes,credits=credits,**extra)
    tmp=os.path.join(d,'.pod.json.tmp'); json.dump(pod,open(tmp,'w',encoding='utf8'),ensure_ascii=False,indent=1); os.replace(tmp,os.path.join(d,'pod.json'))
    return pod

def load(pid): return json.load(open(os.path.join(PODS,pid,'pod.json'),encoding='utf8'))
def chain(pid):
    c=[]
    while pid: p=load(pid); c.insert(0,p); pid=p['parent']
    return c
def can_publish(pid):
    have={p['step'] for p in chain(pid)}; nolyr=any(p.get('noLyrics') for p in chain(pid))
    miss=[s for s in (1,3) if s not in have]+([] if (2 in have or nolyr) else [2])
    return not miss, miss

def bob1():
    pid=alloc(None,1); d=os.path.join(PODS,pid)
    shutil.copy(AAC,os.path.join(d,'hum.aac'))
    ff('-i',os.path.join(V60,'v2/denoised.wav'),'-b:a','160k',os.path.join(d,'denoised.mp3'))
    shutil.copy(os.path.join(V60,'user_v60.mid'),os.path.join(d,'melody.mid'))
    n=sorted(pm.PrettyMIDI(os.path.join(d,'melody.mid')).instruments[0].notes,key=lambda x:x.start)
    json.dump([dict(pitch=x.pitch,start=round(x.start,4),end=round(x.end,4)) for x in n],open(os.path.join(d,'notes.json'),'w'))
    write_pod(pid,None,1,'Bob1',dict(audio='hum.aac',denoised='denoised.mp3',midi='melody.mid',notes='notes.json'),
      f'哼唱 {dur(AAC):.1f} 秒；降噪（80Hz HP＋頻譜 NR 0.5＋向下擴展器）；v60 轉出 {len(n)} 個音、13 句。',[ 'Bob1：哼唱',CRED_V60],title='月台')
    log(f'Bob1 → {pid}（豆1，{len(n)} 音）'); return pid

def lyric_pod(parent,author,lyr,title):
    pid=alloc(parent,2); d=os.path.join(PODS,pid); root=chain(parent)[0]['id']
    shutil.copy(lyr,os.path.join(d,'lyrics.txt'))
    al=json.loads(subprocess.check_output(['node',os.path.join(HERE,'align_cli.js'),os.path.join(PODS,root,'notes.json'),lyr]))
    json.dump(al,open(os.path.join(d,'aligned.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    def ts(t): m=int(t//60); return f'[{m:02d}:{t-60*m:05.2f}]'
    open(os.path.join(d,'lyrics.lrc'),'w',encoding='utf8').write(''.join(f"{ts(a['start'])}{a['text']}\n" for a in al if a['start'] is not None))
    m=pm.PrettyMIDI(os.path.join(PODS,root,'melody.mid'))
    for a in al:
        if a['start'] is not None: m.lyrics.append(pm.Lyric(a['text'].encode('utf8').decode('latin1'),a['start']))
    m.write(os.path.join(d,'melody_lyrics.mid'))
    warn=[f"第{i+1}行 {a['chars']}字/{a['notes']}音" for i,a in enumerate(al) if a['chars']>a['notes']*1.6+1]
    write_pod(pid,parent,2,author,dict(lyrics='lyrics.txt',aligned='aligned.json',lrc='lyrics.lrc',midi='melody_lyrics.mid'),
      f'{len(al)} 行歌詞對到旋律句（行→句）。'+('字數偏多：'+'、'.join(warn) if warn else ''),[f'{author}：作詞'],title=title)
    log(f'{author} → {pid}（豆2，{len(al)} 行）'); return pid

def accomp_pod(parent,author,src,label,true_off):
    pid=alloc(parent,3); d=os.path.join(PODS,pid); root=chain(parent)[0]['id']
    shutil.copy(src,os.path.join(d,'accompaniment.mp3'))
    ff('-i',src,'-ac','1','-ar','22050','-f','f32le','/tmp/acc.f32')
    auto=float(subprocess.check_output(['node',os.path.join(HERE,'autooff_cli.js'),os.path.join(PODS,root,'notes.json'),'/tmp/acc.f32']).decode())
    off=true_off  # uploader listened and nudged to the known-correct value
    ff('-i',os.path.join(PODS,root,'denoised.mp3'),'-i',src,'-filter_complex',
       f'[0:a]adelay={int(off*1000)}|{int(off*1000)},volume=1.0[v];[1:a]volume=0.8[a];[v][a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95',
       '-ac','2','-b:a','160k',os.path.join(d,'preview_mix.mp3'))
    write_pod(pid,parent,3,author,dict(accompaniment='accompaniment.mp3',preview='preview_mix.mp3'),
      f'上傳伴奏「{label}」({dur(src):.1f}s)。自動對齊 {auto:.2f}s，試聽後手動調成 {off:.3f}s（誤差 {abs(auto-off)*1000:.0f} ms）。',
      [f'{author}：配樂（{label}，使用者上傳）',CRED_PIANO],align=dict(auto=auto,offset=off,unit='秒；人聲在伴奏時間軸上延後的秒數'))
    log(f'{author} → {pid}（豆3，{label}，auto {auto:.2f} → {off:.3f}）'); return pid

def ass_time(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f'{h}:{m:02d}:{s:05.2f}'
def bob4(parent,author):
    ok,miss=can_publish(parent)
    if not ok: log(f'{author} 想在 {parent} 做豆4 → 被擋下（缺豆 {miss}）'); return None
    pid=alloc(parent,4); d=os.path.join(PODS,pid); C=chain(parent); root=C[0]; lyr=[p for p in C if p['step']==2]; acc=[p for p in C if p['step']==3][-1]
    off=acc['align']['offset']; accf=os.path.join(PODS,acc['id'],'accompaniment.mp3'); voc=os.path.join(PODS,root['id'],'denoised.mp3')
    os.makedirs(os.path.join(d,'images'))
    imgs=['th1.jpg','th2.jpg','th3.jpg','cover.jpg','p2-bg.jpg']
    for i in imgs: shutil.copy(os.path.join(IMG,i),os.path.join(d,'images',i))
    # mix: vocal on accompaniment timeline + OpenAIR reverb send, loudness -14 LUFS
    ms=int(off*1000)
    ff('-i',voc,'-i',accf,'-i',IR,'-filter_complex',
       f'[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms},asplit[v1][v2];[v2][2:a]afir=dry=0:wet=1[rv];[rv]volume=0.22[rw];'
       f'[1:a]aresample=44100,volume=0.75[a];[v1][rw][a]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11',
       '-ar','44100','-b:a','192k',os.path.join(d,'final_mix.mp3'))
    D=dur(os.path.join(d,'final_mix.mp3'))
    al=json.load(open(os.path.join(PODS,lyr[-1]['id'],'aligned.json'),encoding='utf8')) if lyr else []
    head='[Script Info]\nScriptType: v4.00+\nPlayResX: 720\nPlayResY: 1280\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
    head+='Style: Lyr,Noto Sans CJK TC,50,&H00FFFFFF,&H00FFFFFF,&H99000000,&H00000000,1,0,0,0,100,100,0,0,1,4,1,2,50,50,200,1\nStyle: Ttl,Noto Serif CJK TC,40,&H00E9F5D4,&H00FFFFFF,&H99000000,&H00000000,1,0,0,0,100,100,2,0,1,3,0,8,40,40,90,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    ev=[f'Dialogue: 0,{ass_time(0)},{ass_time(D)},Ttl,,0,0,0,,豆莢浪歌・{root.get("title","")}']
    for i,a in enumerate(al):
        if a['start'] is None: continue
        s=a['start']+off; e=min((al[i+1]['start']+off) if i+1<len(al) and al[i+1]['start'] is not None else a['end']+off+2, a['end']+off+1.5)
        ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Lyr,,0,0,0,,{a['text'].replace('　','\\N') if len(a['text'])>12 else a['text']}")
    open(os.path.join(d,'subtitles.ass'),'w',encoding='utf8').write(head+'\n'.join(ev)+'\n')
    seg=D/len(imgs); xf=1.0; inputs=[]; fl=[]
    for k,i in enumerate(imgs):
        inputs+=['-loop','1','-t',f'{seg+xf:.3f}','-i',os.path.join(d,'images',i)]
        fl.append(f'[{k}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,format=yuv420p[i{k}]')
    last='i0'
    for k in range(1,len(imgs)):
        fl.append(f'[{last}][i{k}]xfade=transition=fade:duration={xf}:offset={k*seg-xf/2 if k==1 else k*seg:.3f}[x{k}]'.replace(f'offset={k*seg-xf/2 if k==1 else k*seg:.3f}',f'offset={k*seg:.3f}')); last=f'x{k}'
    fl.append(f"[{last}]subtitles={os.path.join(d,'subtitles.ass')}:fontsdir=/usr/share/fonts/opentype/noto[vout]")
    ff(*inputs,'-i',os.path.join(d,'final_mix.mp3'),'-filter_complex',';'.join(fl),'-map','[vout]','-map',f'{len(imgs)}:a','-c:v','libx264','-preset','medium','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',os.path.join(d,'video.mp4'))
    ff('-ss','20','-i',os.path.join(d,'video.mp4'),'-frames:v','1','-vf','scale=360:-1',os.path.join(d,'poster.jpg'))
    authors=' → '.join(f"{p['author']}(豆{p['step']})" for p in C)
    write_pod(pid,parent,4,author,dict(mix='final_mix.mp3',video='video.mp4',subtitles='subtitles.ass',poster='poster.jpg',images=[f'images/{i}' for i in imgs]),
      f'選 {acc["id"]}；原唱（Bob1 降噪人聲）＋伴奏，OpenAIR 殘響，−14 LUFS；720×1280 直式 MP4 {D:.1f}s，{len(ev)-1} 句字幕。接力：{authors}',
      sorted({c for p in C for c in p['credits']})+[CRED_IR,'圖片：豆莢浪歌 UX 素材 ux/img','用 豆莢浪歌 製作'],published=True,title=root.get('title'))
    log(f'{author} → {pid}（豆4 發布，{D:.1f}s）'); return pid

def naive_race():
    """What happens WITHOUT atomic allocation: both read the folder, pick the same next name, second write overwrites."""
    base='/tmp/naive_pods'; shutil.rmtree(base,ignore_errors=True); os.makedirs(base+'/8-2a')
    res={}
    def take(who):
        ex=[x for x in os.listdir(base) if x.startswith('8-2')]; pid='8-2'+'abcdefgh'[len(ex)]
        time.sleep(0.05); os.makedirs(base+'/'+pid,exist_ok=True)
        json.dump({'author':who},open(f'{base}/{pid}/pod.json','w')); res[who]=pid
    ts=[threading.Thread(target=take,args=(w,)) for w in ('Bob5','Bob6')]; [t.start() for t in ts]; [t.join() for t in ts]
    survivor=json.load(open(f"{base}/{res['Bob5']}/pod.json"))['author']
    return res,survivor

def main():
    shutil.rmtree(PODS,ignore_errors=True); os.makedirs(PODS)
    r=bob1()
    l=lyric_pod(r,'Bob2',os.path.join(HERE,'lyrics.txt'),'月台')
    a=accomp_pod(l,'Bob3',os.path.join(V60,'v4/accomp_only.mp3'),'極簡鋼琴＋貝斯（v4）',2.8179)
    b=accomp_pod(l,'Bob3',os.path.join(V60,'v3/accomp_only.mp3'),'鋼琴＋弦樂（v3）',2.8179)
    bob4(a,'Bob4')
    # edge 1: skip 豆2 (1 → 3 directly), then try to publish
    s=accomp_pod(r,'Bob3',os.path.join(V60,'v4/accomp_only.mp3'),'極簡鋼琴＋貝斯（v4，跳過豆2）',2.8179)
    bob4(s,'Bob4')
    # edge 2: same author does two 豆 (Bob2 also does 豆3 on his own lyrics)
    accomp_pod(l,'Bob2',os.path.join(V60,'v3/accomp_only.mp3'),'鋼琴＋弦樂（v3，Bob2 自己配）',2.8179)
    # edge 3: two people take the same 豆 at the same moment
    res,surv=naive_race(); log(f'無鎖版同時接手：{res}，資料夾只剩 {surv} 的 pod.json → 覆蓋！')
    out={}
    th=[threading.Thread(target=lambda w,f:out.__setitem__(w,lyric_pod(r,w,os.path.join(HERE,f),'月台')),args=(w,f)) for w,f in (('Bob5','lyrics_bob5.txt'),('Bob6','lyrics_bob6.txt'))]
    [t.start() for t in th]; [t.join() for t in th]; log(f'有鎖版同時接手：{out}（沒有覆蓋）')
    idx=[]
    for pid in sorted(os.listdir(PODS),key=lambda s:(s.count('-'),s)):
        if not os.path.isdir(os.path.join(PODS,pid)): continue
        p=load(pid); idx.append({k:p.get(k) for k in ('id','parent','step','author','created','title','notes','published')})
    json.dump(dict(generated=now(),root='8',pods=idx),open(os.path.join(PODS,'index.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    open(os.path.join(HERE,'sim_log.txt'),'w',encoding='utf8').write('\n'.join(LOG)+'\n')
main()
