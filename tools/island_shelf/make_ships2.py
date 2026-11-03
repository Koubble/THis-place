import csv, random, zlib, sys
M=["standing with his arms crossed","standing relaxed, one hand behind his head","standing square, hands on his hips","standing with a hand on his hip","standing with his weight on one leg","standing with his arms at his sides"]
W=["standing with one hand on her hip","standing with her hair over one shoulder","standing with her arms behind her back","standing with one hand at her collarbone","standing with her weight on one leg","standing with her hands clasped in front"]
HDR="id,name,where,role,sex,age,people,height,build,bust_or_scale,skin,hair,eyes,face,marks,clothed_outfit,clothed_expression,nude_pose,nude_expression,third_image_swim_or_underwear,prompts_needed".split(",")
CUPS=["A cup","B cup","B cup","C cup","C cup","D cup","D cup","E cup","F cup"]
HAIRC=["black","dark brown","chestnut","sandy","red","auburn","light brown","blond","dark blond","copper"]
HSTYLE_F=["in a thick braid","in a plait","in a bun","in loose waves","in a ponytail","pinned up","in a loose twist"]
HSTYLE_M=["cropped short","tousled","tied back","slicked back","short and wind-tangled","swept back"]
EYES=["blue","grey","green","hazel","brown","dark brown","grey-blue","pale blue","amber"]
def rng(n): return random.Random(zlib.crc32(n.encode()))
def human_hair(r,sex,age,style=None):
    if age>=60: c="white"
    elif age>=50: c=r.choice(["grey","iron-grey","white-streaked grey"])
    elif age>=42: c="greying "+r.choice(HAIRC)
    else: c=r.choice(HAIRC)
    if sex=="F": return f"{c} hair {style or r.choice(HSTYLE_F)}"
    s=f"{c} hair, {style or r.choice(HSTYLE_M)}"
    if r.random()<0.4: s+=" and a "+r.choice(["short beard","full beard","stubbled jaw","trimmed beard"])
    return s
def human_phys(r,sex,age,tall=None):
    if sex=="M":
        h=r.choice(["5'8\"","5'9\"","5'10\"","5'11\"","6'0\"","6'1\"","6'2\""]); b=r.choice(["stocky","lean and wiry","broad and strong","heavy-set","spare and tall","solid and thick","compact and tough"]); bs="Scale %d"%r.choice([2,3,3,4,4,5])
    else:
        h=r.choice(["5'2\"","5'3\"","5'4\"","5'5\"","5'6\"","5'7\"","5'8\""]); b=r.choice(["slim","sturdy","curvy","athletic","full-figured","soft and curvy","slim and curvy"]); bs=r.choice(CUPS)
    return h,b,bs
# species presets: (people, skin_choices, hair fn, eyes, extra marks, heights M, heights F, builds M, builds F)
def cat(r,sex):
    skin=r.choice(["olive skin with fine black and white fur patches","fair skin with fine calico fur patches on the arms and shoulders","tan skin with fine tabby fur patches on the arms and shoulders","warm skin with fine tortoiseshell fur patches"])
    hair=r.choice(["calico hair in patches of white, orange and black","tabby-striped brown and black hair","tortoiseshell hair in patches of orange, black and brown","orange and white patched hair, tousled","black and white patched hair, shaggy"])
    eyes=r.choice(["green, slit-pupilled","gold, slit-pupilled","blue, slit-pupilled","amber-green, slit-pupilled"])
    face=r.choice(["a mischievous, pointed face","a curious, bright-eyed face","a delicate face with whisker marks","a fine, sharp-featured face with small fangs"])
    mk=r.choice(["a long patched tail","a white-tipped tail","a bell on a ribbon at the neck","a notched ear","a patched tail with a kink at the tip"])
    h=r.choice(["5'4\"","5'6\"","5'7\"","5'8\""]) if sex=="M" else r.choice(["4'11\"","5'0\"","5'2\"","5'4\"","5'5\""])
    b=r.choice(["slim, lithe and wiry","lean and nimble"]) if sex=="M" else r.choice(["slim, lithe and supple","slender with a soft curve","small and nimble"])
    bs="Scale %d"%r.choice([1,1,2]) if sex=="M" else r.choice(["A cup","B cup","C cup","D cup"])
    return "cat-kin",h,b,bs,skin,hair,eyes,face,mk
def stone(r,sex):
    skin=r.choice(["rust-streaked sandstone skin","slate-blue stone skin with pale veins","grey polished granite skin","rough dark basalt-grey skin","warm sandstone skin"])
    hair=r.choice(["lichen in pale patches","moss growing in place of hair","fine gravel-grey hair","none, a smooth stone scalp"])
    eyes=r.choice(["calm green gem-like","amber gem-like","grey-violet gem-like","deep blue gem-like"])
    face=r.choice(["a broad, calm stone face","a heavy-browed, patient face","a smooth, ageless face with crystal flecks"])
    mk=r.choice(["fine cracks like lines of age","crystal flecks at the temples","moss at the shoulders","a vein of quartz across the cheek"])
    h=r.choice(["6'6\"","6'9\"","7'0\"","7'3\""]) if sex=="M" else r.choice(["6'2\"","6'4\"","6'7\""])
    b="broad, massive and slow-moving" if sex=="M" else "tall, broad and statuesque"
    bs="Scale 5" if sex=="M" else r.choice(["D cup","E cup","F cup"])
    return "stone-folk",h,b,bs,skin,hair,eyes,face,mk
def ogre(r,sex):
    skin=r.choice(["thick green-grey skin","mossy brown-grey skin","mottled green skin","dull grey-green skin","grey-brown hide-like skin"])
    hair=r.choice(["a coarse black mane","matted dark hair","a bone-beaded braid","a shaved scalp with a topknot","shaggy grey-brown hair"]) if sex=="M" else r.choice(["matted brown hair with bone beads","long coarse black hair in thick braids","shaggy grey-brown hair","a dark mane tied with hide cord"])
    eyes=r.choice(["pale green","dark red","amber","yellow","black"])
    face=r.choice(["a broad, flat nose and a jutting jaw with tusks","a scarred, tusked face","a heavy-browed face with two upward tusks","a wide face with small tusks and bright eyes"])
    mk=r.choice(["clan scars across the chest","a notched ear","bone piercings in the ears","tusk-carved bracelets","painted clan stripes"])
    h=r.choice(["8'4\"","8'6\"","8'8\"","9'0\"","9'3\""]) if sex=="M" else r.choice(["7'11\"","8'0\"","8'2\"","8'6\""])
    b=r.choice(["huge and heavily muscled","towering and barrel-chested","massive and thick-limbed"]) if sex=="M" else r.choice(["towering, broad and curvy","massive, powerful and voluptuous","huge, strong and full-figured"])
    bs="Scale %d"%r.choice([5,6]) if sex=="M" else r.choice(["E cup","F cup","G cup"])
    return "ogre",h,b,bs,skin,hair,eyes,face,mk
def amazon(r,sex):
    skin=r.choice(["bronze, sun-dark","golden-tanned","deep tan","weathered brown"])
    hair=r.choice(["chestnut hair in a warrior's braid","black hair in long braids","dark hair braided with bronze beads","sandy blonde braids","a long black braid wrapped round the head","auburn hair in tight braids"])
    eyes=r.choice(["amber","grey","green","hazel"])
    face=r.choice(["a strong-jawed, scarred face","a proud, high-cheekboned face","a sharp, tattooed face","a broad, freckled face"])
    mk=r.choice(["a scar across the ribs","a tattooed band round the upper arm","a spiral tattoo on the shoulder","a painted stripe across the cheeks","battle scars on the forearms"])
    return "amazon",r.choice(["6'2\"","6'3\"","6'4\"","6'6\"","6'7\""]),r.choice(["tall, strong and full-figured","statuesque, muscular and curvy","towering, broad and powerfully muscled"]),r.choice(["E cup","F cup","G cup"]),skin,hair,eyes,face,mk
def ember(r,sex):
    skin=r.choice(["rust-red stone-like skin with bright orange lava veins","charcoal stone-like skin with glowing orange veins","dark grey stone-like skin with amber veins","basalt-black skin with faint ember veins"])
    hair=r.choice(["black ash hair with ember glints","smouldering red-orange hair","grey ash hair, faintly glowing","ash-grey hair, glowing red-orange at the tips","black hair, tips glowing like coals"])
    eyes=r.choice(["amber","glowing amber","burnt orange","orange"])
    face=r.choice(["a broad, heavy-browed face with glowing cracks","a stern face lit by faint ember veins","a strong, soot-dark face with amber light under the skin"])
    mk=r.choice(["burnt-orange veins across the shoulders","a soot-black scar that glows faintly","glowing veins along the forearms"])
    h=r.choice(["5'10\"","6'0\"","6'1\"","6'3\""]) if sex=="M" else r.choice(["5'8\"","5'9\"","6'0\""])
    b=r.choice(["big and solid","broad-shouldered and heavy"]) if sex=="M" else r.choice(["tall and solid","broad-shouldered and shapely"])
    bs="Scale %d"%r.choice([4,5,6]) if sex=="M" else r.choice(["D cup","E cup","F cup"])
    return "ember folk",h,b,bs,skin,hair,eyes,face,mk
def scalekin(r,sex):
    skin=r.choice(["rust-red scaled","ochre scaled","sand-coloured scaled","green scaled"])
    return "scalekin",r.choice(["5'8\"","5'11\"","6'1\""]) if sex=="M" else r.choice(["5'9\"","6'0\"","6'2\""]),r.choice(["compact and tough","lean and wiry"]) if sex=="M" else "sturdy",("Scale 3" if sex=="M" else "D cup"),skin,"none, a ridge of small spines down the back of the head","slit-pupilled gold",r.choice(["a snouted, long-jawed face, patient","a snouted, watchful face"]),r.choice(["a frill dyed with ochre","a banded tail","a notched frill"])
def ghost(r,sex,age):
    hair=r.choice(["wet grey hair, trailing","wet dark hair, trailing","wet fair hair, trailing","pale hair in a wet braid","wet sandy hair, trailing"])
    h,b,bs=human_phys(r,sex,age)
    return "human ghost",h,b,bs,"pale and faintly translucent",hair,"hollow pale","","a faint pale glow"
SPEC={"cat":cat,"stone":stone,"ogre":ogre,"amazon":amazon,"ember":ember,"scale":scalekin}
def build(prefix,label,ships,out,idprefix):
    rows=[];i=0
    for sh in ships:
        name=sh["name"]; kind=sh.get("kind","human"); skinpool=sh.get("skin",["wind-reddened","fair and ruddy","weathered fair"])
        for k,c in enumerate(sh["crew"]):
            i+=1
            pname,sex,age,face,ce=c[0],c[1],c[2],c[3],c[4]
            kk=c[5] if len(c)>5 else kind
            marks=c[6] if len(c)>6 else None
            r=rng(pname+name)
            outfit=(sh["of"] if sex=="F" else sh["om"])
            outfit=outfit[k%len(outfit)] if isinstance(outfit,list) else outfit
            if kk=="human":
                h,b,bs=human_phys(r,sex,age)
                ppl="human"; skin=r.choice(skinpool); hair=human_hair(r,sex,age); eyes=r.choice(EYES)
                mk=marks or r.choice(["a red nose","frost on the lashes","wind-chapped cheeks","a sunburnt nose","weathered hands"])
            elif kk=="ghost":
                ppl,h,b,bs,skin,hair,eyes,_,mk=ghost(r,sex,age)
                mk=marks or mk
            else:
                ppl,h,b,bs,skin,hair,eyes,fc,mk0=SPEC[kk](r,sex)
                mk=marks or mk0
                if not face: face=fc
            tone=ce.split(",")[0].split()[0]
            ne=f"{tone}, unembarrassed"
            pose=(M if sex=="M" else W)[(i+k)%6]
            third=""
            if sh.get("third"): third=sh["third"][0 if sex=="M" else 1]
            rows.append([f"{idprefix}-{i}",pname,f"{idprefix} {label} {name}",sh["role"] if isinstance(sh["role"],str) else sh["role"][k],sex,age,ppl,h,b,bs,skin,hair,eyes,face,mk,outfit,ce,pose,ne,third,"2: clothed, nude"])
    with open(out,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(HDR);w.writerows(rows)
    return rows
