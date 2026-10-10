import gen, collections, re
from gen import *
PLAN={"clothed":20,"underwear":20,"naked":20}
SEED={"clothed":11,"underwear":22,"naked":33}
notes=gen.__dict__.get("notes")
NOTES={"clothed":"Everyday people in working or street clothes. Marine uniforms are generic navy blue with no logos.",
"underwear":"Swimwear, towels, bath wraps, lingerie, plain underwear. Calm, neutral poses.",
"naked":"Plain adult nudity, calm poses, plain pale background, character references only. Seated/kneeling poses use a three-quarter view."}
OUT=gen.OUT
seen=set()
for pool,nf in PLAN.items():
    allrows=[]
    ccount=collections.Counter()
    counts={"W":{}, "M":{}}  # label counts per sex, only used for clothed
    for k in range(1,nf+1):
        gen.FACE_MODE = 'plain' if k>10 else 'std'
        if pool=="clothed":
            rows=gen_rows(pool,100,(k-1)*100+1,SEED[pool]+(k-1)*101,role_counts=ccount)
        else:
            gen.SULTRY_FRAC = (0.3 if k==4 else 0.1 if k>4 else 0) if pool=="naked" else 0
            rows=gen_rows(pool,100,(k-1)*100+1,SEED[pool] if k==1 else SEED[pool]+k*101)
        check(rows)
        for r in rows:
            assert r["prompt"] not in seen; seen.add(r["prompt"])
        allrows+=rows
        write(pool,rows,f"NPC_PROMPTS_{pool}_{k:02d}.md",NOTES[pool],allrows,k)
    old=sum(1 for r in allrows if r["age"] in("forties","fifties","sixties","seventies"))
    print(pool,len(allrows),"forties+",round(old/len(allrows),2),"words max",max(len(r["prompt"].split()) for r in allrows))
    if pool=="clothed":
        c=collections.Counter(r["role"] for r in allrows)
        print(" roles min/max",min(c.values()),max(c.values()), "n roles",len(c))
    else:
        w=[r for r in allrows if r["sex"]=="woman"]; print(" per sex",len(w),len(allrows)-len(w),"settings",len(set(r['role'] for r in allrows)))
