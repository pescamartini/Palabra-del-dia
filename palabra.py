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

# Estrae la parola del giorno dalla classe ufficiale RAE
elemento = soup.select_one(".c-word-day__word")

if not elemento:
    raise Exception("Palabra del día non trovata")

palabra = elemento.get_text(strip=True)

# Recupera il link della voce
link_element = soup.select_one(".c-word-day__link")

if link_element and link_element.get("href"):
    fuente = "https://dle.rae.es" + link_element["href"]
else:
    fuente = URL


Path("palabras").mkdir(exist_ok=True)

oggi = date.today().isoformat()

contenuto = f"""# {oggi}

## Palabra

{palabra}

## Fuente

{fuente}
"""

with open(f"palabras/{oggi}.md", "w", encoding="utf-8") as f:
    f.write(contenuto)

print(f"Creato: palabras/{oggi}.md")
