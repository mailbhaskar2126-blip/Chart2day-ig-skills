import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
COB="#1F4FD8"; RED="#E5484D"; INK="#0B1220"; GREY="#6B7280"; LIGHT="#E5E7EB"
def frame(title,sub,src):
    fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor="white")
    fig.text(0.09,0.935,title,fontsize=44,fontweight="bold",color=INK,va="top",linespacing=1.05)
    fig.text(0.09,0.795,sub,fontsize=20,color=GREY,va="top",linespacing=1.35)
    fig.text(0.09,0.088,src,fontsize=12.5,color=GREY,va="top",linespacing=1.5)
    fig.text(0.09,0.022,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
    return fig
def style(ax,grid=True):
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=15,length=0)
    if grid: ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)
def lab(ax,xy,txt,xyt,ha="center",c=INK,fs=15.5,line=True):
    ax.annotate(txt,xy,xyt,fontsize=fs,fontweight="bold",color=c,ha=ha,va="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1) if line else None)
Y=list(range(1960,2026))
ind=[85,88,92,103,118,122,91,98,102,109,114,121,125,147,167,161,164,190,209,228,271,275,279,296,281,301,315,345,358,350,371,306,319,303,348,375,401,416,414,442,443,450,469,544,624,710,802,1022,993,1095,1348,1445,1429,1433,1554,1584,1708,1950,1966,2041,1907,2240,2280,2434,2592,2702]
chn=[90,76,71,74,86,99,105,97,92,100,113,119,132,157,160,179,166,186,157,184,195,197,204,226,251,295,282,252,284,311,319,334,368,379,476,613,713,787,835,881,969,1065,1164,1307,1531,1778,2129,2735,3523,3898,4629,5704,6405,7147,7781,8175,8255,8980,10086,10343,10627,12887,12971,12951,13293,13862]
assert len(ind)==66 and len(chn)==66
gdp=[321.0,270.1,288.2,279.3,327.3,360.3,392.9,415.9,421.4,458.8,468.4,485.4,514.9,607.7,709.2,820.4,940.3,1216.7,1198.9,1341.9,1675.6,1823.1,1827.6,1856.7,2039.1,2103.6,2294.8,2651.5,2702.9,2835.6,2674.9,3167.3,3249.9,3500.9,3760.8,3956.1]
GY=list(range(1990,2026)); assert len(gdp)==36
fx={2005:44.0002,2006:45.1861,2007:41.1774,2008:43.3859,2009:48.3324,2010:45.6507,2011:46.5782,2012:53.3743,2013:58.5149,2014:60.9953,2015:64.1073,2016:67.1572,2017:65.0659,2018:68.3734,2019:70.3777,2020:74.1429,2021:73.9351,2022:78.5792,2023:82.5708,2024:83.6566,2025:87.1468}

# A: GDP in trillions
fig=frame("From $1 trillion to\nnearly $4 trillion","India's GDP in current US dollars. It took 7 years to go from\n$1 trillion (2007) to $2 trillion (2014), and 7 more to $3 trillion (2021).","Source: World Bank WDI via FRED (current US$). The IMF's own estimates differ slightly.")
ax=fig.add_axes([0.09,0.15,0.84,0.57]); style(ax)
v=[g/1000 for g in gdp]
ax.fill_between(GY,v,0,color=COB,alpha=0.10); ax.plot(GY,v,color=COB,lw=3.4)
for t in (1,2,3,4): ax.axhline(t,color=LIGHT,lw=1,zorder=0)
ax.set_ylim(0,4.7); ax.set_xlim(1990,2026.3); ax.set_yticks([0,1,2,3,4]); ax.yaxis.set_major_formatter(lambda x,_:f"${x:.0f}T"); ax.set_xticks([1990,1995,2000,2005,2010,2015,2020,2025])
def pt(x,y,t,xt,c=COB): ax.scatter([x],[y],color=c,s=80,zorder=5); lab(ax,(x,y),t,xt)
pt(1990,0.321,"1990: $0.32T",(1994,0.95))
pt(2007,1.217,"2007: $1 trillion",(2001.2,1.95))
pt(2014,2.039,"2014: $2 trillion",(2008.2,2.95))
pt(2021,3.167,"2021: $3 trillion",(2015.2,3.8))
pt(2025,3.956,"2025: $3.96T",(2021.6,4.4),RED)
fig.savefig("2026-11-02-india-gdp-trillion.png",facecolor="white"); plt.close(fig)

# B: India vs China per capita (log)
fig=frame("India vs China:\nincome per person","GDP per capita in current US$, log scale. India was ahead in 1990.\nChina has led every year since 1991 and is now about 5x ahead.","Source: World Bank WDI via FRED (GDP per capita, current US$), 1960–2025.")
ax=fig.add_axes([0.09,0.15,0.72,0.57]); style(ax)
ax.set_yscale("log"); ax.plot(Y,chn,color=RED,lw=3.4); ax.plot(Y,ind,color=COB,lw=3.4)
ax.set_ylim(50,25000); ax.set_xlim(1960,2025.4); ax.set_yticks([100,1000,10000]); ax.yaxis.set_major_formatter(lambda x,_:f"${x:,.0f}"); ax.yaxis.set_minor_formatter(lambda x,_:""); ax.set_xticks([1960,1970,1980,1990,2000,2010,2020])
ax.text(2026.2,13862,"China  $13,862",color=RED,fontsize=16,fontweight="bold",va="center",clip_on=False)
ax.text(2026.2,2702,"India  $2,702",color=COB,fontsize=16,fontweight="bold",va="center",clip_on=False)
ax.scatter([1990,1990],[371,319],color=[COB,RED],s=70,zorder=5)
lab(ax,(1990,371),"1990: India $371,\nChina $319",(1984,1500),"center")
ax.scatter([1991],[334],color=INK,s=45,zorder=6)
ax.annotate("",(2025,13862),(2025,2702),arrowprops=dict(arrowstyle="<->",color=GREY,lw=1.2))
ax.text(2023.8,6100,"5.1x",ha="right",va="center",fontsize=17,fontweight="bold",color=INK)
fig.savefig("2026-11-02-india-vs-china-income.png",facecolor="white"); plt.close(fig)

# C: threshold dumbbell
fig=frame("Crossing $1,000 per person:\nChina 2001, India 2007","Year each country first passed a GDP per capita threshold (US$).\nFrom $1,000 to $2,000 took China 5 years and India 12.","Source: World Bank WDI via FRED (GDP per capita, current US$). First year above each threshold.")
ax=fig.add_axes([0.20,0.15,0.73,0.57]); style(ax,False)
rows=[("$1,000",2001,2007),("$2,000",2006,2019),("$3,000",2008,None),("$5,000",2011,None),("$10,000",2018,None)]
for i,(lbl,c,n) in enumerate(rows):
    y=len(rows)-1-i
    ax.axhline(y,color=LIGHT,lw=1,zorder=0)
    if n: ax.plot([c,n],[y,y],color=GREY,lw=2.5,zorder=1); ax.text((c+n)/2,y+0.27,f"India {n-c} years later",ha="center",fontsize=14,color=GREY)
    ax.scatter([c],[y],color=RED,s=260,zorder=3); ax.text(c,y-0.34,str(c),ha="center",va="top",fontsize=17,fontweight="bold",color=RED)
    if n: ax.scatter([n],[y],color=COB,s=260,zorder=3); ax.text(n,y-0.34,str(n),ha="center",va="top",fontsize=17,fontweight="bold",color=COB)
    else: ax.text(2025,y,"India: not yet",ha="right",va="center",fontsize=15,color=GREY,style="italic")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1],fontsize=19,fontweight="bold",color=INK)
ax.set_ylim(-0.9,4.6); ax.set_xlim(1998,2026); ax.set_xticks([2000,2005,2010,2015,2020,2025]); ax.tick_params(axis="y",length=0,pad=12)
ax.scatter([],[],color=RED,s=120,label="China"); ax.scatter([],[],color=COB,s=120,label="India")
ax.legend(loc="upper right",frameon=False,fontsize=16,labelcolor=INK,bbox_to_anchor=(1.0,1.04),ncol=2,handletextpad=0.2,columnspacing=1.2)
fig.savefig("2026-11-02-income-thresholds.png",facecolor="white"); plt.close(fig)

# D: rupee vs dollar GDP
yrs=list(range(2005,2026)); usd=[gdp[GY.index(y)] for y in yrs]
iu=[100*g/usd[0] for g in usd]; ir=[100*usd[i]*fx[y]/(usd[0]*fx[2005]) for i,y in enumerate(yrs)]
print("usd x",iu[-1]/100,"inr x",ir[-1]/100)
fig=frame(f"India's GDP: {ir[-1]/100:.1f}x in rupees,\nbut {iu[-1]/100:.1f}x in dollars","Indexed to 2005 = 100. The gap between the lines is the rupee's slide:\nit now takes about 2x as many rupees to buy a dollar.","Source: World Bank WDI via FRED (GDP, current US$); US Fed G.5A USD/INR (annual average).\nGDP in rupees is estimated as dollar GDP x average USD/INR. Indicative.")
ax=fig.add_axes([0.09,0.15,0.74,0.57]); style(ax)
ax.fill_between(yrs,iu,ir,color=COB,alpha=0.10)
ax.plot(yrs,ir,color=COB,lw=3.4); ax.plot(yrs,iu,color=INK,lw=3.4)
ax.set_xlim(2005,2025.2); ax.set_ylim(0,1050); ax.set_yticks([0,250,500,750,1000]); ax.yaxis.set_major_formatter(lambda x,_:f"{x:.0f}"); ax.set_xticks([2005,2010,2015,2020,2025])
ax.text(2025.5,ir[-1],f"Rupees  {ir[-1]/100:.1f}x",color=COB,fontsize=16,fontweight="bold",va="center",clip_on=False)
ax.text(2025.5,iu[-1],f"Dollars  {iu[-1]/100:.1f}x",color=INK,fontsize=16,fontweight="bold",va="center",clip_on=False)
ax.text(2022.7,575,"The rupee's\nslide",fontsize=17,fontweight="bold",color=INK,ha="center",va="center",linespacing=1.15)
fig.savefig("2026-11-02-gdp-rupee-vs-dollar.png",facecolor="white"); plt.close(fig)
