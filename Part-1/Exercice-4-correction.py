import re  # Module pour les expressions régulières (recherche de patterns dans du texte)

import requests  # Module pour faire des requêtes HTTP
from bs4 import BeautifulSoup  # Module pour parser le HTML

def main():  # On encapsule tout dans une fonction principale, bonne pratique Python
    response = requests.get("https://books.toscrape.com/index.html")  # On récupère le HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')  # On le parse pour pouvoir le manipuler

    # soup.select() utilise des sélecteurs CSS
    # ".star-rating.One" = élément qui a LA FOIS la classe "star-rating" ET la classe "One"
    # Retourne directement une liste de tous les livres 1 étoile, sans boucle + if !
    one_star_books = soup.select(".star-rating.One")

    for book in one_star_books:  # On parcourt chaque livre 1 étoile
        try:
            # find_next("h3") : cherche le prochain h3 APRÈS la balise star-rating
            # .find("a")["href"] : récupère le lien dans ce h3
            book_link = book.find_next("h3").find("a")["href"]
        except AttributeError as e:
            # AttributeError : déclenché si find_next("h3") ou find("a") retourne None
            # (on ne peut pas appeler une méthode sur None)
            print("Impossible de trouver la balise h3 ou a.")
            raise AttributeError from e  # On relance l'erreur pour stopper le programme
        except KeyError as e:
            # KeyError : déclenché si l'attribut "href" n'existe pas dans la balise <a>
            print("Impossible de trouver l'attribut href.")
            raise KeyError from e

        try:
            # re.findall(r"_\d+", book_link) : cherche dans book_link un pattern "_" suivi de chiffres
            # Ex: dans "catalogue/a-light_1000/index.html" il trouve "_1000"
            # [0] : on prend le premier résultat trouvé
            # [1:] : on enlève le "_" au début pour garder uniquement "1000"
            book_id = re.findall(r"_\d+", book_link)[0][1:]
            print(f"ID du livre à enlever : {book_id}")
        except IndexError as e:
            # IndexError : déclenché si re.findall() retourne une liste vide
            # (aucun pattern trouvé dans l'URL, donc [0] plante)
            print("Impossible de trouver l'ID du livre.")
            raise IndexError from e

# Point d'entrée du programme
# "__name__ == '__main__'" est vrai uniquement quand on lance CE fichier directement
# Si ce fichier est importé dans un autre script, main() ne se lance PAS automatiquement
if __name__ == '__main__':
    main()