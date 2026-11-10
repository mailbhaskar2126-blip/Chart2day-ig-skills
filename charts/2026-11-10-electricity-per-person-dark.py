import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False; plt.rcParams["axes.facecolor"]="#0B1220"
COB="#5B88FF"; RED="#FF5C61"; INK="#F8FAFC"; GREY="#9AA4B2"; LIGHT="#243044"; GOLD="#D9961A"
rows=list(csv.DictReader(open("/tmp/owid.csv",encoding="utf-8")))
Y=list(range(2000,2025))
def s(c): 
    d={int(r["year"]):float(r["per_capita_electricity"]) for r in rows if r["country"]==c and r["per_capita_electricity"]}
    return [d[y] for y in Y]
ind,chn,us,wld=s("India"),s("China"),s("United States"),s("World")
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor="#0B1220")
fig.text(0.09,0.935,"China makes 5x India's\nelectricity per person",fontsize=44,fontweight="bold",color=INK,va="top",linespacing=1.05)
fig.text(0.09,0.775,"Electricity generated per person per year (kWh), 2000 to 2024.\nChina passed the world average in 2010. The US peaked\nin 2007 and has slipped since.",fontsize=19,color=GREY,va="top",linespacing=1.35)
fig.text(0.09,0.088,"Source: Ember and Energy Institute via Our World in Data (electricity generation per capita, kWh).",fontsize=12.5,color=GREY,va="top")
fig.text(0.09,0.022,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
ax=fig.add_axes([0.09,0.15,0.70,0.55])
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=15,length=0)
ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)
for d,c,w in ((us,INK,3.4),(chn,RED,3.4),(wld,GREY,2.4),(ind,COB,3.4)): ax.plot(Y,d,color=c,lw=w)
ax.set_xlim(2000,2024.3); ax.set_ylim(0,15500); ax.set_yticks([0,5000,10000,15000]); ax.yaxis.set_major_formatter(lambda v,_:f"{v:,.0f}"); ax.set_xticks([2000,2006,2012,2018,2024])
def end(v,t,c,dy=0): ax.text(2024.9,v+dy,t,color=c,fontsize=16,fontweight="bold",va="center",clip_on=False)
end(us[-1],f"US\n{us[-1]:,.0f}",INK,300); end(chn[-1],f"China\n{chn[-1]:,.0f}",RED); end(wld[-1],f"World\n{wld[-1]:,.0f}",GREY,-150); end(ind[-1],f"India\n{ind[-1]:,.0f}",COB,-420)
ax.scatter([2000]*2,[ind[0],chn[0]],color=[COB,RED],s=70,zorder=5)
ax.annotate(f"2000: China {chn[0]:,.0f}\nIndia {ind[0]:,.0f}",(2000,chn[0]),(2004.2,4200),fontsize=15,fontweight="bold",color=INK,ha="center",va="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
fig.savefig("2026-11-10-electricity-per-person-dark.png",facecolor="#0B1220"); plt.close(fig)
print([ (y,round(a),round(b)) for y,a,b in zip(Y,chn,ind)][-3:], round(chn[-1]/ind[-1],2), [y for y,c,w in zip(Y,chn,wld) if c>w][:1], max(zip(us,Y)))
