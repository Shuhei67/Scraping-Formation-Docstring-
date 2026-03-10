import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/index.html"
# Pour ce script on me demandais de gérer les erreurs potentiel :
try:
    response = requests.get(BASE_URL)
    response.raise_for_status()
except requests.exceptions.HTTPError as error:
    print(50 * "-")
    print("Http Error:", error)
    print(50 * "-")
    exit()
except requests.exceptions.ConnectionError as error:
    print(50 * "-")
    print("Error Connecting:", error)
    print(50 * "-")
    exit()
except requests.exceptions.Timeout as error:
    print(50 * "-")
    print("Timeout Error:", error)
    print(50 * "-")
    exit()
except requests.exceptions.RequestException as error:
    print(50 * "-")
    print("OOps: Something Else", error)
    print(50 * "-")
    exit()

# Récupère la page d'accueil de books.toscrape.com
soup = BeautifulSoup(response.text, "html.parser")

# Extrait la liste des livres depuis la page d'accueil
articles = soup.find_all("article", class_ = "product_pod")

# Pour chaque livre, vérifie s'il a une note de 1 étoile et affiche la phrase demandée
for bad_articles in articles:
    if bad_articles.find("p", class_ = "star-rating One"):
        print(50 * "-")
        print(f"Le livre {bad_articles.find("h3").text}, ayant pour id {bad_articles.find("a")["href"].split("_")[-1].split("/")[0]} est présent sur la page d'accueil malgré sa mauvaise note.")