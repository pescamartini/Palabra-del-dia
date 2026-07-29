from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date

URL = "https://dle.rae.es/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    )

    page.goto(URL, wait_until="networkidle")

    html = page.content()

    browser.close()

soup = BeautifulSoup(html, "html.parser")

# Cerca la sezione della parola del giorno
testo = soup.get_text(" ", strip=True)

parola = None

if "Palabra del día" in testo:
    parti = testo.split("Palabra del día")
    if len(parti) > 1:
        parola = parti[1].split()[0]

if not parola:
    raise Exception("Non trovata la Palabra del día")

Path("palabras").mkdir(exist_ok=True)

oggi = date.today().isoformat()

contenuto = f"""# {oggi}

## Palabra

{parola}

## Fuente

{URL}
"""

with open(f"palabras/{oggi}.md", "w", encoding="utf-8") as f:
    f.write(contenuto)

print("Creato file:", oggi)
