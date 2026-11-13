import json, subprocess, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
BG="#FFFFFF"; INK="#0B1220"; GREY="#6B7280"; LIGHT="#E5E7EB"; COB="#1F4FD8"; RED="#E5484D"; BAR="#AEBBD6"
D={k:{int(y):v for y,v in d.items()} for k,d in json.load(open("2026-11-13-population-race-worldbank.json")).items()}
WLD={int(y):v for y,v in json.load(open("2026-11-13-world-population-worldbank.json")).items()}
SHORT={"United States":"United States","Russian Federation":"Russia","United Kingdom":"UK"}
YRS=np.arange(1960,2026); N=list(D)
V=np.array([[D[n][y]/1e6 for y in YRS] for n in N])            # millions
RK=np.array([np.argsort(np.argsort(-V[:,j])) for j in range(len(YRS))]).T.astype(float)
FPS=30; HOOK=1.6; SEG=[(9.0,1960,2015),(4.0,2015,2025)]; HOLD=2.2; END=3.2
RACE=sum(d for d,_,_ in SEG); TOT=HOOK+RACE+HOLD+END; NF=int(TOT*FPS)
def year_at(t):
    t-=HOOK
    if t<=0: return 1960.0
    for d,a,b in SEG:
        if t<=d: return a+(b-a)*t/d
        t-=d
    return 2025.0
ease=lambda x:1-(1-min(max(x,0),1))**3
fig=plt.figure(figsize=(10.8,19.2),dpi=100,facecolor=BG); ax=fig.add_axes([0,0,1,1]); W,H=1080,1920
X0,XW=330,560; Y0,RH=560,104
cross=None
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","/tmp/claude-0/-home-claude/69c34abb-c808-5373-8a6a-0e6de21c468a/scratchpad/pop/silent.mp4"],stdin=subprocess.PIPE)
for f in range(NF):
    t=f/FPS; y=year_at(t); ax.clear(); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    tl=t-(HOOK+RACE); ending=tl>=HOLD; e=ease((tl-HOLD)/0.5) if ending else 0
    ax.text(70,150,"CHART2DAY",fontsize=22,fontweight="bold",color=COB,va="center")
    ax.text(70,250,"The world's most\npopulous countries",fontsize=58,fontweight="bold",color=INK,va="top",linespacing=1.05)
    if t<HOOK:
        a=ease(t/0.25); ax.text(540,880,"8.2",fontsize=300,fontweight="bold",color=COB,ha="center",va="center",alpha=a)
        ax.text(540,1090,"billion people",fontsize=64,fontweight="bold",color=INK,ha="center",va="center",alpha=a)
        ax.text(540,1210,"Which countries have the most?",fontsize=36,color=GREY,ha="center",va="center",alpha=ease((t-0.4)/0.3))
    elif not ending or e<1:
        al=1-e; j=min(int(y-1960),len(YRS)-2); u=y-1960-j
        v=V[:,j]*(1-u)+V[:,j+1]*u; r=RK[:,j]*(1-(u*u*(3-2*u)))+RK[:,j+1]*(u*u*(3-2*u))
        wv=(WLD[1960+j]*(1-u)+WLD[1961+j]*u)/1e9; mx=v.max()
        ax.text(70,420,f"Population, millions · World: {wv:.1f} billion",fontsize=24,color=GREY,va="center",alpha=al)
        ax.text(1010,1560,f"{int(y)}",fontsize=120,fontweight="bold",color=LIGHT,ha="right",va="center",alpha=al)
        for i,n in enumerate(N):
            if r[i]>9.6: continue
            ba=al*min(1,(9.6-r[i])/0.6) if r[i]>9 else al
            yy=Y0+r[i]*RH; col=COB if n=="India" else RED if n=="China" else BAR; wd=XW*v[i]/mx
            ax.add_patch(Rectangle((X0,yy),wd,RH*0.72,color=col,alpha=ba,lw=0))
            ax.text(X0-18,yy+RH*0.36,SHORT.get(n,n),fontsize=25,fontweight="bold",color=INK,ha="right",va="center",alpha=ba)
            ax.text(X0+wd+14,yy+RH*0.36,f"{v[i]:,.0f}",fontsize=25,fontweight="bold",color=col if col!=BAR else GREY,va="center",alpha=ba)
        iI,iC=N.index("India"),N.index("China")
        if v[iI]>v[iC] and cross is None: cross=t
        if cross is not None and not ending:
            b=ease((t-cross)/0.3); ax.text(540,1700,"India passes China",fontsize=34,fontweight="bold",color="white",ha="center",va="center",alpha=b,bbox=dict(boxstyle="round,pad=0.5",fc=COB,ec="none",alpha=b))
    if ending:
        ax.text(540,860,"India: 1.46 billion.\nChina: 1.41 billion.",fontsize=52,fontweight="bold",color=INK,ha="center",va="center",alpha=e,linespacing=1.3)
        ax.text(540,1120,"Who enters the\ntop 10 next?",fontsize=64,fontweight="bold",color=COB,ha="center",va="center",alpha=ease((tl-HOLD-0.3)/0.5),linespacing=1.15)
        ax.text(540,1340,"Tell us below · Follow @chart2day",fontsize=30,color=GREY,ha="center",va="center",alpha=ease((tl-HOLD-0.7)/0.5))
    ax.text(70,1830,"Source: World Bank (population, total), 1960 to 2025",fontsize=19,color=GREY,va="center")
    fig.canvas.draw(); ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
ff.stdin.close(); ff.wait(); print("frames",NF,"sec",round(TOT,1),"cross at",cross and round(cross,2))
