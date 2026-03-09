import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/index.html"
response = requests.get(url)

# Le "parser" est la méthode d'analyse du fichier 
# Utiliser "html.parser" pour analyser le contenu HTML de la page; "html5lib" ou "lxml" sont possible aussi
soup = BeautifulSoup(response.text, "html.parser") 

 # "print(soup.prettify())" ici pourrait permettrer d'afficher le contenu de la page de manière lisible


 # Fonction pour parcourir récursiveement le DOM et donc affiché l'intégralité de la page HTML
def traverse_dorm(element, level=0):
    # Afficher l'élément actuel
    if element.name:
        print("  " * level + element.name)

    # Si l'élément actuel a des enfants, les parcourir
    if hasattr(element, "children"):
        for child in element.children:
            traverse_dorm(child, level + 1)


# Commencer le parcours depuis la racine de l'arbre
traverse_dorm(soup)