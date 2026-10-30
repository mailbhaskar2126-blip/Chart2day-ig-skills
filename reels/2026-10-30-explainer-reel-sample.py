import subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/Inter-%s.otf"
fnt=lambda w,s: ImageFont.truetype(F%w,s)
INK=(20,20,24); PAPER=(238,236,230); G1=(120,120,124); G2=(165,165,168); G3=(205,204,200); YEL=(250,204,40); COB=(31,79,216); WHITE=(255,255,255); RED=(229,72,77)
ease=lambda x:(lambda y:1-(1-y)**3)(max(0,min(1,x)))
back=lambda x:(lambda y:1+2.7*(y-1)**3+1.7*(y-1)**2)(max(0,min(1,x)))
bg=Image.new("RGB",(W,H),PAPER); bd=ImageDraw.Draw(bg)
for y in range(H): 
    c=int(238-14*abs(y-H/2)/(H/2)); bd.line([(0,y),(W,y)],fill=(c,c-2,c-8))
def tag(im,text,cx,cy,t,t0,rot=-4,size=64,fill=YEL,fg=INK):
    p=back((t-t0)/0.35)
    if p<=0: return
    f=fnt("ExtraBold",size); b=ImageDraw.Draw(Image.new("RGB",(1,1))).textbbox((0,0),text,font=f)
    w,h=b[2]-b[0]+56,b[3]-b[1]+40
    t_im=Image.new("RGBA",(w,h),(0,0,0,0)); td=ImageDraw.Draw(t_im)
    td.rectangle([0,0,w,h],fill=fill+(255,)); td.text((w/2,h/2-4),text,font=f,fill=fg,anchor="mm")
    t_im=t_im.resize((max(1,int(w*p)),max(1,int(h*p)))).rotate(rot,expand=True,resample=Image.BICUBIC)
    im.paste(t_im,(int(cx-t_im.width/2),int(cy-t_im.height/2)),t_im)
def typed(d,text,x,y,t,t0,f,fill=INK,cps=26,maxw=960):
    n=int(max(0,(t-t0))*cps); s=text[:n]
    d.multiline_text((x,y),s,font=f,fill=fill,spacing=12)
def bank(d,cx,base,s=1.0,col=G1):
    w=520*s
    d.polygon([(cx-w/2-30*s,base-330*s),(cx,base-470*s),(cx+w/2+30*s,base-330*s)],fill=col)
    d.rectangle([cx-w/2-30*s,base-330*s,cx+w/2+30*s,base-300*s],fill=G2)
    for i in range(5):
        x=cx-w/2+i*(w/4)
        d.rectangle([x-28*s,base-300*s,x+28*s,base-40*s],fill=G3 if i%2 else (190,190,192))
    d.rectangle([cx-w/2-60*s,base-40*s,cx+w/2+60*s,base],fill=G2)
    d.ellipse([cx-40*s,base-420*s,cx+40*s,base-340*s],fill=PAPER)
    d.text((cx,base-380*s),"₹",font=fnt("ExtraBold",int(70*s)),fill=INK,anchor="mm")
def house(d,cx,base,s=1.0):
    d.polygon([(cx-260*s,base-250*s),(cx,base-460*s),(cx+260*s,base-250*s)],fill=G1)
    d.rectangle([cx-210*s,base-250*s,cx+210*s,base],fill=G3)
    d.rectangle([cx-50*s,base-170*s,cx+50*s,base],fill=G1)
    for x in (-150,110): d.rectangle([cx+x*s,base-200*s,cx+(x+60)*s,base-130*s],fill=G2)
def coin(d,cx,cy,r,label="₹"):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=G1); d.ellipse([cx-r*0.8,cy-r*0.8,cx+r*0.8,cy+r*0.8],fill=G3)
    d.text((cx,cy-4),label,font=fnt("ExtraBold",int(r*1.1)),fill=INK,anchor="mm")
def brand(d):
    d.text((60,70),"CHART2DAY",font=fnt("ExtraBold",44),fill=COB)
def source(d,t):
    d.text((60,1800),"Source: Reserve Bank of India policy decision, 7 Oct 2026",font=fnt("Regular",26),fill=G1)
DUR=22.5
def frame(t):
    im=bg.copy(); d=ImageDraw.Draw(im); brand(d); source(d,t)
    if t<4.5:   # S1
        typed(d,"RBI just\nraised\ninterest rates",60,300,t,0.2,fnt("ExtraBold",118),cps=18)
        by=H-120+(1-ease(t/1.2))*600; bank(d,540,by,1.25)
        tag(im,"RBI",800,520,t,0.5,-6); tag(im,"Oct 2026",780,1010,t,2.6,5,52,WHITE,INK)
    elif t<9.2: # S2
        u=t-4.5
        d.text((60,300),"The repo rate",font=fnt("ExtraBold",92),fill=INK)
        d.text((60,410),"went up by",font=fnt("ExtraBold",92),fill=INK)
        tag(im,"25 bps",420,640,t,5.0,-4,92)
        p=ease((u-1.2)/1.6); v=5.25+0.25*p
        d.text((540,1040),f"{v:.2f}%",font=fnt("ExtraBold",260),fill=INK,anchor="mm")
        d.text((540,1230),"from 5.25%",font=fnt("SemiBold",50),fill=G1,anchor="mm")
        coin(d,230,1480,110); coin(d,860,1500,80,"%")
        tag(im,"repo rate",800,780,t,6.2,5,56,WHITE,INK)
    elif t<14.0: # S3 timeline
        u=t-9.2
        d.text((60,300),"First hike\nsince Feb 2023",font=fnt("ExtraBold",104),fill=INK,spacing=10)
        pts=[(2023.1,6.50),(2025.1,6.25),(2025.3,6.00),(2025.45,5.50),(2025.95,5.25),(2026.77,5.50)]
        X0,X1,Y0,Y1=90,990,1200,1560
        mx=lambda x:X0+(x-2023.0)/(2026.9-2023.0)*(X1-X0); my=lambda r:Y1-(r-5.0)/(6.7-5.0)*(Y1-Y0)
        d.line([(X0,Y1),(X1,Y1)],fill=G2,width=3)
        for yr in (2023,2024,2025,2026): d.text((mx(yr+0.5),Y1+34),str(yr),font=fnt("SemiBold",28),fill=G1,anchor="mm")
        prog=ease((u-0.8)/2.6); segs=[]
        for i,(x,r) in enumerate(pts):
            segs.append((mx(x),my(r)))
            if i+1<len(pts): segs.append((mx(pts[i+1][0]),my(r)))
        n=max(2,int(len(segs)*prog)); d.line(segs[:n],fill=COB,width=9,joint="curve")
        if prog>0.98:
            d.ellipse([mx(2026.77)-16,my(5.5)-16,mx(2026.77)+16,my(5.5)+16],fill=RED)
        tag(im,"6.50%",mx(2023.35),my(6.5)-70,t,10.4,-4,48,WHITE,INK); tag(im,"5.25%",mx(2025.95),my(5.25)+80,t,12.2,4,48,WHITE,INK)
        tag(im,"5.50%",mx(2026.5)-30,my(5.5)-84,t,13.0,-4,52,YEL,INK)
    elif t<19.0: # S4
        u=t-14.0
        hy=H-220+(1-ease(u/1.0))*700; house(d,560,hy,1.35)
        typed(d,"Why it matters:\nloans can get\ncostlier",60,300,t,14.2,fnt("ExtraBold",104),cps=20)
        tag(im,"EMIs",760,1000,t,16.0,5,76); tag(im,"home loans",330,1180,t,17.0,-5,56,WHITE,INK)
    else:        # S5
        typed(d,"The RBI also\nswitched its\nstance to",60,300,t,19.2,fnt("ExtraBold",104),cps=22)
        tag(im,"calibrated tightening",540,900,t,20.0,-3,64)
        d.text((60,1150),"More charts every day",font=fnt("SemiBold",52),fill=INK)
        d.text((60,1230),"Follow @chart2day",font=fnt("ExtraBold",64),fill=COB)
    return im
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-an","2026-10-30-explainer-reel-sample.mp4"],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); ff.wait(); print("ok")
