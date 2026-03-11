from selectolax.parser import HTMLParser # même chose que "from bs4 import BeautifulSoup"
from loguru import logger
import sys
import requests

logger.remove() # Supprime le comportement par défaut de loguru

# Crée fichier "books.log" (enregistre messages)
# rotation="500kb" : quand fichier dépasse 500kb, il en crée un nouveau
# level="WARNING" : enregistre que les messages WARNING et plus graves
logger.add("books.log", rotation = "500kb", level = "WARNING")

# Affiche les messages dans le terminal
# level="INFO" : affiche INFO et plus graves
logger.add(sys.stderr, level = "INFO")

url = "https://books.toscrape.com/"
r = requests.get(url)

tree = HTMLParser(r.text)
# Si j'utilisais beautifulSoup j'aurai pu écrire : 
# soup = BeautifulSoup(r.text, "html.parser")

tree.css("a") # soup.select("a")
tree.css_first("a") # soup.select_one("a")