import re  # Pour manipuler du texte avec des expressions régulières (regex)
import logging  # Pour afficher des messages (debug, erreurs, etc.)

import requests  # Pour faire des requêtes HTTP (récupérer une page web)
from requests.exceptions import RequestException  # Pour gérer les erreurs de requêtes

from bs4 import BeautifulSoup  # Pour parser le HTML (scraping)
from pathlib import Path  # Pour gérer les chemins de fichiers facilement

# Chemin vers le fichier local où sera sauvegardé le HTML
FILEPATH = Path(__file__).parent / "airbnb.html"

# Initialisation du logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)  # Affiche seulement warnings et erreurs


def fetch_content(url: str, from_disk: bool = False) -> str:
    """Récupère le contenu HTML d'une page (soit en ligne, soit depuis un fichier local)"""

    # Si on veut lire depuis le disque ET que le fichier existe → on le lit directement
    if from_disk and FILEPATH.exists():
        return _read_from_file()

    try:
        logger.debug(f"Making request to {url}")

        # Requête HTTP pour récupérer la page
        response = requests.get(url)

        # Vérifie si la requête a réussi (sinon lève une erreur)
        response.raise_for_status()

        # Récupère le HTML sous forme de texte
        html_content = response.text

        # Sauvegarde le HTML dans un fichier local
        _write_to_file(content=html_content)

        return html_content

    except RequestException as e:
        # Log l'erreur si la requête échoue
        logger.error(f"Couldn't fetch content from {url} due to {str(e)}")
        raise e  # Relance l'erreur


def _write_to_file(content: str) -> bool:
    """Écrit le contenu HTML dans un fichier"""

    logger.debug("Writing content to file")

    # Ouvre le fichier en écriture et écrit le contenu
    with open(FILEPATH, "w") as f:
        f.write(content)

    # Retourne True si le fichier existe (écriture réussie)
    return FILEPATH.exists()


def _read_from_file() -> str:
    """Lit le contenu HTML depuis le fichier local"""

    logger.debug("Reading content from file")

    # Ouvre le fichier en lecture et retourne son contenu
    with open(FILEPATH, "r") as f:
        return f.read()


def get_average_price(html: str) -> int:
    """Extrait les prix depuis le HTML et calcule la moyenne"""

    prices = []  # Liste pour stocker tous les prix trouvés

    # Transforme le HTML en objet manipulable
    soup = BeautifulSoup(html, 'html.parser')

    # Récupère toutes les annonces (chaque div représente un logement)
    divs = soup.find_all('div', itemprop="itemListElement")

    for div in divs:
        # Cherche le prix dans deux classes possibles (Airbnb change souvent ses classes)
        price = div.find("span", class_="_tyxjp1") or div.find("span", class_="_1y74zjx")

        # Si aucun prix trouvé → on passe à l'annonce suivante
        if not price:
            logger.warning(f"Couldn't find price in {div}")
            continue

        # Supprime tout ce qui n'est pas un chiffre (€, espaces, etc.)
        price = re.sub(r"\D", "", price.text)

        # Vérifie que c'est bien un nombre
        if price.isdigit():
            logger.debug(f"Price found : {price}")
            prices.append(int(price))  # Ajoute le prix à la liste
        else:
            logger.warning(f"Price {price} is not a digit")

    # Calcule la moyenne des prix
    # Si la liste est vide → retourne 0 pour éviter une division par 0
    return round(sum(prices) / len(prices)) if len(prices) else 0


if __name__ == '__main__':
    # URL de recherche Airbnb (ici Rio de Janeiro avec filtres)
    url = "https://www.airbnb.fr/s/Rio-de-Janeiro--Rio-de-Janeiro--Br%C3%A9sil/homes?tab_id=home_tab&monthly_start_date=2024-01-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&query=Rio%20de%20Janeiro,%20Br%C3%A9sil&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=28&place_id=ChIJW6AIkVXemwARTtIvZ2xC3FA"

    # Récupère le HTML (depuis le fichier local si possible)
    html_content = fetch_content(url, from_disk=True)

    # Calcule et affiche le prix moyen
    print(get_average_price(html_content))