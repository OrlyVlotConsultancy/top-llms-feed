#!/usr/bin/env python
import json, requests, pandas as pd
from bs4 import BeautifulSoup

URL = "https://openlm.ai/chatbot-arena/"
html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

# alle tabellen in de pagina
tables = pd.read_html(str(soup))

df = tables[1]                      # tweede tabel = Full Leaderboard
df.columns = ["Model", "Arena Elo", *df.columns[2:]]

top10 = (df.head(10)
           .loc[:, ["Model", "Arena Elo"]]
           .to_dict("records"))

with open("top-llms.json", "w") as f:
    json.dump(top10, f, indent=2)
