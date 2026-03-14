import requests
import random
from bs4 import BeautifulSoup

# Liste des proxies disponibles (adresse IP + port)
proxies = [
    "117.250.3.58:8080",
]

def get_random_proxy(proxies):
    """ Sélectionne un proxy aléatoire de la liste """
    random_proxy = random.choice(proxies)  # Choisit un proxy au hasard dans la liste
    return {"http": f"http://{random_proxy}", "https": f"https://{random_proxy}"}  # Retourne le proxy formaté pour requests

def scrape_site(url, proxies):
    """ Scraper un site en utilisant un proxy rotatif """
    try:
        proxy = get_random_proxy(proxies)  # Sélectionne un proxy aléatoire
        response = requests.get(url, proxies=proxy)  # Envoie la requête via le proxy
        return response.text
    except requests.exceptions.ProxyError:
        # Si le proxy échoue, on réessaie avec un autre proxy (appel récursif)
        print("Erreur de proxy, en essayant un autre...")
        return scrape_site(url, proxies)

url = 'http://127.0.0.1:8080/scraping/'
page_content = scrape_site(url, proxies)
soup = BeautifulSoup(page_content, 'html.parser')
print(soup.select_one("h1"))  # Affiche la première balise <h1> de la page
