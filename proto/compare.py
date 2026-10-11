from PIL import Image,ImageDraw,ImageFont
B='/workspace/doujia/proto/'
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',26)
f2=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',20)
pairs=[('ref/ref-1.png','shots/01-onboard.png','首次啟動'),('ref/ref-2.png','shots/ref-b1.png','錄音'),('ref/ref-3.png','shots/06-b2-melody.png','旋律完成（版面已依新流程調整）')]
w,h=390,844; g=24; pg=60; top=110
W=pg*2+3*(2*w+g)+2*pg; H=top+h+70
S=Image.new('RGB',(W,H),(236,233,226)); d=ImageDraw.Draw(S)
d.text((pg,30),'豆莢浪歌 · 參考圖 vs HTML 原型（真文字、可互動）',font=f,fill=(20,30,25))
for i,(a,b,lab) in enumerate(pairs):
    x=pg+i*(2*w+g+pg)
    d.text((x,top-36),lab,font=f2,fill=(60,70,65))
    for j,fn in enumerate([a,b]):
        im=Image.open(B+fn).convert('RGB').resize((w,h),Image.LANCZOS)
        m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),46,fill=255)
        xx=x+j*(w+g); S.paste(im,(xx,top),m)
        d.text((xx+4,top+h+14),['參考圖（AI 生成 PNG）','HTML 原型截圖'][j],font=f2,fill=(80,90,85))
S.save(B+'compare.png'); print(S.size)
