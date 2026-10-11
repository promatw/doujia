import sys,subprocess,re
from PIL import Image
name,out=sys.argv[1],sys.argv[2]
url=f'file:///workspace/doujia/mockup/src/{name}'
base=['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1','--virtual-time-budget=3000']
dom=subprocess.run(base+['--window-size=1400,1500','--dump-dom',url],capture_output=True,text=True).stdout
h=int(float(re.search(r'data-h="([\d.]+)"',dom).group(1)))
subprocess.run(base+[f'--window-size=1400,{h}',f'--screenshot={out}',url],capture_output=True)
print(Image.open(out).size)
