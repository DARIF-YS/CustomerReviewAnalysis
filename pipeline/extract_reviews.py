import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from pathlib import Path
import time
import json, os, sys

def extract():

    # chromedriver_autoinstaller.install()
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bank_urls')))
    from banks_links import  links

    # Supprimer le fichier s’il existe
    file_path = Path('/home/ubuntu/CustomerReviewAnalysis/raw_data/raw_data.json')
    if file_path.exists():
        file_path.unlink()
        
    # Lancer le navigateur Chrome
    driver = webdriver.Chrome()
    links = links

    for index, cle in enumerate(links):
        driver.get(links[cle])

        # Attendre le chargement de la page
        time.sleep(3)

        # Récupérer le code HTML de la page de Presentation
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')

        bank_name_element     = soup.find('h1', class_="DUwDvf lfPIob")
        bank_location_element = soup.find('div', class_='Io6YTe fontBodyMedium kR99db fdkmkc')
        bank_rating_element   = soup.find('div', class_='F7nice')

        if not bank_name_element:
            bank_name = None
        else:
            bank_name = bank_name_element.get_text()
        
        if not bank_location_element:
            bank_location = None
        else:
            bank_location = bank_location_element.get_text()

        if not bank_rating_element:
            bank_rating = None
        else:
            bank_rating   = bank_rating_element.span.span.get_text()
                    
        button = driver.find_element(By.XPATH, "//button[@aria-selected='false']")
        button.click()

        time.sleep(4)

        # Trouver l'élément contenant les avis
        avis_container = driver.find_element(By.XPATH, "//div[@jslog='26354;mutable:true;']")

        # Scroller dynamiquement jusqu'à la fin
        last_height = driver.execute_script("return arguments[0].scrollHeight;", avis_container)

        while True:
            # Scroller vers le bas
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", avis_container)

            # Attendre le chargement du contenu
            time.sleep(4)

            # Récupérer les boutons "Voir l'original"
            buttons_original = driver.find_elements(By.XPATH, "//button[@class='kyuRq fontTitleSmall WOKzJe' and @aria-checked='true' and @role='switch']")
            
            # Récupérer les boutons "Voir plus"
            buttons_plus = driver.find_elements(By.XPATH, "//button[@class='w8nwRe kyuRq' and @aria-label='Voir plus']")

            # Cliquer sur les boutons "Voir l'original"
            for btn_or in buttons_original:
                try:
                    btn_or.click()
                    time.sleep(0.2)
                except Exception as e:
                    print(f"Erreur lors du clic sur 'Voir l'original' : {e}")

            # Cliquer sur les boutons "Voir plus"
            for btn_pl in buttons_plus:
                try:
                    btn_pl.click()
                    time.sleep(0.2)
                except Exception as e:
                    print(f"Erreur lors du clic sur 'Voir plus' : {e}")

            # Obtenir la nouvelle hauteur après le défilement
            new_height = driver.execute_script("return arguments[0].scrollHeight;", avis_container)

            # Vérifier si la hauteur n'a pas changé (fin du scroll)
            if new_height == last_height:
                print("Fin du scroll.")
                break

            # Mettre à jour la hauteur
            last_height = new_height

        # Récupérer le code HTML de la page d'Avis
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')

        review_infos = soup.find_all('div', class_='jftiEf fontBodyMedium')

        for review_info in review_infos:
            review_date_element   = review_info.find('span', class_='rsqaWe')
            review_text_element   = review_info.find('div', class_='MyEned')
            review_rating_element = review_info.find_all('span', class_='elGi1d')

            if not review_date_element:
                review_date = None
            else:
                review_date = review_date_element.get_text()
            
            if not review_text_element:
                review_text = None
            else:
                review_text = review_text_element.span.get_text()
            
            if not review_rating_element:
                review_rating = None
            else:
                review_rating = len(review_rating_element)

            nouveau_commentaire = {
            "bank_name"    : bank_name    ,
            "bank_rating"  : bank_rating  ,
            "bank_location": bank_location,
            "review_date"  : review_date  ,
            "review_text"  : review_text  ,
            "review_rating": review_rating
            }
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current_dir, '..', 'raw_data', 'raw_data.json')

            # Charger les commentaires existants
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fichier:
                    commentaires = json.load(fichier)
            except FileNotFoundError:
                commentaires = []

            commentaires.append(nouveau_commentaire)                
            
            # Enregistrer la mise à jour
            with open(path, "w", encoding="utf-8") as fichier:
                json.dump(commentaires, fichier, indent=4, ensure_ascii=False)

    # Fermer le navigateur
    driver.quit()