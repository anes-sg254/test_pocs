from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Lancer le navigateur Chrome
driver = webdriver.Chrome()

# Ouvrir la page des nouveautés
driver.get("https://www.action.com/fr-fr/nouveautes/")

# Attendre que la page charge complètement
time.sleep(3)

# Accepter les cookies si nécessaire
try:
    cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    cookie_button.click()
    print("Cookies acceptés !")
    time.sleep(2)
except:
    print("Pas de bouton de cookies trouvé ou déjà accepté.")

# Attendre un peu pour que les produits chargent
time.sleep(3)

# Sélectionner tous les produits dans Nouveautés
products = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='product-card-link']")

# Extraire les informations des premiers produits
for product in products[:10]:  # Limité à 10 produits pour l'exemple
    try:
        title = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-title']").text
        url = product.get_attribute("href")
        price_whole = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-price-whole']").text
        price_fraction = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-price-fractional']").text
        description = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-description']").text
        price = f"{price_whole},{price_fraction}€"

        print(f"Titre : {title}")
        print(f"URL : {url}")
        print(f"Prix : {price}")
        print(f"Description : {description}")
        print("-" * 80)
    except Exception as e:
        print(f"Erreur pour un produit : {e}")
        continue  # Ignorer les erreurs et passer au produit suivant

# Fermer le navigateur
driver.quit()
