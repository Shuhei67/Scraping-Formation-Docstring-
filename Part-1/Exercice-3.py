# Mon script permet d'obtenir exactement le même résulat que le script de correction
# Cette version est simplement la première que j'ai écrite, à ma manière et avec mes connaissances 

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)

with open("index.html", "w") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")

liste_categories = soup.find("aside").find("div", class_ = "side_categories").find("ul").find("li").find("ul")
for category in liste_categories.children:
    if category.name:
        if category.a:
            page_categorie = requests.get(url + category.a["href"])
            contenue_page_categorie = BeautifulSoup(page_categorie.text, "html.parser")
            articles = contenue_page_categorie.find("section").find_all("article")
            if len(articles) < 20:
                if len(articles) < 5:
                    print(category.text.strip())


# Récupère la page d'accueil de books.toscrape.com
# Extrait la liste des catégories depuis la barre latérale
# Pour chaque catégorie :
#   - Visite sa page
#   - Compte le nombre de livres
#   - Si moins de 20 livres, vérifie si moins de 5
#   - Si moins de 5 livres, affiche le nom de la catégorie