import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md
from datetime import date
from matplotlib import font_manager as fm
names={f.name for f in fm.fontManager.ttflist}
font=next((n for n in ["Inter","Helvetica Neue","Liberation Sans","DejaVu Sans"] if n in names),"sans-serif")
plt.rcParams["font.family"]=font
COB="#1F4FD8"; INK="#0B1220"; GREY="#6B7280"; LIGHT="#E5E7EB"
d=[(date(2019,1,1),6.50),(date(2019,2,7),6.25),(date(2019,4,4),6.00),(date(2019,6,6),5.75),(date(2019,8,7),5.40),(date(2019,10,4),5.15),(date(2020,3,27),4.40),(date(2020,5,22),4.00),(date(2022,5,4),4.40),(date(2022,6,8),4.90),(date(2022,8,5),5.40),(date(2022,9,30),5.90),(date(2022,12,7),6.25),(date(2023,2,8),6.50),(date(2025,2,7),6.25),(date(2025,4,9),6.00),(date(2025,6,6),5.50),(date(2025,12,5),5.25),(date(2026,10,7),5.50)]
end=date(2026,10,30)
xs=[];ys=[]
for i,(dt,r) in enumerate(d):
    nxt=d[i+1][0] if i+1<len(d) else end
    xs+= [dt,nxt]; ys+=[r,r]
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor="white")
ax=fig.add_axes([0.09,0.20,0.84,0.60])
ax.axvspan(date(2020,3,27),date(2022,5,4),color=COB,alpha=0.07,lw=0)
ax.plot(xs,ys,color=COB,lw=3.2,solid_joinstyle="miter")
ax.scatter([date(2020,5,22)],[4.0],color=COB,zorder=5,s=70)
ax.scatter([end],[5.5],color=COB,zorder=5,s=70)
ax.set_ylim(3.75,7.0); ax.set_yticks([4,4.5,5,5.5,6,6.5,7]); ax.set_xlim(date(2019,1,1),date(2027,2,1))
ax.yaxis.set_major_formatter(lambda v,_:f"{v:.1f}%")
ax.xaxis.set_major_locator(md.YearLocator()); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(LIGHT)
ax.tick_params(colors=GREY,labelsize=15,length=0)
ax.annotate("Record low\n4.00%\nMay 2020",(date(2020,5,22),4.0),(date(2020,7,1),4.55),fontsize=16,color=INK,fontweight="bold",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
ax.text(date(2020,9,1),6.55,"Pandemic easing\nMar 2020 – May 2022",fontsize=14,color=GREY)
ax.annotate("Hiked 25 bps\nOct 2026",(end,5.5),(date(2024,6,1),6.8),fontsize=16,color=INK,fontweight="bold",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
ax.text(date(2022,9,1),6.62,"",fontsize=1)
fig.text(0.09,0.915,"RBI repo rate",fontsize=52,fontweight="bold",color=INK)
fig.text(0.09,0.868,"First rate hike since Feb 2023: repo rate rises to 5.50%",fontsize=22,color=GREY)
fig.text(0.09,0.115,"Policy repo rate, % · Jan 2019 – Oct 2026",fontsize=15,color=GREY)
fig.text(0.09,0.085,"Source: Reserve Bank of India, rate-change history (stableinvestor.com); Oct 2026 decision per news reports",fontsize=13,color=GREY)
fig.text(0.09,0.05,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
fig.savefig("2026-10-30-repo-rate.png",facecolor="white")
print(font)
