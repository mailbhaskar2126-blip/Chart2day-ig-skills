import numpy as np, wave, subprocess
sr=44100; T=19.3; n=int(sr*T); t=np.arange(n)/sr
rng=np.random.default_rng(7)
def env(a,b,x): return np.clip((x-a)/(b-a),0,1)
# drone
drone=0.5*np.sin(2*np.pi*55*t)+0.3*np.sin(2*np.pi*55.4*t)+0.25*np.sin(2*np.pi*110*t+0.5*np.sin(2*np.pi*0.2*t))
drone*=0.35+0.5*env(0,8,t)
# pulse: heartbeat speeds up
ph=np.cumsum(1.0+1.2*env(0,8,t))/sr*1.2
pulse=np.exp(-((ph%1)*14))*np.sin(2*np.pi*70*t)*(0.25+0.6*env(0,8,t))
# riser: filtered noise rising to 2010
noise=rng.standard_normal(n); k=np.ones(200)/200
low=np.convolve(noise,k,'same'); hi=noise-low
riser=(low*0.6+hi*0.6*env(0,8,t))*env(2,8,t)*(1-env(8,8.3,t))*0.7
# impact at 8.05s
ti=t-8.05; hit=np.where(ti>=0,np.exp(-ti*2.2)*(np.sin(2*np.pi*(45+30*np.exp(-ti*6))*ti)*1.1+0.5*rng.standard_normal(n)*np.exp(-ti*9)),0)
# arpeggio tension after hit (minor)
notes=[220,261.63,329.63,261.63]; arp=np.zeros(n)
for i in range(int(8.4*4),int(16.3*4)):
    s=i/4.0; f=notes[i%4]*(1.5 if (i//16)%2 else 1); m=(t>=s)&(t<s+0.25); tt=t[m]-s
    arp[m]+=np.sin(2*np.pi*f*tt)*np.exp(-tt*9)*0.18
# end card: warm resolve pad
pad=sum(np.sin(2*np.pi*f*t) for f in (110,164.81,220,277.18))*0.09*env(16.1,17.2,t)
mix=drone*0.55+pulse+riser+hit*0.9+arp+pad
mix*=env(0,0.15,t)*(1-env(18.4,19.3,t))
mix=np.tanh(mix*1.2); mix/=np.abs(mix).max(); mix*=0.8
st=np.stack([mix,np.roll(mix,60)],1)
w=wave.open("/tmp/claude-0/-home-claude/69c34abb-c808-5373-8a6a-0e6de21c468a/scratchpad/elec-music.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype("<i2").tobytes()); w.close()
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","2026-11-10-chart2day-electricity-race.mp4","-i","/tmp/claude-0/-home-claude/69c34abb-c808-5373-8a6a-0e6de21c468a/scratchpad/elec-music.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","2026-11-10-chart2day-electricity-race-music.mp4"],check=True)
print("ok")
