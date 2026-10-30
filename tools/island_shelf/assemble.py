import json, sys
islands = {}
for spec in sys.argv[2:]:
    key, name, path = spec.split("|")
    islands[key] = {"name": name, "people": json.load(open(path))}
html = open("tpl_island.html").read().replace("__DATA__", json.dumps(islands, separators=(",", ":")))
open(sys.argv[1], "w").write(html)
print({k: len(v["people"]) for k, v in islands.items()}, round(len(html) / 1e6, 2), "MB")
