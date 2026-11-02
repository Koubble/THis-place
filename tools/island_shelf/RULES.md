# Island shelf rules (from the user)
- Two prompts per person (clothed, studio/nude), plus a third swimwear/underwear prompt when the roster has one.
- Core appearance block is identical in every prompt for a person (name, age, people incl. "East-Asian looking" etc., height, build, bust cup for women only, skin, face, eyes, hair, marks). Men's Scale never appears.
- Prompt age is never below 22 (roster ages 19 to 21 are written as 22 in prompts only).
- Framing: "three-quarter length shot framed from the head down to the knees, knees included, hips and thighs fully in view" (never "full body").
- Poses are body-only: no objects that need anything beyond the plain background. Vary them (shy, bold, relaxed). Nude poses must not hide the anatomy (no crossed/wrapped arms on women, no hands clasped in front on men).
- Studio (nude) prompts end, after the background, with: women "nipples and vagina visible"; men "average size penis", unless the roster note states a size ("larger than average" -> "larger than average penis", "huge" -> "huge penis").
- UI label for nude is "Studio". Nude and swimwear prompts are shown by default, with tick boxes to hide them.
- Build: python3 -I build_island.py ROSTER.csv OUT.json poses_<island>; then assemble.py with "key|Name|file.json" per island.
- Relatives of player characters: the roster note names the character they resemble (e.g. "Duncan's colouring"). Prompts never contain those names. Keep the shared features themselves (colouring, brows, grin, glasses, beauty spot, cheekbones) as plain description. Corrected rows live in Relatives_Fixed_Rows.csv; merge_fixed.py swaps them into the island rosters (with names stripped) before build_island.py runs.
