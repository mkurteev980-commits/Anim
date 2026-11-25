import sys,re,wave,json,numpy as np
D=sys.argv[1];HTML=sys.argv[2];SR=48000
def rd(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
src={k:rd(f'{D}/{k}.wav') for k in ['narr','gena_old','gena3','final']}
def envl(x):
    h=int(0.02*SR);return np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0,len(x)-h,h)])
E={k:envl(v) for k,v in src.items()}
def tend(k,b):
    e=E[k];i=int(b/0.02)
    while i<len(e) and 20*np.log10(e[i]+1e-9)>-45:i+=1
    return i*0.02
def tstart(k,a):
    e=E[k];i=int(a/0.02)
    while i>0 and 20*np.log10(e[i-1]+1e-9)>-45:i-=1
    return i*0.02
V=[('narr',0.16,2.76,0.3,0,'n',[('В ЛАГЕРЕ «ЗОРЬКА» ЕСТЬ ТРИ *ПРАВИЛА.',0.16,2.76)]),
 ('narr',3.15,5.64,3.05,1,'n',[('ПЕРВОЕ: НОЧЬЮ НЕ ОТКРЫВАЙ ГЛАЗА.',3.15,5.64)]),
 ('gena_old',0,1.49,5.8,2,'g',[('«МА-АША…»',0,1.49)]),
 ('narr',5.92,6.76,7.6,2,'n',[('ТЫ *ОТКРЫЛА.',5.92,6.76)]),
 ('gena_old',1.89,3.46,8.75,3,'g',[]),
 ('narr',7.04,9.36,10.5,4,'n',[('ВСЕ КРОВАТИ ПУСТЫЕ.',7.04,8.36),('ЗАПРАВЛЕНЫ.',8.56,9.36)]),
 ('narr',9.6,12.44,13.05,5,'n',[('ВТОРОЕ: НОЧЬЮ — НИКАКОЙ ЛИНЕЙКИ.',9.6,12.44)]),
 ('narr',12.64,16.2,16.0,6,'n',[('НО ГОРН ЗОВЁТ.',12.64,13.72),('ВЕСЬ ОТРЯД УЖЕ ТАМ.',13.92,15.08),('*СПИНОЙ К ТЕБЕ.',15.28,16.2)]),
 ('gena_old',3.74,5.75,19.8,7,'g',[]),
 ('narr',16.48,19.4,22.0,8,'n',[('У ВСЕХ *МОКРЫЕ ВОЛОСЫ.',16.48,18.04),('И *ТИНА НА САНДАЛИЯХ.',18.08,19.4)]),
 ('narr',19.66,22.52,25.05,9,'n',[('ТРЕТЬЕ: НИКОГДА НЕ ПОДХОДИ К ОЗЕРУ.',19.66,22.52)]),
 ('gena3',0.24,2.02,28.0,10,'g',[]),
 ('gena3',2.44,3.65,29.85,10,'g',[]),
 ('narr',22.56,25.2,31.1,11,'n',[('ТЫ СТОИШЬ У ВОДЫ.',22.56,23.76),('СЗАДИ — ВЕСЬ ОТРЯД.',23.84,25.2)]),
 ('narr',25.44,30.32,33.9,12,'n',[('НА СТОЛБЕ — ТАБЛИЧКА.',25.44,26.99),('«ОТРЯД НОМЕР ТРИ.',27.01,28.28),('ТЫСЯЧА ДЕВЯТЬСОТ ПЯТЬДЕСЯТ ШЕСТОЙ».',28.32,30.32)]),
 ('narr',30.4,32.36,38.9,12,'n',[('ПОСЛЕДНЕЕ ИМЯ — *ТВОЁ.',30.4,32.36)]),
 ('narr',32.47,34.3,41.1,13,'n',[('А В ВОДЕ ТВОЁ ОТРАЖЕНИЕ…',32.47,34.28)]),
 ('narr',34.32,35.55,43.0,13,'n',[('*УЛЫБАЕТСЯ.',34.32,35.55)]),
 ('final',0.0,5.6,46.5,14,'n',[('ЧТО ТЫ СДЕЛАЕШЬ?',0.0,1.16),('НЫРНЁШЬ В ВОДУ…',1.59,2.62),('ИЛИ ПОБЕЖИШЬ К *СТОРОЖУ?',3.06,4.29),('ПИШИТЕ В КОММЕНТАРИЯХ.',4.77,5.6)])]
G=[(0,3.0),(3.0,5.6),(5.6,8.6),(8.6,10.4),(10.4,13.0),(13.0,15.9),(15.9,19.6),(19.6,21.9),(21.9,25.0),(25.0,28.0),(28.0,31.0),(31.0,33.8),(33.8,41.0),(41.0,46.2),(46.2,52.7)]
PAD=0.45;GAP=0.15;VV=[]
for k,a,b,at,g,who,subs in V:
    VV.append(dict(k=k,a=max(0,tstart(k,a)-0.03),b=tend(k,b)+0.06,at=at,g=g,who=who,subs=subs))
fs=[]
for gi,(o0,o1) in enumerate(G):
    vs=[v for v in VV if v['g']==gi];f=1.0
    for i,v in enumerate(vs):
        dur=v['b']-v['a'];f=max(f,(dur+(PAD if gi<len(G)-1 else 0.3))/(o1-v['at']))
        if i+1<len(vs):f=max(f,(dur+GAP)/(vs[i+1]['at']-v['at']))
    fs.append(f)
NB=[0.0]
for gi,(o0,o1) in enumerate(G):NB.append(NB[-1]+(o1-o0)*fs[gi])
OB=[g[0] for g in G]+[G[-1][1]];DUR=round(NB[-1],2)
def O2N(to):
    for i in range(len(G)):
        if to<=G[i][1] or i==len(G)-1:return NB[i]+(to-G[i][0])*fs[i]
N=int((DUR+0.1)*SR);tr={w:np.zeros(N) for w in 'ng'};subs=[];TARGET=10**(-19/20);place=[]
for v in VV:
    st=max(O2N(v['at']),NB[v['g']]+0.08);seg=src[v['k']][int(v['a']*SR):int(v['b']*SR)].copy()
    act=seg[np.abs(seg)>0.01];rms=np.sqrt(np.mean(act**2)) if len(act) else 1e-3;seg*=min(TARGET/rms,4.0)
    f=int(0.012*SR);seg[:f]*=np.linspace(0,1,f);seg[-f:]*=np.linspace(1,0,f);i=int(st*SR);tr[v['who']][i:i+len(seg)]+=seg[:N-i]
    for txt,ws,we in v['subs']:subs.append((round(st+max(0,ws-v['a']),2),round(st+we-v['a'],2),txt))
    place.append((v['who'],round(st,2),round(st+v['b']-v['a'],2)))
for w in 'ng':np.save(f'{D}/{w}v.npy',tr[w])
json.dump(dict(NB=NB,OB=OB,fs=fs,DUR=DUR,place=place),open(D+'/warp.json','w'))
def lipof(x):
    hop=SR//30;F=int(DUR*30)+2;env=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(F)]);ref=np.percentile(env[env>0.005],90)
    l=np.clip(env/ref,0,1);l=np.convolve(l,[0.25,0.5,0.25],'same');l[l<0.08]=0;return ','.join(f'{q:.2f}' for q in l)
s=open(HTML).read()
s=re.sub(r"let LIPG=\[[^\]]*\];","let LIPG=["+lipof(tr['g'])+"];",s)
s=re.sub(r"const SUBS_RAW=\[.*?\n\];","const SUBS_RAW=[\n"+"\n".join(f" [{a},{b},'{t}']," for a,b,t in subs)+"\n];",s,flags=re.S)
s=re.sub(r"const W=1080,H=1920,DUR=[0-9.]+;",f"const W=1080,H=1920,DUR={DUR};",s)
s=re.sub(r"const WNB=\[[^\]]*\],WOB=\[[^\]]*\];","const WNB="+json.dumps([round(x,4) for x in NB])+",WOB="+json.dumps(OB)+";",s)
open(HTML,'w').write(s);print('DUR',DUR,'factors',[round(x,2) for x in fs]);print(place)
