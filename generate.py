#!/usr/bin/env python
import json, requests, pandas as pd
from bs4 import BeautifulSoup

URL = "https://openlm.ai/chatbot-arena/"
html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

# volledige tabel pakken
table = soup.find("table")
df = pd.read_html(str(table))[0]
df.columns = ["Model", "Arena Elo", *df.columns[2:]]

top10 = (df.head(10)
           .loc[:, ["Model", "Arena Elo"]]
           .to_dict("records"))

with open("top-llms.json", "w") as f:
    json.dump(top10, f, indent=2)
