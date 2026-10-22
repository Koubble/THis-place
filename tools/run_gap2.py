import sys, collections, random, glob
sys.path.insert(0,'.')
import gen
from gen import *
import roles2
def weights(rs):
    d={}
    for r in rs:
        if r[0]: d[(r[0],0)]=r[5]
        if r[1]: d[(r[1],1)]=r[6]
    return d
gen.FACE_MODE='plain'; gen.PICKER_SEP=True
gen.AGE_DECK_BY_SEX={"W":["twenties","thirties","thirties","forties","forties","forties","fifties","fifties","fifties","sixties","sixties","seventies"],
                     "M":["twenties","twenties","twenties","thirties","thirties","thirties","forties","forties","fifties","fifties","sixties","seventies"]}
gen.ACTIVE_ROLES=roles2.SEA; gen.ROLE_W=weights(roles2.SEA)
rows_b=gen_rows("clothed",100,1,912,role_counts=collections.Counter())
gen.ACTIVE_ROLES=None; gen.ROLE_W={}
gen.AGE_DECK_BY_SEX={"W":["twenties","thirties","forties","forties","forties","fifties","fifties","fifties","sixties","sixties","thirties","seventies"],
                     "M":["twenties","twenties","twenties","twenties","thirties","thirties","forties","forties","fifties","sixties","thirties","seventies"]}
gen.BUILD_BY_SEX={"W":gen.BUILDS+["athletic"]*6+["muscular"]*2,"M":gen.BUILDS}
okw=("lingerie","night room","plain underwear")
gen.U_W=[t for t in gen.U_W if t[0] in okw]
gen.U_M=[t for t in gen.U_M if any(k in t[1] for k in ("briefs","boxers","robe","thong","long johns","union suit","vest and drawers","sleeping trousers","nightshirt")) and "swim" not in t[1]]
rows_c=gen_rows("underwear",60,1,913)
check(rows_b); check(rows_c)
old=set()
for fn in glob.glob("/home/user/THis-place/NPC_PROMPTS_gap_[0-9][0-9].md"):
    for l in open(fn):
        if l.startswith("| gap_"): old.add(l.split(" | ")[15].strip().rstrip("|").strip())
new=rows_b+rows_c
random.Random(6).shuffle(new)
for i,r in enumerate(new,1001):
    r["id"]=f"gap_{i:04d}"; r["pool"]="gap"
    assert r["prompt"] not in old
note="Gap-list top-up: 100 more sea faces (pirates, privateers, mercenaries, Wardens, yacht people, bounty hunters, odd vessels) and 60 more underwear (lingerie, nightwear, briefs, boxers, robes)."
write("gap",new[:100],"NPC_PROMPTS_gap_11.md",note,new[:100],11)
write("gap",new[100:],"NPC_PROMPTS_gap_12.md",note,new,12)
print(len(new),"new;",collections.Counter(r['sex'] for r in rows_b),collections.Counter(r['age'] for r in rows_b))
print(collections.Counter(r['role'] for r in rows_b).most_common(20))
