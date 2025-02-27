import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    """ Initialise le navigateur et ferme après les tests """
    # Si tu veux toujours exécuter en mode headless en local, garde ce code :
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # décommenter si tu veux en mode headless
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_action_nouveautes(driver):
    """ Teste la récupération des produits dans la catégorie Nouveautés """
    
    driver.get("https://www.action.com/fr-fr/nouveautes/")

    # On attend ici un peu plus longtemps (pour être sûr que tout est chargé)
    time.sleep(5)  # Un délai de 5 secondes pour que les éléments se chargent correctement

    try:
        cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        cookie_button.click()
        time.sleep(2)
    except:
        print("Pas de bouton de cookies trouvé ou déjà accepté.")

    # Attendre encore un peu pour que les produits apparaissent après le clic sur le cookie
    time.sleep(5)

    # On s'assure que les produits sont présents
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
