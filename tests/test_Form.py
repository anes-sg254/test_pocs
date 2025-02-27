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

    # Crée un service pour le ChromeDriver avec webdriver_manager
    service = Service(ChromeDriverManager().install())
    
    # Initialise le navigateur avec les options et le service
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # Temps d'attente implicite
    yield driver
    driver.quit()

def test_registration(driver):
    """ Vérifie que l'inscription fonctionne correctement """
    
    driver.get("https://tutorialsninja.com/demo/index.php?route=account/register")

    driver.find_element(By.ID, "input-firstname").send_keys("John")  
    driver.find_element(By.ID, "input-lastname").send_keys("Doe")  
    email = f"johndoe{int(time.time())}@example.com"  # Email unique
    driver.find_element(By.ID, "input-email").send_keys(email)  
    driver.find_element(By.ID, "input-telephone").send_keys("0612345678")  
    driver.find_element(By.ID, "input-password").send_keys("Password123")  
    driver.find_element(By.ID, "input-confirm").send_keys("Password123")  

    driver.find_element(By.NAME, "agree").click()
    driver.find_element(By.XPATH, "//input[@value='Continue']").click()

    success_message = driver.find_element(By.XPATH, "//h1[contains(text(), 'Your Account Has Been Created!')]")
    assert success_message is not None, "L'inscription a échoué !"
