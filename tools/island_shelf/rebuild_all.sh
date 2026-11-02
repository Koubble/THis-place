set -e
b(){ python3 -I build_island.py $1 $2.json poses_$2 | tail -1; }
b hearthstone_merged.csv hearthstone
b tidewick_merged.csv tidewick
b vellumhold_merged.csv vellumhold
b dunmarrow_merged.csv dunmarrow
b coldwatch_clean.csv coldwatch
b /root/.claude/uploads/909bbc03-ce55-5daf-8b55-ea0f864e9bba/ed5c8497-Rimefair_NPC_Roster.csv rimefair
b gloamfjord_clean.csv gloamfjord
b steamhaven_clean.csv steamhaven
b hartfell_clean.csv hartfell
b hrimvar_clean.csv hrimvar
b aurelune_clean.csv aurelune
b blackharpoon_clean.csv blackharpoon
b wrackmoor_clean.csv wrackmoor
b /root/.claude/uploads/909bbc03-ce55-5daf-8b55-ea0f864e9bba/4f12b05b-Whitesail_NPC_Roster.csv whitesail
b veilhollow_clean.csv veilhollow
b brinewatch_clean.csv brinewatch
