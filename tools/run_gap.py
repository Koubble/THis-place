import sys, collections, random
sys.path.insert(0,'.')
import gen
from gen import *
import roles2
OUT=gen.OUT
# sanity: old pools unchanged by patches
def weights(rs):
    d={}
    for r in rs:
        if r[0]: d[(r[0],0)]=r[5]
        if r[1]: d[(r[1],1)]=r[6]
    return d
gen.FACE_MODE='plain'
gen.PICKER_SEP=True
gen.AGE_DECK_BY_SEX={"W":["twenties","thirties","thirties","forties","forties","forties","fifties","fifties","fifties","sixties","sixties","seventies"],
                     "M":["twenties","twenties","twenties","thirties","thirties","thirties","forties","forties","fifties","fifties","sixties","seventies"]}
rows=[]
# clothed gap roles (760)
gen.ACTIVE_ROLES=roles2.ROLES2; gen.ROLE_W=weights(roles2.ROLES2)
rows_a=gen_rows("clothed",760,1,901,role_counts=collections.Counter())
# sea faces (100)
gen.ACTIVE_ROLES=roles2.SEA; gen.ROLE_W=weights(roles2.SEA)
rows_b=gen_rows("clothed",100,1,902,role_counts=collections.Counter())
# underwear gap (140): lingerie/nightwear/plain underwear for women, briefs/boxers/robe for men
gen.ACTIVE_ROLES=None; gen.ROLE_W={}
gen.AGE_DECK_BY_SEX={"W":["twenties","thirties","forties","forties","forties","fifties","fifties","fifties","sixties","sixties","thirties","seventies"],
                     "M":["twenties","twenties","twenties","twenties","thirties","thirties","forties","forties","fifties","sixties","thirties","seventies"]}
gen.BUILD_BY_SEX={"W":gen.BUILDS+["athletic"]*6+["muscular"]*2,"M":gen.BUILDS}
okw=("lingerie","night room","plain underwear")
gen.U_W=[t for t in gen.U_W if t[0] in okw]
gen.U_M=[t for t in gen.U_M if any(k in t[1] for k in ("briefs","boxers","robe","thong","long johns","union suit","vest and drawers","sleeping trousers","nightshirt")) and "swim" not in t[1]]
rows_c=gen_rows("underwear",140,1,903)
allr=rows_a+rows_b+rows_c
check(rows_a); check(rows_b); check(rows_c)
random.Random(5).shuffle(allr)
seen=set()
for i,r in enumerate(allr,1):
    r["id"]=f"gap_{i:04d}"; r["pool"]="gap"
    assert r["prompt"] not in seen; seen.add(r["prompt"])
note="Gap-list prompts: roles and looks the game library is short of (officials, scholars, performers, bath and hair work, craft, healers, food, the shady, gentry and servants, the poor end, boat work), sea faces, and underwear gaps. Ages, builds, skin tones and hair vary in every role."
cum=[]
for k in range(1,11):
    chunk=allr[(k-1)*100:k*100]; cum+=chunk
    write("gap",chunk,f"NPC_PROMPTS_gap_{k:02d}.md",note,cum,k)
def share(f): return round(100*sum(1 for r in allr if f(r))/len(allr))
print("total",len(allr),"women",share(lambda r:r["sex"]=="woman"),"% ; forties+ women",share(lambda r:r["sex"]=="woman" and r["age"] in("forties","fifties","sixties","seventies")),"% of all; men 20s",share(lambda r:r["sex"]=="man" and r["age"]=="twenties"),"% of all")
c=collections.Counter(r["role"] for r in allr); print("roles",len(c),"min",min(c.values()),"max",max(c.values()))
print(c.most_common(8))
