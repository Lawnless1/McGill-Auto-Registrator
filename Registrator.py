from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from contextlib import contextmanager
import time
import random
import json
from config import *



class Registrator:
    
    def __init__(self):
        self.setup_driver()
        
    @contextmanager
    def manage_exception(self, step):
        try:
            yield
        except Exception as e:
            print(f"An error occurred: {e}\nStep failed was {step}")
            print("Closing the driver...")
            self.driver.quit()
            raise e
        
    def select(self, Button):
        time.sleep(random.randint(3000,8000)/10000)
        Button.click()
    
    def setup_driver(self):
        with self.manage_exception("Setting up driver"):
            options = Options()
            options.add_argument("--headless=new")
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_window_size(300, 300)
            self.driver.implicitly_wait(30)
    
    def get_text_safely(self, index, By, key_str:str, base =None, retries=3, silent=False):
        for _ in range(retries):
            try:
                if base == None:
                    item = self.driver.find_elements(By, key_str)[index]
                else:
                    item = base.find_elements(By, key_str)[index]
                return (item, item.text.strip())
            except Exception as e:
                if not silent:
                    print(f"Error retrieving text at index {index}\nfor context: {key_str}.\n Retrying...")
                time.sleep(0.1)

        
    def login(self, IS_NEW_STUDENT, USERNAME, PASSWORD):
        with self.manage_exception("Logging in"):
            #Open Website
            self.driver.get("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")
                #Filling Credentials
            if IS_NEW_STUDENT:
                Username, Password = self.driver.find_element(By.ID, "UserID"), self.driver.find_element(By.ID, "PIN")
                Username.send_keys(USERNAME)
                Password.send_keys(PASSWORD)
                Login_Button = self.driver.find_element(By.ID, "mcg_id_submit")
            else:
                # Adding the login cookies
                for item in json.loads(open("cookies.txt", "r").read()):
                    if item["domain"] != ".horizon.mcgill.ca":
                        self.driver.add_cookie(item)
                    
                Login_Button = self.driver.find_element(By.TAG_NAME, "button")
            self.select(Login_Button)
    
    def navigate_to_registration(self)-> bool:
        with self.manage_exception("Navigating to registration"):
            Student_Button = self.driver.find_element(By.LINK_TEXT, "Student")
            self.select(Student_Button)
            Registration_Button = self.driver.find_element(By.LINK_TEXT, "Registration Menu")
            self.select(Registration_Button)
            Search_Class_Button = self.driver.find_element(By.LINK_TEXT, "Step 2: Search Class Schedule and Add Course Sections")
            self.select(Search_Class_Button)
    
    def enter_semester(self):
        with self.manage_exception(f"Entering semester {SEMESTER}"):
            Semester_Slider = self.driver.find_elements(By.TAG_NAME, "option")
            for i in range(len(Semester_Slider)):
                semester_choice, content = self.get_text_safely(i, By.TAG_NAME, "option")
                if content == SEMESTER:
                    self.select(semester_choice)
            Semester_Submit_Button = self.driver.find_elements(By.TAG_NAME, "input")
            self.select(Semester_Submit_Button[4])

    def pick_department(self, wanted_department):
        with self.manage_exception(f"Picking department {wanted_department}"):
            department_dropdown = self.driver.find_elements(By.TAG_NAME, "option")
            for i in range(len(department_dropdown)):
                department, content = self.get_text_safely(i, By.TAG_NAME, "option")
                if content.startswith(wanted_department):
                    self.select(department)
                    break
            Course_Search_Button = self.driver.find_element(By.NAME, "SUB_BTN")
            self.select(Course_Search_Button)
    
    def selecting_class(self, class_number, retries=3):
        with self.manage_exception(f"Selecting class {class_number}"):
            is_class_number = lambda txt : txt[:3].isnumeric()
            Found_class = False
            for _ in range(retries):
                class_grid = self.driver.find_elements(By.TAG_NAME, "td")
                correct_class_button_index = -2
                for i in range(len(class_grid)):
                    _ , content = self.get_text_safely(i, By.TAG_NAME, "td")
                    if is_class_number(content):
                        correct_class_button_index += 1
                        if content == class_number:
                            Found_class = True
                            break
                if not Found_class:
                    print(f"Class {class_number} not found in the grid. Retrying...")
                    continue
                Class_Submit_Buttons = self.driver.find_elements(By.NAME, "SUB_BTN")
                self.select(Class_Submit_Buttons[correct_class_button_index])
                return
            raise ValueError(f"Class {class_number} not found in the grid.")
      

    def parsing_table(self, department, CRN):
        with self.manage_exception("Parsing class data"):
            table = []
            i = 0
            while True:
                try:
                    _, content = self.get_text_safely(i, By.TAG_NAME, "td",silent=True)
                    table.append(content)
                    i += 1
                except Exception as e:
                    break
                
            while True:
                try:
                    i = table.index(department)-2
                    table = table[i:]
                    print(f"Status: {table[0]} | CRN: {table[1]} | Title: {table[2]} {table[3]} | Section: {table[4]} | Type: {table[5]} | Instructor: {table[16]} | Rem: {table[12]}/{table[10]} | WL Rem: {table[15]}/{table[13]}")
                    if int(table[12]) > 0:
                        self.take_class(CRN, False)
                    table = table[20:]
                except ValueError:
                    break
    
    def reset_position(self):
        with self.manage_exception("Resetting position"):
            New_Search_Button = self.driver.find_elements(By.NAME, "ADD_BTN")[-1]
            self.select(New_Search_Button)
            
    def take_class(self, crn, waitlist):
        with self.manage_exception(f"Taking class with CRN {crn} and waitlist status {waitlist}"):
            #Clicking on add_to_worksheet_button
            add_to_worksheet_button = self.driver.find_elements(By.NAME, "ADD_BTN")[-2]
            self.select(add_to_worksheet_button)
            crn_field = self.driver.find_elements(By.NAME, "crn_in")[-1]
            crn_field.send_keys(str(crn))
            submit_change_button = self.driver.find_elements(By.NAME, "REG_BTN")[-2]
            self.select(submit_change_button)
            if not waitlist:
                time.sleep(10)
                class_search_button = self.driver.find_elements(By.NAME, "REG_BTN")[-1]
                self.select(class_search_button)
            else:
                print("entered")
                #select(driver.find_element(By.NAME, "RSTS_IN")) # Clicks the action b
                choices = self.driver.find_elements(By.TAG_NAME, "option")
                for i in range(len(choices)):
                    _, content = self.get_text_safely(i, By.TAG_NAME, "option", silent=True)
                    if content == "(Add(ed) to Waitlist)":
                        self.select(i)
                class_search_button = self.driver.find_elements(By.NAME, "REG_BTN")[-1]
                submit_change_button = self.driver.find_elements(By.NAME, "REG_BTN")[-2]
                self.select(submit_change_button)
                time.sleep(10)
                self.select(class_search_button)
            print(f"Added CRN {crn}")
            exit()
            
    def check_class(self, class_number, CRN):
        department, number = class_number.upper().strip().split(" ")
        self.pick_department(department)
        self.selecting_class(number)
        self.parsing_table(department, CRN)
        self.reset_position()
            
                
if __name__ == "__main__":
    while True:
        registrator = Registrator()
        registrator.login(IS_NEW_STUDENT, USERNAME, PASSWORD)
        registrator.navigate_to_registration()
        registrator.enter_semester()
        for i, class_number in enumerate(CLASSES):
            registrator.check_class(class_number, WANTED_CRN[i])
        time.sleep(3)
        registrator.driver.quit()
        time.sleep(TIMER)
