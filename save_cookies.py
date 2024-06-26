from selenium import webdriver
from selenium.webdriver.common.by import By
from pygame import mixer
import time
import random
import json

# Function to click button
def r_click(Button):
    time.sleep(random.randint(3000,8000)/10000)
    Button.click()
    
#You have 1 min to save the cookies
driver = webdriver.Chrome()

# Implicit total wait time
driver.implicitly_wait(30)

#Open Website
driver.get("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")
Login_Button = driver.find_element(By.TAG_NAME, "button")
r_click(Login_Button)
time.sleep(2)
cookies = open("cookies.txt", "w")
time.sleep(60)
print(driver.get_cookies())
cookies.write(json.dumps(driver.get_cookies()))
cookies.close()
driver.close()