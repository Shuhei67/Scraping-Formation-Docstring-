import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Fonction pour parcourir récursivement l'arbre DOM
def traverse_dom(element, level=0):
    # Afficher l'élément actuel
    if element.name:
        print("  " * level + element.name)

    # Si l'élément actuel a des enfants, les parcourir
    if hasattr(element, "children"):
        for child in element.children:
            traverse_dom(child, level + 1)


# Commencer le parcours depuis la racine de l'arbre
traverse_dom(soup)