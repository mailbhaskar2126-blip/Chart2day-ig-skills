import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
COB="#1F4FD8"; INK="#0B1220"; GREY="#6B7280"; LIGHT="#E5E7EB"
rows=list(csv.DictReader(open("/tmp/owid.csv",encoding="utf-8")))
Y=list(range(2000,2025))
def g(col): 
    d={int(r["year"]):float(r[col]) for r in rows if r["country"]=="World" and r[col]}
    return [d[y] for y in Y]
coal=g("coal_share_elec"); oilgas=[a+b for a,b in zip(g("oil_share_elec"),g("gas_share_elec"))]
nuc=g("nuclear_share_elec"); hyd=g("hydro_share_elec"); ws=[a+b for a,b in zip(g("solar_share_elec"),g("wind_share_elec"))]
oth=[a+b for a,b in zip(g("biofuel_share_elec"),g("other_renewables_share_elec"))]

print("ws",round(ws[0],2),round(ws[-1],2),"coal",round(coal[0]),round(coal[-1]),"og",round(oilgas[0]),round(oilgas[-1]),"nuc",round(nuc[0]),round(nuc[-1]),"hyd",round(hyd[0]),round(hyd[-1]),"oth",round(oth[0],1),round(oth[-1],1))
S=[("Coal",coal,"#4B5563"),("Oil & gas",oilgas,"#9CA3AF"),("Nuclear",nuc,"#D1D5DB"),("Hydro",hyd,"#93C5FD"),("Wind & solar",ws,COB),("Other",oth,"#DBEAFE")]
S=[("Coal",coal,"#4B5563",0),("Oil & gas",oilgas,"#9CA3AF",0),("Hydro",hyd,"#60A5FA",-1.6),("Nuclear",nuc,"#9CA3AF",0),("Wind & solar",ws,COB,1.6)]
first=lambda a,b:[y for y,x,z in zip(Y,a,b) if x>z][0]
y_n=first(ws,nuc); y_h=first(ws,hyd); print("ws passes nuclear",y_n,"hydro",y_h)
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor="white")
fig.text(0.09,0.935,"Wind and solar: from 0.2%\nto 15% of world electricity",fontsize=44,fontweight="bold",color=INK,va="top",linespacing=1.05)
fig.text(0.09,0.815,"Share of the world's electricity by source, 2000 to 2024. Fossil fuels\nfell from 65% to 59%, while wind and solar added almost 15 points.",fontsize=19,color=GREY,va="top",linespacing=1.35)
fig.text(0.09,0.088,"Source: Ember and Energy Institute via Our World in Data (share of electricity generation, world).",fontsize=12.5,color=GREY,va="top")
fig.text(0.09,0.022,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
ax=fig.add_axes([0.09,0.15,0.68,0.58])
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=15,length=0); ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)
for n,v,c,dy in S:
    ax.plot(Y,v,color=c,lw=4.4 if n=="Wind & solar" else 3.0,ls="--" if n=="Oil & gas" else "-")
    ax.text(2024.6,v[-1]+dy,f"{n}\n{v[-1]:.1f}%" if n=="Wind & solar" else f"{n}\n{v[-1]:.0f}%",fontsize=15,fontweight="bold",color=c if n in("Wind & solar","Hydro") else INK,va="center",clip_on=False)
ax.set_xlim(2000,2024); ax.set_ylim(0,42); ax.set_yticks([0,10,20,30,40]); ax.yaxis.set_major_formatter(lambda v,_:f"{v:.0f}%"); ax.set_xticks([2000,2006,2012,2018,2024])
ax.scatter([2000,2024],[ws[0],ws[-1]],color=COB,s=80,zorder=6)
ax.annotate("2000: 0.2%",(2000,ws[0]),(2004.5,6),fontsize=15,fontweight="bold",color=COB,ha="center",va="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=1))
fig.savefig("2026-11-10-world-electricity-mix.png",facecolor="white"); plt.close(fig)
