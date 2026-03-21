import requests
from pathlib import Path
import sys
import logging
import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

FILEPATH = Path(__file__).parent / "airbnb.html"
# Path(__file__) = l'emplacement du script
# .parent = le dossier qui contient le script
# / "airbnb.html" = on crée un chemin vers un fichier airbnb.html
# Résultat : C:\Users\MonPrénom\Desktop\Scraping Docstring\Part-3\airbnb-scraper\airbnb.html

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
# logging.basicConfig(level=logging.DEBUG)
# Ça permet d'afficher des messages de debug dans le terminal, plus besoin vu que fini

"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""

# Récupère le contenu de la page à l'URL donnée :
def fetch_content(url: str, from_disk: bool = False) -> str:

    # Si from_disk = False, alors on va sur internet pour récupérer le contenu
    # Donc ces 2 lignes ne servent à rien
    # Par contre si je télécharge je retélécharge pas, je lis le fichier
    if from_disk and FILEPATH.exists():
        return read_from_file()

    try:
        logger.debug(f"Récupération du contenu de l'URL : {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector("[data-testid='card-container']")
            html_content = page.content()
            browser.close()

        write_to_file(content=html_content)
        return html_content
    except PlaywrightTimeoutError as e:
        logger.error(f"Timeout : les annonces n'ont pas chargé : {e}")
        raise e
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du contenu : {e}")
        raise e
 

# Traite le contenu HTML pour extraire le prix moyen :
def get_average_price(html: str) -> int:
    prices = []

    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", {"data-testid": "card-container"})
    for div in divs:
        price_div = div.find("span", class_= "sjwpj0z") or div.find("span", class_="u174bpcy")
        if not price_div:
            logger.warning(f"Pas réussi à trouver le prix de la div {div}")
            continue
        price = re.sub(r"\D", "", price_div.text)
        if price.isdigit():
            logger.debug(f"Prix trouvé : {price}")
            prices.append(int(price))
        else:
            logger.warning(f"Le prix trouvé n'est pas un nombre : {price}")
    
    # J'ajoute ces 3 bloc pour que le script soit plus intéressant
    # Ca n'aide en rien pour le calcul du prix moyen
    print(f"Nombre d'annonces analysées : {len(prices)}")
    print(f"Prix le moins cher : {min(prices)}€")
    print(f"Prix le plus cher : {max(prices)}€")

    return round(sum(prices) / len(prices)) if prices else 0


# Écrit le contenu dans un fichier :
def write_to_file(content: str) -> bool:
    logger.debug(f"Écriture du contenu dans le fichier")
    with open(FILEPATH, "w", encoding="utf-8") as f:
        f.write(content)

    return FILEPATH.exists()
    # Vérifie si le fichier a été créé avec succès


# Lit le contenu du fichier :
def read_from_file() -> str:
    logger.debug(f"Lecture du contenu du fichier")
    with open(FILEPATH, "r", encoding="utf-8") as f:
        return f.read()


# Ce bloc s'exécute seulement si je lances ce fichier directement
if __name__ == "__main__":
    url = sys.argv[-1]
    content = fetch_content(url=url, from_disk=False) # En mettant false il ne lit pas le fichier même s'il existe, il va sur internet
    average_price = get_average_price(html=content,)
    print(50 * "-")
    print(f"Le prix moyen des annonces est de {average_price}€")