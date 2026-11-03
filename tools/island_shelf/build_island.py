import csv, json, re, sys, collections
sys.path.insert(0, ".")
import importlib
from species import SPECIES
from ugly_overrides import UGLY
from beauty_overrides import BEAUTY

CSV_PATH, OUT_JSON = sys.argv[1], sys.argv[2]
PH = importlib.import_module(sys.argv[3] if len(sys.argv) > 3 else 'poses_hearthstone')

STYLE = ("One Piece anime art style, adventure manga anime style, bold clean ink outlines, vivid flat colours with cel "
         "shading, expressive exaggerated features, stylised adult proportions, mature adult character, dynamic composition")
BG = {"clothed": "plain cream background (#FFF8E7)",
      "nude": "plain pale lavender-tinted cream background (#EEE6F7)",
      "swim": "plain pale aqua-tinted cream background (#DDF3F1)"}
FRAME = "three-quarter length shot framed from the head down to the knees, knees included, hips and thighs fully in view"
ANAT = {"F": "nipples and vagina visible", "M": "average size penis"}


def parse_people(raw):
    """-> (species base, species description, extra descriptors). The roster may carry its own description after a colon."""
    raw = raw.strip()
    if ":" in raw:
        base, desc = raw.split(":", 1)
        return base.strip(), desc.strip(), []
    pp = [x.strip() for x in raw.split(",")]
    base = re.sub(r"\s+(man|woman)$", "", pp[0])
    extra = [x for x in pp[1:] if "grown adult" not in x]
    return base, SPECIES.get(base, ("", None))[0], extra


def anat(r):
    """Women: fixed wording. Men: a roster size/shape note wins, then the species default, then 'average size penis'."""
    if r["sex"] == "F":
        return ANAT["F"]
    s = r["bust_or_scale"].lower()
    if re.search(r"huge|enormous|massive|giant", s):
        return "huge penis"
    if re.search(r"very large|much larger|well above", s):
        return "very large penis"
    if re.search(r"larger than average|\blarge\b|\bbig\b|above average", s):
        return "larger than average penis"
    if re.search(r"tiny|very small", s):
        return "very small penis"
    if re.search(r"smaller than average|\bsmall\b|below average", s):
        return "smaller than average penis"
    if "knotted" in s:
        return "knotted penis"
    if "barbed" in s:
        return "barbed penis"
    if "ridged" in s:
        return "ridged paired penis"
    base = parse_people(r["people"])[0]
    return SPECIES.get(base, ("", None))[1] or ANAT["M"]

PROMPT_AGE = {}  # user asked for this one to be written as 18
# wording fixes so no youthful words reach a prompt, and no weapon words
SUB = [("blood-stained", "dark-stained"), ("petite", "small-framed"), ("boyish", "cheeky"), ("wide-eyed, trusting smile", "trusting smile"), ("wide-eyed, shy", "shy"),
       ("a wide-eyed trusting smile", "a bright trusting smile"), ("a thin cleaver scar", "a thin scar"),
       ("cleaver scar", "scar")]
SKIN_OVERRIDE = {}
OVERRIDE = {  # id: {field: replacement} for entries the template reads badly
    "T8-1": {"hair": "brown hair"},
    "T8-1.eyes": "brown",
}


def fix(s):
    for a, b in SUB:
        s = s.replace(a, b)
    return s


def article(w):
    return "an" if w[0].upper() in "AEFHILMNORSX" else "a"


def skin_phrase(s):
    s = s.strip()
    if "skin" in s:
        return s
    if " with " in s:
        return s.replace(" with ", " skin with ", 1)
    if "," in s or "across" in s or " from " in s:
        return f"skin that is {s}"
    return f"{s} skin"


def eyes_phrase(e):
    e = fix(e.strip())
    if e.startswith("wide "):
        e = e[5:]
    if "eye" in e:  # "one pale blue eye and an eye-patch"
        return e
    if " behind" in e:
        return e.replace(" behind", " eyes behind", 1)
    if ", with" in e:
        return e.replace(", with", " eyes with", 1)
    if " with " in e:
        return e.replace(" with ", " eyes with ", 1)
    return f"{e} eyes"


def face_phrase(f):
    f = fix(f.strip())
    if "face" in f:
        return f if f.startswith(("a ", "an ")) else f"a face with {f}" if not f.startswith("a ") else f
    if f.startswith(("a ", "an ")):
        return "a face with " + f
    return "a face with " + f


UNGLAM = re.compile(r"ugly|wart|pockmark|lumpy|crooked|broken nose|dented nose|flattened nose|big nose|bulbous|jowl|sagging|gap-toothed|"
                    r"missing (tooth|ear|fingertip|front)|cleft|blotch|leer|sleazy|oily|greasy|sweating|puffy|red nose|gold tooth|"
                    r"squint|hollow|gaunt|coarse|rough-hewn|lopsided|weathered|lined|wrinkled|papery|sallow|haggard|shifty|"
                    r"hard face|heavy brow|flat face|tired face|worn face|plain", re.I)
PRETTYRE = re.compile(r"beautiful|pretty|handsome|glamorous|elegant|striking|gorgeous|stunning", re.I)


def apply_ugly(r):
    o = UGLY.get(r["id"])
    if o:
        if o.get("face_add"):
            r["face"] = r["face"].rstrip(" .") + ", " + o["face_add"]
        if o.get("skin"):
            r["skin"] = o["skin"]
        if o.get("build"):
            r["build"] = o["build"]
    return r


def core(r):
    sex = r["sex"]
    woman = sex == "F"
    age = int(r["age"])
    pa = PROMPT_AGE.get(r["id"], max(age, 22))  # prompt age: the three youngest are written as 22
    people, desc, extra = parse_people(r["people"])
    sw = "woman" if woman else "man"
    her = "her" if woman else "his"
    head = f"{r['name']}, {pa}-year-old {people} {sw}"
    if pa >= 40:
        head += f" who looks {her} age"
    if desc:
        head += ", " + desc
    if extra:
        head += ", " + ", ".join(extra)
    if pa >= 55:
        head += f", an older {sw}"
    if age < 22:
        head += f", an adult {sw} with defined cheekbones and mature features"
    parts = [head, r["height"].replace('""', '"'), fix(r["build"])]
    if woman:
        cup = r["bust_or_scale"].strip()
        parts.append(f"{article(cup)} {cup} bust")
    parts.append(skin_phrase(fix(r["skin"])))
    parts.append(face_phrase(r["face"]))
    ftext = r["face"] + " " + r["marks"] + " " + r["skin"]
    if r["id"] in BEAUTY:
        parts.append("exceptionally beautiful, strikingly attractive, flawless radiant skin, perfectly balanced symmetrical features, luminous eyes, full lips" if woman else "exceptionally handsome, strikingly attractive, flawless skin, sculpted jaw and cheekbones, magnetic eyes")
    elif r["id"] in UGLY or (UNGLAM.search(ftext) and not PRETTYRE.search(r["face"])):
        if re.search(r"powder|painted|rouge", ftext, re.I):
            parts.append("plain unglamorous looks, blemished uneven skin")
        else:
            parts.append("plain ordinary unglamorous looks, bare face with no makeup, natural skin with pores, blemishes and uneven tone")
        if r["id"] in UGLY:
            parts.append("unflattering rough-hewn features")
    parts.append(eyes_phrase(r["eyes"]))
    hair = fix(r["hair"].strip())
    if r["id"] == "T8-1":
        hair = "brown hair"
    parts.append(hair)
    if r["marks"].strip():
        parts.append(fix(r["marks"].strip()))
    return ", ".join(parts)


# A third (swimwear/underwear) prompt is only made for people who are in, or could turn up in, a place where
# swimwear or bathwear is worn: beaches, baths, spas, pools, springs, caves, changing huts, wash and scrub houses,
# massage rooms, and swimmers, lifeguards and bathers.
SWIM_PLACE = re.compile(r"\bbath|\bspa\b|\bpools\b|\bbeach\b|\bcove\b|\bshore\b(?! leave)|\bshingle\b|\bstrand\b|\bspring|\bseep\b|"
                        r"\bbasins?\b|\bplunge\b|\bsauna|sweat hall|thaw house|scrub house|\bwash|\blido\b|tide cave|"
                        r"sunbath|pontoon|\bmere\b|cleansing|changing hut|massage|masseu|kneading|swimm|lifeguard|"
                        r"surfer|steam kettle|hammam|rinse|scrubbing|rain butts|steam jetty|dampf|breakwater|diving|grotta|clinker steams|quenching lake|cenote|immersion trough|slack water|grotto|humid cavern|\bdips?\b|ablution|thermal|vapour tank|cistern|cauldron|sudatorium|strigil|soak|lagoon|jetty|wallow|oasis dip|brimstone fount|\bpond\b|\btubs?\b|mudflat|"
                        r"moorage|moorings|canal pier|seaward", re.I)


# Adult-venue workers and people who sell themselves (brothel, parlour, tent, salon and lodging-house staff, companions,
# hustlers, alley and street folk, homeless) also get one: lingerie, drawers or ragged underwear is their normal state.
ADULT_ROLE = re.compile(r"madam|madame|hostess|\bworker\b|companion|works the arch|works there|hustler|"
                        r"offers (himself|herself|company)|\bselling\b|sells (his|her) nights|chosen (man|woman)|"
                        r"rent in kind|woman of the (back )?lane|available|host of the tent|rarer appetites|girl (from|who)|house's one man|\bescort\b|courtesan|sells smiles|slipping into the dunes|girl slipping|girl meeting|in the alley|sells (his|her) (nights|evenings)|sells hustles|woman of the (arena )?fringe", re.I)
ADULT_PLACE = re.compile(r"lattice|late lanterns|shared rite|whisper salon|decanter|silk cellar|ruby parlour|red shutter|"
                         r"warm tent|windward bunk|brass latch|rented hour|chosen house|lodging house|floating party|pink pennant|mizzen lounge", re.I)
ADULT_STAFF = re.compile(r"attendant|keeper|cellarman|\bhost\b|hostess|madam|\bgirl\b|house's one man", re.I)
ALLEY_PLACE = re.compile(r"back alley", re.I)
# venues where everyone listed is an adult worker
ADULT_VENUE = re.compile(r"crimson crypt|\bdomino\b|discreet suite|oubliette|\bunmasked\b|murmur booths|twilight revel|\bsmoulder\b|"
                         r"peephole|rouge vestibule|private stakes|redemption rail|laurel chambers|scale boudoir|collectors snug|"
                         r"sixpenny cots|poppy den|jasmine house|saffron house|cypress majlis|ember divan|unlicensed entrance|"
                         r"obligation dormitory|hidden arbour|mirrored hall|hourly cabins|pillars below|ninth bolt|companions' agency|"
                         r"hushed apartments|frosted cubicles|starlit cottages|lamplit sampan|oleander bower|doffing vestry|\bquadrille\b|"
                         r"\bfelze\b|grille confessionals|dare peristyle|mermaids cradle|hammock tiers|moidore divans|kindling closets|mating copse|werg nischen|cercle loup noir|scellees souterrains|honeyed amber ottoman|subjugation vault|soft voices recess", re.I)
NOT_ADULT = {"E03-33", "E08-8", "E12-6", "E12-27", "E05-26", "S05-12", "S05-W3", "S06-25", "S05-16"}  # Dagmar: hostess of a social circle, not an adult worker


RAGGED = re.compile(r"selling|desperate|homeless|alley|street|sells (his|her) nights|lane|hustler|thief|drunk|pickpocket", re.I)
ADULT_DEFAULTS = {
    ("F", False): ["a black lace lingerie set with stockings", "a red silk slip with stockings", "a cream lace chemise with stockings",
                   "a plum corset set with stockings"],
    ("M", False): ["black silk drawers", "snug white drawers", "red silk drawers"],
    ("F", True): ["a thin worn slip", "a ragged torn chemise", "a patched worn shift"],
    ("M", True): ["patched drawers", "ragged torn shorts", "worn wool drawers"],
}


def adult_default(r):
    """Fallback when a roster gives an adult worker no underwear item."""
    ragged = bool(RAGGED.search(r["role"] + " " + r["where"]))
    opts = ADULT_DEFAULTS[(r["sex"], ragged)]
    return opts[sum(map(ord, r["name"])) % len(opts)]


def is_adult_worker(r):
    """Adult-venue workers, people who sell themselves, alley and street folk."""
    if r["id"] in NOT_ADULT:
        return False
    if ADULT_ROLE.search(r["role"]) or ALLEY_PLACE.search(r["where"]) or ADULT_VENUE.search(r["where"]):
        return True
    return bool(ADULT_PLACE.search(r["where"]) and ADULT_STAFF.search(r["role"]))


def wants_third(r):
    """A separate swimwear/underwear prompt: only for swimwear/bathing places, and never for adult workers."""
    return bool(SWIM_PLACE.search(r["where"] + " " + r["role"])) and not is_adult_worker(r)


def tidy_third(t):
    t = t.strip()
    m = {"a one-piece": "a plain one-piece swimsuit", "trunks": "plain swim trunks", "red trunks": "red swim trunks",
         "striped trunks": "striped swim trunks", "a patched shift": "a patched ragged shift",
         "board shorts": "board shorts", "plain underwear": "plain underwear"}
    return m.get(t, t)


rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
people = []
bad_obj = re.compile(r"\b(holding|hold|towel|tray|fan|spoon|rope|crate|book|ledger|stool|chair|wall|table|counter|bed|door|bottle|basket|pin cushion|tape|strap)\b", re.I)
for r in rows:
    r = {k: (v or "").strip() for k, v in r.items()}
    r = apply_ugly(r)
    cb = core(r)
    woman = r["sex"] == "F"
    pid = r["id"]
    cl_pose, nu_pose, sw_pose = PH.P[pid]
    for p in (cl_pose, nu_pose, sw_pose or ""):
        assert not bad_obj.search(p), (pid, p)
    if woman:
        assert not re.search(r"\barms? (folded|crossed)(?! behind)|wrapped round", nu_pose), (pid, nu_pose)
    clothed_out = fix(r["clothed_outfit"])
    if is_adult_worker(r):
        # STANDING RULE: adult workers are never seen in normal clothes. Their one non-nude prompt is their normal attire
        # (lingerie, drawers, a slutty dress, ragged torn underwear), whatever the roster's clothed/third columns say.
        t3 = r["third_image_swim_or_underwear"]
        clothed_out = fix(tidy_third(t3)) if t3 and not re.search(r"swimsuit|towel|wrap-cloth|trunks|bikini", t3, re.I) \
            else adult_default(r)
    cl_expr = fix(r["clothed_expression"])
    nu_expr = fix(r["nude_expression"])
    pr = {}
    pr["clothed"] = (f"{STYLE}, one {'woman' if woman else 'man'}, {cb}, wearing {clothed_out}, {cl_pose}, {FRAME}, "
                     f"soft even light, {cl_expr}, {BG['clothed']}")
    pr["nude"] = (f"{STYLE}, one {'woman' if woman else 'man'}, {cb}, fully nude, no clothing, {nu_pose}, {FRAME}, "
                  f"soft even light, {nu_expr}, {BG['nude']}, {anat(r)}")
    if r["third_image_swim_or_underwear"] and wants_third(r):
        sw_expr = cl_expr
        pr["swim"] = (f"{STYLE}, one {'woman' if woman else 'man'}, {cb}, wearing {tidy_third(r['third_image_swim_or_underwear'])}, "
                      f"{sw_pose}, {FRAME}, soft even light, {sw_expr}, {BG['swim']}")
    people.append(dict(id=pid, name=r["name"], where=r["where"], role=r["role"], sex="woman" if woman else "man",
                       age=int(r["age"]), prompts=pr))

# safety/consistency checks
BAN = re.compile(r"\b(girl|boy|young|youthful|teen|schoolgirl|cute|petite|childlike|baby|loli|chibi|child|kid|sword|gun|knife|axe|cleaver)\b", re.I)
for p in people:
    for k, t in p["prompts"].items():
        assert not BAN.search(t), (p["id"], k, BAN.search(t).group(0))
        assert t.startswith(STYLE)
    # the core appearance block must be word-for-word identical across a person's prompts
    cores = []
    for k, t in p["prompts"].items():
        s = t.split(", one ", 1)[1].split(", ", 1)[1]
        cores.append(s.split(", wearing ")[0].split(", fully nude")[0])
    assert len(set(cores)) == 1, p["id"]
    ages = re.findall(r"(\d+)-year-old", p["prompts"]["clothed"])
    assert int(ages[0]) >= 22 or p["id"] in PROMPT_AGE, p["id"]
json.dump(people, open(OUT_JSON, "w"), indent=1)
n = sum(len(p["prompts"]) for p in people)
print(len(people), "people,", n, "prompts; words max", max(len(t.split()) for p in people for t in p["prompts"].values()))
