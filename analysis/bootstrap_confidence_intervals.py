import math, collections, sys
import numpy as np
ds=sys.argv[1]
def load(p):
    T=[]
    for l in open(p,encoding="utf-8"):
        l=l.strip()
        if l: h,r,t=l.split("\t"); T.append((h,r,t))
    return T
tr=load(f"./kg/{ds}/train.txt"); va=load(f"./kg/{ds}/valid.txt"); te=load(f"./kg/{ds}/test.txt")
R=sorted({r for _,r,_ in tr}); Rs=set(R); N=len(R); a=0.1
glob=collections.Counter(r for _,r,_ in tr)
hr=collections.defaultdict(collections.Counter); tc=collections.defaultdict(collections.Counter)
for h,r,t in tr: hr[h][r]+=1; tc[t][r]+=1
ht={h:sum(c.values()) for h,c in hr.items()}; tt={t:sum(c.values()) for t,c in tc.items()}
logp={r:math.log((glob[r]+a)/(len(tr)+a*N)) for r in R}
known=collections.defaultdict(set)
for h,r,t in tr+va+te: known[(h,t)].add(r)
def s_h(h,t):
    c=hr.get(h); tot=ht.get(h,0)
    return {r:(c[r]+a)/(tot+a*N) if c else glob[r] for r in R}
def s_t(h,t):
    c=tc.get(t); tot=tt.get(t,0)
    return {r:(c[r]+a)/(tot+a*N) if c else glob[r] for r in R}
def s_nb(h,t):
    ch=hr.get(h); th=ht.get(h,0); ct=tc.get(t); ttt=tt.get(t,0); o={}
    for r in R:
        lp=logp[r]
        if ch: lp+=math.log((ch[r]+a)/(th+a*N))
        if ct: lp+=math.log((ct[r]+a)/(ttt+a*N))
        o[r]=lp
    return o
def rr(scores,gold,keep):
    gs=scores[gold]; g=e=0
    for r,s in scores.items():
        if r not in keep or r==gold: continue
        if s>gs: g+=1
        elif s==gs: e+=1
    return 1.0/(g+e/2.0+1.0)
fns={"p(r|h)":s_h,"p(r|t)":s_t,"NB":s_nb}
out={k:[] for k in fns}
for h,r,t in te:
    if r not in Rs: continue
    keep=set(R)-(known[(h,t)]-{r})
    for k,f in fns.items(): out[k].append(rr(f(h,t),r,keep))
rng=np.random.default_rng(0); B=1000
print(f"=== {ds} (n={len(out['p(r|t)'])}) ===")
for k in fns:
    v=np.array(out[k]); n=len(v)
    idx=rng.integers(0,n,size=(B,n)); bm=v[idx].mean(axis=1)
    print(f"  {k:7s} MRR={v.mean():.4f}  95% CI [{np.percentile(bm,2.5):.4f}, {np.percentile(bm,97.5):.4f}]")
