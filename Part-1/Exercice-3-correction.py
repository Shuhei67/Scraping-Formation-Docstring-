from urllib.parse import urljoin  # Construit des URLs complètes proprement
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/index.html"

def main(threshold: int = 5):  # Fonction principale, seuil de 5 livres par défaut
    with requests.Session() as session:  # Ouvre une session HTTP réutilisable
        response = session.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupère tous les liens de catégories depuis la navigation
        categories = soup.select('ul.nav.nav-list a')
        categories_urls = [category['href'] for category in categories]  # List comprehension
        
        for category_url in categories_urls:
            full_url = urljoin(BASE_URL, category_url)  # Construit l'URL complète
            response = session.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            books = soup.select('article.product_pod')  # Tous les livres de la page
            category_title = soup.find("h1").text  # Nom de la catégorie
            number_of_books = len(books)
            
            if number_of_books <= threshold:  # Filtre selon le seuil
                print(f"La catégorie '{category_title}' ne contient pas assez de livres ({number_of_books})")

if __name__ == '__main__':
    main(threshold=5)  # Point d'entrée du script