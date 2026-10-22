# (woman label, man label, outfit variants, prop, wealth options, weight women, weight men)
def R2(w, m, o, p, wl="plain comfortable", ww=1.0, wm=1.0):
    return (w, m, o, p or None, wl.split(), ww, wm)

ROLES2 = [
 # officials: the world asks for these most; women especially
 R2("customs officer","customs officer","navy-blue coat, brass buttons, peaked cap|{c} official coat, ink-stained cuffs|w:{c} jacket, long skirt, stiff collar|m:{c} waistcoat, armband, cap|grey official coat, stamp pouch","a stamped manifest","plain comfortable",2.5,2),
 R2("tax collector","tax collector","dark coat, spectacles chain|{c} frock coat, leather satchel|w:{c} high-collar dress, ledger strap|m:grey suit, cravat|armband, ink-stained gloves","a heavy ledger","plain comfortable",2.5,2),
 R2("notary","notary","black gown, stiff collar|{c} waistcoat, sleeve guards|w:{c} formal dress, brooch|m:{c} frock coat, signet ring|pince-nez, dark robe","a sealed document","comfortable rich",2.5,2),
 R2("town clerk","town clerk","sleeve garters, waistcoat|{c} cardigan, ink-stained fingers|w:{c} blouse, long skirt|m:{c} jacket, round collar|eyeshade, apron","a quill","plain comfortable",2.5,2),
 R2("port official","port official","{c} coat with gold braid|buttoned coat, peaked cap|w:{c} tailored jacket, pencil skirt|m:{c} frock coat, sash of office|armband, clipboard pocket","a clipboard","comfortable rich",2,1.5),
 # scholars and books: women especially
 R2("scholar","scholar","long robe, scarf|{c} academic gown|round spectacles, tweed coat|w:{c} high-collar dress|m:waistcoat, loose shirt","a heavy book","plain comfortable",2.5,1.5),
 R2("teacher","teacher","{c} cardigan, spectacles|chalk-dusted waistcoat|w:{c} blouse, long skirt|m:{c} jacket, bow tie|shawl, reading glasses","a slate and chalk","plain comfortable",2.5,1.5),
 R2("bookseller","bookseller","long coat, scarf|{c} cardigan|waistcoat, half-moon spectacles|sleeve garters, apron","a stack of books","plain comfortable",2.5,1.5),
 R2("librarian","librarian","long vest, shirt, spectacles chain|{c} cardigan, spectacles|shawl, high collar|w:{c} blouse, long skirt|m:waistcoat, bow tie","a book","plain comfortable",2.5,1.5),
 R2("scribe","scribe","ink-stained robe|{c} smock, sleeve guards|eyeshade, apron|w:{c} dress, ink-stained cuffs|m:{c} tunic, belt","a scroll and quill","plain rough",2.5,1.5),
 # performers: male dancers especially
 R2("fiddle player","fiddle player","loose shirt, sash|{c} waistcoat, rolled sleeves|embroidered jacket|bright {c} scarf, vest","a fiddle","plain comfortable",1.5,1.5),
 R2("lute player","lute player","{c} doublet, loose sleeves|embroidered jacket|cloak, wide hat|w:{c} bodice, wide sleeves|m:{c} tunic, belt","a lute","plain comfortable",1.5,1.5),
 R2("flute player","flute player","loose shirt, waistcoat|{c} tunic, headband|patched cloak|w:{c} dress, shawl|m:{c} vest, bare forearms","a flute","plain rough",1.5,1.5),
 R2("street singer","street singer","patched coat, scarf|{c} shawl, bright headscarf|bright mismatched coat|w:{c} dress, apron|m:{c} waistcoat, cap","a songbook","ragged rough plain",1.5,1.5),
 R2("storyteller","storyteller","{c} cloak, many pockets|patched robe, rope belt|embroidered waistcoat|w:{c} shawl, long skirt|m:{c} coat, scarf","a lantern","plain comfortable",1.5,1.5),
 R2("dancer","dancer","bright skirt, bangles|{c} wrap top, sash, bangles|loose silk trousers, bolero|w:{c} short skirt, bodice|m:{c} open vest, sash, bare chest","a scarf","plain comfortable rich",1.5,3),
 # bath, massage, hair, laundry: men especially
 R2("bath attendant","bath attendant","short yukata|{c} tunic, sash|loose robe, tied-back sleeves|towel on shoulder, apron|{c} wrap, bare arms","a wooden bucket","plain",1.5,3),
 R2("masseuse","masseur","loose tunic|{c} wrap top, trousers|sleeveless robe|short sleeves, apron|{c} vest, bare arms","a towel","plain comfortable",1.5,3),
 R2("hairdresser","hairdresser","{c} apron, comb in pocket|smock, scissors belt|waistcoat, rolled sleeves|w:{c} dress, apron|m:{c} shirt, apron","a comb","plain comfortable",2,2),
 R2("barber","barber","striped apron, rolled sleeves|{c} waistcoat, apron|vest, bare forearms|w:{c} shirt, long apron|m:{c} shirt, braces","a comb and scissors","plain comfortable",2,2.5),
 R2("laundress","launderer","damp apron, rolled sleeves|{c} headscarf, wet dress|bare forearms, wash apron|skirt tied up, apron|m:{c} shirt, wet apron","a laundry basket","rough ragged plain",2,2.5),
 # cloth and craft
 R2("tailor","tailor","waistcoat, measuring tape|{c} jacket, pins on cuff|apron with pockets|w:{c} dress, tape around neck|m:{c} shirt, braces","a cloth roll","plain comfortable",1.5,1.5),
 R2("dyer","dyer","{c} dye-stained apron|stained forearms, rolled sleeves|headscarf, wet apron|w:{c} dress, stained apron|m:{c} shirt, stained apron","a cloth bolt","rough plain",1.5,1.5),
 R2("weaver","weaver","plain smock|{c} headscarf, shawl|vest, wool-flecked|w:{c} dress, apron|m:{c} shirt, braces","a spindle","rough plain",1.5,1.5),
 R2("leatherworker","leatherworker","leather apron, rolled sleeves|{c} work shirt, leather apron|vest, bare forearms|bandana, tool pouch","a leather strap","rough plain",1.5,1.5),
 R2("potter","potter","clay-smeared apron|{c} smock, headband|rolled sleeves, apron|vest, clay-stained","a clay pot","rough plain",1.5,1.5),
 R2("glassblower","glassblower","scorched apron, rolled sleeves|{c} sleeveless shirt, apron|leather gloves, vest|bandana, soot-smeared apron","a glass blowpipe","rough plain",1.5,1.5),
 R2("sailmaker","sailmaker","canvas apron, rolled sleeves|{c} work shirt, thimble belt|vest, needle roll|w:{c} headscarf, canvas apron|m:{c} cap, canvas apron","a needle and canvas","rough plain",2,1.5),
 # healers
 R2("apothecary","apothecary","white apron, rolled sleeves|{c} coat, rows of small pouches|waistcoat, spectacles|w:{c} dress, apron|m:{c} jacket, apron","a mortar and pestle","plain comfortable",2,1.5),
 R2("herbalist","herbalist","shawl, pouch belt|{c} apron, herb pouches|hooded {c} cloak|w:{c} skirt, vest|m:{c} coat, satchel","a herb bundle","rough plain",2,1.5),
 R2("midwife","midwife","clean apron, headscarf|{c} dress, shawl|rolled sleeves, white apron|dark dress, satchel","a cloth bundle","plain",2.5,1),
 R2("bonesetter","bonesetter","rolled sleeves, apron|{c} work shirt, strong forearms|vest, bandage roll at belt|w:{c} dress, apron|m:{c} coat, satchel","rolls of bandage","plain rough",2,2),
 R2("healer","healer","plain robe, shoulder bag|{c} tunic, bandage belt|hooded cloak, satchel|w:{c} shawl, long skirt|m:{c} waistcoat, rolled sleeves","a healer's bag","plain",2,2),
 # farm and food: male bakers and cooks especially
 R2("farmer","farmer","straw hat, work clothes|{c} overalls|patched shirt, braces|w:{c} headscarf, apron dress|m:rolled trousers, vest","a hoe","rough ragged",1.5,1.5),
 R2("grocer","grocer","{c} apron, rolled sleeves|waistcoat, sleeve garters|w:{c} dress, apron|m:{c} shirt, braces, apron|flat cap, long apron","a crate of vegetables","plain comfortable",1.5,1.5),
 R2("fruit seller","fruit seller","{c} headscarf, apron|straw hat, rolled sleeves|patched vest|w:{c} dress, apron|m:{c} shirt, apron","a basket of fruit","rough plain",1.5,1.5),
 R2("brewer","brewer","leather apron, shirt|{c} work shirt, rolled sleeves|heavy {c} coat, boots|wet canvas apron|{c} waistcoat, cap","a barrel stave","rough plain",1.5,1.5),
 R2("butcher","butcher","stained apron, rolled sleeves|{c} work shirt, long apron|vest, strong forearms|w:{c} headscarf, long apron|m:{c} cap, striped apron","a wrapped parcel","rough plain",1.5,2),
 R2("seafood seller","seafood seller","wet apron, boots|{c} oilskin apron|striped shirt, rubber apron|{c} headscarf, long apron","a covered basket","rough ragged",2,1.5),
 R2("cook","cook","stained apron, cap|{c} chef coat, neckerchief|rolled sleeves, towel at belt|{c} bandana, apron|tall chef hat, white coat","a ladle","plain rough",1.5,3),
 R2("baker","baker","flour-dusted apron|{c} cap, floury shirt|rolled sleeves, linen apron|w:{c} headscarf, apron dress|m:vest, floury forearms","a bread paddle","plain comfortable",1,3),
 R2("barmaid","waiter","tavern apron and blouse|{c} vest, bow tie|w:laced {c} bodice, short skirt|w:off-shoulder blouse, apron|m:{c} shirt, long apron|m:waistcoat, rolled sleeves","a tray","plain comfortable",2,1.5),
 # the shady: women especially
 R2("bouncer","bouncer","tight dark shirt|{c} sleeveless jacket|leather vest, arms bare|heavy coat, collar up","","plain rough",2.5,1.5),
 R2("bodyguard","bodyguard","dark suit, no tie|{c} long coat, gloves|waistcoat, folded sleeves|w:{c} fitted jacket, trousers|m:{c} tight jacket, collar up","","comfortable rich",2.5,1.5),
 R2("thief","thief","hooded cloak|{c} dark coat, scarf over chin|dark vest, many pockets|w:{c} cloak, fitted trousers|m:{c} jacket, flat cap","a stolen purse","ragged rough",2.5,1.5),
 R2("fence","fence","patched coat, many pockets|{c} long coat, scarf|waistcoat, flat cap|hooded cloak","a small sack","rough plain",2,1.5),
 R2("smuggler","smuggler","hooded cloak, satchel|{c} long coat, scarf|dark vest, hidden pockets|wide hat, travel cloak","a small crate","rough plain",2.5,1.5),
 R2("pawnbroker","pawnbroker","dark coat, small spectacles|{c} brocade vest, rings|sleeve garters, loupe|w:{c} dress, cameo brooch|m:{c} jacket, watch chain","a pawn ticket","plain comfortable",2.5,1.5),
 R2("gambler","gambler","waistcoat, rolled sleeves|{c} suit, gold chain|sleeve garters, visor|silk shirt, rings","playing cards","comfortable rich",2.5,1.5),
 R2("debt collector","debt collector","dark coat, hat low|{c} frock coat, ledger under arm|waistcoat, stern collar|w:{c} dark dress, gloves|m:{c} overcoat, bowler hat","a ledger","plain comfortable",2.5,1.5),
 # gentry and servants
 R2("noble lady","noble lord","w:ornate gown, lace gloves|w:{c} velvet gown|w:brocade dress, fan|m:embroidered frock coat, cravat|m:silk waistcoat, ruffled shirt|m:gold-buttoned coat, sash","a folded fan","noble rich",2,2),
 R2("maid","footman","w:{c} maid dress, white apron, cap|w:black uniform, frilled apron|m:{c} liveried coat, white gloves|m:striped waistcoat, bow tie","a silver tray","plain comfortable",3,1),
 R2("housekeeper","butler","w:dark formal dress, keys at belt|w:{c} high-neck dress, apron|m:formal dark coat, white gloves|m:waistcoat, bow tie|m:grey formal jacket, pocket watch","a ring of keys","comfortable",2,2.5),
 R2("wealthy merchant","wealthy merchant","{c} velvet coat, rings|silk waistcoat, gold chain|w:{c} fine gown, pearls|m:{c} frock coat, cravat","a coin purse","rich",1.5,1.5),
 # the poor end
 R2("vagrant","vagrant","layers of rags, scarf|{c} blanket cloak|torn coat, bare feet|rags, rope belt","a bundle","ragged",1.5,1.5),
 R2("scavenger","scavenger","patched apron, gloves|{c} torn coat, sack on back|rags, wrapped hands|oilskin scraps, rope belt","a sack of salvage","ragged",1.5,1.5),
 R2("beggar","beggar","rags|{c} blanket cloak|torn coat, bare feet|layers of rags, scarf","a tin cup","ragged",1.5,1.5),
 R2("hermit","hermit","long ragged robe|{c} patched cloak, rope belt|tattered coat, long hair|hooded {c} cloak","a walking staff","ragged rough",1.5,1.5),
 R2("rag picker","rag picker","torn shawl, sack|patched apron, headscarf|rags, string belt|oversized {c} coat, rags","a rag sack","ragged",1.5,1.5),
 # boat work: women especially
 R2("shipwright","shipwright","tool belt, work shirt|{c} work jacket, cap|canvas apron, rolled sleeves|vest, sawdust-dusted|bandana, tool pouch","a hand saw","rough plain",2.5,1.5),
 R2("rigger","rigger","sleeveless vest, rope belt|{c} work shirt, harness|canvas trousers, gloves|bandana, rope over shoulder","a coil of rope","rough plain",2.5,1.5),
 R2("ferrywoman","ferryman","wide hat, plain shirt|{c} oilskin, cap|rolled trousers, vest|woolly {c} scarf, jacket","a long oar","rough plain",2.5,1.5),
 R2("lighthouse keeper","lighthouse keeper","heavy {c} coat, wool cap|oilskin, scarf|woollen jumper, boots|w:{c} shawl, long coat|m:{c} chunky knit jumper","a brass lantern","rough plain",2,1.5),
 R2("harbour officer","harbour officer","blue coat, brass buttons, cap|{c} jacket, armband, whistle|w:{c} fitted coat, skirt|m:{c} coat, peaked cap|buttoned coat, gold braid","a clipboard","comfortable",3,1.5),
]

# sea faces (~100): women who read as sailors/pirates/privateers/mercenaries/smugglers, wardens, yacht people, bounty hunters, odd vessels
SEA = [
 R2("pirate","pirate","open coat, eyepatch, sash|{c} captain-style coat, sash|ragged striped shirt, bandana|tricorn hat, leather vest|w:{c} long coat, sash, boots|m:bandana, gold hoop earrings, open vest","a mug","rough ragged",3.5,1.5),
 R2("privateer captain","privateer captain","{c} long coat, gold braid, sash|tricorn hat, brass buttons|w:{c} coat over waistcoat, boots|m:{c} frock coat, cravat|eyepatch, sash","a spyglass","comfortable rich",3.5,1.5),
 R2("mercenary","mercenary","studded leather vest, scarf|{c} long coat, wide belt|sleeveless jerkin, wrapped forearms|w:{c} coat, scarred forearms|m:{c} coat, scar across brow","a bedroll","rough plain",3.5,1.5),
 R2("sea smuggler","sea smuggler","hooded oilskin|{c} coat, sash, satchel|dark vest, hidden pockets|eyepatch, scarf","a small crate","rough plain",3.5,1.5),
 R2("sailor","sailor","striped shirt, sash|{c} bandana, open vest|wide-collar {c} shirt|knit {c} cap, pea jacket","a rope coil","rough plain",3.5,1.5),
 R2("Warden officer","Warden officer","blue coat, gold buttons, shoulder tabs, cap, no logos|blue coat open, white shirt, gold buttons, shoulder tabs, no logos|blue peaked cap, gold braid, shoulder tabs, no logos","a clipboard","comfortable rich",2.5,2.5),
 R2("Warden rank-and-file","Warden rank-and-file","blue coat, gold buttons, shoulder tabs, no logos|blue cap, white shirt, shoulder tabs, no logos|blue jacket, rolled sleeves, gold buttons, no logos","a folded flag","plain",2.5,2.5),
 R2("yacht host","yacht host","w:{c} evening gown, jewellery|w:{c} silk dress, gloves|m:{c} evening jacket, cravat|m:{c} waistcoat, open collar|white linen suit, sash","a champagne glass","rich",2.5,2.5),
 R2("yacht guest","yacht guest","w:{c} sundress, wide hat, sunglasses|w:{c} silk wrap, jewellery|m:white linen shirt, {c} trousers|m:{c} blazer, cravat","a drink","rich comfortable",2.5,2.5),
 R2("yacht captain","yacht captain","white captain's coat, gold braid, white cap|white uniform, gold buttons, white cap|white jacket, {c} sash, white cap","a spyglass","comfortable rich",2,2.5),
 R2("yacht servant","yacht servant","w:black dress, white apron, cap|w:{c} uniform, white gloves|m:white jacket, black tie|m:{c} livery, white gloves","a silver tray","plain comfortable",2.5,2.5),
 R2("bounty hunter","bounty hunter","long coat, wide hat|{c} poncho, scarf|dusty long coat, goggles|hood, leather vest","a wanted poster","rough plain",2.5,2.5),
 R2("ghostly sailor","ghostly sailor","faded tattered coat, pale hollow face|{c} rotted sash, torn shirt|salt-stained pea jacket, bare feet|wet ragged sailor shirt","a rusted lantern","ragged",1,1),
 R2("castaway","castaway","rags of a sailor's shirt|{c} torn coat, sun-burned skin|palm-leaf wrap, bare feet|scraps of canvas, rope belt","a driftwood staff","ragged",1,1),
 R2("ringmaster","ringmaster","red coat, gold braid, top hat|{c} striped coat, bow tie|w:{c} tailcoat jacket, short skirt, top hat|m:{c} tailored coat, top hat","a cane","comfortable rich",1,1),
 R2("mission-ship nun","mission-ship nun","simple habit, wooden cross|{c} habit, white wimple|grey habit, rolled sleeves|hooded {c} habit","a prayer book","plain",1,1),
]
