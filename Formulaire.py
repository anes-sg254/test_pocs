from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://tutorialsninja.com/demo/index.php?route=account/register")

driver.find_element(By.ID, "input-firstname").send_keys("John")  
driver.find_element(By.ID, "input-lastname").send_keys("Doe")  
driver.find_element(By.ID, "input-email").send_keys(f"johndoe{int(time.time())}@example.com")  
driver.find_element(By.ID, "input-telephone").send_keys("0612345678") 
driver.find_element(By.ID, "input-password").send_keys("Password123")  
driver.find_element(By.ID, "input-confirm").send_keys("Password123")  

driver.find_element(By.NAME, "agree").click()

driver.find_element(By.XPATH, "//input[@value='Continue']").click()

time.sleep(3)


driver.quit()
