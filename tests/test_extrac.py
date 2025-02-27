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
    options.add_argument("--headless")  # Mode headless obligatoire pour GitHub Actions
    options.add_argument("--no-sandbox")  # Évite les erreurs liées aux permissions
    options.add_argument("--disable-dev-shm-usage")  # Évite les erreurs de mémoire partagée
    options.add_argument("--disable-gpu")  # Désactiver GPU pour éviter certains bugs graphiques

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # Ajout d'une attente implicite
    yield driver
    driver.quit()

def test_action_nouveautes(driver):
    """ Teste la récupération des produits dans la catégorie Nouveautés """
    
    driver.get("https://www.action.com/fr-fr/nouveautes/")
    
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        cookie_button.click()
        print("Cookies acceptés.")
    except Exception as e:
        print(f"Pas de bouton de cookies trouvé ou déjà accepté. {e}")

    try:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='product-card-link']"))
        )
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
        
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        assert False, f"Test échoué : {e}"

