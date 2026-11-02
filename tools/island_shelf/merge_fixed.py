import csv, sys
FIXED_IN, ISLAND_IN, OUT = sys.argv[1:4]
# Name references removed; the shared features stay. Only these four fields differ from the uploaded fixed rows.
CLEAN = {
 "N3-15": dict(skin="pale with fine lines", hair="thin white hair that was once grey-brown, in a small bun",
               eyes="pale grey-blue eyes, kind and a little tired, behind wire glasses",
               face="a round, plain, soft face with a kind tired look, an old woman's face"),
 "N4-14": dict(skin="deep reddish-orange tan with deep lines, age spots on the forearms",
               eyes="brown eyes, wide under raised sly brows",
               face="a huge silent weathered face with raised sly brows and deep forehead furrows"),
 "N4-15": dict(skin="deep reddish-orange tan",
               hair="thick scruffy silver-grey hair swept up, a short grey beard",
               eyes="brown eyes, wide under raised sly brows",
               face="a big slow weathered face with raised sly brows and, when he smiles, a huge toothy grin, only slower"),
 "N4-16": dict(skin="deep reddish-orange tan",
               hair="thick scruffy silver-grey hair tied at the nape, a full grey-brown beard",
               eyes="brown eyes, wide under raised sly brows",
               face="a wry weathered face with raised sly brows and crow's feet, and a toothy sly grin"),
 "N9-2": dict(skin="fairly light, slightly peachy skin with fine lines",
              eyes="large dark brown eyes behind red-framed glasses on a chain",
              face="a precise, sharp face with a perfectionist's frown, a small nose and a small soft mouth, and a beauty spot on the chin just below the lower lip"),
 "T7-1": dict(face="defined cheekbones and a wide mouth, a quick tongue and laugh lines"),
}
fixed = {}
for r in csv.DictReader(open(FIXED_IN, encoding="utf-8")):
    r = dict(r)
    r.update(CLEAN.get(r["id"], {}))
    fixed[r["id"]] = r
rd = csv.DictReader(open(ISLAND_IN, encoding="utf-8"))
rows, hit = [], []
for r in rd:
    if r["id"] in fixed:
        rows.append({k: fixed[r["id"]][k] for k in rd.fieldnames}); hit.append(r["id"])
    else:
        rows.append(r)
w = csv.DictWriter(open(OUT, "w", encoding="utf-8", newline=""), fieldnames=rd.fieldnames)
w.writeheader(); w.writerows(rows)
print(ISLAND_IN.split("/")[-1][:12], "replaced", hit)
