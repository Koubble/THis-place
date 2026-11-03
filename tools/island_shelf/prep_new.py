import csv, re, sys, zlib
isl = sys.argv[1]
rows = list(csv.DictReader(open(f"{isl}_raw.csv", encoding="utf-8-sig")))
fields = list(rows[0].keys())
PROP = re.compile(r"\b(ledger|tray|notebook|slate|stack of papers|clipboard|armful of books|baton|parasol|umbrella|briefcase|clutch|"
                  r"fan|menu card|programme|script|sheet music|wax tablet|ladle|goblet|wine jug|basket|tasting spoon|scroll|brass pot|"
                  r"long pipe|long holder|mask on a stick|ticket book|ticket pouch|satchel|canvas bag|deck of cards|coil of rope|"
                  r"rope coiled|bag of surgical tools|gold-handled bag|scales|mortar|magnifier|bar cloth|bar towel|limp cloth|"
                  r"stub of chalk|tape and chalk|reed pen|gold-nibbed pen|tuning fork|violin bow|ticker tape|chalkboard|"
                  r"ticket|gloves in (his|her) (belt|pocket)|speaking trumpet|lantern on a pole|thimble|sealing-wax stick|"
                  r"small brass bell|baton in one hand|tall brass pot|scraper-brush|toll box|tasting|wreath in hand|"
                  r"make-up brush|tiny scales|a ring of keys|key ring|chain of keys|bruise|rake|brass scale|dipper|beard comb|fine tools|"
                  r"tally cord|sack|bucket|bunch of keys|bottle|tin cup|cheap pies|stamp and an ink pad|lantern|bar rag|barrel tap|"
                  r"crate of oddments|snuffbox|stocks|ring of rusty keys|huge ring of keys|a rope|rope around|lute|pen box|pen case|vial|a seal)\b", re.I)
KEEP = re.compile(r"behind (the|his|her) ear", re.I)
HELD = re.compile(r"\b(in hand|in one hand|under (his|her|one) arm|over (one|his|her) shoulder|in (his|her) pocket|in (his|her) hand)\b", re.I)
CLEAN = {}
exec(open(f"clean_{isl}.py").read()) if __import__("os").path.exists(f"clean_{isl}.py") else None
changed = []
for r in rows:
    # garbled hair text: "greying dark  in a chignon hair"
    h = r["hair"]
    m = re.match(r"(.*?)\s{2,}(.*) hair$", h)
    if m:
        h = f"{m.group(1)} hair {m.group(2)}"
    r["hair"] = h
    for pre, nm in (("ember folk", "ember folk"), ("ogre", "ogre"), ("amazon", "amazon"), ("cat-kin", "cat-kin"), ("wolf-kin", "wolf-kin")):
        if r["people"].startswith(pre):
            r["people"] = nm
    r["skin"] = re.sub(r"bruised and ", "", r["skin"])
    r["marks"] = re.sub(r"^(bruises|a collar-mark on the neck)$", "", r["marks"])
    if r["people"].startswith("reptile-folk"):
        r["people"] = "scalekin"
        r["skin"] = re.sub(r"\bscales\b", "scaled", r["skin"])
        r["hair"] = re.sub(r"^none", "no hair", r["hair"])
    # outfit: drop carried-prop segments
    segs = [s.strip() for s in re.split(r",\s*", r["clothed_outfit"]) if s.strip()]
    keep = [s for s in segs if KEEP.search(s) or not (PROP.search(s) or HELD.search(s))]
    if keep != segs:
        new = ", ".join(keep)
        changed.append((r["id"], r["clothed_outfit"], new))
        r["clothed_outfit"] = new
    for k in ("clothed_outfit", "third_image_swim_or_underwear"):
        r[k] = re.sub(r"\b(damp|wet) ", "", r[k])
    r["face"] = re.sub(r"\byoung,?\s*", "", r["face"])
    r.update(CLEAN.get(r["id"], {}))
w = csv.DictWriter(open(f"{isl}_clean.csv", "w", newline="", encoding="utf-8"), fieldnames=fields)
w.writeheader(); w.writerows(rows)
for c in changed: print(c[0], "|", c[1], "=>", c[2])

# ---- poses (body-only, varied) ----
W = {
 "hip": ["standing with one hand on the hip and the weight on one leg","standing with one hand resting on the hip, the head tilted","standing with a hand on the hip and the shoulders back","standing with the hand on the hip and the chin lifted"],
 "collar": ["standing with one hand at the collarbone","standing with the fingertips resting at the collarbone, the head tilted","standing with one hand lifted to the collarbone and the other arm loose","standing with one hand at the collarbone and the weight on one leg"],
 "behind": ["standing with the arms behind the back","standing with the hands clasped behind the back and the chest lifted","standing with the hands behind the back, leaning slightly forward","standing with the arms behind the back and the head tilted"],
 "hair": ["standing with the hair over one shoulder","standing with one hand sweeping the hair over one shoulder","standing with the head tilted and the hair falling over one shoulder","standing with one hand lifted to the hair, the other arm loose"],
 "weight": ["standing with the weight on one leg","standing with the weight on one hip and the arms loose","standing with a relaxed hip tilt, the arms loose at the sides","standing with the weight on one leg and the head tilted"],
 "sides": ["standing with the arms loose at the sides","standing tall with the arms relaxed at the sides","standing with the arms loose at the sides and the head tilted"],
 "clasp": ["standing with the hands clasped in front","standing with the hands lightly clasped in front and the shoulders back","standing with the hands clasped in front and the head tilted"],
}
M = {
 "head": ["standing relaxed with one hand behind the head","standing with one hand behind the head and the weight on one leg","standing with both hands behind the head, relaxed","standing relaxed with one hand behind the head, the other arm loose"],
 "hips": ["standing square with the hands on the hips","standing with the hands on the hips and the chest out","standing with the hands on the hips and the chin lifted","standing square with the hands on the hips, the shoulders back"],
 "sides": ["standing with the arms at the sides","standing tall with the arms loose at the sides","standing with the arms relaxed at the sides and the chin lifted","standing upright with the arms at the sides"],
 "weight": ["standing with the weight on one leg","standing with the weight on one leg and the arms loose","standing with a relaxed hip tilt, the arms loose","standing easy with the weight on one leg, the head tilted"],
 "cross": ["standing with the arms crossed over the chest","standing with the arms folded over the chest, the shoulders back","standing with the arms crossed and the chin lifted","standing with the arms folded across the chest and the weight on one leg"],
 "hip": ["standing with one hand on the hip","standing with one hand on the hip and the weight on one leg","standing with a hand on the hip and the head tilted","standing with one hand on the hip, the other arm loose"],
}
def cls(p, woman):
    p = p.lower()
    if "behind his head" in p or "behind her head" in p: return "head"
    if "hands on his hips" in p or "hands on her hips" in p: return "hips"
    if "collarbone" in p: return "collar"
    if "behind her back" in p or "behind his back" in p: return "behind"
    if "hair over" in p: return "hair"
    if "weight on one leg" in p: return "weight"
    if "clasped" in p: return "clasp"
    if "crossed" in p or "folded" in p: return "cross"
    if "hand on his hip" in p or "hand on her hip" in p: return "hip"
    return "sides"
out = ["# generated: body-only, varied. id: (clothed pose, nude pose, swim/underwear pose or None)", "P = {"]
for r in rows:
    woman = r["sex"] == "F"
    pool = W if woman else M
    c = cls(r["nude_pose"], woman)
    if woman and c == "cross": c = "behind"
    if not woman and c in ("collar", "behind", "hair", "clasp"): c = "sides"
    if not woman and c == "sides" and "behind his back" in r["nude_pose"]: c = "sides"
    k = zlib.crc32(r["id"].encode())
    nu_c = c if c in pool and c != "clasp" else "behind"
    if woman and c == "clasp": nu_c = "behind"
    nu = pool[nu_c][k % len(pool[nu_c])]
    cc = c if c in pool else "sides"
    cl = pool[cc][(k + 1) % len(pool[cc])]
    sw = (pool.get("weight" if woman else "head") )[(k + 2) % 4] if r["third_image_swim_or_underwear"] else None
    if sw and woman and "hair" in c: sw = W["hair"][(k + 2) % 4]
    out.append(f'"{r["id"]}": ({cl!r}, {nu!r}, {sw!r}),')
out.append("}")
open(f"poses_{isl}.py", "w").write("\n".join(out) + "\n")
