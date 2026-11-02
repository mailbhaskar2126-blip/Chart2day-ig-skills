import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.family"]="Inter"
COB="#1F4FD8"; RED="#E5484D"; INK="#0B1220"; GREY="#6B7280"; LIGHT="#E5E7EB"; GOLD="#D9961A"; TEAL="#0E9488"
fx={1990:17.4922,1991:22.7116,1992:28.1558,1993:31.2911,1994:31.3939,1995:32.4181,1996:35.5060,1997:36.3645,1998:41.3561,1999:43.1274,2000:44.9975,2001:47.2200,2002:48.6257,2003:46.5908,2004:45.2610,2005:44.0002,2006:45.1861,2007:41.1774,2008:43.3859,2009:48.3324,2010:45.6507,2011:46.5782,2012:53.3743,2013:58.5149,2014:60.9953,2015:64.1073,2016:67.1572,2017:65.0659,2018:68.3734,2019:70.3777,2020:74.1429,2021:73.9351,2022:78.5792,2023:82.5708,2024:83.6566,2025:87.1468}
cpi={1960:1.78,1961:1.70,1962:3.63,1963:2.95,1964:13.36,1965:9.47,1966:10.80,1967:13.06,1968:3.24,1969:-0.58,1970:5.09,1971:3.08,1972:6.44,1973:16.94,1974:28.60,1975:5.75,1976:-7.63,1977:8.31,1978:2.52,1979:6.28,1980:11.35,1981:13.11,1982:7.89,1983:11.87,1984:8.32,1985:5.56,1986:8.73,1987:8.80,1988:9.38,1989:7.07,1990:8.97,1991:13.87,1992:11.79,1993:6.33,1994:10.25,1995:10.22,1996:8.98,1997:7.16,1998:13.23,1999:4.67,2000:4.01,2001:3.78,2002:4.30,2003:3.81,2004:3.77,2005:4.25,2006:5.80,2007:6.37,2008:8.35,2009:10.88,2010:11.99,2011:8.91,2012:9.48,2013:10.02,2014:6.67,2015:4.91,2016:4.95,2017:3.33,2018:3.94,2019:3.73,2020:6.62,2021:5.13,2022:6.70,2023:5.65,2024:4.95,2025:2.40}
sensex={2005:9397.93,2025:85220.60}; gold={2005:7000,2025:133195}
def frame(title,sub,src,h=13.5):
    fig=plt.figure(figsize=(10.8,h),dpi=100,facecolor="white")
    fig.text(0.09,0.935,title,fontsize=46,fontweight="bold",color=INK,va="top",linespacing=1.05)
    fig.text(0.09,0.795,sub,fontsize=20,color=GREY,va="top",linespacing=1.35)
    fig.text(0.09,0.088,src,fontsize=12.5,color=GREY,va="top",linespacing=1.5)
    fig.text(0.09,0.022,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
    return fig
def style(ax):
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=15,length=0)
    ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)

# A: rupee
fig=frame("The rupee: ₹17.5\nto ₹87 a dollar","Annual average USD/INR, 1990–2025.\nIt now takes about 5x as many rupees to buy a dollar.","Source: US Federal Reserve G.5A (annual average of daily rates), via FRED; 2025 is the last full year.")
ax=fig.add_axes([0.09,0.15,0.84,0.57]); style(ax)
y=list(fx); v=[fx[k] for k in y]
ax.fill_between(y,v,0,color=COB,alpha=0.10); ax.plot(y,v,color=COB,lw=3.4)
ax.set_ylim(0,100); ax.set_xlim(1990,2027); ax.set_yticks([0,25,50,75,100]); ax.yaxis.set_major_formatter(lambda x,_:f"₹{x:.0f}")
ax.set_xticks([1990,1995,2000,2005,2010,2015,2020,2025])
def pt(x,yv,t,dx,dy,ha="left",c=COB):
    ax.scatter([x],[yv],color=c,s=70,zorder=5)
    ax.annotate(t,(x,yv),(x+dx,yv+dy),fontsize=15.5,fontweight="bold",color=INK,ha=ha,va="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
pt(1990,17.49,"1990: ₹17.5",3,-9)
pt(1991,22.71,"1991 crisis: +30% in a year",5,42,"left",RED)
pt(2007,41.18,"2007: ₹41.2, strongest\nthis century",-1,-20,"center")
pt(2013,58.51,"2013: ₹58.5 taper tantrum",-2.5,22,"right",RED)
pt(2025,87.15,"2025: ₹87.1",-2,9,"right")
fig.savefig("2026-11-02-rupee.png",facecolor="white"); plt.close(fig)

# B: inflation bars
fig=frame("India's inflation:\nlowest since 1976","Consumer price inflation, annual %, 1960–2025.\nRed bars mark years of 10% or more.","Source: World Bank WDI (FP.CPI.TOTL.ZG) via FRED.\nDiffers slightly from MoSPI's official CPI.")
ax=fig.add_axes([0.09,0.15,0.84,0.57]); style(ax)
y=list(cpi); v=[cpi[k] for k in y]
cols=[RED if x>=10 else COB for x in v]; cols[-1]="#0B1220"
ax.bar(y,v,color=cols,width=0.78); ax.axhline(0,color=INK,lw=1.2)
ax.set_ylim(-11,33); ax.set_yticks([0,10,20,30]); ax.yaxis.set_major_formatter(lambda x,_:f"{x:.0f}%"); ax.set_xticks([1960,1970,1980,1990,2000,2010,2020])
ax.text(1974,29.8,"1974: 28.6%",ha="center",fontsize=16,fontweight="bold",color=INK)
ax.text(1976,-8.6,"1976: −7.6%",ha="left",fontsize=15,fontweight="bold",color=INK)
ax.text(2010,13.4,"2010: 12.0%",ha="center",fontsize=15,fontweight="bold",color=INK)
ax.plot([2025,2025],[3.4,14.3],color=GREY,lw=1); ax.text(2025.6,15.2,"2025: 2.4%",fontsize=17,fontweight="bold",color=INK,ha="right",va="center")
ax.fill([2015.5,2025.6,2025.6,2015.5],[2,2,6,6],color=COB,alpha=0.10,lw=0); ax.text(2018.2,7.7,"RBI target band\n2–6% (since 2016)",fontsize=12.5,color=GREY,ha="center",va="bottom")
fig.savefig("2026-11-02-inflation.png",facecolor="white"); plt.close(fig)

# C: purchasing power
pp={2000:100.0}
for k in range(2001,2026): pp[k]=pp[k-1]/(1+cpi[k]/100)
end=pp[2025]; print("pp2025",round(end,1))
fig=frame(f"₹100 in 2000 now\nbuys about ₹{end:.0f}","Purchasing power of ₹100 in 2000,\nusing annual CPI inflation (World Bank).","Source: World Bank WDI CPI inflation via FRED; compounded annual rates 2001–2025.\nAuthor's calculation. Indicative.")
ax=fig.add_axes([0.09,0.15,0.84,0.57]); style(ax)
y=list(pp); v=[pp[k] for k in y]
ax.fill_between(y,v,0,color=COB,alpha=0.10); ax.step(y,v,where="post",color=COB,lw=3.4)
ax.set_ylim(0,110); ax.set_xlim(2000,2026.4); ax.set_yticks([0,25,50,75,100]); ax.yaxis.set_major_formatter(lambda x,_:f"₹{x:.0f}"); ax.set_xticks([2000,2005,2010,2015,2020,2025])
ax.scatter([2025],[end],color=RED,s=90,zorder=5)
ax.annotate(f"2025: ₹{end:.1f}",(2025,end),(2021.2,end+22),fontsize=19,fontweight="bold",color=INK,ha="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
p10=pp[2010]; ax.annotate(f"2010: ₹{p10:.0f}\n(after the 2009–10\ndouble-digit years)",(2010,p10),(2006.2,p10-34),fontsize=15,fontweight="bold",color=INK,ha="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
ax.annotate("Prices have\nmore than tripled",(2013,70),(2013,98),fontsize=16,color=GREY,ha="center") if False else None
fig.savefig("2026-11-02-purchasing-power.png",facecolor="white"); plt.close(fig)

# D: indexed 2005=100 (log)
lvl={2005:100.0}
for k in range(2006,2026): lvl[k]=lvl[k-1]*(1+cpi[k]/100)
yrs=list(range(2005,2026))
# sensex & nifty-free series: use sensex year-end from earlier table, gold avg, fx avg
sx=[9397.93,13786.91,20286.99,9647.31,17464.81,20509.09,15454.92,19426.71,21170.68,27499.42,26117.54,26626.46,34056.83,36068.33,41253.74,47751.33,58253.82,60840.74,72240.26,78139.01,85220.60]
gl=[7000,8400,9428,12361,15417,18448,24130,29926,28848,27708,26671,30128,29174,30692,35154,47562,47437,51249,58836,77000,133195]
S={"Gold":[100*g/gl[0] for g in gl],"Sensex":[100*s/sx[0] for s in sx],"Prices":[lvl[k] for k in yrs],"USD/INR":[100*fx[k]/fx[2005] for k in yrs]}
cols={"Gold":GOLD,"Sensex":COB,"Prices":INK,"USD/INR":RED}
e={k:v[-1] for k,v in S.items()}; print({k:round(x) for k,x in e.items()})
fig=frame("What beat inflation\nsince 2005?",f"Indexed to 2005 = 100, log scale. Gold {e['Gold']/100:.1f}x, Sensex {e['Sensex']/100:.1f}x,\nprices {e['Prices']/100:.1f}x, the dollar in rupees {e['USD/INR']/100:.1f}x.","Sources: BSE (Sensex year-end); gold yearly avg 24K, India; World Bank CPI; US Fed USD/INR.\nMixed year-end and average data. Indicative, pre-tax. Not investment advice.")
ax=fig.add_axes([0.09,0.15,0.74,0.57]); style(ax)
ax.set_yscale("log")
for k,v in S.items(): ax.plot(yrs,v,color=cols[k],lw=3.4 if k!="Prices" else 3.0,ls="-" if k!="Prices" else (0,(5,3)))
ax.set_ylim(80,2600); ax.set_yticks([100,200,500,1000,2000]); ax.yaxis.set_major_formatter(lambda x,_:f"{x:.0f}"); ax.yaxis.set_minor_formatter(lambda x,_:""); ax.set_xlim(2005,2025.3); ax.set_xticks([2005,2010,2015,2020,2025])
ys={"Gold":e["Gold"]*1.0,"Sensex":e["Sensex"]*1.0,"Prices":e["Prices"]*1.0,"USD/INR":e["USD/INR"]*0.93}
for k in S: ax.text(2025.5,ys[k],f"{k}  {e[k]/100:.1f}x",color=cols[k] if k!="Prices" else INK,fontsize=16,fontweight="bold",va="center",clip_on=False)
ax.annotate("Gold surged\nin 2025",(2025,e["Gold"]),(2019.2,1500),fontsize=14.5,color=GREY,ha="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
fig.savefig("2026-11-02-beat-inflation.png",facecolor="white"); plt.close(fig)
