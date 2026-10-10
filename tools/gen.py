import random, re, sys, collections

OUT = "/home/user/THis-place/"
STYLE = "hand-drawn manga, One Piece anime style, art by Eiichiro Oda, thick bold black ink contour lines, gritty cel shading, textured crosshatch shadows, matte skin, warm saturated colors, expressive face"
FRAME = "three-quarter body shot, head to mid-thigh"
BASE = "1person, adult, {frame}, plain soft pale background, no weapons"
NEG = "child, teen, teenager, young-looking, baby face, schoolgirl, loli, shota, chibi, cute, glossy skin, airbrushed, shiny highlights, 3D render, soft pastel colors, storybook illustration, watercolor, thin lines, beauty filter, extra fingers, deformed hands, extra limbs, text, watermark, realistic photo, blurry, low quality"
NEG_PLAIN = "beautiful, glamorous, model, perfect skin, makeup"

FACE_MODE = "std"
PLAINS = ["plain mature face", "plain ordinary face", "ugly crooked-nosed face", "weathered face with deep lines",
          "gap-toothed grin", "big lumpy nose", "small eyes", "double chin", "heavy brow and flat face",
          "sagging jowls", "pockmarked skin", "long gaunt face", "receding chin", "crooked teeth",
          "bushy eyebrows and wide mouth", "thick neck and heavy jaw", "sunken cheeks", "wide flat nose",
          "sallow tired face", "lopsided face"]
GOODS = ["round friendly face", "freckled face", "dimples", "soft jaw", "attractive mature face with high cheekbones",
         "handsome strong features", "striking face"]
FACES_PLAIN = PLAINS + GOODS
AGES = ["twenties", "thirties", "forties", "fifties", "sixties", "seventies"]
AGE_DECK = ["twenties", "twenties", "thirties", "thirties", "thirties", "forties", "forties", "forties",
            "fifties", "fifties", "sixties", "seventies"]
SKINS = ["pale freckled", "fair", "light tan", "warm tan", "olive", "brown", "deep brown", "weathered ruddy"]
BUILDS = ["thin and wiry", "lean", "average", "athletic", "muscular", "stocky", "broad", "heavyset", "plump",
          "very fat", "tall and lanky", "short and round", "tall and broad", "small and slight"]
BUSTS = ["flat-chested", "small bust", "modest bust", "medium bust", "full bust", "large bust", "very large bust"]
W_SHAPE_ALL = ["narrow hips", "average hips", "wide hips", "pear-shaped", "hourglass", "apple-shaped",
               "straight-figured", "soft belly", "toned stomach", "stretch marks", "broad shoulders", "muscular thighs"]
M_DETAIL_ALL = ["lean", "wiry", "soft belly", "barrel chest", "broad shoulders", "hairy chest", "smooth chest",
                "muscular arms", "thin legs", "heavy thighs"]
HEAVY = {"stocky", "broad", "heavyset", "plump", "very fat", "short and round", "tall and broad"}
THIN = {"thin and wiry", "lean", "tall and lanky", "small and slight"}
FACES = ["plain mature face"] * 3 + ["ugly crooked-nosed face"] * 2 + ["weathered face with deep lines"] * 2 + [
    "round friendly face", "sharp narrow face", "scarred face", "freckled face", "gap-toothed grin", "strong jaw",
    "soft jaw", "big nose", "small eyes", "wide set eyes", "double chin", "dimples"]
PLAIN_FACES = set(PLAINS) | {"plain mature face", "ugly crooked-nosed face", "weathered face with deep lines", "gap-toothed grin",
               "big nose", "small eyes", "double chin"}
FACIAL = ["clean-shaven", "clean-shaven", "stubble", "short beard", "full beard", "long beard", "moustache",
          "long sideburns"]
HAIR_COLORS = ["black", "dark brown", "chestnut", "auburn", "red", "ginger", "blonde", "dirty blonde", "platinum",
               "grey", "white", "silver streaked", "dyed blue", "dyed green", "dyed pink", "two-tone"]
OLD_COLORS = ["grey", "white", "silver streaked", "grey", "white", "dark brown", "black", "silver streaked"]
MID_COLORS = ["black", "dark brown", "chestnut", "auburn", "grey", "silver streaked", "red", "dirty blonde", "white"]
STYLES_M = ["short cropped", "shaggy", "curly", "afro", "tight curls", "bald", "balding", "shaved sides",
            "tied back", "wild", "side-swept", "long and wavy", "long braided", "dreadlocks", "long and straight"]
STYLES_W = ["short cropped", "shaggy", "long braided", "curly", "afro", "tight curls", "shaved sides", "tied back",
            "bun", "high knot", "twin braids", "wild", "side-swept", "bob", "long and straight", "long and wavy",
            "dreadlocks"]
EYES = ["brown", "dark brown", "hazel", "green", "grey", "blue", "amber"]
MARKS_C = ["scar across the cheek", "eyepatch over one eye", "missing front tooth", "tattoo on the forearm",
           "freckles", "moles", "birthmark", "round spectacles", "broken nose", "burn mark on the arm",
           "calloused hands"]
MARKS_N = MARKS_C + ["tattoos on the shoulder", "tattoos on the shoulder"]
EXPR_C = ["friendly", "grumpy", "suspicious", "bored", "cheerful", "shy", "shrewd", "tired", "amused", "stern",
          "worried", "calm"]
EXPR_SUG = ["coy smile", "sultry half-lidded eyes", "knowing smirk"]
EXPR_U = EXPR_C + EXPR_SUG * 3
EXPR_N = ["relaxed", "calm", "relaxed", "playful teasing smile", "playful teasing smile", "stern teasing look",
          "stern teasing look", "amused", "shy smile", "confident smirk", "content"]
SUG_ROLES = {"hostess", "host", "companion", "dancer", "barmaid", "waiter", "masseuse", "masseur", "fortune teller",
             "gambler", "dealer", "bath attendant", "madam", "street performer", "musician", "noble lady", "noble lord",
             "courier", "tattoo artist", "innkeeper"}

# pose: key -> (text, frame or None)
POSES = {
    "standing relaxed": ("standing relaxed", None),
    "arms crossed": ("arms crossed", None),
    "hands on hips": ("hands on hips", None),
    "one hand on a hip": ("one hand on a hip", None),
    "leaning on a wall": ("leaning on a wall", None),
    "leaning on a counter": ("leaning on a plain counter", None),
    "hands behind the back": ("hands behind the back", None),
    "holding an object of the trade": (None, None),
    "looking over the shoulder": ("looking over the shoulder", None),
    "walking": ("walking", None),
    "sitting on a stool": ("sitting on a stool", "seated, three-quarter view"),
    "sitting on a crate": ("sitting on a crate", "seated, three-quarter view"),
    "sitting on the edge of a bed": ("sitting on the edge of a bed", "seated, three-quarter view"),
    "sitting cross-legged": ("sitting cross-legged", "seated, three-quarter view"),
    "kneeling": ("kneeling", "full body"),
    "crouching": ("crouching", "full body"),
    "stretching": ("stretching", None),
    "tying up hair": ("tying up hair", None),
    "adjusting a collar": ("adjusting a collar", None),
    "drying with a towel": ("drying with a towel", None),
    "lying on one side": ("lying on one side on a towel", "reclining, three-quarter view"),
    "reclining on cushions": ("reclining on cushions", "reclining, three-quarter view"),
    "arms raised": ("arms raised", None),
    "arms folded under the chest": ("arms folded under the chest", None),
    "hands clasped in front": ("hands clasped in front", None),
    "holding a cup": ("holding a cup", None),
    "holding a lantern": ("holding a lantern", None),
    "mid-laugh": ("mid-laugh", None),
    "glancing away": ("glancing away", None),
}
NAKED_FRAMES = {"kneeling": "three-quarter view, head to knees"}
POSE_C = [k for k in POSES if k not in ("lying on one side", "reclining on cushions", "drying with a towel")]
POSE_U = [k for k in POSES if k not in ("adjusting a collar", "leaning on a counter", "holding an object of the trade")]
POSE_N = [k for k in POSES if k not in ("adjusting a collar", "leaning on a counter", "holding an object of the trade",
                                         "crouching", "holding a lantern", "leaning on a wall")]

WEALTH = {"ragged": "ragged", "rough": "rough worn", "plain": "plain", "comfortable": "comfortable",
          "rich": "rich fine", "noble": "noble ornate"}

# role: (woman label, man label, outfit, prop, wealth options)
R = lambda w, m, o, p, wl="rough plain comfortable": (w, m, o, p, wl.split())
ROLES = [
    R("shopkeeper", "shopkeeper", "{c} apron over shirt|waistcoat, sleeve garters|long {c} coat, scarf|vest, rolled sleeves|w:{c} dress, shawl, apron|m:{c} shirt, braces, cloth cap", "a ledger", "plain comfortable rich"),
    R("tavern keeper", "tavern keeper", "rolled-sleeve shirt, apron|{c} waistcoat, towel on shoulder|leather vest, bare forearms|w:{c} bodice, apron, rolled sleeves|m:open shirt, long apron", "a tankard", "plain comfortable"),
    R("barmaid", "waiter", "tavern apron and blouse|{c} vest, bow tie|w:laced {c} bodice, short skirt|w:off-shoulder blouse, apron|m:{c} shirt, long apron|m:waistcoat, rolled sleeves", "a tray", "plain comfortable"),
    R("cook", "cook", "stained apron, cap|{c} chef coat, neckerchief|rolled sleeves, towel at belt|{c} bandana, apron|tall chef hat, white coat", "a ladle", "plain rough"),
    R("baker", "baker", "flour-dusted apron|{c} cap, floury shirt|rolled sleeves, linen apron|w:{c} headscarf, apron dress|m:vest, floury forearms", "a bread paddle", "plain comfortable"),
    R("brewer", "brewer", "leather apron, shirt|{c} work shirt, rolled sleeves|heavy {c} coat, rubber boots|wet canvas apron, boots|{c} waistcoat, cap", "a barrel stave", "rough plain"),
    R("market seller", "market seller", "wet apron, boots|{c} oilskin apron|striped shirt, rubber apron|{c} headscarf, long apron|woolly {c} vest, rolled sleeves", "a market basket", "rough ragged"),
    R('sea angler', 'sea angler', "oilskin coat|{c} sou'wester hat, oilskins|woollen {c} jumper, waders|net over shoulder, shirt|{c} knit cap, jumper", 'a coiled net', 'rough ragged'),
    R("sailor", "sailor", "striped shirt, sash|{c} bandana, open vest|wide-collar {c} shirt, bell trousers|knit {c} cap, pea jacket|sleeveless {c} shirt, rope belt", "a rope coil", "rough plain"),
    R('old sailor', 'old sailor', "faded jacket, cap|{c} knit jumper, rolled trousers|patched pea jacket|worn captain's {c} coat|oilskin, weathered hat", 'a pipe', 'rough ragged'),
    R("dockworker", "dockworker", "sleeveless vest, trousers|{c} work shirt, braces|leather harness vest, bare arms|canvas apron, cap|torn sleeves, rope belt", "a rope coil", "rough plain"),
    R("ferry boatwoman", "ferry boatman", "wide hat, plain shirt|{c} oilskin, cap|rolled trousers, vest|woolly {c} scarf, jacket|w:headscarf, sleeveless blouse", "a long oar", "rough plain"),
    R("harbour master", "harbour master", "buttoned coat, cap|{c} frock coat, brass buttons|waistcoat, pocket watch|gold-braided coat", "a clipboard", "comfortable rich"),
    R("clerk", "clerk", "waistcoat, sleeve guards|{c} jacket, cravat|plain shirt, ink-stained cuffs|w:{c} blouse, long skirt|m:{c} suit, round collar", "a quill", "plain comfortable"),
    R("scholar", "scholar", "long robe, scarf|{c} academic gown|tweed coat, cravat|w:{c} high-collar dress|m:waistcoat, loose shirt", "a heavy book", "plain comfortable"),
    R("librarian", "librarian", "long vest, shirt|{c} cardigan, spectacles chain|shawl, high collar|w:{c} blouse, long skirt|m:waistcoat, bow tie", "a book stack", "plain comfortable"),
    R("priest", "priest", "plain clerical robe|{c} cassock|stole over robe|hooded {c} vestment|plain robe, rope belt", "a prayer book", "plain comfortable"),
    R("nun", "monk", "simple habit|{c} hooded habit|plain tunic, rope belt|robe, wooden beads", "prayer beads", "plain"),
    R("herbalist", "herbalist", "shawl, pouch belt|{c} apron, herb pouches|hooded {c} cloak|w:{c} skirt, vest|m:{c} coat, satchel", "a herb bundle", "rough plain"),
    R("doctor", "doctor", "long coat, satchel|white coat, {c} scarf|waistcoat, rolled sleeves|{c} frock coat, spectacles chain|dark coat, stethoscope", "a medicine bottle", "comfortable rich"),
    R("blacksmith", "blacksmith", "scorched leather apron|sleeveless {c} shirt, apron|leather vest, heavy gloves|rolled sleeves, soot-smeared|{c} headband, apron", "iron tongs", "rough plain"),
    R("shipwright", "shipwright", "tool belt, work shirt|{c} work jacket, cap|canvas apron, rolled sleeves|vest, sawdust-dusted|bandana, tool pouch", "a hand saw", "rough plain"),
    R("carpenter", "carpenter", "work vest, rolled sleeves|{c} overalls|leather apron, pencil in hand|flat cap, canvas apron|tool belt, shirt", "a plank", "rough plain"),
    R("tailor", "tailor", "waistcoat, measuring tape|{c} jacket, pins on cuff|apron with pockets|w:{c} dress, tape around neck|m:{c} shirt, braces", "a cloth roll", "plain comfortable"),
    R("jeweller", "jeweller", "vest, loupe|{c} brocade waistcoat|jacket, signet rings|dark apron, loupe on forehead", "a small box", "comfortable rich"),
    R("bookseller", "bookseller", "long coat, scarf|{c} cardigan|waistcoat, half-moon spectacles|sleeve garters, apron", "a book", "plain comfortable"),
    R("florist", "florist", "apron, sun hat|{c} headscarf, apron|rolled sleeves, flower-stained apron|w:{c} dress, apron|m:{c} shirt, apron", "a flower bunch", "plain comfortable"),
    R("toymaker", "toymaker", "paint-spotted apron|{c} smock, cap|waistcoat, sawdust|goggles on forehead, apron", "a wooden toy", "plain rough"),
    R("farmer", "farmer", "straw hat, work clothes|{c} overalls|patched shirt, braces|w:{c} headscarf, apron dress|m:rolled trousers, vest", "a hoe", "rough ragged"),
    R("pasture worker", "pasture worker", "wide hat, long coat|{c} poncho|woolly vest, boots|scarf, heavy jacket", "a wooden crook", "rough plain"),
    R("miner", "miner", "dusty overalls, helmet|{c} jacket, headlamp|sooty shirt, braces|leather cap, kerchief", "a lamp", "rough ragged"),
    R("lumberjack", "lumberjack", "checked shirt, suspenders|{c} flannel, rolled sleeves|sleeveless vest, hat|heavy coat, boots", "a sawn log", "rough plain"),
    R("gardener", "gardener", "apron, gloves|{c} straw hat, smock|rolled trousers, vest|w:{c} dress, apron|m:{c} shirt, braces", "a trowel", "rough plain"),
    R("town watchwoman", "town watchman", "dark coat, cap|{c} greatcoat|leather jerkin, armband|cloak, wide hat", "a lantern", "plain"),
    R("Marine officer", "Marine officer", "white uniform coat, navy-blue collar and cuffs, no logos|white coat open over shirt, navy-blue trim, no logos|white officer cap with navy-blue band, no logos|white uniform, navy-blue epaulettes, sleeves rolled, no logos", "a clipboard", "comfortable rich"),
    R("Marine rank-and-file", "Marine rank-and-file", "white uniform, navy-blue collar, no logos|white sailor shirt, navy-blue stripes, cap|white jacket, navy-blue cuffs, rolled sleeves, no logos|white vest, navy-blue sailor collar, no logos", "a folded flag", "plain"),
    R("pirate", "pirate", "open coat, bandana|{c} captain-style coat, sash|ragged striped shirt|tricorn hat, leather vest|bandana, gold hoop earrings", "a mug", "rough ragged"),
    R("smuggler", "smuggler", "hooded cloak, satchel|{c} long coat, scarf|dark vest, hidden pockets|wide hat, travel cloak", "a small crate", "rough plain"),
    R("thug", "thug", "sleeveless vest, wrapped fists|{c} leather jacket|torn shirt, studded belt|heavy coat, scarf", "a tankard", "rough ragged"),
    R("bounty hunter", "bounty hunter", "long coat, wide hat|{c} poncho, scarf|dusty long coat|hood, leather vest", "a wanted poster", "rough plain"),
    R("fortune teller", "fortune teller", "beaded shawl, headscarf|{c} robe, many rings|veil, jewelled collar|hooded {c} cloak", "a crystal ball", "plain comfortable"),
    R("musician", "musician", "loose shirt, sash|{c} waistcoat, cravat|embroidered jacket|bright {c} scarf, vest", "a fiddle", "plain comfortable"),
    R("dancer", "dancer", "bright skirt, bangles|{c} wrap top, sash, bangles|loose silk trousers, bolero|w:{c} short skirt, bodice|m:{c} open vest, sash", "a scarf", "plain comfortable rich"),
    R("street performer", "street performer", "jester coat|{c} striped vest, hat|patched harlequin outfit|bright mismatched coat", "juggling balls", "ragged rough"),
    R("hostess", "host", "silk shawl, jewellery|w:{c} evening gown|w:{c} silk dress, gloves|w:{c} corseted dress|m:{c} evening jacket, cravat|m:{c} waistcoat, open collar", "a fan", "rich comfortable"),
    R("madam", None, "fine robe, jewellery|{c} silk gown, fan|embroidered robe, long pipe|velvet {c} dress, long gloves", "a long pipe", "rich comfortable"),
    R("street vendor", "street vendor", "apron, flat cap|{c} vest, rolled sleeves|headscarf, tray strap|patched coat, fingerless gloves", "a food tray", "rough plain"),
    R("innkeeper", "innkeeper", "waistcoat, rolled sleeves|{c} apron, key ring|w:{c} dress, apron|m:{c} coat, cravat|cardigan, keys", "a key ring", "plain comfortable"),
    R("artist", "artist", "paint-smeared smock|{c} beret, smock|loose shirt, scarf|stained waistcoat, rolled sleeves", "a paintbrush", "plain rough"),
    R("navigator", "navigator", "weathered coat, compass|{c} coat, goggles on forehead|vest, rolled chart|jacket, spyglass at belt", "a rolled chart", "plain comfortable"),
    R("village elder", "village elder", "long robe, shawl|{c} woolly cloak|embroidered vest, cane|{c} coat", "a walking cane", "plain comfortable"),
    R("gambler", "gambler", "waistcoat, rolled sleeves|{c} suit, gold chain|sleeve garters, visor|silk shirt, ring", "playing cards", "comfortable rich"),
    R("bouncer", "bouncer", "tight dark shirt|{c} sleeveless jacket|leather vest, arms bare|heavy coat, collar up", None, "plain rough"),
    R("courier", "courier", "messenger bag, cap|{c} jacket, satchel|vest, goggles|long {c} coat, boots", "a sealed letter", "rough plain"),
    R("tattoo artist", "tattoo artist", "sleeveless top, ink-stained gloves|{c} apron, tattoo sleeves|vest, rolled sleeves|bandana, leather apron", "an ink bottle", "rough plain"),
    R("bath attendant", "bath attendant", "short yukata|{c} tunic, sash|loose robe, tied-back sleeves|towel on shoulder, apron", "a wooden bucket", "plain"),
    R("masseuse", "masseur", "loose tunic|{c} wrap top, trousers|sleeveless robe|short sleeves, apron", "a towel", "plain comfortable"),
    R("noble lady", None, "gown, lace gloves|{c} velvet gown|brocade dress, fan|high-collar silk dress, jewels", "a folded parasol", "noble rich"),
    R(None, "noble lord", "embroidered frock coat, cravat|{c} velvet coat|silk waistcoat, ruffled shirt|gold-buttoned coat, sash", "a gloved cane", "noble rich"),
    R("servant", "servant", "neat uniform, apron|{c} livery, gloves|w:{c} maid dress, white apron|m:{c} liveried coat", "a tray", "plain"),
    R("housekeeper", "butler", "dark formal dress, keys|{c} high-neck dress, apron|w:{c} dress, white collar|m:formal dark coat, white gloves|m:waistcoat, bow tie|m:grey formal jacket, pocket watch", "a silver tray", "comfortable"),
    R("beggar", "beggar", "rags|{c} blanket cloak|torn coat, bare feet|layers of rags, scarf", "a tin cup", "ragged"),
    R("washerwoman", None, "damp apron, rolled sleeves|{c} headscarf, wet dress|bare forearms, wash apron|skirt tied up, apron", "a laundry basket", "rough ragged"),
    R("rope-maker", "rope-maker", "leather apron|{c} work shirt, rope belt|vest, rope over shoulder|rolled sleeves, cap", "twisted rope", "rough plain"),
    R("net-mender", "net-mender", "worn smock, headscarf|{c} jumper, cap|oilskin apron|rolled trousers, shawl", "a net", "rough ragged"),
    R("midwife", None, "clean apron, headscarf|{c} dress, shawl|rolled sleeves, white apron|dark dress, satchel", "a cloth bundle", "plain"),
    R("undertaker", "undertaker", "black frock coat|{c} dark coat, top hat|black waistcoat, gloves|long black cloak", "a top hat", "comfortable"),
    R("auctioneer", "auctioneer", "striped waistcoat|{c} frock coat, cravat|bright jacket, gavel pocket|bowler hat, coat", "a small gavel", "comfortable rich"),
    R("moneylender", "moneylender", "dark coat, small spectacles|{c} brocade vest|fine coat, ring|sleeve garters, eyeshade", "a coin purse", "comfortable rich"),
    R("fence", "fence", "patched coat, many pockets|{c} long coat, scarf|waistcoat, flat cap|hooded cloak", "a small sack", "rough plain"),
    R("forger", "forger", "ink-stained cuffs, eyeshade|{c} vest, spectacles|sleeve garters, apron|dark coat, ink-stained fingers", "a quill", "plain rough"),
    R("chimney sweep", "chimney sweep", "soot-black overalls|{c} soot-smeared coat, cap|rags, brush|tight cap, sooty shirt", "a long brush", "ragged rough"),
    R("lamplighter", "lamplighter", "long coat, cap|{c} greatcoat, scarf|vest, pole at shoulder|cloak, lantern on belt", "a lighting pole", "plain rough"),
    R("mason", "mason", "dusty apron, cap|{c} work shirt, leather apron|vest, rolled sleeves|bandana, chalk-covered", "a chisel", "rough plain"),
    R("potter", "potter", "clay-smeared apron|{c} smock, headband|rolled sleeves, apron|vest, clay-stained", "a clay pot", "rough plain"),
    R("weaver", "weaver", "plain smock|{c} headscarf, shawl|vest, wool-flecked|w:{c} dress, apron|m:{c} shirt, braces", "a spindle", "rough plain"),
]
OLD_ROLES = {"madam", "village elder", "old sailor"}
ELDER_AGES = ["fifties", "sixties", "seventies"]

U_W_OLD = [  # (setting, outfit)
    ("beach swimwear", "a halter bikini"), ("beach swimwear", "a simple bikini"),
    ("beach swimwear", "a plain one-piece swimsuit"), ("beach swimwear", "a high-waisted bikini"),
    ("beach swimwear", "a sarong over a bikini"), ("hot spring", "a towel wrap, hair up"),
    ("bathhouse", "a short bathing cloth"), ("bathhouse", "a robe loosely tied"),
    ("lingerie", "lace lingerie"), ("lingerie", "a silk slip"), ("lingerie", "a corset and stockings"),
    ("lingerie", "a thin nightgown"), ("plain underwear", "bloomers and a chemise"),
    ("plain underwear", "plain cotton underwear"), ("sauna", "a towel wrap"),
    ("night room", "a long nightgown"), ("drying off", "a towel over a one-piece swimsuit"),
]
U_M_OLD = [
    ("beach swimwear", "swim trunks"), ("beach swimwear", "board shorts"), ("beach swimwear", "a sarong"),
    ("beach swimwear", "short swim trunks"), ("hot spring", "a towel wrap at the waist"),
    ("bathhouse", "a short bathing cloth"), ("bathhouse", "a robe loosely tied"),
    ("plain underwear", "boxers"), ("plain underwear", "briefs"), ("plain underwear", "a vest and drawers"),
    ("sauna", "a towel at the waist"), ("night room", "loose sleeping trousers"),
    ("drying off", "a towel over swim trunks"),
]

COLOURS = ["red", "black", "white", "ivory", "navy", "sky blue", "teal", "emerald green", "yellow", "orange", "coral",
           "pink", "hot pink", "lilac", "purple", "burgundy", "gold", "silver", "striped blue-and-white",
           "floral print", "polka-dot", "plaid", "brown", "olive green", "mustard", "turquoise", "grey", "cream"]
WORK_COL = ["brown", "grey", "navy", "olive green", "rust red", "faded blue", "cream", "black", "dark green", "mustard", "maroon", "white", "tan", "charcoal", "teal", "sand", "faded red", "slate blue"]
RICH_COL = ["crimson", "royal blue", "emerald green", "plum", "ivory", "burgundy", "gold-trimmed black", "silver-grey", "deep purple", "teal"]
LEVELS = {1: "minimal", 2: "skimpy", 3: "moderate", 4: "full coverage"}
U_W = [  # (setting, outfit template with {c} colour, coverage level)
    ("beach swimwear", "a tiny {c} string bikini", 1), ("beach swimwear", "a {c} micro bikini with thin ties", 1),
    ("lingerie", "a {c} lace thong and bralette", 1), ("lingerie", "a {c} G-string and small triangle top", 1),
    ("lingerie", "a short sheer {c} lace nightie", 1), ("lingerie", "a {c} sheer lace set, barely covering", 1),
    ("beach swimwear", "a tiny {c} thong bikini", 1), ("lingerie", "a {c} strappy lace harness set", 1),
    ("beach swimwear", "a {c} triangle bikini", 2), ("beach swimwear", "a {c} bandeau bikini", 2),
    ("lingerie", "a {c} lace bralette and briefs", 2), ("lingerie", "a short {c} silk slip", 2),
    ("lingerie", "a {c} lace camisole and tap shorts", 2), ("lingerie", "a {c} corset and stockings", 2),
    ("lingerie", "a {c} garter belt, stockings and lace set", 2), ("beach swimwear", "a {c} cut-out one-piece", 2),
    ("beach swimwear", "a {c} plunging one-piece", 2), ("hot spring", "a {c} towel wrap, hair up", 2),
    ("bathhouse", "a short {c} bathing cloth", 2), ("lingerie", "a {c} bodysuit with lace panels", 2),
    ("beach swimwear", "a {c} halter bikini", 3), ("beach swimwear", "a {c} high-waisted bikini", 3),
    ("beach swimwear", "a {c} skirted bikini", 3), ("beach swimwear", "a {c} bikini with shorts-style bottoms", 3),
    ("beach swimwear", "a {c} monokini", 3), ("beach swimwear", "a {c} sports bra and swim shorts", 3),
    ("beach swimwear", "a {c} sarong over a bikini", 3), ("bathhouse", "a {c} robe loosely tied", 3),
    ("lingerie", "a {c} satin chemise", 3), ("beach swimwear", "a {c} high-leg one-piece", 3),
    ("drying off", "a {c} towel over a one-piece swimsuit", 3), ("sauna", "a {c} towel wrap", 3),
    ("plain underwear", "plain {c} cotton underwear", 3), ("plain underwear", "snug {c} cotton shorts and a vest top", 3),
    ("beach swimwear", "a plain {c} one-piece swimsuit", 4), ("beach swimwear", "a {c} swim dress", 4),
    ("beach swimwear", "a {c} tankini with swim shorts", 4), ("night room", "a long {c} nightgown", 4),
    ("plain underwear", "bloomers and a {c} chemise", 4), ("plain underwear", "big {c} cotton briefs and a vest", 4),
    ("plain underwear", "{c} high-waisted full briefs and a plain bra", 4),
    ("beach swimwear", "a {c} retro one-piece with a short skirt", 4),
    ("beach swimwear", "a {c} long-sleeved rash vest and leggings", 4), ("night room", "a {c} flannel nightgown", 4),
    ("plain underwear", "{c} granny briefs and a camisole", 4), ("bathhouse", "a full {c} bathing gown", 4),
]
U_M = [
    ("beach swimwear", "tiny {c} swim briefs", 1), ("plain underwear", "a {c} thong", 1),
    ("bathhouse", "a {c} fundoshi loincloth", 1), ("beach swimwear", "{c} string-side swim briefs", 1),
    ("beach swimwear", "{c} tight swim briefs", 2), ("plain underwear", "snug {c} briefs", 2),
    ("beach swimwear", "a {c} sarong tied low", 2), ("bathhouse", "a short {c} bathing cloth", 2),
    ("hot spring", "a small {c} towel wrap at the waist", 2), ("plain underwear", "{c} low-rise briefs", 2),
    ("beach swimwear", "{c} square-cut swim trunks", 3), ("plain underwear", "{c} boxer briefs", 3),
    ("beach swimwear", "{c} board shorts", 3), ("sauna", "a {c} towel at the waist", 3),
    ("bathhouse", "a {c} robe loosely tied", 3), ("drying off", "a {c} towel over swim trunks", 3),
    ("beach swimwear", "{c} jammer swim shorts", 3), ("plain underwear", "plain {c} briefs", 3),
    ("beach swimwear", "long {c} board shorts", 4), ("plain underwear", "{c} boxers", 4),
    ("plain underwear", "a {c} vest and drawers", 4), ("night room", "loose {c} sleeping trousers", 4),
    ("plain underwear", "{c} long johns", 4), ("night room", "a {c} nightshirt and drawers", 4),
    ("beach swimwear", "a {c} rash vest and swim shorts", 4), ("plain underwear", "a {c} full union suit", 4),
]


class Deck:
    def __init__(self, items, rng):
        self.items, self.rng, self.q = list(items), rng, []

    def next(self, ok=None):
        rej = []
        for _ in range(300):
            if not self.q:
                self.q = self.items[:]
                self.rng.shuffle(self.q)
            v = self.q.pop()
            if ok is None or ok(v):
                self.q = rej + self.q
                return v
            rej.append(v)
        self.q = rej + self.q
        return self.items[0]


def article(w):
    return "an" if w[0] in "aeiou" else "a"


def mkdecks(rng, pool):
    d = {}
    for sx in "WM":
        d[sx] = dict(
            age=Deck(AGE_DECK, rng), skin=Deck(SKINS, rng), build=Deck(BUILDS, rng), face=Deck(FACES_PLAIN if FACE_MODE == "plain" else FACES, rng),
            hcol=Deck(HAIR_COLORS, rng), hsty=Deck(STYLES_W if sx == "W" else STYLES_M, rng),
            eyes=Deck(EYES, rng), mark=Deck(MARKS_N if pool == "naked" else MARKS_C + ["none"] * 5, rng),
            expr=Deck({"clothed": EXPR_C, "underwear": EXPR_U, "naked": EXPR_N}[pool], rng),
            pose=Deck({"clothed": POSE_C, "underwear": POSE_U, "naked": POSE_N}[pool], rng),
            fh=Deck(FACIAL, rng), bust=Deck(BUSTS, rng), shape=Deck(W_SHAPE_ALL, rng), det=Deck(M_DETAIL_ALL, rng),
            wl=Deck(["a", "b", "c", "d"], rng), col=Deck(COLOURS, rng))
    return d


def hair_phrase(sx, age, d):
    if age in ("sixties", "seventies"):
        col = d["hcol"].next(lambda c: c in OLD_COLORS)
    elif age == "fifties":
        col = d["hcol"].next(lambda c: c in OLD_COLORS + MID_COLORS)
    elif age == "forties":
        col = d["hcol"].next(lambda c: not c.startswith("dyed") and c != "two-tone" or True)
    else:
        col = d["hcol"].next()
    if age in ("fifties", "sixties", "seventies") and col.startswith("dyed"):
        col = "grey"
    if sx == "M":
        sty = d["hsty"].next(lambda s: not (s in ("bald", "balding") and age in ("twenties",)) )
    else:
        sty = d["hsty"].next()
    if sty == "bald":
        return "bald", "bald", "bald"
    if sty == "balding":
        return f"balding {col} hair", col, sty
    return f"{sty} {col} hair", col, sty


SULTRY_FRAC = 0
SULTRY = {
    "leaning on a wall, knee bent": ("leaning against a plain wall, one knee bent", None),
    "leaning back on a wall": ("leaning back against a plain wall, arms above the head", None),
    "lying on a bed, on one side": ("lying on a bed on one side, head propped on one hand", "reclining, three-quarter view"),
    "lying on a bed, on the back": ("lying on a bed on the back, one arm above the head", "reclining, three-quarter view"),
    "lying on a bed, on the stomach": ("lying on a bed on the stomach, chin on hands, looking back", "reclining, three-quarter view"),
    "propped on elbows on a bed": ("reclining on a bed, propped on the elbows", "reclining, three-quarter view"),
    "leaning back on a bed edge": ("sitting on the edge of a bed, leaning back on the hands", "seated, three-quarter view"),
    "hip cocked, hand in hair": ("standing with the hip cocked, one hand running through the hair", None),
    "arched back, looking back": ("looking back over the shoulder, back arched", None),
    "stretching on a bed": ("stretching on a bed, arms overhead", "reclining, three-quarter view"),
    "sitting on a chair, legs crossed": ("sitting on a chair, legs crossed, leaning back", "seated, three-quarter view"),
    "kneeling on a bed, hand in hair": ("kneeling on a bed, one hand in the hair", "three-quarter view, head to knees"),
}
SULTRY_EXPR = ["sultry half-lidded eyes", "seductive smile", "teasing smirk", "inviting look", "sultry stare"]


class Picker:
    def __init__(self, items, rng, counts, idx):
        self.items, self.rng, self.counts, self.idx = items, rng, counts, idx

    def next(self, ok=None):
        lab = lambda r: r[self.idx]
        m = min(self.counts.get(lab(r), 0) for r in self.items)
        c = [r for r in self.items if self.counts.get(lab(r), 0) == m]
        r = self.rng.choice(c)
        n = self.counts.get(lab(r), 0)
        self.counts[lab(r)] = n + 1
        vs = [v for v in r[2].split("|") if not v.startswith(("w:", "m:")) or v[0] == "wm"[self.idx]]
        vs = [v[2:] if v[:2] in ("w:", "m:") else v for v in vs]
        v = vs[(n + sum(map(ord, lab(r)))) % len(vs)]
        return (r[0], r[1], v, r[3], r[4])


def gen_rows(pool, n, start, seed, role_counts=None):
    rng = random.Random(seed)
    dk = mkdecks(rng, pool)
    sexes = []
    while len(sexes) < n:
        pair = ["W", "M"]
        rng.shuffle(pair)
        sexes += pair
    sexes = sexes[:n]
    if pool == "clothed":
        role_decks = {"W": Deck([r for r in ROLES if r[0]], rng), "M": Deck([r for r in ROLES if r[1]], rng)}
        if role_counts is not None:
            role_decks = {"W": Picker([r for r in ROLES if r[0]], rng, role_counts, 0),
                          "M": Picker([r for r in ROLES if r[1]], rng, role_counts, 1)}
        for sx in "WM" if role_counts is None else "":
            role_decks[sx].q = role_decks[sx].items[:]
            rng.shuffle(role_decks[sx].q)
    else:
        sets = {"W": U_W, "M": U_M} if pool == "underwear" else {"W": U_W_OLD, "M": U_M_OLD}
        set_decks = {sx: Deck(sets[sx], rng) for sx in "WM"}
    rows = []
    prev = None
    for i in range(n):
        sx = sexes[i]
        d = dk[sx]
        for attempt in range(40):
            row = build_row(pool, sx, d, rng, role_decks[sx] if pool == "clothed" else set_decks[sx], dk, i)
            if prev is None:
                break
            keys = ["sex", "age", "skin", "build", "face", "hair", "eyes", "marks", "expression", "pose", "role"]
            diff = sum(1 for k in keys if row[k] != prev[k])
            if diff >= 4:
                break
        rows.append(row)
        prev = row
    for j, r in enumerate(rows):
        r["id"] = f"{pool}_{start + j:03d}"
    return rows


def build_row(pool, sx, d, rng, rd, dk, i):
    woman = sx == "W"
    noun, pron = ("woman", "her") if woman else ("man", "his")
    role = outfit = prop = wl = setting = level = colour = None
    if pool == "clothed":
        rr = rd.next()
        role = rr[0] if woman else rr[1]
        outfit, prop = rr[2], rr[3]
        wl_key = rng.choice(rr[4])
        wl = wl_key
        colour = rng.choice(RICH_COL if wl_key in ("rich", "noble") else WORK_COL)
        outfit = f"{WEALTH[wl_key]} " + outfit.replace("{c}", colour)
        age = d["age"].next(lambda a: (role in OLD_ROLES and a in ELDER_AGES) or role not in OLD_ROLES)
    else:
        t = rd.next()
        age = d["age"].next()

        if pool == "underwear":
            for _ in range(30):
                if age in ("sixties", "seventies") and t[2] <= 2 and rng.random() < 0.75:
                    t = rd.next()
                else:
                    break
            level = LEVELS[t[2]]
            colour = d["col"].next()
            outfit = re.sub(r"\ba ([aeiouAEIOU])", r"an \1", t[1].format(c=colour))
        else:
            outfit = t[1]
        setting = t[0]
        role = f"{setting} ({outfit})"
    build = d["build"].next(lambda b: not (b == "small and slight" and age == "twenties"))
    skin = d["skin"].next()
    face = d["face"].next()
    eyes = d["eyes"].next()
    hair, hcol, hsty = hair_phrase(sx, age, d)
    mark = d["mark"].next()
    if pool == "clothed" and mark == "tattoo on the forearm":
        mark = "tattoo on the forearm, rolled sleeves"
    marks_txt = "" if mark == "none" else mark
    fh = ""
    if not woman:
        fh = d["fh"].next(lambda f: not (f == "long beard" and age in ("twenties", "thirties")))
    pose_key = d["pose"].next(lambda p: not (p == "tying up hair" and hsty in ("bald", "balding", "short cropped", "shaved sides", "afro", "tight curls")))
    if pool == "clothed" and pose_key == "holding an object of the trade" and prop is None:
        pose_key = "arms crossed"
    ptxt, frame = POSES[pose_key]
    if pose_key == "holding an object of the trade":
        ptxt = f"holding {prop}"
    if pool == "naked" and pose_key in NAKED_FRAMES:
        frame = NAKED_FRAMES[pose_key]
    if pose_key == "holding a lantern":
        pass
    if pose_key == "mid-laugh":
        expr = ""
    else:
        sug_ok = pool != "clothed" or (role in SUG_ROLES)
        expr = d["expr"].next(lambda e: sug_ok or e not in EXPR_SUG)
    if pool == "naked" and SULTRY_FRAC and rng.random() < SULTRY_FRAC:
        pose_key = rng.choice(list(SULTRY))
        ptxt, frame = SULTRY[pose_key]
        expr = rng.choice(SULTRY_EXPR)
        role = "adult entertainer, sultry pose"
    # body detail
    if woman:
        bust = d["bust"].next()
        if build in HEAVY:
            ok = {"soft belly", "wide hips", "pear-shaped", "apple-shaped", "hourglass", "stretch marks", "average hips"}
        elif build in THIN:
            ok = {"narrow hips", "straight-figured", "toned stomach", "average hips", "pear-shaped"}
        elif build in ("athletic", "muscular"):
            ok = {"toned stomach", "broad shoulders", "muscular thighs", "hourglass", "straight-figured", "average hips"}
        else:
            ok = set(W_SHAPE_ALL)
        shape = d["shape"].next(lambda s: s in ok)
        detail = f"{bust}, {shape}"
        bust_label = bust
    else:
        if build in HEAVY:
            ok = {"soft belly", "barrel chest", "hairy chest", "smooth chest", "heavy thighs", "broad shoulders"}
        elif build in THIN:
            ok = {"lean", "wiry", "smooth chest", "hairy chest", "thin legs"}
        else:
            ok = set(M_DETAIL_ALL) - {"soft belly"} if build in ("athletic", "muscular") else set(M_DETAIL_ALL)
        detail = d["det"].next(lambda s: s in ok)
        bust_label = detail
    show_body = pool != "clothed" or (woman and rng.random() < 0.18)
    if pool == "clothed" and not woman:
        show_body = False
    # prompt
    who = f"{article(build)} {build} {noun}"
    if pool == "clothed":
        who += f" {role}"
    ageclause = {"twenties": "mature adult face with fully developed adult features",
                 "thirties": "mature adult face with fully developed adult features",
                 "forties": "mature face with visible age lines",
                 "fifties": "aged face with wrinkles and age spots",
                 "sixties": "aged face with deep wrinkles, age spots and thinning skin",
                 "seventies": "very aged face with deep wrinkles, age spots and thin sagging skin"}[age]
    plainish = face in PLAIN_FACES or (wl in ("ragged", "rough") if wl else False) or build in HEAVY
    plainclause = ("plain ordinary unglamorous looks, bare face with no makeup, natural skin with pores, blemishes "
                   "and uneven tone") if plainish else ""
    if face in ("ugly crooked-nosed face", "big lumpy nose", "big nose", "pockmarked skin", "lopsided face",
                "heavy brow and flat face", "wide flat nose", "sagging jowls", "crooked teeth"):
        plainclause += ", unflattering rough-hewn features"
    parts = [f"{who} in {pron} {age}", f"{skin} skin", face, ageclause]
    if plainclause:
        parts.append(plainclause)
    if woman and (build in ("muscular", "athletic", "broad", "tall and broad") or face == "strong jaw"):
        parts.append("feminine facial features")
    if not woman and (build in HEAVY or build in ("muscular",) or face in ("strong jaw", "thick neck and heavy jaw")):
        parts.append("rugged masculine facial features")
    parts += [f"{eyes} eyes", hair]
    if fh:
        parts.append(fh)
    if marks_txt:
        parts.append(marks_txt)
    if show_body:
        parts.append(detail)
    if pool == "clothed":
        parts.append(f"wearing {outfit}")
    elif pool == "underwear":
        parts.append(f"wearing {outfit}")
        parts.append("natural adult body proportions, matte skin")
    else:
        parts.append("nude, bare skin")
        parts.append("natural adult body proportions, matte skin")
    parts.append(ptxt)
    if expr:
        parts.append(f"{expr} expression" if not expr.endswith(("smile", "look", "smirk", "half-lidded eyes")) else expr)
    parts.append("hand-drawn manga page look, flat matte cel colours, crosshatch shadow texture, "
                 "each hand with five distinct fingers" if pool == "naked" else
                 "hand-drawn manga page look, flat matte cel colours, crosshatch shadow texture, correct anatomy, "
                 "each hand with five distinct fingers")
    if pool == "naked":
        parts.append("nipples and vagina visible" if woman else "average sized penis")
    base = BASE.format(frame=frame or FRAME)
    prompt = f"{STYLE}, {base}, " + ", ".join(parts)
    # negative
    neg = ""
    add = []
    return dict(pool=pool, sex="woman" if woman else "man", **{"age": age}, skin=skin, build=build, face=face,
                hair=hair, eyes=eyes, level=level, colour=colour, bust_detail=(detail if (woman or pool != "clothed") else "n/a (clothed)"),
                bust=bust_label if woman else None, hcol=hcol, marks=marks_txt or "none", expression=expr,
                pose=pose_key, role=role, wealth=wl or "n/a", prompt=prompt, neg=neg)


BAN = re.compile(r"\b(girl|girls|boy|boys|young|youthful|teen|teens|teenager|schoolgirl|school|student|cute|petite|childlike|"
                 r"baby|loli|shota|chibi|child|kid|tail|tails|ear|ears|fur|furry|paw|paws|cat|cats|catlike|cat-like|dog|"
                 r"wolf|fox|bird|animal|horse|bull|goat|rabbit|bunny|fish|fishmonger|fisherman|whisker|whiskers|"
                 r"mutton|duck|crab|seal|bear|lion|tiger|hawk|eagle|snake|mouse|rat|pig|cow|sheep|ram|hen|crow|"
                 r"sex|aroused|arousal|bondage|bound|chained|blood|gore|sword|gun|knife|axe)\b", re.I)
AGE_RE = re.compile(r"in (her|his) (twenties|thirties|forties|fifties|sixties|seventies)")


def check(rows):
    prev = None
    seen = set()
    for r in rows:
        p = r["prompt"]
        assert p.startswith(STYLE + ", "), r["id"]
        assert AGE_RE.search(p), r["id"]
        m = BAN.search(p)
        assert not m, (r["id"], m.group(0), p)
        assert p not in seen
        seen.add(p)
        if prev:
            keys = ["sex", "age", "skin", "build", "face", "hair", "eyes", "marks", "expression", "pose", "role"]
            assert sum(1 for k in keys if r[k] != prev[k]) >= 3, (r["id"], "neighbour diff")
        prev = r
    old = sum(1 for r in rows if r["age"] in ("forties", "fifties", "sixties", "seventies"))
    return old / len(rows)


def counts(rows, key, order=None):
    c = collections.Counter(r[key] for r in rows if r[key])
    keys = order or sorted(c, key=lambda k: -c[k])
    return " | ".join(f"{k}: {c.get(k, 0)}" for k in keys)


def write(pool, rows, fname, note, allrows=None, fileno=1):
    allrows = allrows or rows
    cols = ["id", "pool", "sex", "age band", "skin", "build", "face", "hair", "eyes",
            "bust (women) or body detail (men)", "marks", "expression", "pose", "role or setting", "wealth look",
            "PROMPT"]
    L = [f"# NPC prompts — {pool} — file {fileno:02d} (ids {rows[0]['id']} to {rows[-1]['id']})", "",
         f"**Style block (start of every PROMPT):** `{STYLE}`", "",
         f"**Fixed base:** `{BASE.format(frame=FRAME)}`", "", "**Everything is in the one PROMPT box; there is no separate negative prompt.**", "", note, "",
         "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        det = r["bust_detail"]
        L.append("| " + " | ".join([r["id"], r["pool"], r["sex"], r["age"], r["skin"], r["build"], r["face"],
                                    r["hair"], r["eyes"], det, r["marks"], r["expression"], r["pose"], r["role"],
                                    r["wealth"], r["prompt"]]) + " |")
    L += ["", "## Coverage so far", ""]
    rows = allrows
    old = sum(1 for r in rows if r["age"] in ("forties", "fifties", "sixties", "seventies"))
    L.append(f"- **Total (all files so far):** {len(rows)}; forties or older: {old} ({100 * old // len(rows)}%)")
    L.append("- **Sex:** " + counts(rows, "sex"))
    L.append("- **Age band:** " + counts(rows, "age", AGES))
    L.append("- **Skin:** " + counts(rows, "skin", SKINS))
    L.append("- **Build:** " + counts(rows, "build", BUILDS))
    wm = [r for r in rows if r["bust"]]
    if wm and pool != "clothed":
        L.append("- **Bust (women):** " + counts(wm, "bust", BUSTS))
    elif wm:
        L.append("- **Bust (women, shown in the few clothed prompts that state it):** see table")
    L.append("- **Hair colour (bald excluded):** " + counts([r for r in rows if r["hcol"] != "bald"], "hcol", HAIR_COLORS)
             + f" | bald: {sum(1 for r in rows if r['hcol']=='bald')}")
    if pool == "clothed":
        L.append("- **Main clothing colour:** " + counts(rows, "colour"))
    if pool == "underwear":
        L.append("- **Coverage level:** " + counts(rows, "level", list(LEVELS.values())))
        L.append("- **Colour:** " + counts(rows, "colour", COLOURS))
    L.append("- **Face:** " + counts(rows, "face"))
    L.append("- **Role / setting:** " + counts(rows, "role"))
    L.append("- **Expression:** " + counts(rows, "expression"))
    open(OUT + fname, "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    notes = {
        "clothed": "Everyday people in working or street clothes. Marine uniforms are generic white with navy-blue accents (One Piece style), no logos.",
        "underwear": "Swimwear, towels, bath wraps, lingerie, plain underwear. Calm, neutral poses.",
        "naked": "Plain adult nudity, calm poses, plain pale background, character references only. Seated/kneeling poses use a three-quarter view.",
    }
    for pool, seed in (("clothed", 11), ("underwear", 22), ("naked", 33)):
        rows = gen_rows(pool, 100, 1, seed)
        frac = check(rows)
        wc = max(len(r["prompt"].split()) for r in rows)
        print(pool, "forties+", round(frac, 2), "max words", wc, "avg", sum(len(r["prompt"].split()) for r in rows) / 100)
        write(pool, rows, f"NPC_PROMPTS_{pool}_01.md", notes[pool])
