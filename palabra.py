import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date
import re

BASE_URL = "https://dle.rae.es/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(BASE_URL, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# Cerca un link contenente "Palabra del día"
link = None
for a in soup.find_all("a", href=True):
    text = a.get_text(" ", strip=True)
    if "Palabra del día" in text:
        link = a["href"]
        break

if link is None:
    raise Exception("Palabra del día non trovata.")

if not link.startswith("http"):
    if not link.startswith("/"):
        link = "/" + link
    palabra_url = "https://dle.rae.es" + link
else:
    palabra_url = link

r = requests.get(palabra_url, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# Titolo
h1 = soup.find("h1")
palabra = h1.get_text(strip=True) if h1 else "Sconosciuta"

# Prima definizione disponibile
definizione = ""

for d in soup.find_all(["p", "div"]):
    txt = d.get_text(" ", strip=True)
    if re.match(r"^\d+\.", txt):
        definizione = txt
        break

if not definizione:
    definizione = "Definizione non trovata."

Path("palabras").mkdir(exist_ok=True)

oggi = date.today().isoformat()

contenuto = f"""# {oggi}

## Palabra

{palabra}

## Definición

{definizione}

## Fuente

{palabra_url}
"""

with open(f"palabras/{oggi}.md", "w", encoding="utf-8") as f:
    f.write(contenuto)

print("Creato:", f"palabras/{oggi}.md")
