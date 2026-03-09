# On me demandais dans ce premier exercice de récupérer tout les titres
# des livres présent sur la page d'acceuil

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)

with open("index.html", "w") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("article", class_ = "product_pod")

for article in articles:
    article_name = article.find("h3").find("a")["title"]
    print(article_name)

# Autre manière de faire dans la correction, pas bien compris, à revoir :
# titles = [a["title"] for a in soup.find_all("a", title = True)]
# pprint(titles)
# Je récupererai alors tout les titres en une seule ligne de code