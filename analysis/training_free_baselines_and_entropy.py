import math, collections
DATASETS=["CoDEx-S","CoDEx-M","FB15k-237"]

def load(path):
    T=[]
    for line in open(path, encoding="utf-8"):
        line=line.strip()
        if not line: continue
        h,r,t=line.split("\t")
        T.append((h,r,t))
    return T

def rr_hits(scores, gold, filtered_gold_ok):
    # scores: dict r->score over candidate relations (R_train). Higher=better.
    # filtered_gold_ok: set of relations to KEEP (gold + non-known-true). Others removed.
    gs=scores[gold]
    greater=0; equal=0
    for r,s in scores.items():
        if r not in filtered_gold_ok: continue  # filtered out (other known-true)
        if r==gold: continue
        if s>gs: greater+=1
        elif s==gs: equal+=1
    rank=greater + equal/2.0 + 1.0          # expected rank under random tie-break
    rr=1.0/rank
    hits1 = (1.0/(equal+1.0)) if greater==0 else 0.0
    return rr, hits1

for ds in DATASETS:
    tr=load(f"./kg/{ds}/train.txt")
    va=load(f"./kg/{ds}/valid.txt")
    te=load(f"./kg/{ds}/test.txt")
    Rtrain=sorted({r for _,r,_ in tr})
    Rset=set(Rtrain)
    # stats from TRAIN only
    glob=collections.Counter(r for _,r,_ in tr)
    hr=collections.defaultdict(collections.Counter)   # head -> relation counts
    tr_=collections.defaultdict(collections.Counter)  # tail -> relation counts
    for h,r,t in tr:
        hr[h][r]+=1; tr_[t][r]+=1
    htot={h:sum(c.values()) for h,c in hr.items()}
    ttot={t:sum(c.values()) for t,c in tr_.items()}
    Nrel=len(Rtrain)
    a=0.1  # smoothing
    # filtered known-true map from all splits
    known=collections.defaultdict(set)
    for h,r,t in tr+va+te: known[(h,t)].add(r)
    # log priors
    Ntr=len(tr)
    logprior={r: math.log((glob[r]+a)/(Ntr+a*Nrel)) for r in Rtrain}

    def score_global(h,t): return {r: glob[r] for r in Rtrain}
    def score_h(h,t):
        c=hr.get(h); tot=htot.get(h,0)
        if not c: return {r: glob[r] for r in Rtrain}     # backoff
        return {r: (c[r]+a)/(tot+a*Nrel) for r in Rtrain}
    def score_t(h,t):
        c=tr_.get(t); tot=ttot.get(t,0)
        if not c: return {r: glob[r] for r in Rtrain}
        return {r: (c[r]+a)/(tot+a*Nrel) for r in Rtrain}
    def score_ht(h,t):
        ch=hr.get(h); toth=htot.get(h,0); ct=tr_.get(t); tott=ttot.get(t,0)
        out={}
        for r in Rtrain:
            lp=logprior[r]
            if ch: lp+=math.log((ch[r]+a)/(toth+a*Nrel))
            if ct: lp+=math.log((ct[r]+a)/(tott+a*Nrel))
            out[r]=lp
        return out

    methods={"Global freq":score_global,"p(r|h)":score_h,"p(r|t)":score_t,"NB p(r|h,t)":score_ht}
    res={}
    # also top-1 head/tail accuracy and candidate counts
    top1h=top1t=0; candh=candt=0
    for h,r,t in te:
        candh+=len(hr.get(h,{})); candt+=len(tr_.get(t,{}))
        if hr.get(h) and hr[h].most_common(1)[0][0]==r: top1h+=1
        if tr_.get(t) and tr_[t].most_common(1)[0][0]==r: top1t+=1
    for name,fn in methods.items():
        srr=sh=0.0; n=0
        for h,r,t in te:
            if r not in Rset: continue   # unseen gold relation excluded (matches paper)
            sc=fn(h,t)
            keep=set(Rtrain)-(known[(h,t)]-{r})   # filtered: drop other known-true
            rr,h1=rr_hits(sc,r,keep)
            srr+=rr; sh+=h1; n+=1
        res[name]=(srr/n, sh/n, n)
    # entropy (bits) from TRAIN
    def H(counter):
        tot=sum(counter.values()); 
        return -sum((c/tot)*math.log2(c/tot) for c in counter.values() if c>0)
    HR=H(glob)
    # H(R|H)=sum_h P(h)H(R|h)
    def cond_H(mapc, totmap):
        tot=sum(totmap.values()); s=0.0
        for k,c in mapc.items():
            ph=totmap[k]/tot; s+=ph*H(c)
        return s
    HRH=cond_H(hr,htot); HRT=cond_H(tr_,ttot)
    print(f"\n===== {ds} =====")
    print(f"  |R_train|={Nrel}  test={len(te)}")
    print(f"  Filtered MRR / Hits@1 (training-free baselines):")
    for name in methods:
        mrr,h1,n=res[name]; print(f"    {name:14s}  MRR={mrr:.4f}  Hits@1={h1:.4f}  (n={n})")
    print(f"  Entropy (bits):  H(R)={HR:.3f}   H(R|H)={HRH:.3f}   H(R|T)={HRT:.3f}")
    print(f"  Top-1 relation accuracy:  by head={top1h/len(te):.4f}   by tail={top1t/len(te):.4f}")
    print(f"  Avg candidate relations per endpoint:  head={candh/len(te):.2f}   tail={candt/len(te):.2f}")
