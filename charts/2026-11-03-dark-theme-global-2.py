import re
src=open("/tmp/dk_g1.py").read()
exec(src.split("# 1 US vs China GDP")[0])
ff=[3.22,1.96,2.71,3.18,3.50,4.08,5.11,4.22,5.66,8.20,7.18,4.66,4.43,8.73,10.50,5.82,5.05,5.54,7.93,11.19,13.36,16.38,12.26,9.09,10.23,8.10,6.81,6.66,7.57,9.22,8.10,5.69,3.52,3.02,4.20,5.84,5.30,5.46,5.35,4.97,6.36,3.89,1.67,1.13,1.35,3.21,4.96,5.02,1.93,0.16,0.18,0.10,0.14,0.11,0.09,0.13,0.40,1.00,1.83,2.16,0.38,0.08,1.68,5.02,5.14,4.21]
assert len(ff)==66
usi=[1.46,1.07,1.20,1.24,1.28,1.59,3.02,2.77,4.27,5.46,5.84,4.29,3.27,6.18,11.05,9.14,5.74,6.50,7.63,11.25,13.55,10.33,6.13,3.21,4.30,3.55,1.90,3.66,4.08,4.83,5.40,4.23,3.03,2.95,2.61,2.81,2.93,2.34,1.55,2.19,3.38,2.83,1.59,2.27,2.68,3.39,3.23,2.85,3.84,-0.36,1.64,3.16,2.07,1.46,1.62,0.12,1.26,2.13,2.44,1.81,1.23,4.70,8.00,4.12,2.95]
x1=list(range(1960,2026))
fig=frame("In 2022 the Fed's rate sat\n6 points below inflation","Average US federal funds rate vs consumer price inflation. Shaded:\nyears the rate was below inflation.","Source: Federal Reserve (annual average of monthly effective rate) and World Bank via FRED. CPI ends 2024.")
ax=fig.add_axes([0.09,0.15,0.74,0.57]); style(ax)
xs=x1[:65]; f65=ff[:65]
ax.fill_between(xs,f65,usi,where=[a<b for a,b in zip(f65,usi)],color=RED,alpha=0.18,interpolate=True,lw=0)
ax.plot(x1,ff,color=COB,lw=3.4); ax.plot(xs,usi,color=INK,lw=2.4,ls=(0,(5,2)))
ax.set_xlim(1960,2025.4); ax.set_ylim(0,18); ax.set_yticks([5,10,15]); ax.yaxis.set_major_formatter(lambda v,_:f"{v:.0f}%"); ax.set_xticks([1960,1970,1980,1990,2000,2010,2020])
ax.text(2026,4.21,"Fed funds\n4.2%",color=COB,fontsize=15.5,fontweight="bold",va="center")
ax.text(2026,2.4,"Inflation\n2.9%",color=INK,fontsize=15.5,fontweight="bold",va="center")
ax.scatter([1981,2022],[16.38,1.68],color=COB,s=80,zorder=5); ax.scatter([2022],[8.0],color=INK,s=60,zorder=5)
lab(ax,(1981,16.38),"1981: 16.4%",(1991,16.8),c=COB)
lab(ax,(2022,8.0),"2022: inflation 8.0%\nrate 1.7%",(2008.5,11.5),c=RED)
ax.text(1975.5,13.8,"1974-77:\nrate below\ninflation",color=RED,fontsize=14,fontweight="bold",ha="center",va="center")
fig.savefig("2026-11-02-fed-rate-vs-inflation-dark.png",facecolor="#0B1220"); plt.close(fig)

# B
ger=[1.778,1.876,2.141,2.079,2.215,2.593,2.507,2.219,2.248,2.214,1.967,1.966,2.102,2.535,2.852,2.893,3.046,3.484,3.808,3.479,3.467,3.824,3.596,3.807,3.965,3.425,3.537,3.765,4.055,3.960,3.941,4.355,4.201,4.562,4.686,5.051]
jpg=[3.253,3.725,4.065,4.632,5.104,5.640,5.021,4.580,4.150,4.689,5.042,4.439,4.246,4.573,4.941,4.876,4.648,4.625,5.160,5.337,5.812,6.279,6.334,5.272,4.986,4.534,5.110,5.038,5.154,5.246,5.189,5.226,4.448,4.385,4.190,4.435]
ukg=[1.093,1.143,1.180,1.061,1.140,1.349,1.425,1.569,1.661,1.693,1.672,1.656,1.791,2.061,2.430,2.551,2.720,3.105,2.945,2.429,2.497,2.676,2.720,2.797,3.085,2.946,2.707,2.699,2.897,2.876,2.724,3.195,3.181,3.421,3.696,4.003]
ing=gdp=[g/1000 for g in [321.0,270.1,288.2,279.3,327.3,360.3,392.9,415.9,421.4,458.8,468.4,485.4,514.9,607.7,709.2,820.4,940.3,1216.7,1198.9,1341.9,1675.6,1823.1,1827.6,1856.7,2039.1,2103.6,2294.8,2651.5,2702.9,2835.6,2674.9,3167.3,3249.9,3500.9,3760.8,3956.1]]
for a in (ger,jpg,ukg,ing): assert len(a)==36
fig=frame("Germany overtook Japan\nas the No. 3 economy","GDP in current US dollars. Japan was 2.2x Germany in 1995 and is\n0.9x today. India is closing in on both Japan and the UK.","Source: World Bank WDI via FRED (current US$). The yen's fall since 2012 explains much of Japan's slide.")
ax=fig.add_axes([0.09,0.15,0.74,0.57]); style(ax)
S=[("Japan",jpg,INK),("Germany",ger,COB),("United Kingdom",ukg,TEAL),("India",ing,GOLD)]
for n,v,c in S: ax.plot(GY,v,color=c,lw=3.2)
ax.set_xlim(1990,2025.4); ax.set_ylim(0,6.8); ax.set_yticks([2,4,6]); ax.yaxis.set_major_formatter(lambda v,_:f"${v:.0f}T"); ax.set_xticks([1990,2000,2010,2020])
for n,v,c,dy in (("Japan",jpg,INK,0.25),("Germany",ger,COB,0.35),("UK",ukg,TEAL,0.05),("India",ing,GOLD,-0.55)):
    ax.text(2026,{"Japan":4.75,"Germany":5.45,"UK":4.05,"India":3.3}[n],f"{n}\n${v[-1]:.1f}T",color=c,fontsize=15.5,fontweight="bold",va="center")
ax.scatter([1995],[5.640],color=INK,s=80,zorder=5); lab(ax,(1995,5.64),"1995: Japan $5.6T,\nGermany $2.6T",(2003.5,6.35))
ax.scatter([2025],[5.051],color=COB,s=80,zorder=5)
fig.savefig("2026-11-02-germany-overtakes-japan-dark.png",facecolor="#0B1220"); plt.close(fig)

# C bubble
pts=[("US",90027,30.769/7.640,30.77,INK),("China",13862,19.498/0.738,19.50,RED),("Japan",35951,4.435/5.640,4.44,TEAL),("Germany",60496,5.051/2.593,5.05,COB),("UK",57602,4.003/1.349,4.00,GOLD),("India",2702,3.956/0.360,3.96,"#7C3AED")]
fig=frame("Since 1995, China's economy\ngrew 26x. Japan's shrank.","2025 GDP as a multiple of 1995, in current US$, vs GDP per person.\nBubble size = 2025 GDP.","Source: World Bank WDI via FRED (current US$, not inflation-adjusted). Exchange rates affect all figures.")
ax=fig.add_axes([0.11,0.15,0.82,0.57]); style(ax)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1800,170000); ax.set_ylim(0.5,45)
ax.axhline(1,color=GREY,lw=1.2,ls=(0,(4,4))); ax.text(1900,1.08,"1995 level",color=GREY,fontsize=13.5)
for n,xv,yv,s,c in pts:
    ax.scatter([xv],[yv],s=s*95,color=c,alpha=0.85,edgecolor="#0B1220",lw=2,zorder=4)
off={"US":(0,1.55),"China":(0,1.4),"Japan":(0,0.8),"Germany":(0.72,0.88),"UK":(0.76,1.12),"India":(0,1.4)}
for n,xv,yv,s,c in pts:
    ax.text(xv*off[n][0] if off[n][0] else xv,yv*off[n][1],f"{n}  {yv:.1f}x" if yv>=1 else f"{n}  {yv:.1f}x",color=c,fontsize=16,fontweight="bold",ha="center",va="center",zorder=6)
ax.set_xticks([3000,10000,30000,100000]); ax.set_xticklabels(["$3k","$10k","$30k","$100k"]); ax.set_yticks([1,2,5,10,20,40]); ax.set_yticklabels(["1x","2x","5x","10x","20x","40x"])
ax.minorticks_off(); ax.tick_params(labelsize=14)
ax.set_xlabel("GDP per person, 2025 (log scale)",color=GREY,fontsize=14,labelpad=10)
fig.savefig("2026-11-02-gdp-growth-bubble-dark.png",facecolor="#0B1220"); plt.close(fig)
