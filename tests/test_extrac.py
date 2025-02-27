import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def driver():
    """ Initialise le navigateur en mode headless et ferme après les tests """
    options = Options()
    
    # Pour l'exécution dans un environnement CI (headless)
    options.add_argument("--headless")  # Mode headless, sans interface graphique
    options.add_argument("--no-sandbox")  # Résoudre les problèmes dans les environnements CI
    options.add_argument("--disable-dev-shm-usage")  # Pour les environnements limités en mémoire
    options.add_argument("--disable-gpu")  # Désactive le GPU (recommandé dans CI headless)
    
    # Crée un service pour le ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # Initialise le navigateur avec les options et le service
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_action_nouveautes(driver):
    """ Teste la récupération des produits dans la catégorie Nouveautés """
    
    driver.get("https://www.action.com/fr-fr/nouveautes/")
    time.sleep(3)

    try:
        cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        cookie_button.click()
        time.sleep(2)
    except:
        print("Pas de bouton de cookies trouvé ou déjà accepté.")

    time.sleep(3)

    products = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='product-card-link']")
    assert len(products) > 0, "Aucun produit trouvé dans la section Nouveautés"

    product = products[0]  # Prendre le premier produit
    title = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-title']").text
    url = product.get_attribute("href")
    price_whole = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-price-whole']").text
    price_fraction = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-price-fractional']").text
    description = product.find_element(By.CSS_SELECTOR, "[data-testid='product-card-description']").text
    price = f"{price_whole},{price_fraction}€"

    assert title, "Le titre du produit est vide"
    assert url.startswith("https"), "L'URL du produit n'est pas valide"
    assert price_whole.isdigit(), "Le prix du produit est invalide"
    assert description, "La description du produit est vide"

    print(f"Test réussi pour le produit : {title} - {price}€")
