import csv, subprocess, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
BG="#0B1220"; INK="#F8FAFC"; GREY="#9AA4B2"; GRID="#1B2538"; COB="#5B88FF"; RED="#FF5C61"; GOLD="#E0A22B"
rows=list(csv.DictReader(open("/tmp/owid.csv",encoding="utf-8")))
Y=np.arange(2000,2025)
def s(c):
    d={int(r["year"]):float(r["per_capita_electricity"]) for r in rows if r["country"]==c and r["per_capita_electricity"]}
    return [d[int(y)] for y in Y]
S=[("US",s("United States"),INK),("China",s("China"),RED),("World",s("World"),GREY),("India",s("India"),GOLD)]
FPS=30
SEG=[(6.0,2000,2009),(2.5,2009,2011),(5.0,2011,2024)]
INTRO=0.8; HOLD=2.0; END=3.0
def year_at(t):
    if t<INTRO: return 2000.0
    t-=INTRO
    for d,a,b in SEG:
        if t<=d: return a+(b-a)*t/d
        t-=d
    return 2024.0
total=INTRO+sum(d for d,_,_ in SEG)+HOLD+END; NF=int(total*FPS)
fig=plt.figure(figsize=(10.8,19.2),dpi=100,facecolor=BG)
fig.text(0.09,0.945,"China makes 5x\nIndia's electricity\nper person",fontsize=56,fontweight="bold",color=INK,va="top",linespacing=1.05)
sub=fig.text(0.09,0.790,"",fontsize=25,color=GREY,va="top",linespacing=1.35)
yr=fig.text(0.91,0.700,"2000",fontsize=70,fontweight="bold",color=INK,ha="right",va="center",alpha=0.95)
unit=fig.text(0.09,0.700,"kWh generated per person",fontsize=19,color=GREY,va="center")
fig.text(0.09,0.095,"Source: Ember and Energy Institute via Our World in Data",fontsize=15,color=GREY,va="top")
fig.text(0.09,0.060,"CHART2DAY",fontsize=24,fontweight="bold",color=COB,va="top")
ax=fig.add_axes([0.09,0.20,0.64,0.47],facecolor=BG)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=GREY,labelsize=17,length=0); ax.tick_params(axis="x",pad=22)
ax.set_xlim(2000,2024.8); ax.set_ylim(0,15500); ax.set_xticks([2000,2008,2016,2024]); ax.set_yticks([5000,10000,15000]); ax.yaxis.set_major_formatter(lambda v,_:f"{v:,.0f}")
ax.grid(axis="y",color=GRID,lw=1.2); ax.set_axisbelow(True)
glow=[];line=[];dot=[];ring=[];lab=[]
for n,v,c in S:
    g,=ax.plot([],[],color=c,lw=11,alpha=0.14,solid_capstyle="round"); l,=ax.plot([],[],color=c,lw=4.2,solid_capstyle="round")
    d=ax.scatter([],[],s=170,color=c,zorder=6); r=ax.scatter([],[],s=170,facecolor="none",edgecolor=c,lw=2,zorder=5)
    t=fig.text(0.81,0.5,"",fontsize=22,fontweight="bold",color=c,va="center",ha="left")
    glow.append(g);line.append(l);dot.append(d);ring.append(r);lab.append(t)
banner=fig.text(0.5,0.135,"",fontsize=28,fontweight="bold",color=BG,ha="center",va="center",bbox=dict(boxstyle="round,pad=0.55",fc=RED,ec="none"),alpha=0)
cta=fig.text(0.5,0.50,"",fontsize=44,fontweight="bold",color=INK,ha="center",va="center",linespacing=1.3,alpha=0)
fig.canvas.draw(); W,H=fig.canvas.get_width_height()
out="2026-11-10-chart2day-electricity-race.mp4"
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
def subtitle(y,fin):
    if fin: return "2024: China 7,107 kWh, India 1,404\nWorld 3,790, US 12,712"
    if y<2007: return "2000: China makes 2x India's\nelectricity per person"
    if y<2010: return "2007: the US peaks at 13,724 kWh\nper person"
    return "China: 3,113 kWh in 2010,\n7,107 in 2024"
for f in range(NF):
    t=f/FPS; tl=t-(INTRO+sum(d for d,_,_ in SEG)); ending=tl>=HOLD
    y=year_at(t)
    xs=np.linspace(2000,y,max(2,int((y-2000)*8)+2)); ends=[]
    for i,(n,v,c) in enumerate(S):
        yy=np.interp(xs,Y,v); glow[i].set_data(xs,yy); line[i].set_data(xs,yy)
        cur=float(np.interp(y,Y,v)); ends.append(cur); dot[i].set_offsets([[y,cur]])
        k=(t*1.6)%1.0; ring[i].set_offsets([[y,cur]]); ring[i].set_sizes([170+900*k]); ring[i].set_alpha(0.7*(1-k))
    order=np.argsort(ends)[::-1]; pos={}; last=None
    for idx in order:
        yv=ends[idx]
        if last is not None and last-yv<1200: yv=last-1200
        pos[idx]=yv; last=yv
    for i,(n,v,c) in enumerate(S):
        px=ax.transData.transform((min(y,2024)+0.6,pos[i])); lab[i].set_position(((px[0]+24)/W,px[1]/H)); lab[i].set_text(f"{n} {ends[i]:,.0f}")
    yr.set_text(str(min(2024,int(round(y)))))
    sub.set_text(subtitle(y,y>=2024 and tl>=0.2))
    ba=0
    if 2010.0<=y<2014.5 and not ending: ba=min(1,(y-2010.0)/0.3)
    banner.set_text("China passes the world average: 2010" if ba>0 else ""); banner.set_alpha(ba)
    if ending:
        e=min(1,(tl-HOLD)/0.5); banner.set_text("")
        if e>=1: ax.set_visible(False)
        for tt in [sub,yr,unit]: tt.set_alpha(max(0,1-e)*(0.95 if tt is yr else 1))
        for i in range(4): lab[i].set_alpha(max(0,1-e)); glow[i].set_alpha(0.14*(1-e)); line[i].set_alpha(1-e); dot[i].set_alpha(1-e); ring[i].set_alpha(0)
        cta.set_text("Does power per person\nmean progress?\n\nTell us below.\nFollow @chart2day"); cta.set_alpha(e)
    fig.canvas.draw(); ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
ff.stdin.close(); ff.wait(); print("frames",NF,"sec",round(NF/FPS,1))
