"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
Exercice final de la Partie 1, la consigne est la suivante:

Le propriétaire de la librairie veut connaître la valeur totale de son inventaire. 
Pour chaque livre du site, récupère son prix et sa quantité en stock, multiplie les deux, 
et additionne tout pour obtenir la valeur totale du stock.
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""

import sys # Module pour intéragir avec le système d'exploitation
from typing import List # Permet de préciser les types de données
import re

from selectolax.parser import HTMLParser # Equivalent de BeautifulSoup
from loguru import logger # Vas gérer nos messages à la place des print()
import requests

logger.remove() # Supprime comportement par défaut
logger.add(f"books.log", # Sauvegarde nos messages dans un fichier
           level = "WARNING", # Uniquement les messages graves
           rotation = "500kb") # Nouveau fichier tout les 500kb
logger.add(sys.stderr, level = "INFO") # Affiche messages type INFO ou +


def get_all_books_urls(url: str) -> List[str]:
        # Récupère tout les url des livres sur toutes les pages a partir d'une url
        pass

def get_next_page_url(html: HTMLParser) -> str:
        # Récupère l'url de la page suivante à partir du html d'une page
        pass

def get_all_books_urls_on_page(html: HTMLParser) -> List[str]:
        # Récupère tout les url des livres sur une page à partir du html de la page
        pass

def get_book_price(url: str) -> float: # Récupère le prix d'un livre à partir de son url
        try:
            response = requests.get(url)
            response.raise_for_status() # Vérifie que la requete a réussi
            tree = HTMLParser(response.text)
            price = extract_price_from_page(tree = tree)
            stock = extract_stock_quantity_from_page(tree = tree)
            return price * stock
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la requête HTTP : {e}")
            return 0.0 # Retourne 0 en cas d'erreur

def extract_price_from_page(tree: HTMLParser) -> float: # Extrait le prix d'un livre à partir de son arbre HTML
        price_node = tree.css_first("p.price_color")
        if price_node:
               price_string = price_node.text()
        else:
            logger.error("Aucun noeud contenant le prix n'a été trouver.")
            return 0.0
        try:
            price = re.findall(r"[0-9.]+", price_string)[0]
        except IndexError as e:
            logger.error(f"Aucun nombre n'a été trouvé : {e}")
            return 0.0
        else:
            return float(price)

def extract_stock_quantity_from_page(tree: HTMLParser) -> int:
        # Extrait la quantité en stock d'un livre à partir de son arbre HTML
        try:
            stock_node = tree.css_first("p.instock.availability")
            return int(re.findall(f"\d+", stock_node.text())[0])
        except AttributeError as e:
            logger.error(f"Aucun noeud 'p.instock.availability' n'a été trouvé : {e}")
            return 0
        except IndexError as e:
            logger.error(f"Aucun nombre n'a été trouvé dans le noeud : {e}")
            return 0

def main():
        base_url = "http://books.toscrape.com/index.html"
        all_books_urls = get_all_books_urls(url = base_url)
        total_price = 0
        for book_url in all_books_urls:
                price = get_book_price(url = book_url)
                total_price += price
        return total_price
                

if __name__ == "__main__":
        url = "http://books.toscrape.com/index.html"
        get_book_price(url = url)
        main()