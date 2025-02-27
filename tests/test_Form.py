import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    """ Initialise le navigateur et ferme après le test """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  
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
