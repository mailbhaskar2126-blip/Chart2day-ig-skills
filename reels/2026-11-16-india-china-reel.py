import subprocess, json
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w,s): return ImageFont.truetype(F%w,s)
COB=(31,79,216); ORG=(255,106,19); INK=(11,18,32); GREY=(107,114,128); LIGHT=(229,231,235); WHITE=(255,255,255)
D=json.load(open("2026-11-16-india-china-gdp-per-capita.json"))
YRS=list(range(1990,2026)); IN=[D["IN"][str(y)] for y in YRS]; CN=[D["CN"][str(y)] for y in YRS]
X0,X1=130,930; YT,YB=720,1520; VMAX=15000
def vx(i): return X0+(X1-X0)*i/(len(YRS)-1)
def vy(v): return YB-v/VMAX*(YB-YT)
T0=1.2; PER=0.26; T_END=T0+PER*(len(YRS)-1); DUR=T_END+3.6
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
bg=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(bg)
d.text((60,210),"In 1990, India was",font=font("ExtraBold",92),fill=INK)
d.text((60,320),"richer than China.",font=font("ExtraBold",92),fill=COB)
d.text((60,450),"GDP per person, current US$",font=font("Regular",38),fill=GREY)
for v in (0,5000,10000,15000):
    y=vy(v); d.line([(X0,y),(X1,y)],fill=INK if v==0 else LIGHT,width=3 if v==0 else 2)
    d.text((X0-14,y),f"${v//1000}k" if v else "$0",font=font("Regular",26),fill=GREY,anchor="rm")
for y in (1990,2000,2010,2020,2025):
    d.text((vx(y-1990),YB+36),str(y),font=font("SemiBold",26),fill=GREY,anchor="mm")
d.text((60,1740),"Source: World Bank, GDP per capita (current US$), 1990–2025",font=font("Regular",26),fill=GREY)
d.text((60,1790),"CHART2DAY",font=font("ExtraBold",40),fill=COB)
def pos(vals,t):
    f=min(len(YRS)-1,max(0,(t-T0)/PER)); i=int(f); r=f-i
    pts=[(vx(k),vy(vals[k])) for k in range(i+1)]
    if i<len(YRS)-1:
        a=vals[i]+(vals[i+1]-vals[i])*r; pts.append((vx(i+r),vy(a)))
    else: a=vals[-1]
    return pts,a
def frame(t):
    im=bg.copy(); d=ImageDraw.Draw(im)
    if t>=T0:
        for vals,col,name,dy in ((IN,COB,"India",-1),(CN,ORG,"China",1)):
            pts,a=pos(vals,t)
            if len(pts)>1: d.line(pts,fill=col,width=10,joint="curve")
            x,y=pts[-1]; d.ellipse([x-13,y-13,x+13,y+13],fill=col)
            lab=f"{name} ${a:,.0f}"
            d.text((min(x-20,X1-20),y+(-44 if dy<0 else -50 if name=="China" else 44)),lab,font=font("Bold",34),fill=col,anchor="rm" if x>700 else "lm")
        f=min(len(YRS)-1,(t-T0)/PER); d.text((60,560),str(1990+int(f)),font=font("ExtraBold",80),fill=INK)
    if t>=T_END+0.5:
        a=ease((t-T_END-0.5)/0.7)
        ov=Image.new("RGBA",(W,H),(255,255,255,0)); od=ImageDraw.Draw(ov)
        od.rectangle([40,190,1040,540],fill=(255,255,255,int(255*a)))
        im=Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(im)
        d.text((60,210),"Today, China is",font=font("ExtraBold",92),fill=INK,)
        d.text((60,320),"5× richer per person.",font=font("ExtraBold",92),fill=ORG)
        d.text((60,450),"GDP per person, current US$",font=font("Regular",38),fill=GREY)
        # only fade in new text over blank: cheat by drawing at alpha
    return im
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-an","/tmp/ic_silent.mp4"],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); ff.wait(); print("dur",DUR)
