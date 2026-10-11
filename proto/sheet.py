import sys,glob
from PIL import Image,ImageDraw,ImageFont
files=sys.argv[2:]; out=sys.argv[1]
cols=min(5,len(files)); w,h=390,844; g=30; lab=40
rows=(len(files)+cols-1)//cols
S=Image.new('RGB',(g+cols*(w+g),g+rows*(h+lab+g)),(8,12,10))
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',20)
d=ImageDraw.Draw(S)
for i,fn in enumerate(files):
    im=Image.open(fn).convert('RGB').resize((w,h),Image.LANCZOS)
    x=g+(i%cols)*(w+g); y=g+(i//cols)*(h+lab+g)
    d.text((x,y),fn.split('/')[-1][:-4],font=f,fill=(190,210,200))
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),44,fill=255)
    S.paste(im,(x,y+lab),m)
S.save(out); print(S.size)
