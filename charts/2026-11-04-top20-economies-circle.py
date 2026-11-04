import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from PIL import Image
plt.rcParams["font.family"]="Inter"; plt.rcParams["text.parse_math"]=False
THEME=sys.argv[1] if len(sys.argv)>1 else "light"
if THEME=="dark": BG="#0B1220"; INK="#F8FAFC"; GREY="#9AA4B2"; LINE="#243044"; COBT="#5B88FF"
else: BG="#FFFFFF"; INK="#0B1220"; GREY="#6B7280"; LINE="#E5E7EB"; COBT="#1F4FD8"
# (name, label, GDP $T 2025 (World Bank via FRED), region)
D=[("United States","US",30.770,"North America"),("China","China",19.498,"Asia"),("Germany","Germany",5.051,"Europe"),("Japan","Japan",4.435,"Asia"),("United Kingdom","UK",4.003,"Europe"),("India","India",3.956,"Asia"),("France","France",3.366,"Europe"),("Russia","Russia",2.561,"Europe"),("Italy","Italy",2.552,"Europe"),("Canada","Canada",2.320,"North America"),("Brazil","Brazil",2.280,"South America"),("Spain","Spain",1.906,"Europe"),("South Korea","S. Korea",1.872,"Asia"),("Mexico","Mexico",1.833,"North America"),("Australia","Australia",1.799,"Oceania"),("Turkey","Turkey",1.597,"Middle East"),("Indonesia","Indonesia",1.446,"Asia"),("Netherlands","Netherlands",1.333,"Europe"),("Saudi Arabia*","Saudi*",1.240,"Middle East"),("Switzerland","Switzerland",1.044,"Europe")]
TOT=sum(d[2] for d in D); print("total",round(TOT,3),"US+China share",round((30.770+19.498)/TOT*100,1))
REG=["North America","Asia","Europe","Middle East","South America","Oceania"]
RC={"North America":"#0E9488","Asia":"#2F5BEA","Europe":"#7C4DDB","Middle East":"#D9961A","South America":"#E5484D","Oceania":"#6B7FA3"}
rv={r:sum(d[2] for d in D if d[3]==r) for r in REG}
rng=np.random.default_rng(7)
def grid(n):
    c=(np.arange(n)+.5)/n*2-1; X,Y=np.meshgrid(c,c); return X,Y
def power(mask,vals,sites,X,Y,iters=260):
    P=np.stack([X[mask],Y[mask]],1); N=len(P); K=len(vals); t=np.array(vals)/sum(vals)*N
    s=sites.copy(); w=np.zeros(K)
    for it in range(iters):
        d=((P[:,None,:]-s[None,:,:])**2).sum(2)-w[None,:]
        lab=d.argmin(1); a=np.bincount(lab,minlength=K).astype(float)
        step=0.9*(1-it/iters)+0.1
        w+= (t-a)/N*step*(P.var(0).sum())*1.2
        for k in range(K):
            if a[k]>0: s[k]=0.6*s[k]+0.4*P[lab==k].mean(0)
    d=((P[:,None,:]-s[None,:,:])**2).sum(2)-w[None,:]; lab=d.argmin(1)
    a=np.bincount(lab,minlength=K)/N; err=np.abs(a-np.array(vals)/sum(vals))/(np.array(vals)/sum(vals))
    return s,w,err.max()
def assign(mask,X,Y,s,w):
    P=np.stack([X[mask],Y[mask]],1); d=((P[:,None,:]-s[None,:,:])**2).sum(2)-w[None,:]; return d.argmin(1)
nc=360; Xc,Yc=grid(nc); mc=(Xc**2+Yc**2)<=1
s0=rng.uniform(-.6,.6,(len(REG),2)); s0=np.array([[-.5,.2],[.45,.3],[.05,-.55],[.5,-.5],[-.45,-.6],[.0,.8]])
sr,wr,e1=power(mc,[rv[r] for r in REG],s0,Xc,Yc); print("region err",round(e1,3))
lab1=np.full(mc.shape,-1); lab1[mc]=assign(mc,Xc,Yc,sr,wr)
CS={}
for ri,r in enumerate(REG):
    cs=[d for d in D if d[3]==r]; m=(lab1==ri)
    if len(cs)==1: CS[r]=(None,None,cs); continue
    idx=np.argwhere(m); pick=idx[rng.choice(len(idx),len(cs),replace=False)]
    sites=np.stack([Xc[pick[:,0],pick[:,1]],Yc[pick[:,0],pick[:,1]]],1)
    s,w,e=power(m,[c[2] for c in cs],sites,Xc,Yc); print(r,"err",round(e,3)); CS[r]=(s,w,cs)
# hi-res raster
n=1500; Xh,Yh=grid(n); mh=(Xh**2+Yh**2)<=1
l1=np.full(mh.shape,-1); l1[mh]=assign(mh,Xh,Yh,sr,wr)
l2=np.full(mh.shape,-1)   # country index into D
for ri,r in enumerate(REG):
    s,w,cs=CS[r]; m=(l1==ri)
    if s is None: l2[m]=D.index(cs[0]); continue
    a=assign(m,Xh,Yh,s,w); l2[m]=[D.index(cs[k]) for k in a]
# colors
img=np.zeros((n,n,4),float); bgc=np.array(matplotlib.colors.to_rgb(BG))
for i,d in enumerate(D):
    base=np.array(matplotlib.colors.to_rgb(RC[d[3]])); rank=[x for x in D if x[3]==d[3]].index(d)
    sh=1.0-0.10*rank if rank<4 else 0.6
    col=np.clip(base*sh,0,1); img[l2==i,:3]=col; img[l2==i,3]=1
def edges(L,k):
    e=np.zeros(L.shape,bool)
    e[:-1]|=L[:-1]!=L[1:]; e[1:]|=L[:-1]!=L[1:]; e[:,:-1]|=L[:,:-1]!=L[:,1:]; e[:,1:]|=L[:,:-1]!=L[:,1:]
    return ndi.binary_dilation(e,iterations=k)&mh
img[edges(l2,2)]=[*bgc,1]; img[edges(l1,4)]=[*bgc,1]
img[(Xh**2+Yh**2)>0.99**2]=[*bgc,1]
im=Image.fromarray((img*255).astype(np.uint8)).resize((900,900),Image.LANCZOS); arr=np.asarray(im)/255
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor=BG)
fig.text(0.09,0.945,"The 20 biggest\neconomies, sized by GDP",fontsize=40,fontweight="bold",color=INK,va="top",linespacing=1.05)
fig.text(0.09,0.826,f"Each slice is one country's 2025 GDP, grouped by region. The US and\nChina alone are {(30.770+19.498)/TOT*100:.0f}% of the combined ${TOT:.1f}T.",fontsize=19.5,color=GREY,va="top",linespacing=1.35)
fig.text(0.09,0.078,"Source: World Bank WDI via FRED, GDP in current US$, 2025. *Saudi Arabia: 2024 (latest available).",fontsize=12.5,color=GREY,va="top")
fig.text(0.09,0.034,"CHART2DAY",fontsize=20,fontweight="bold",color=COBT)
ax=fig.add_axes([0.05,0.10,0.90,0.68],facecolor=BG); ax.set_xlim(-1.16,1.16); ax.set_ylim(-1.16,1.16); ax.set_aspect("equal"); ax.axis("off")
ax.imshow(arr,extent=[-1,1,-1,1],origin="upper",zorder=1)
th=np.linspace(0,2*np.pi,400); ax.plot(1.04*np.cos(th),1.04*np.sin(th),color=LINE,lw=1.8,zorder=2)
dist=ndi.distance_transform_edt(l2>=0)
pxu=lambda c,r:(-1+2*(c+.5)/n, 1-2*(r+.5)/n)
inch_per_unit=ax.get_window_extent().width/100/2.32
for i,d in enumerate(D):
    m=(l2==i); dm=ndi.distance_transform_edt(m); r,c=np.unravel_index(dm.argmax(),dm.shape); x,y=pxu(c,r)
    rad=dm.max()/n*2*inch_per_unit*72   # inscribed radius in pt
    nm=d[1]; fs=min(50,1.2*rad/(0.56*len(nm)),0.62*rad); fs=max(fs,7.5)
    big=fs>=14
    ax.text(x,y+(0.012 if big else 0.0)*(fs/30),nm,color="white",fontsize=fs,fontweight="bold",ha="center",va="center" if not big else "bottom",zorder=5)
    if big: ax.text(x,y+0.0,f"${d[2]:.1f}T",color="white",fontsize=max(fs*0.72,9),ha="center",va="top",zorder=5,alpha=0.92)
    else: ax.text(x,y-0.035,f"${d[2]:.1f}T",color="white",fontsize=7.5,ha="center",va="center",zorder=5,alpha=0.9)
for ri,r in enumerate(REG):
    m=(l1==ri); rr,cc=np.nonzero(m); x,y=pxu(cc.mean(),rr.mean()); a=np.arctan2(y,x)
    rot=np.degrees(a)-90; rot=rot+180 if (rot<-90 or rot>90) else rot
    ax.text(1.085*np.cos(a),1.085*np.sin(a),f"{r.upper()}  {rv[r]/TOT*100:.0f}%",rotation=rot,rotation_mode="anchor",ha="center",va="center",fontsize=13,fontweight="bold",color=RC[r] if THEME=="dark" else RC[r],zorder=6)
fig.savefig(f"2026-11-04-top20-economies-circle-{THEME}.png",facecolor=BG); print("saved")
