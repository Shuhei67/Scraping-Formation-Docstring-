import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = "https://books.toscrape.com/index.html"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser") # Je récupère le HTML de la page
aside = soup.find("aside") # Je cherche le <aside> dans le HTML
side_categories = aside.find("div", class_ = "side_categories") # Je cherche les <div> avec la classe <side_categories>
links = side_categories.find_all("a") # La je cherche tout le liens

# Ici j'affiche alors tout les liens, de la <div class= "side_categories">
# Etant dans le aside du code Html récupéré
pprint(links)
