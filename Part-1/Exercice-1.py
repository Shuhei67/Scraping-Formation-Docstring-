import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = "https://books.toscrape.com/index.html"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
aside = soup.find("div", class_ = "side_categories")
categories_div = aside.find("ul").find("li").find("ul")
# J'utilise une compréhension de liste plutot q'une boucle "for" :
categories = [child.text.strip() for child in categories_div.children if child.name]
# J'aurai pu l'écrire de cette façon sinon : 
# for category in categories.children:
#        if category.name:
#            print(category.text.strip()) # Le .strip() permet de récupérer le texte sans les espaces autour

pprint(categories) # J'affiche le nom de toute les catégories de la liste dans Aside

images = soup.find("section").find_all("img")
for image in images:
    print(image["src"]) # Ici je récupère le lien "src" de toutes les images de <section>