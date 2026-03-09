import requests

# Ici l'URL n'existe pas volontairement pour provoquer une erreur
url = "http://cetteurlnextistepas.com"


# Le bloc try permet de tester du code qui pourrait provoquer une erreur
try:
    response = requests.get(url)
    response.raise_for_status()

# Gestion d'une erreur HTTP (ex : page non trouvée 404, erreur serveur 500) :
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
# Gestion d'une erreur de connexion (ex : domaine inexistant, serveur inaccessible) :
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
# Gestion d'une erreur de délai dépassé (timeout, si serveur met trop de temps à répondre) :
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
# Gestion de toutes les autres erreurs possibles liées à requests ;
# RequestException est la classe mère de toutes les exceptions de requests :
except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)
