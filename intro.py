import requests

# On utilise la bibliothèque requests pour faire une requête GET à l'URL de Google
response = requests.get("https://www.google.com")

# On ouvre un fichier index.html et on y écrit le contenu HTML du site google     
with open("index.html", "w") as f:
    f.write(response.text) # on peut aussi demander au format json avec .json