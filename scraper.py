# Importation des bibliotiques
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
#import schedule 
import sqlite3
import datetime

connection = sqlite3.connect("db.sqlite3")

cursor = connection.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS arrticle_table(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article Text, 
                    date Date, 
                    press_name Text)
               """)

connection.commit()
# En-têtes pour simuler une requête du navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def faire_requete(url):
    """ 
    Effectuer une requête HTTP avec gestion des erreurs
    Args:
        url (str): l'URL de la requête HTTP
    
    Returns:
        bytes or None: Le contenu de la réponse si la requête est réussie, sinon None.
        
    """
    try:
        with requests.get(url, headers=headers) as reponse:
            reponse.raise_for_status()
            return reponse.content
        
    except requests.RequestException as e:
        print(f"Erreur de requête HTTP: {e}")
        return None


def aujourdui_scrape_articles(press_name):
    """
    Extraction des liens des articles.
    Args:
        nombre_pages: présente le nombre de page dans la catégorie de l'économie
    """

    liens_articles = []
    for page in range(1):
        lien_page = f"https://aujourdhui.ma/category/economie/"
        time.sleep(2)
        contenu = faire_requete(lien_page)

        if contenu:
            soup = BeautifulSoup(contenu, "html.parser")
            liens = soup.find_all("div", {"class":"jl_clist_layout"})
            liens_articles.extend([lien.a["href"] for lien in liens])
     
    
    lignes = []
    for lien in liens_articles:
        time.sleep(2)
        contenu = faire_requete(lien)
        if contenu:
            soup = BeautifulSoup(contenu, "html.parser")
            try:
                titre = soup.find("h1", {"class":"jl_head_title"}).text.replace("\n", "").strip()
            except:
                titre = None
            try:
                description = soup.find("div", {"class":"post_content"}).text.replace("\n", "").strip()
            except:
                description = None
            try:
                date = soup.find("span", {"class":"post-date"}).text.replace("\n", "").strip()
                #date_obj = datetime.datetime.strptime(date_str, "%d %B %Y")
                #date = date_obj.strftime("%d/%m/%Y")
            except:
                date = None
            
            article = titre + description
            row = [article, date, press_name]
            cursor.execute("""
                           INSERT INTO arrticle_table(article, date, press_name) VALUES('{article}', '{date}', '{press_name}') 
                        """)
            connection.commit()
            
            lignes.append(row)

    aujourdui_articles_df = pd.DataFrame(lignes, columns=["article", "date", "press_name"]) 
    #aujourdui_articles_df.to_csv(f"/home/ubuntu/INAC - HCP Training/construction-economic-indicator/news-data/data_files_csv/{press_name}.csv", index=False)
    return aujourdui_articles_df


if __name__ == "__main__":
    df = aujourdui_scrape_articles(press_name="aujourdhui")  
    print(df.shape)
    print(df.head())
    print(df.dtypes)

    # Schedule the scraping task to run every 24 hours
    #schedule.every(24).hours.do(scrape_articles)

    #schedule.every(10).minutes.do(aujourdui_scrape_articles)
    # Run the scheduler in an infinite loop
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
    