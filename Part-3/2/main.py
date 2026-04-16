from playwright.sync_api import sync_playwright

def run(pw):
    print("Launching browser...")
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    url = "https://www.airbnb.fr/s/Barcelone--Espagne/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJ5TCOcRaYpBIRCmZHTz37sEQ&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=may&adults=1&search_type=AUTOSUGGEST"
    page.goto(url)
    page_number = 1

    # Ici je lance un page.pause() et je lance le mode Rekord
    # Ca va me permettre d'avoir le chemin / code exact pour accéder a ce que je veux
    
    # Fermeture fenetre des cookies
    page.get_by_role("button", name="Uniquement les cookies né").click()

    while True:
        print(f"Scraping page {page_number}...")
        next_page_link = page.get_by_role("link", name="Suivant") 
        if next_page_link.get_attribute("aria-disabled") == "true":
            break

        page_number += 1  
        page.wait_for_timeout(2000)  # Attendre que la page se charge (éthique)
        next_page_link.click()

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(pw=playwright)