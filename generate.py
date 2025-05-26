#!/usr/bin/env python
import json, requests, pandas as pd
from collections import defaultdict

URL = "https://storage.googleapis.com/arena_external_data/public/clean_battle_20240814_public.json"
battles = pd.read_json(URL)
battles = battles[battles["anony"]]
battles = battles[battles["dedup_tag"].apply(lambda x: x.get("sampled", False))]

def elo(df, K=4):
    r = defaultdict(lambda: 1000)
    for _, a, b, w in df[['model_a','model_b','winner']].itertuples():
        ra, rb = r[a], r[b]
        ea = 1/(1+10**((rb-ra)/400))
        sa = 1 if w=="model_a" else 0 if w=="model_b" else .5
        r[a] += K*(sa-ea);  r[b] += K*((1-sa)-(1-ea))
    return sorted(r.items(), key=lambda x: x[1], reverse=True)[:10]

top10 = [{"model": m, "elo": round(s,2)} for m,s in elo(battles)]
with open("top-llms.json","w") as f:
    json.dump(top10, f, indent=2)
