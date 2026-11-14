import json, subprocess, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from PIL import Image
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
BG="#FFFFFF"; INK="#111318"; GREY="#8B919B"; BLUE="#4E8FC2"; ORANGE="#F2B33D"; COB="#1F4FD8"; PILL="#EFF0F3"; GRID="#E6E8EC"
D={k:{int(y):v for y,v in d.items()} for k,d in json.load(open("2026-11-14-gdp-race-worldbank.json")).items()}
ISO={"China":"cn","India":"in","United States":"us","Russian Federation":"ru","Indonesia":"id","Japan":"jp","Germany":"de","Brazil":"br","United Kingdom":"gb","France":"fr","Italy":"it","Canada":"ca","Korea, Rep.":"kr","Spain":"es","Australia":"au","Mexico":"mx"}
SHORT={"United States":"US","Russian Federation":"Russia","United Kingdom":"UK","Korea, Rep.":"S. Korea"}
FW,FH=92,62
FLAG={n:np.asarray(Image.open(f"2026-11-13-flags/{c}.png").convert("RGB").resize((FW*2,FH*2),Image.LANCZOS)) for n,c in ISO.items()}
YRS=np.arange(1990,2026); N=list(D)
V=np.array([[D[n][y] for y in YRS] for n in N],dtype=float)
RK=np.array([np.argsort(np.argsort(-V[:,j])) for j in range(len(YRS))]).T.astype(float)
EV=[(1990,"1990: US $6.0T, Japan $3.3T, China $0.4T"),(2007,"2007: China passes Germany for No. 3"),(2010,"2010: China passes Japan for No. 2"),(2023,"2023: Germany passes Japan for No. 3"),(2024.4,"2025: China $19.5T, 54× its 1990 size")]
FPS=30; START=0.8; RACE=11.7; HOLD=2.0; TOT=START+RACE+HOLD; NF=int(TOT*FPS)
W,H=1080,1920; X0=250; BW=420; Y0=608; RH=76; BH=62; ROWS=12
fig=plt.figure(figsize=(10.8,19.2),dpi=100,facecolor=BG); ax=fig.add_axes([0,0,1,1])
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","/tmp/claude-0/-home-claude/69c34abb-c808-5373-8a6a-0e6de21c468a/scratchpad/gdp/silent.mp4"],stdin=subprocess.PIPE)
def nice(mx):
    for s in (1e12,2e12,5e12,10e12):
        if mx/s<=3.2: return s
    return 10e12
for f in range(NF):
    t=f/FPS; y=1990+35*min(max((t-START)/RACE,0),1)
    ax.clear(); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    ax.text(68,186,"China's economy is 54×\nbigger than in 1990",fontsize=46,fontweight="bold",color=INK,va="top",linespacing=1.08)
    ax.text(70,378,"G D P ,   C U R R E N T   U S $",fontsize=19,color=INK,va="center")
    ax.add_patch(FancyBboxPatch((76,408),928,66,boxstyle="round,pad=6,rounding_size=10",fc=PILL,ec="none"))
    k=max(i for i,(ey,_) in enumerate(EV) if y>=ey); ta=min(1,(y-EV[k][0])/0.5+0.001) if k>0 else 1
    ax.text(540,441,EV[k][1],fontsize=22.5,color=INK,ha="center",va="center",alpha=ta)
    j=min(int(y-1990),len(YRS)-2); u=y-1990-j; q=min(1,u/0.45); s=q*q*(3-2*q)
    v=V[:,j]*(1-u)+V[:,j+1]*u; r=RK[:,j]*(1-s)+RK[:,j+1]*s; mx=v.max(); sc=BW/mx
    st=nice(mx); tk=0
    while tk<=mx*1.02:
        x=X0+tk*sc; ax.plot([x,x],[594,Y0+ROWS*RH-8],color=GRID,lw=1.2,zorder=1); ax.text(x,574,f"${tk/1e12:.0f}T",fontsize=12,color=GREY,ha="center",va="center"); tk+=st
    for i,n in enumerate(N):
        if r[i]>ROWS-0.4: continue
        a=min(1,(ROWS-0.4-r[i])/0.6) if r[i]>ROWS-1 else 1
        yy=Y0+r[i]*RH; wd=max(v[i]*sc,6)
        ax.add_patch(Rectangle((X0,yy),wd,BH,color=ORANGE if n=="China" else BLUE,lw=0,alpha=a,zorder=2))
        ax.imshow(FLAG[n],extent=(X0+wd,X0+wd+FW,yy+BH,yy),zorder=3,alpha=a,interpolation="bilinear",aspect="auto")
        ax.text(X0-14,yy+BH/2,SHORT.get(n,n),fontsize=22,fontweight="bold" if n=="China" else "normal",color=INK,ha="right",va="center",alpha=a)
        ax.text(X0+wd+FW+12,yy+BH/2,(f"${v[i]/1e12:.1f}T" if v[i]>=1e12 else f"${v[i]/1e12:.2f}T"),fontsize=20.5,color="#3B4048",va="center",alpha=a)
    ax.set_xlim(0,W); ax.set_ylim(H,0)
    ax.text(1004,1438,f"{int(y)}",fontsize=112,fontweight="bold",color="#9AA1AC",ha="right",va="center",zorder=4)
    ax.text(70,1568,"Source: World Bank, GDP (current US$), 1990–2025",fontsize=15,color=GREY,va="center")
    ax.text(1004,1568,"CHART2DAY",fontsize=22,fontweight="bold",color=COB,ha="right",va="center")
    fig.canvas.draw(); ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
ff.stdin.close(); ff.wait(); print("frames",NF,"sec",TOT)
