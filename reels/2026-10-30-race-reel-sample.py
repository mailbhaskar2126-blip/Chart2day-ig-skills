import subprocess
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/Inter-%s.otf"
fnt=lambda w,s: ImageFont.truetype(F%w,s)
COB=(31,79,216); GOLD=(214,150,10); TEAL=(14,148,136); INK=(11,18,32); GREY=(107,114,128); LIGHT=(229,231,235); WHITE=(255,255,255)
yrs=list(range(2005,2027))
sensex=[9397.93,13786.91,20286.99,9647.31,17464.81,20509.09,15454.92,19426.71,21170.68,27499.42,26117.54,26626.46,34056.83,36068.33,41253.74,47751.33,58253.82,60840.74,72240.26,78139.01,85220.60,73123.83]
nifty=[2836.55,3966.40,6138.60,2959.15,5201.05,6134.50,4624.30,5905.10,6304.00,8282.70,7946.35,8185.80,10530.70,10862.55,12168.45,13981.75,17354.05,18105.30,21731.40,23644.80,26129.60,22600.00]
gold=[7000,8400,9428,12361,15417,18448,24130,29926,28848,27708,26671,30128,29174,30692,35154,47562,47437,51249,58836,77000,133195,143020]
S=[("Gold",[100000*g/gold[0] for g in gold],GOLD),("Sensex",[100000*s/sensex[0] for s in sensex],COB),("Nifty 50",[100000*n/nifty[0] for n in nifty],TEAL)]
T0,STEP,HOLD=1.2,0.5,3.0; DUR=T0+STEP*(len(yrs)-1)+HOLD
ease=lambda t:(lambda x:x*x*(3-2*x))(max(0,min(1,t)))
def val(vs,u):
    u=max(0,min(len(vs)-1,u)); i=int(u); 
    if i>=len(vs)-1: return vs[-1]
    return vs[i]+(vs[i+1]-vs[i])*ease(u-i)
bg=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(bg)
d.rectangle([0,230,W,470],fill=COB)
d.text((60,262),"₹1 lakh invested in 2005",font=fnt("ExtraBold",66),fill=WHITE)
d.text((60,348),"What is it worth now?",font=fnt("SemiBold",52),fill=(200,214,250))
d.text((60,415),"Gold vs Sensex vs Nifty 50",font=fnt("Regular",34),fill=(200,214,250))
d.text((60,1650),"Source: BSE, NSE year-end closes. Gold: yearly average 24K price",font=fnt("Regular",24),fill=GREY)
d.text((60,1688),"per 10g (2026: spot price, 29 Jun). Indicative, pre-tax.",font=fnt("Regular",24),fill=GREY)
d.text((60,1726),"Not investment advice.",font=fnt("Regular",24),fill=GREY)
d.text((60,1790),"CHART2DAY",font=fnt("ExtraBold",40),fill=COB)
X0,X1=330,1020; BH=130; GAP=45; Y0=620
def frame(t):
    u=(t-T0)/STEP; im=bg.copy(); d=ImageDraw.Draw(im)
    vals=[(n,val(vs,u),c) for n,vs,c in S]
    mx=max(v for _,v,_ in vals)*1.12
    order=sorted(vals,key=lambda r:-r[1])
    for n,v,c in vals:
        import math
        rank=sum(max(0.0,min(1.0,(o-v)/(0.003*mx)+0.5)) for _,o,_ in vals if o is not v)
        # smooth rank via previous-step ordering blend
        u2=max(0,u-0.0); y=Y0+rank*(BH+GAP)
        w=max(6,(X1-X0)*v/mx)
        d.rounded_rectangle([X0,y,X0+w,y+BH],radius=10,fill=c)
        d.text((60,y+BH/2),n,font=fnt("Bold",42),fill=INK,anchor="lm")
        d.text((X0+w-16,y+BH/2),f"₹{v/100000:.1f} L" if w>260 else "",font=fnt("ExtraBold",44),fill=WHITE,anchor="rm")
        if w<=260: d.text((X0+w+14,y+BH/2),f"₹{v/100000:.1f} L",font=fnt("ExtraBold",44),fill=INK,anchor="lm")
    yi=int(round(max(0,min(len(yrs)-1,u))))
    d.text((1020,1330),str(yrs[yi]),font=fnt("ExtraBold",190),fill=LIGHT,anchor="ra")
    d.text((1020,1330),str(yrs[yi]),font=fnt("ExtraBold",190),fill=(205,213,238),anchor="ra")
    return im
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-an","2026-10-30-race-reel-sample.mp4"],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); ff.wait(); print(DUR)
