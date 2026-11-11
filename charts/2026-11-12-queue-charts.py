import json, csv, collections, datetime as dt, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
def wb(f):
    t=collections.defaultdict(dict)
    for x in json.load(open(f))[1]:
        if x["value"] is not None: t[x["country"]["value"]][int(x["date"])]=x["value"]
    return t
def frame(dark,title,sub,src):
    BG="#0B1220" if dark else "white"; INK="#F8FAFC" if dark else "#0B1220"; GREY="#9AA4B2" if dark else "#6B7280"; LIGHT="#243044" if dark else "#E5E7EB"; COB="#5B88FF" if dark else "#1F4FD8"
    fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor=BG)
    fig.text(0.09,0.935,title,fontsize=44,fontweight="bold",color=INK,va="top",linespacing=1.05)
    fig.text(0.09,0.815,sub,fontsize=19,color=GREY,va="top",linespacing=1.35)
    fig.text(0.09,0.088,src,fontsize=12.5,color=GREY,va="top"); fig.text(0.09,0.022,"CHART2DAY",fontsize=20,fontweight="bold",color=COB)
    ax=fig.add_axes([0.09,0.15,0.70,0.58],facecolor=BG)
    for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(LIGHT); ax.tick_params(colors=GREY,labelsize=15,length=0); ax.grid(axis="y",color=LIGHT,lw=1); ax.set_axisbelow(True)
    return fig,ax,dict(BG=BG,INK=INK,GREY=GREY,LIGHT=LIGHT,COB=COB)
# A: share of world GDP (light)
g=wb("2026-11-12-world-bank-gdp.json"); Y=list(range(1990,2026)); sh=lambda c:[100*g[c][y]/g["World"][y] for y in Y]
S=[("United States",sh("United States"),"#0B1220",0),("European Union",sh("European Union"),"#6B7280",0.9),("China",sh("China"),"#E5484D",-0.9),("Japan",sh("Japan"),"#9CA3AF",0.9),("India",sh("India"),"#1F4FD8",-0.9)]
print("A",[(n,round(v[0],1),round(v[-1],1)) for n,v,_,_ in S])
fig,ax,C=frame(False,"China: from 2% to 16%\nof the world economy","Share of world GDP (current US dollars), 1990 to 2025. The US held its\nquarter. Europe and Japan gave up the most ground.","Source: World Bank (GDP, current US$; shares calculated from country and world totals).")
for n,v,c,dy in S:
    ax.plot(Y,v,color=c,lw=4 if n=="China" else 3); ax.text(2025.6,v[-1]+dy,f"{'US' if n=='United States' else 'EU' if n=='European Union' else n}\n{v[-1]:.0f}%",fontsize=15,fontweight="bold",color=c,va="center",clip_on=False)
ax.set_xlim(1990,2025); ax.set_ylim(0,32); ax.yaxis.set_major_formatter(lambda v,_:f"{v:.0f}%"); ax.set_xticks([1990,1997,2004,2011,2018,2025])
fig.savefig("2026-11-12-share-of-world-gdp.png",facecolor=C["BG"]); plt.close(fig)
# B: life expectancy (dark)
l=wb("2026-11-13-world-bank-life-expectancy.json"); Y=list(range(1960,2025))
S=[("High income",[l["High income"][y] for y in Y],"#F8FAFC"),("World",[l["World"][y] for y in Y],"#9AA4B2"),("Low income",[l["Low income"][y] for y in Y],"#5B88FF")]
gap0=S[0][1][0]-S[2][1][0]; gap1=S[0][1][-1]-S[2][1][-1]; print("B",[(n,round(v[0],1),round(v[-1],1)) for n,v,_ in S],round(gap0,1),round(gap1,1))
fig,ax,C=frame(True,"The rich-poor life gap\nfell from 27 years to 15","Life expectancy at birth, 1960 to 2024. Low-income countries gained\n24 years. High-income countries gained 12.","Source: World Bank (life expectancy at birth, total, by income group).")
for n,v,c in S:
    ax.plot(Y,v,color=c,lw=3.4 if n!="World" else 2.4); ax.text(2025,v[-1],f"{n}\n{v[-1]:.0f} years",fontsize=15,fontweight="bold",color=c,va="center",clip_on=False)
ax.fill_between(Y,S[2][1],S[0][1],color="#5B88FF",alpha=0.07)
ax.annotate("",xy=(1962,S[0][1][2]),xytext=(1962,S[2][1][2]),arrowprops=dict(arrowstyle="<->",color="#9AA4B2",lw=1.5)); ax.text(1963.5,55,"27-year gap",fontsize=15,fontweight="bold",color="#F8FAFC",va="center")
ax.annotate("",xy=(2022,S[0][1][-3]),xytext=(2022,S[2][1][-3]),arrowprops=dict(arrowstyle="<->",color="#9AA4B2",lw=1.5)); ax.text(2020.5,58,"15-year\ngap",fontsize=15,fontweight="bold",color="#F8FAFC",va="center",ha="right")
ax.set_xlim(1960,2024); ax.set_ylim(35,85); ax.set_xticks([1960,1976,1992,2008,2024])
fig.savefig("2026-11-13-life-expectancy-gap-dark.png",facecolor=C["BG"]); plt.close(fig)
# C: India vs China population (light)
pp=wb("2026-11-14-world-bank-population.json"); Y=sorted(set(pp["India"])&set(pp["China"])); I=[pp["India"][y]/1e9 for y in Y]; Cn=[pp["China"][y]/1e9 for y in Y]
cross=[y for y,a,b in zip(Y,I,Cn) if a>b][0]; pkc=max(zip(Cn,Y)); print("C",Y[0],Y[-1],round(I[0],2),round(Cn[0],2),round(I[-1],3),round(Cn[-1],3),"cross",cross,"china peak",pkc)
fig,ax,C=frame(False,"India has passed China.\nThe gap is growing.",f"Population, {Y[0]} to {Y[-1]} (billions). World Bank figures put India ahead\nfrom {cross}; the UN dated it to 2023. China is now shrinking.","Source: World Bank (population, total).")
ax.plot(Y,Cn,color="#E5484D",lw=3.4); ax.plot(Y,I,color=C["COB"],lw=3.4)
ax.text(Y[-1]+.8,I[-1]+.03,f"India\n{I[-1]:.2f}bn",fontsize=15,fontweight="bold",color=C["COB"],va="center",clip_on=False); ax.text(Y[-1]+.8,Cn[-1]-.04,f"China\n{Cn[-1]:.2f}bn",fontsize=15,fontweight="bold",color="#E5484D",va="center",clip_on=False)
ci=Y.index(cross); ax.scatter([cross],[I[ci]],color=C["INK"],s=70,zorder=6); ax.annotate("India moves\nahead",(cross,I[ci]),(cross-14,1.52),fontsize=15,fontweight="bold",color=C["INK"],ha="center",va="center",arrowprops=dict(arrowstyle="-",color=C["GREY"],lw=1))
ax.text(Y[0]+1,I[0]-.06,f"{I[0]:.2f}bn",fontsize=14,fontweight="bold",color=C["COB"],va="top"); ax.text(Y[0]+1,Cn[0]+.11,f"{Cn[0]:.2f}bn",fontsize=14,fontweight="bold",color="#E5484D",va="bottom")
ax.set_xlim(Y[0],Y[-1]); ax.set_ylim(0.3,1.6); ax.yaxis.set_major_formatter(lambda v,_:f"{v:.1f}bn"); ax.set_xticks([1960,1973,1986,1999,2012,2025])
fig.savefig("2026-11-14-india-china-population.png",facecolor=C["BG"]); plt.close(fig)
