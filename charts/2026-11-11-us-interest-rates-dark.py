import csv, datetime as dt, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
BG="#0B1220"; COB="#5B88FF"; RED="#FF5C61"; INK="#F8FAFC"; GREY="#9AA4B2"; LIGHT="#243044"
r=[(dt.date.fromisoformat(a),float(b)) for a,b in list(csv.reader(open("2026-11-11-fed-funds-rate-fred.csv")))[1:] if b not in("",".") and a>="1990"]
X=[a for a,b in r]; Y=[b for a,b in r]
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor=BG)
fig.text(0.09,0.935,"US interest rates:\n36 years of cuts and hikes",fontsize=44,fontweight="bold",color=INK,va="top",linespacing=1.05)
fig.text(0.09,0.815,f"The Fed funds rate, monthly, 1990 to October 2026. From 8.3% in 1990\nto near zero twice, then back above 5% by 2023. Now {Y[-1]:.2f}%.",fontsize=19,color=GREY,va="top",linespacing=1.35)
fig.text(0.09,0.088,"Source: Federal Reserve via FRED (effective federal funds rate, monthly average, FEDFUNDS).",fontsize=12.5,color=GREY,va="top")
fig.text(0.09,0.022,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
ax=fig.add_axes([0.09,0.15,0.82,0.58],facecolor=BG)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=15,length=0); ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)
for a,b,lab in ((dt.date(2008,12,1),dt.date(2015,12,1),"Near zero\n2008–2015"),(dt.date(2020,4,1),dt.date(2022,2,1),"Near zero\n2020–22")):
    ax.axvspan(a,b,color=COB,alpha=0.10,lw=0); ax.text(a+(b-a)/2,(1.55 if a.year==2008 else 3.3),lab,fontsize=13.5,color=GREY,ha="center",va="center",linespacing=1.3)
ax.fill_between(X,Y,0,color=COB,alpha=0.12); ax.plot(X,Y,color=COB,lw=3)
ax.set_ylim(0,9.6); ax.set_xlim(dt.date(1990,1,1),dt.date(2027,6,1)); ax.yaxis.set_major_formatter(lambda v,_:f"{v:.0f}%"); ax.xaxis.set_major_locator(md.YearLocator(6)); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
def note(d,v,t,xy,ha="center"):
    ax.scatter([d],[v],color=INK,s=55,zorder=6); ax.annotate(t,(d,v),xy,fontsize=14.5,fontweight="bold",color=INK,ha=ha,va="center",linespacing=1.3,arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
note(dt.date(1990,6,1),8.29,"8.3%\nJun 1990",(dt.date(1994,6,1),8.9))
note(dt.date(2000,7,1),6.54,"6.5%\ndot-com peak",(dt.date(2000,7,1),7.6))
note(dt.date(2007,2,1),5.26,"5.3%\nbefore the\n2008 crisis",(dt.date(2007,2,1),6.7))
note(dt.date(2023,8,1),5.33,"5.3%\nAug 2023",(dt.date(2019,6,1),6.4))
ax.scatter([X[-1]],[Y[-1]],color=RED,s=90,zorder=7); ax.annotate(f"Now\n{Y[-1]:.2f}%",(X[-1],Y[-1]),(dt.date(2025,3,1),2.4),fontsize=16,fontweight="bold",color=RED,ha="center",va="center",arrowprops=dict(arrowstyle="-",color=RED,lw=1))
fig.savefig("2026-11-11-us-interest-rates-dark.png",facecolor=BG); plt.close(fig)
