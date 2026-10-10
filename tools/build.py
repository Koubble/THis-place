import json,re
base="/home/user/THis-place/"
NEG=None
data={}
for p in ["clothed","underwear","naked"]:
    rows=[]
    import glob
    for fn in sorted(glob.glob(f"{base}NPC_PROMPTS_{p}_[0-9][0-9].md")):
        frows=[]
        for l in open(fn):
            if re.match(rf"\| {p}_\d+ \|",l):
                c=[x.strip() for x in l.strip().strip("|").split(" | ")]
                frows.append(dict(pool=p,id=c[0],sex=c[2],age=c[3],build=c[5],role=c[13],prompt=c[15]))
        open(fn[:-3]+".txt","w").write("\n\n".join(r["prompt"] for r in frows)+"\n")
        rows+=frows
    data[p]=rows
    open(f"{base}NPC_PROMPTS_{p}_ALL.txt","w").write("\n\n".join(r["prompt"] for r in rows)+"\n")
# base negative = shortest common
import random
rnd=random.Random(7)
rnd.shuffle(data["naked"])
allrows=[r for k in ("clothed","underwear","naked") for r in data[k]]
rnd.shuffle(allrows)
open(f"{base}NPC_PROMPTS_naked_ALL.txt","w").write("\n\n".join(r["prompt"] for r in data["naked"])+"\n")
open(f"{base}NPC_PROMPTS_EVERYTHING.txt","w").write("\n\n".join(r["prompt"] for r in allrows)+"\n")
data=allrows
html=open("tpl.html").read().replace("__DATA__",json.dumps(data,separators=(",",":")))
open("copy_page.html","w").write(html)
print(len(data))
