from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as playwright:
    # J'aurai aussi peu mettre firefox si j'avais voulu
    # Si je veux voir le navigateur je dois mettre False
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.docstring.fr/scraping/")
    # page.pause() permet de faire une pause et d'inspecter la page
    # Pour faire une pause je peux aussi utilise time.sleep(10) pour faire une pause de 10 secondes
    page.locator("css=#get-secrets-books").click() 
    page.wait_for_timeout(1000) # permet de faire une pause de 1 seconde
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for titre in soup.select("h2"):
        print(titre.text)

    browser.close()
