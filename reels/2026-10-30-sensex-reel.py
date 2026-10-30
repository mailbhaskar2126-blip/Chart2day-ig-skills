import subprocess, math
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w,s): return ImageFont.truetype(F%w,s)
COB=(31,79,216); RED=(229,72,77); INK=(11,18,32); GREY=(107,114,128); LIGHT=(229,231,235); WHITE=(255,255,255)
yrs=list(range(2005,2027))
ret=[42.3,46.7,47.1,-52.4,81.0,17.4,-24.6,25.7,9.0,29.9,-5.0,1.9,27.9,5.9,14.4,15.8,22.0,4.4,18.7,8.2,9.1,-14.2]
X0,X1=60,1020; YT,YB=640,1500          # chart box
VMIN,VMAX=-60,90
def vy(v): return YB-(v-VMIN)/(VMAX-VMIN)*(YB-YT)
slot=(X1-X0)/len(yrs); bw=slot*0.74
T_BARS=1.4; PER=0.42; T_BARS_END=T_BARS+PER*len(yrs)   # ~10.6
T_HOLD=T_BARS_END+1.6                                   # suspense on 2026
DUR=T_HOLD+3.2
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def ctext(d,xy,t,f,fill,anchor="mm"): d.text(xy,t,font=f,fill=fill,anchor=anchor)

# static background
bg=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(bg)
d.text((60,250),"Sensex:",font=font("ExtraBold",104),fill=INK)
d.text((60,365),"worst year since 2011",font=font("ExtraBold",78),fill=INK)
d.text((60,490),"Calendar-year return, BSE Sensex",font=font("Regular",36),fill=GREY)
for v in (-50,-25,0,25,50,75):
    y=vy(v); d.line([(X0,y),(X1,y)],fill=INK if v==0 else LIGHT,width=3 if v==0 else 2)
    d.text((X0-8,y-30),(f"{v:+d}%" if v else "0%"),font=font("Regular",24),fill=GREY,anchor="la") if False else None
for v in (-50,-25,25,50,75):
    d.text((X0+4,vy(v)-30),f"{v:+d}%",font=font("Regular",24),fill=GREY)
for i,y in enumerate(yrs):
    if y in (2005,2010,2015,2020,2026):
        ctext(d,(X0+slot*(i+0.5),YB+34+ (0)),str(y),font("SemiBold",26),GREY)
d.text((60,1740),"Source: BSE Sensex annual data; 2026 is year to date as of 23 Oct 2026",font=font("Regular",26),fill=GREY)
d.text((60,1790),"CHART2DAY",font=font("ExtraBold",40),fill=COB)

stripe=Image.new("L",(W,H),0); sd=ImageDraw.Draw(stripe)
for k in range(-H,W+H,22): sd.line([(k,0),(k+H,H)],fill=255,width=7)

notable={2008:"−52.4%",2009:"+81.0%",2011:"−24.6%",2015:"−5.0%"}
def frame(t):
    im=bg.copy(); d=ImageDraw.Draw(im)
    dim = ease((t-(T_HOLD+0.4))/0.8)           # end-phase dimming of old bars
    cur=None
    for i,y in enumerate(yrs):
        p=ease((t-(T_BARS+PER*i))/(PER*1.1))
        if p<=0: continue
        cur=i
        v=ret[i]*p; x=X0+slot*i+(slot-bw)/2
        y0,y1=vy(0),vy(v)
        top,bot=min(y0,y1),max(y0,y1)
        col=RED if ret[i]<0 else COB
        if i<len(yrs)-1: col=lerp(col,(235,238,245),0.70*dim)
        if y==2026:
            col=RED
        d.rectangle([x,top,x+bw,bot],fill=col)
        if y==2026 and bot-top>2:
            m=stripe.crop((0,0,W,H)); box=Image.new("RGB",(W,H),WHITE)
            region=Image.new("L",(W,H),0); ImageDraw.Draw(region).rectangle([x,top,x+bw,bot],fill=255)
            from PIL import ImageChops
            mm=ImageChops.multiply(m,region); im.paste(box,(0,0),mm.point(lambda a:int(a*0.55)))
            d=ImageDraw.Draw(im)
        if p>0.95 and y in notable and i<len(yrs)-1:
            ly=(bot+16) if ret[i]<0 else (top-52)
            c=INK if dim<0.5 else lerp(INK,(200,205,215),dim)
            ctext(d,(x+bw/2,ly+18),notable[y],font("Bold",30),c)
    # counter: year + return
    if cur is not None and t<T_HOLD:
        yr=yrs[cur]; r=ret[cur]*ease((t-(T_BARS+PER*cur))/(PER*1.1))
        d.text((60,560),str(yr),font=font("ExtraBold",70),fill=INK)
        col=RED if ret[cur]<0 else COB
        s=f"{ret[cur]:+.1f}%".replace("-","−")
        d.text((330,568),s,font=font("ExtraBold",62),fill=col)
    # 2026 suspense pulse + end callout
    if t>=T_BARS_END:
        a=ease((t-(T_HOLD+0.3))/0.7)
        if a>0:
            ov=Image.new("RGBA",(W,H),(255,255,255,0)); od=ImageDraw.Draw(ov)
            od.rectangle([40,560,1040,640],fill=(255,255,255,int(255*a)))
            im=Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(im)
            d.text((60,555),"2026",font=font("ExtraBold",70),fill=INK)
            d.text((330,563),"−14.2%",font=font("ExtraBold",62),fill=RED)
            d.text((640,590),"year to date",font=font("Regular",34),fill=GREY)
    return im

ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-an","2026-10-30-sensex-reel.mp4"],stdin=subprocess.PIPE)
n=int(DUR*FPS)
for k in range(n):
    ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); ff.wait()
print("frames",n,"dur",DUR)
