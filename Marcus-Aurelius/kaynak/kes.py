import json,re,wave,numpy as np
w=json.load(open('words-raw.json'))
sents=[];cur=[]
for i,x in enumerate(w):
  cur.append(i)
  if re.search(r"[.!?:]$",x['w']): sents.append(cur);cur=[]
if cur: sents.append(cur)
CUT=[11,18,23,47,48,57,58,67]
r=wave.open('audio/vo.wav'); sr=r.getframerate(); ch=r.getnchannels()
a=np.frombuffer(r.readframes(r.getnframes()),np.int16).reshape(-1,ch).astype(np.float32)
mono=np.abs(a).mean(1)
def snap(t,lo,hi):
  i0=int(max(lo,t-0.2)*sr); i1=int(min(hi,t+0.2)*sr)
  win=int(0.02*sr); seg=mono[i0:i1]
  e=np.convolve(seg,np.ones(win)/win,'same'); return (i0+int(np.argmin(e)))/sr
cuts=[]
for k in CUT:
  prev_e=w[sents[k-1][-1]]['e']; s=w[sents[k][0]]['s']
  n_s=w[sents[k+1][0]]['s']; e=w[sents[k][-1]]['e']
  A=snap(s-0.05,prev_e,s); B=snap(n_s-0.05,e,n_s)
  cuts.append((A,B)); print(k,round(A,2),round(B,2)," ".join(w[i]['w'] for i in sents[k]))
keep=[];t=0
for A,B in cuts: keep.append((t,A)); t=B
keep.append((t,len(a)/sr))
fade=int(0.012*sr); out=[]
for A,B in keep:
  p=a[int(A*sr):int(B*sr)].copy()
  if len(p)<3*fade: continue
  ramp=np.linspace(0,1,fade)[:,None]; p[:fade]*=ramp; p[-fade:]*=ramp[::-1]; out.append(p)
o=np.concatenate(out); print('yeni sure',round(len(o)/sr,2),'kesilen',round(sum(B-A for A,B in cuts),2))
wo=wave.open('audio/vo-kesik.wav','w'); wo.setnchannels(ch); wo.setsampwidth(2); wo.setframerate(sr)
wo.writeframes(np.clip(o,-32768,32767).astype(np.int16).tobytes()); wo.close()
json.dump(cuts,open('kesimler.json','w'))
