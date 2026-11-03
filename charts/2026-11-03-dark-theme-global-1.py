import re
src=open("/tmp/dk_week.py").read()
head=src.split("Y=list(range(1960,2026))")[0]
exec(head)
import numpy as np
exec(re.search(r"Y=list.*?assert len\(ind\)==66 and len\(chn\)==66",src,re.S).group(0))
GOLD="#D9961A"; TEAL="#0E9488"
usg=[5.963,6.158,6.520,6.859,7.287,7.640,8.073,8.578,9.063,9.631,10.251,10.582,10.929,11.456,12.217,13.039,13.816,14.474,14.770,14.478,15.049,15.600,16.254,16.881,17.608,18.295,18.805,19.612,20.657,21.540,21.375,23.726,26.055,27.812,29.298,30.770]
chg=[0.362,0.385,0.429,0.447,0.567,0.738,0.869,0.968,1.037,1.104,1.224,1.355,1.490,1.684,1.984,2.318,2.791,3.604,4.667,5.190,6.193,7.672,8.674,9.743,10.675,11.281,11.456,12.538,14.148,14.560,14.996,18.202,18.317,18.270,18.730,19.498]
GY=list(range(1990,2026)); assert len(usg)==len(chg)==36
jp=[519,622,699,792,922,1015,1168,1354,1586,1841,2145,2370,3095,4147,4542,4876,5422,6609,9202,9497,9872,10806,9986,10876,11443,12058,17819,21587,26037,25798,26345,30048,32667,37111,40774,44947,39930,36331,32835,37029,39753,34910,33316,35809,38678,38159,36354,36130,40294,41678,45378,49122,49627,41369,39173,35665,40215,39680,40645,41425,41099,41581,35548,35215,33797,35951]
kr=[159,94,107,147,124,109,134,162,200,245,282,304,328,412,572,627,847,1073,1429,1814,1746,1918,2032,2246,2469,2543,2911,3658,4889,5989,6813,7873,8387,9180,10734,13002,13865,12822,8583,11063,12710,11981,13643,15212,17122,20167,22610,25078,22252,19937,24071,26175,26601,28449,30667,30172,30832,33297,35364,33827,33646,37518,34822,35674,36239,36227]
us=[3000,3059,3236,3366,3565,3818,4136,4326,4685,5020,5234,5609,6094,6726,7226,7801,8592,9453,10565,11674,12575,13976,14434,15544,17121,18237,19071,20039,21417,22857,23889,24342,25419,26387,27695,28691,29968,31459,32854,34515,36330,37134,37998,39490,41725,44123,46302,48050,48570,47195,48643,50025,51708,53297,55153,56849,57977,60048,62876,65228,64465,71441,78009,82587,86170,90027]
for a in (jp,kr,us): assert len(a)==66,len(a)

# 1 US vs China GDP
fig=frame("China's GDP: 6% of the\nUS in 1990, 77% by 2021","GDP in current US dollars. China's share of the US peaked in 2021\nand has slipped since.","Source: World Bank WDI via FRED (current US$, not inflation-adjusted). Exchange-rate effects matter.")
ax=fig.add_axes([0.09,0.15,0.74,0.57]); style(ax)
ax.axvspan(2021,2025.4,color=RED,alpha=0.07)
ax.plot(GY,usg,color=INK,lw=3.4); ax.plot(GY,chg,color=COB,lw=3.4)
ax.set_xlim(1990,2025.4); ax.set_ylim(0,34); ax.set_yticks([10,20,30]); ax.yaxis.set_major_formatter(lambda x,_:f"${x:.0f}T"); ax.set_xticks([1990,2000,2010,2020])
ax.text(2026,30.77,"US\n$30.8T",color=INK,fontsize=17,fontweight="bold",va="center")
ax.text(2026,19.5,"China\n$19.5T",color=COB,fontsize=17,fontweight="bold",va="center")
ax.scatter([1990,2021,2025],[0.362,18.202,19.498],color=COB,s=70,zorder=5)
lab(ax,(1990,0.362),"1990: 6% of US",(1997,4.5),c=COB)
lab(ax,(2021,18.202),"2021: 77% of US\n(peak)",(2011.5,25.5),c=RED)
lab(ax,(2025,19.498),"2025: 63%",(2017.5,9.5),c=COB)
fig.savefig("2026-11-02-us-vs-china-gdp-dark.png",facecolor="#0B1220"); plt.close(fig)

# 2 catch-up
fig=frame("Japan was richer than\nAmerica in 1995","GDP per person as a % of the US level (current US$). Japan fell back,\nSouth Korea caught up, China and India are still climbing.","Source: World Bank WDI via FRED (GDP per capita, current US$). Moves partly reflect exchange rates.")
ax=fig.add_axes([0.09,0.15,0.74,0.57]); style(ax)
def pct(a): return [x/u*100 for x,u in zip(a,us)]
yrs=list(range(1960,2026))
S={"Japan":(pct(jp),INK),"South Korea":(pct(kr),TEAL),"China":(pct(chn),RED),"India":(pct(ind),GOLD)}
ax.axhline(100,color=GREY,lw=1.2,ls=(0,(4,4)))
for k,(v,c) in S.items(): ax.plot(yrs,v,color=c,lw=3.2)
ax.text(1961,103,"US = 100%",color=GREY,fontsize=13.5)
ax.set_xlim(1960,2025.4); ax.set_ylim(0,170); ax.set_yticks([50,100,150]); ax.yaxis.set_major_formatter(lambda x,_:f"{x:.0f}%"); ax.set_xticks([1960,1980,2000,2020])
jv=S["Japan"][0]
for k,(v,c),dy in (("Japan",S["Japan"],-7),("South Korea",S["South Korea"],6),("China",S["China"],0),("India",S["India"],0)):
    ax.text(2026,v[-1]+dy,f"{k}\n{v[-1]:.0f}%",color=c,fontsize=15.5,fontweight="bold",va="center")
ax.scatter([1995],[jv[35]],color=INK,s=80,zorder=5)
lab(ax,(1995,jv[35]),f"1995: Japan at {jv[35]:.0f}%\nof US income",(1976,150),c=INK)
fig.savefig("2026-11-02-catch-up-vs-us-dark.png",facecolor="#0B1220"); plt.close(fig)

# 3 inflation small multiples
tur=[5.66,3.17,3.89,6.36,1.12,4.56,8.47,13.97,6.05,4.92,7.92,19.01,15.42,13.94,23.90,21.23,17.46,25.99,61.90,63.54,94.26,37.61,29.14,31.39,48.39,44.96,34.61,38.86,68.81,63.27,60.30,65.98,70.08,66.09,105.22,89.11,80.41,85.67,84.64,64.87,54.92,54.40,44.96,21.60,8.60,8.18,9.60,8.76,10.44,6.25,8.57,6.47,8.89,7.49,8.85,7.67,7.78,11.14,16.33,15.18,12.28,19.60,72.31,53.86,58.51,34.88]
uk=[1.00,3.45,4.20,2.02,3.28,4.77,3.91,2.48,4.70,5.45,6.37,9.44,7.07,9.20,16.04,24.21,16.56,15.84,8.26,13.42,17.97,11.88,8.60,4.61,4.96,6.07,3.43,4.15,4.16,5.76,8.06,7.46,4.59,2.56,2.22,2.70,2.85,2.20,1.82,1.75,1.18,1.53,1.52,1.38,1.39,2.09,2.46,2.39,3.52,1.96,2.49,3.86,2.57,2.29,1.45,0.37,1.01,2.56,2.29,1.74,0.99,2.52,7.92,6.79,3.27,3.88]
usi=[1.46,1.07,1.20,1.24,1.28,1.59,3.02,2.77,4.27,5.46,5.84,4.29,3.27,6.18,11.05,9.14,5.74,6.50,7.63,11.25,13.55,10.33,6.13,3.21,4.30,3.55,1.90,3.66,4.08,4.83,5.40,4.23,3.03,2.95,2.61,2.81,2.93,2.34,1.55,2.19,3.38,2.83,1.59,2.27,2.68,3.39,3.23,2.85,3.84,-0.36,1.64,3.16,2.07,1.46,1.62,0.12,1.26,2.13,2.44,1.81,1.23,4.70,8.00,4.12,2.95]
jpi=[3.57,5.37,6.84,6.71,3.80,6.66,5.04,3.99,5.34,5.25,6.92,6.40,4.84,11.61,23.22,11.73,9.37,8.16,4.21,3.70,7.78,4.91,2.74,1.90,2.26,2.03,0.60,0.13,0.68,2.27,3.08,3.25,1.76,1.24,0.70,-0.13,0.14,1.75,0.66,-0.34,-0.68,-0.74,-0.92,-0.26,-0.01,-0.28,0.25,0.06,1.38,-1.35,-0.73,-0.27,-0.04,0.34,2.76,0.80,-0.13,0.48,0.99,0.47,-0.02,-0.23,2.50,3.27,2.74,3.17]
for a,n in ((tur,66),(uk,66),(usi,65),(jpi,66)): assert len(a)==n,(len(a),n)
fig=frame("Four countries,\nfour inflation stories","Annual consumer price inflation, 1960 to latest. Same scale would hide\nthree of them, so each panel has its own axis.","Source: World Bank WDI via FRED (CPI inflation, annual %). US series ends 2024; others 2025.")
panels=[("United States",usi,list(range(1960,2025)),COB,[(1980,"1980: 13.5%"),(2022,"2022: 8.0%")],(-1.5,18)),
        ("United Kingdom",uk,yrs,INK,[(1975,"1975: 24.2%"),(2022,"2022: 7.9%")],(-2,31)),
        ("Japan",jpi,yrs,TEAL,[(1974,"1974: 23.2%"),(2009,"2009: -1.4%")],(-5,32)),
        ("Turkey",tur,yrs,RED,[(1994,"1994: 105%"),(2022,"2022: 72%")],(-5,135))]
pos=[(0.09,0.46),(0.57,0.46),(0.09,0.19),(0.57,0.19)]
for (nm,d,x,c,ann,yl),(px,py) in zip(panels,pos):
    ax=fig.add_axes([px,py,0.35,0.17]); style(ax)
    ax.axhline(0,color=GREY,lw=1)
    ax.fill_between(x,d,0,color=c,alpha=0.12); ax.plot(x,d,color=c,lw=2.4)
    ax.set_ylim(*yl); ax.set_xlim(1960,2026); ax.set_xticks([1960,1990,2020]); ax.tick_params(labelsize=12)
    ax.yaxis.set_major_formatter(lambda v,_:f"{v:.0f}%")
    ax.set_title(nm,loc="left",fontsize=19,fontweight="bold",color=c,pad=26)
    for yr,t in ann:
        v=d[x.index(yr)]; ax.scatter([yr],[v],color=c,s=40,zorder=5)
        ax.annotate(t,(yr,v),(yr,v+(yl[1]-yl[0])*0.13) if v>0 else (yr-3,v+(yl[1]-yl[0])*0.30),fontsize=11.5,fontweight="bold",color=INK,ha="center",arrowprops=dict(arrowstyle="-",color=GREY,lw=0.8))
fig.savefig("2026-11-02-inflation-four-countries-dark.png",facecolor="#0B1220"); plt.close(fig)

# 4 Turkey
fig=frame("Turkey: 26 straight years\nof 25%+ inflation","Annual consumer price inflation, 1977-2002 never below\n25%. Calm in 2004-16, then 72% in 2022.","Source: World Bank WDI via FRED (CPI inflation, annual %), 1960 to 2025.")
ax=fig.add_axes([0.09,0.15,0.84,0.57]); style(ax)
ax.axvspan(2004,2016.5,color=COB,alpha=0.08)
ax.fill_between(yrs,tur,0,color=RED,alpha=0.12); ax.plot(yrs,tur,color=RED,lw=3.2)
ax.set_xlim(1960,2026); ax.set_ylim(0,125); ax.set_yticks([25,50,75,100]); ax.yaxis.set_major_formatter(lambda v,_:f"{v:.0f}%"); ax.set_xticks([1960,1970,1980,1990,2000,2010,2020])
ax.text(2010.3,112,"2004-16:\n6-10%",ha="center",color=COB,fontsize=15,fontweight="bold",va="center")
def pt(yr,t,xt,c=RED):
    v=tur[yr-1960]; ax.scatter([yr],[v],color=c,s=80,zorder=5); lab(ax,(yr,v),t,xt)
pt(1980,"1980: 94%",(1971,100))
pt(1994,"1994: 105%",(1984,118))
pt(2022,"2022: 72%",(2013.5,86))
pt(2025,"2025: 35%",(2013,45),COB)
fig.savefig("2026-11-02-turkey-inflation-dark.png",facecolor="#0B1220"); plt.close(fig)
