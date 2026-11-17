# Altyazı kelimelerini senaryo metnine eşler (yazım senaryodan, zaman whisper'dan)
import json,re,difflib
W=json.load(open('words.json'))['words']
t=open('../ses/elevenlabs-metin.txt').read(); t=re.sub(r'\[[^\]]*\]','',t)
for a,b in {"/ˈɪpsən/":"Ibsen","/peːr jʏnt/":"Peer Gynt","/ɛnˈkoʊd/":"ENCODE","/frɔʏt/":"Freud","/jʊŋ/":"Jung","/laˈkɑ̃/":"Lacan","/hjuːm/":"Hume","/saʁtʁ/":"Sartre"}.items(): t=t.replace(a,b)
S=t.split(); n=lambda s:re.sub(r"[^\wçğıöşüâîû']","",s.lower())
out=[]
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,[n(x) for x in S],[n(x['w']) for x in W],autojunk=False).get_opcodes():
    if op=='equal':
        for k in range(i2-i1): out.append({'w':S[i1+k],'s':W[j1+k]['s'],'e':W[j1+k]['e'],'p':1})
    elif op in('replace','insert') and i2>i1:
        a=W[j1]['s'] if j2>j1 else out[-1]['e']; b=W[j2-1]['e'] if j2>j1 else a+0.3
        L=[len(x) for x in S[i1:i2]]; T=sum(L); c=a
        for k,x in enumerate(S[i1:i2]):
            d=(b-a)*L[k]/T; out.append({'w':x,'s':round(c,3),'e':round(c+d,3),'p':1}); c+=d
json.dump(out,open('words-raw.json','w'),ensure_ascii=False,indent=0)
print(len(out),'kelime, senaryo',len(S))
