from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.action.com/fr-fr/nouveautes/")

time.sleep(3)

try:
    cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    cookie_button.click()
    print("Cookies acceptés !")
    time.sleep(2)
except:
    print("Pas de bouton de cookies trouvé ou déjà accepté.")

time.sleep(3)

products = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='product-card-link']")

for product in products[:10]:  
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
        continue  
    
driver.quit()
