# Species guide (from the user; follow it whenever a person of that species appears, on any island)
Each species has a home island, but its people can live elsewhere. Wherever they appear, follow this guide, randomised within it, and make every individual look different. These are generalisations, not fixed templates.

HUMAN (about 95% of people): ordinary human build and features, with skin, hair and eye colour set by the island. Men: ordinary shape, Scale 2 to 3. Scale 4 or 5 is notably large.

AMAZON (women only, mostly Maenara): human women 6'2" to 6'8", bigger-boned, with broad shoulders. Strong and athletic, larger-breasted (not extreme), tanned, with braided hair, scars and ritual tattoos.

YETI (Hrimvar): a huge furred humanoid, 7' to 8'+, with thick white or grey-brown fur over the body and a bare pale face and hands. Heavy brow, broad flat nose, small dark eyes, big hands and feet, a deep rough voice. Lonely and grabby. Men: very large and thick in proportion, Scale 5 to 6.

OGRE (Thornmaw): a huge brutish humanoid, 8' to 9', with thick green-grey or grey-brown skin and small tusks rising from the lower jaw. Heavy brow, small eyes, massive arms and belly, scarred and tattooed with hunting marks, wearing hides. Men: very large and thick in proportion, Scale 5 to 6.

WOLF-KIN (Rimefair): human-like with pointed wolf ears on top of the head (no human ears), a bushy wolf tail, and a thick ruff of fur at the neck and down the spine. Fine fur on the forearms and shins, sharp canine teeth, amber eyes. Ears, tail and ruff match the hair colour (grey, brown, black, white or sandy). Direct, tactile, plain-spoken, loyal to the pack. Men: knotted (a canine-style knot), Scale 3 to 4.

CAT-KIN (Calico): human-like, slim and nimble, smaller on average, with cat ears on top of the head (no human ears) and a long slender cat tail. Large slit-pupilled eyes (green, gold or blue) and small fangs. The coat is patched in colour (calico, tabby or tortoiseshell patches) on the tail and ears, and as fine fur patches on the arms and shoulders, and the hair follows the same patches. Curious, flirty and quick. Men: barbed (a cat-style barbed shape), Scale 1 to 2.

STONE-FOLK (Stonewake): tall, broad, slow and patient, with mineral skin that looks like polished or rough stone (grey, slate, sandstone, granite or marble, sometimes with veins or crystals). Hair like moss, lichen or fine gravel, or none. Calm gem-like eyes, heavy hands, old and unhurried. Men: heavy and smooth-surfaced, large, Scale 5 to 6.

SCALEKIN (Saltglare): reptile-folk, humanoid, 5'6" to 6'6", with fine scales over the whole body (green, ochre, rust, grey or sand) and a thick tail. A ridge of small spines or a frill down the back of the head and neck. A snouted but human-shaped face with slit-pupilled golden eyes and a forked tongue, no hair. Heat-loving, often wrapped in cloth against the sun. Men: ridged and paired (a reptile-style shape), Scale 3 to 4.

FROST FOLK (Coldwatch, the northern seas): cold-adapted humans with pale blue-white skin with faint frost patterns (on the cheeks, temples and wrists), white or silver hair and pale ice-blue eyes. Men: ordinary shape, Scale 3 to 4.

EMBER FOLK (Emberfall, warm and volcanic islands): stone-like dark skin (charcoal, basalt or rust) with glowing orange lava veins and a faint ember light along the veins. Hair like ash or smouldering embers (black, grey, or glowing red-orange at the tips), amber or orange eyes, warm to the touch. Men: ordinary shape, large, Scale 4 to 6.

GHOST FOLK (sea events only, never on islands): eerie sea-people, pale, translucent and silvery, with trailing wet hair, hollow pale eyes and a faint glow. No anatomy notes and no scenes. (Saved for memory only; no studio prompts.)

## How the builder uses this
- species.py holds the appearance wording that is added to every prompt for that species, plus the men's anatomy wording used when the roster has no explicit size or shape note: wolf-kin "knotted penis", cat-kin "barbed penis", ember folk "larger than average penis", others as in species.py. Frost folk and humans stay "average size penis".
- A roster 'people' field that carries its own description after a colon (as Rimefair's wolf-kin do) wins over the default.
- An explicit size note in the roster ("larger than average", "huge", "knotted", "barbed") always wins over the species default.
