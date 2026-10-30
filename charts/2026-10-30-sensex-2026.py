import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="Inter"
COB="#1F4FD8"; RED="#E5484D"; INK="#0B1220"; GREY="#6B7280"; LIGHT="#E5E7EB"
yrs=list(range(2005,2027))
close=[9397.93,13786.91,20286.99,9647.31,17464.81,20509.09,15454.92,19426.71,21170.68,27499.42,26117.54,26626.46,34056.83,36068.33,41253.74,47751.33,58253.82,60840.74,72240.26,78139.01,85220.60,73123.83]
ret=[42.3,46.7,47.1,-52.4,81.0,17.4,-24.6,25.7,9.0,29.9,-5.0,1.9,27.9,5.9,14.4,15.8,22.0,4.4,18.7,8.2,9.1,-14.2]
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor="white")
a=fig.add_axes([0.09,0.41,0.84,0.31]); b=fig.add_axes([0.09,0.17,0.84,0.16],sharex=a)
cols=[RED if r<0 else COB for r in ret]
bars=a.bar(yrs,ret,color=cols,width=0.72)
bars[-1].set_hatch("////"); bars[-1].set_edgecolor("white")
a.axhline(0,color=INK,lw=1.2)
a.set_ylim(-62,100); a.set_yticks([-50,-25,0,25,50,75])
a.yaxis.set_major_formatter(lambda v,_:f"{v:+.0f}%" if v else "0%")
a.grid(axis="y",color=LIGHT,lw=1); a.set_axisbelow(True)
for ax in (a,b):
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    
    ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=14,length=0)
a.tick_params(labelbottom=False); a.spines["bottom"].set_visible(False)
def lab(x,y,t,dy,ha="center"): a.text(x,y+dy,t,ha=ha,va="bottom" if dy>0 else "top",fontsize=15,fontweight="bold",color=INK)
lab(2008,-52.4,"−52.4%",-3); lab(2009,81.0,"+81.0%",3); lab(2011,-24.6,"−24.6%",-3); lab(2015,-5.0,"−5.0%",-3)
lab(2026,-14.2,"−14.2%\nYTD",-3)
a.set_title("Calendar-year return, BSE Sensex",loc="left",fontsize=15,color=GREY,pad=14)
a.text(2020.5,67,"10 straight up years, 2016–2025",fontsize=14,color=GREY,ha="center")
a.annotate("",(2025.4,62),(2015.6,62),arrowprops=dict(arrowstyle="<->",color=GREY,lw=1.2))
b.fill_between(yrs,close,color=COB,alpha=0.12); b.plot(yrs,close,color=COB,lw=3)
b.scatter([2025,2026],[85220.60,73123.83],color=[COB,RED],zorder=5,s=70)
b.set_ylim(0,100000); b.set_yticks([0,50000,100000]); b.yaxis.set_major_formatter(lambda v,_:f"{int(v/1000)}k")
b.grid(axis="y",color=LIGHT,lw=1); b.set_axisbelow(True)
b.text(2024.4,89500,"85,221",fontsize=14,fontweight="bold",color=INK,ha="right")
b.text(2026.2,64500,"73,124",fontsize=14,fontweight="bold",color=RED,ha="right",va="top")
b.set_xticks([2005,2008,2011,2014,2017,2020,2023,2026]); b.set_xticklabels(["2005","2008","2011","2014","2017","2020","2023","2026"])
b.set_title("Year-end level",loc="left",fontsize=15,color=GREY,pad=10)
fig.text(0.09,0.93,"Sensex: worst year\nsince 2011",fontsize=50,fontweight="bold",color=INK,va="top",linespacing=1.05)
fig.text(0.09,0.775,"Down 14.2% in 2026 so far, after 10 straight up years",fontsize=22,color=GREY)
fig.text(0.09,0.085,"2026 is year to date as of 23 Oct 2026 (hatched). Sensex year-end closes.",fontsize=13,color=GREY)
fig.text(0.09,0.06,"Source: BSE Sensex annual data compiled by simianx.ai; Oct 2026 levels cross-checked with market reports",fontsize=12,color=GREY)
fig.text(0.09,0.025,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
fig.savefig("2026-10-30-sensex-2026.png",facecolor="white")
