import json,sys
data=json.load(open(sys.argv[1]));W,H=1080,1920
def kind(s):return s.split('#')[0]
def inter(a,b):
    x0,y0=max(a[0],b[0]),max(a[1],b[1]);x1,y1=min(a[2],b[2]),min(a[3],b[3])
    return max(0,x1-x0)*max(0,y1-y0)
issues={}
for fr in data:
    els={}
    for r in fr['r']:
        if r['a']<0.25:continue
        key=r['src'] if r['src']!='art' else 'art:'+r['text'][:20]
        b=els.setdefault(key,{'b':list(r['b']),'txt':r['text']})['b']
        b[0]=min(b[0],r['b'][0]);b[1]=min(b[1],r['b'][1]);b[2]=max(b[2],r['b'][2]);b[3]=max(b[3],r['b'][3])
        if r['src']!='art' and len(els[key]['txt'])<40 and r['text'] not in els[key]['txt']:els[key]['txt']+=' '+r['text']
    ks=list(els)
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            a,b=ks[i],ks[j]
            if a.startswith('art') and b.startswith('art'):continue
            if kind(a)==kind(b)=='tag':continue
            A,B=els[a]['b'],els[b]['b'];ia=inter(A,B)
            sm=min((A[2]-A[0])*(A[3]-A[1]),(B[2]-B[0])*(B[3]-B[1]))+1e-6
            if ia/sm>0.04:
                k=(kind(a) if not a.startswith('art') else 'надпись фона',els[a]['txt'][:28],kind(b) if not b.startswith('art') else 'надпись фона',els[b]['txt'][:28])
                issues.setdefault(k,[]).append(fr['t'])
    for k,e in els.items():
        if k.startswith('art'):continue
        b=e['b']
        if b[0]<-4 or b[2]>W+4 or b[1]<-4 or b[3]>H+4:
            issues.setdefault(('за краем экрана',e['txt'][:28],'',''),[]).append(fr['t'])
for k,ts in sorted(issues.items(),key=lambda x:x[1][0]):
    print(f"{ts[0]:6.2f}-{ts[-1]:6.2f}с ({len(ts)} кадр.)  {k[0]} «{k[1]}»  ×  {k[2]} «{k[3]}»")
print('ИТОГО проблем:',len(issues))
