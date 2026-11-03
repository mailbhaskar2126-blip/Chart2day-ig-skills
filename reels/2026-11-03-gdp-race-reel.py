import subprocess, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
BG="#0B1220"; INK="#F8FAFC"; GREY="#9AA4B2"; GRID="#1B2538"; COB="#5B88FF"; TEAL="#12B5A5"; GOLD="#E0A22B"
Y=np.arange(1990,2026)
jp=[3.253,3.725,4.065,4.632,5.104,5.640,5.021,4.580,4.150,4.689,5.042,4.439,4.246,4.573,4.941,4.876,4.648,4.625,5.160,5.337,5.812,6.279,6.334,5.272,4.986,4.534,5.110,5.038,5.154,5.246,5.189,5.226,4.448,4.385,4.190,4.435]
ge=[1.778,1.876,2.141,2.079,2.215,2.593,2.507,2.219,2.248,2.214,1.967,1.966,2.102,2.535,2.852,2.893,3.046,3.484,3.808,3.479,3.467,3.824,3.596,3.807,3.965,3.425,3.537,3.765,4.055,3.960,3.941,4.355,4.201,4.562,4.686,5.051]
uk=[1.093,1.143,1.180,1.061,1.140,1.349,1.425,1.569,1.661,1.693,1.672,1.656,1.791,2.061,2.430,2.551,2.720,3.105,2.945,2.429,2.497,2.676,2.720,2.797,3.085,2.946,2.707,2.699,2.897,2.876,2.724,3.195,3.181,3.421,3.696,4.003]
ind=[0.321,0.270,0.288,0.279,0.327,0.360,0.393,0.416,0.421,0.459,0.468,0.485,0.515,0.608,0.709,0.820,0.940,1.217,1.199,1.342,1.676,1.823,1.828,1.857,2.039,2.104,2.295,2.651,2.703,2.836,2.675,3.167,3.250,3.501,3.761,3.956]
S=[("Japan",jp,INK),("Germany",ge,COB),("UK",uk,TEAL),("India",ind,GOLD)]
assert all(len(v)==36 for _,v,_ in S)
FPS=30
# timeline: (seconds, year_start, year_end)
SEG=[(9.0,1990,2019),(3.0,2019,2022),(3.0,2022,2023),(3.5,2023,2025)]
INTRO=1.0; HOLD=2.5; END=2.2
def year_at(t):
    if t<INTRO: return 1990.0
    t-=INTRO
    for d,a,b in SEG:
        if t<=d:
            u=t/d; return a+(b-a)*u
        t-=d
    return 2025.0
total=INTRO+sum(d for d,_,_ in SEG)+HOLD+END
NF=int(total*FPS)
def val(v,y):
    return float(np.interp(y,Y,v))
fig=plt.figure(figsize=(10.8,19.2),dpi=100,facecolor=BG)
fig.text(0.09,0.935,"Who is the world's\nNo. 3 economy?",fontsize=54,fontweight="bold",color=INK,va="top",linespacing=1.05)
sub=fig.text(0.09,0.832,"",fontsize=25,color=GREY,va="top",linespacing=1.35)
yr=fig.text(0.91,0.738,"1990",fontsize=70,fontweight="bold",color=INK,ha="right",va="center",alpha=0.95)
unit=fig.text(0.09,0.738,"GDP, trillions of US$",fontsize=19,color=GREY,va="center")
fig.text(0.09,0.095,"Source: World Bank WDI via FRED (current US$)",fontsize=15,color=GREY,va="top")
fig.text(0.09,0.060,"CHART2DAY",fontsize=24,fontweight="bold",color=COB,va="top")
ax=fig.add_axes([0.09,0.20,0.64,0.50],facecolor=BG)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=GREY,labelsize=17,length=0)
ax.set_xlim(1990,2026); ax.set_ylim(0,6.9); ax.set_xticks([1990,2000,2010,2020]); ax.set_yticks([2,4,6]); ax.yaxis.set_major_formatter(lambda v,_:f"${v:.0f}T")
ax.grid(axis="y",color=GRID,lw=1.2); ax.set_axisbelow(True)
glow=[];line=[];dot=[];ring=[];lab=[]
for n,v,c in S:
    g,=ax.plot([],[],color=c,lw=11,alpha=0.14,solid_capstyle="round"); l,=ax.plot([],[],color=c,lw=4.2,solid_capstyle="round")
    d=ax.scatter([],[],s=170,color=c,zorder=6); r=ax.scatter([],[],s=170,facecolor="none",edgecolor=c,lw=2,zorder=5)
    t=fig.text(0.81,0.5,"",fontsize=22,fontweight="bold",color=c,va="center",ha="left")
    glow.append(g);line.append(l);dot.append(d);ring.append(r);lab.append(t)
banner=fig.text(0.5,0.135,"",fontsize=30,fontweight="bold",color=BG,ha="center",va="center",bbox=dict(boxstyle="round,pad=0.55",fc=COB,ec="none"),alpha=0)
cta=fig.text(0.5,0.52,"",fontsize=46,fontweight="bold",color=INK,ha="center",va="center",linespacing=1.3,alpha=0)
fig.canvas.draw()
W,H=fig.canvas.get_width_height()
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","2026-11-03-gdp-race-reel.mp4"],stdin=subprocess.PIPE)
def subtitle(y,t_end):
    if t_end: return "2025: Germany $5.1T, Japan $4.4T,\nUK $4.0T, India $4.0T"
    if y<1996: return "1995: Japan's economy is\n2.2x the size of Germany's"
    if y<2000: return "1995-98: Japan's GDP falls 26%\nin dollars as the yen crashes"
    if y<2022: return "Japan: $5.0T in 2000, $5.2T\nin 2021. Almost no growth."
    if y<2023: return "2022: Japan's GDP falls 15%\nin a single year"
    return "2023: Germany overtakes Japan"
for f in range(NF):
    t=f/FPS
    tl=t-(INTRO+sum(d for d,_,_ in SEG))
    ending=tl>=HOLD
    y=year_at(t); yi=int(y+1e-9)
    xs=np.linspace(1990,y,max(2,int((y-1990)*8)+2))
    ends=[]
    for i,(n,v,c) in enumerate(S):
        yy=np.interp(xs,Y,v)
        glow[i].set_data(xs,yy); line[i].set_data(xs,yy)
        cur=val(v,y); ends.append(cur)
        dot[i].set_offsets([[y,cur]])
        k=(t*1.6)%1.0
        ring[i].set_offsets([[y,cur]]); ring[i].set_sizes([170+900*k]); ring[i].set_alpha(0.7*(1-k))
    order=np.argsort(ends)[::-1]; pos={}; last=None
    for idx in order:
        yv=ends[idx]
        if last is not None and last-yv<0.50: yv=last-0.50
        pos[idx]=yv; last=yv
    for i,(n,v,c) in enumerate(S):
        px=ax.transData.transform((min(y,2025)+0.55,pos[i]))
        lab[i].set_position(((px[0]+24)/W,px[1]/H)); lab[i].set_text(f"{n} ${ends[i]:.1f}T")
    yr.set_text(str(min(2025,int(round(y)))) if y<2025 else "2025")
    sub.set_text(subtitle(y,y>=2025 and tl>=0.2))
    ba=0
    if y>=2023.0 and not ending: ba=min(1,(y-2023.0)/0.25) if y<2025 else 1
    banner.set_text("Germany passes Japan: 2023" if y>=2023 else ""); banner.set_alpha(ba if not ending else 0)
    if ending:
        e=min(1,(tl-HOLD)/0.5)
        banner.set_text("")
        if e>=1: ax.set_visible(False)
        for tt in [sub,yr,unit]: tt.set_alpha(max(0,1-e)*(0.95 if tt is yr else 1))
        for i in range(4): lab[i].set_alpha(max(0,1-e)); glow[i].set_alpha(0.14*(1-e)); line[i].set_alpha(1-e); dot[i].set_alpha(1-e); ring[i].set_alpha(0)
        cta.set_text("Germany is No. 3.\n\nOne chart a day.\nFollow @chart2day"); cta.set_alpha(e)
    fig.canvas.draw()
    ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
ff.stdin.close(); ff.wait()
print("frames",NF,"sec",round(NF/FPS,1))
