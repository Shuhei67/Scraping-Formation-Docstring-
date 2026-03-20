import requests
from pathlib import Path
import logging

FILEPATH = Path(__file__).parent / "airbnb.html"
# Path(__file__) = l'emplacement du script
# .parent = le dossier qui contient le script
# / "airbnb.html" = on crée un chemin vers un fichier airbnb.html
# Résultat : C:\Users\MonPrénom\Desktop\Scraping Docstring\Part-3\airbnb-scraper\airbnb.html

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
# Ça permet d'afficher des messages de debug dans le terminal

"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""

# Récupère le contenu de la page à l'URL donnée :
def fetch_content(url: str, from_disk: bool = False) -> str:

    if from_disk and FILEPATH.exists():
        return read_from_file()

    try:
        logger.debug(f"Récupération du contenu de l'URL : {url}")
        response = requests.get(url)
        response.raise_for_status()  # Vérifie que la requête a réussi
        html_content = response.text
        write_to_file(content = html_content)
        return html_content
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la récupération du contenu : {e}")
        raise e
 
# Écrit le contenu dans un fichier :
def write_to_file(content: str) -> bool:
    logger.debug(f"Écriture du contenu dans le fichier")
    with open(FILEPATH, "w", encoding="utf-8") as f:
        f.write(content)

    return FILEPATH.exists()
    # Vérifie si le fichier a été créé avec succès

# Lit le contenu du fichier :
def read_from_file() -> str:
    logger.debug(f"Lecture du contenu du fichier")
    with open(FILEPATH, "r", encoding="utf-8") as f:
        return f.read()
        




# Ce bloc s'exécute seulement si je lances ce fichier directement
if __name__ == "__main__":
    url = "https://www.airbnb.fr/s/Bangkok--Tha%C3%AFlande/homes?refinement_paths%5B%5D=%2Fhomes&acp_id=f766c3c4-071d-469d-9a15-c8760e5d1c99&date_picker_type=monthly_stay&monthly_start_date=2026-04-01&monthly_end_date=2026-05-01&monthly_length=3&adults=1&search_type=user_map_move&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=1&price_filter_num_nights=30&channel=EXPLORE&zoom_level=11.976609218960075&place_id=ChIJ82ENKDJgHTERIEjiXbIAAQE&query=Bangkok%2C%20Tha%C3%AFlande&search_mode=regular_search&ne_lat=13.826318493439837&ne_lng=100.61760046298133&sw_lat=13.6785445179013&sw_lng=100.50155065953635&zoom=11.976609218960075&search_by_map=true"
    content = fetch_content(url=url, from_disk=True)