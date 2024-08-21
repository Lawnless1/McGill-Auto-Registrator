from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import json

IS_NEW_STUDENT = False
USERNAME = "" #Write down your Mcgill ID as a string
PASSWORD = "" # Write down your Mcgill Password as string
SEMESTER = "Fall 2024" # Which semester do you want to check?
CLASSES = ["ECON 208"]
WANTED_CRN = {2106}
TIMER = 100 # in seconds

# This bot checks for availabilities in classes specified by the user
# Inside their program
while True:
    print(time.strftime("%H:%M:%S"))
    driver = webdriver.Edge()
    driver.set_window_size(300, 300)
    
    # Implicit total wait time
    driver.implicitly_wait(30) 

    #Open Website
    driver.get("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")

    def r_click(Button):
        time.sleep(random.randint(3000,8000)/10000)
        Button.click()
        
    #Filling Credentials
    if IS_NEW_STUDENT:
        Username, Password = driver.find_element(By.ID, "UserID"), driver.find_element(By.ID, "PIN")
        Username.send_keys(USERNAME)
        Password.send_keys(PASSWORD)
        Login_Button = driver.find_element(By.ID, "mcg_id_submit")
    else:
        # Adding the login cookies
        for item in json.loads(open("cookies.txt", "r").read()):
            if item["domain"] != ".horizon.mcgill.ca":
                driver.add_cookie(item)
            
        Login_Button = driver.find_element(By.TAG_NAME, "button")
    r_click(Login_Button)

    # Navigating once logged in
    Student_Button = driver.find_element(By.LINK_TEXT, "Student")
    r_click(Student_Button)
    Registration_Button = driver.find_element(By.LINK_TEXT, "Registration Menu")
    r_click(Registration_Button)
    Search_Class_Button = driver.find_element(By.LINK_TEXT, "Step 2: Search Class Schedule and Add Course Sections")
    r_click(Search_Class_Button)

    #Entering Semester
    Semester_Slider = driver.find_elements(By.TAG_NAME, "option")
    for i in Semester_Slider:
        if i.text == SEMESTER:
            r_click(i)
    Semester_Submit_Button = driver.find_elements(By.TAG_NAME, "input")
    r_click(Semester_Submit_Button[4])
    
    def take_class(crn, waitlist):
        #Clicking on add_to_worksheet_button
        add_to_worksheet_button = driver.find_elements(By.NAME, "ADD_BTN")[-2]
        r_click(add_to_worksheet_button)
        crn_field = driver.find_elements(By.NAME, "crn_in")[-1]
        crn_field.send_keys(str(crn))
        submit_change_button = driver.find_elements(By.NAME, "REG_BTN")[-2]
        r_click(submit_change_button)
        if not waitlist:
            time.sleep(10)
            class_search_button = driver.find_elements(By.NAME, "REG_BTN")[-1]
            r_click(class_search_button)
        else:
            print("entered")
            #r_click(driver.find_element(By.NAME, "RSTS_IN")) # Clicks the action b
            choices = driver.find_elements(By.TAG_NAME, "option")
            for i in choices:
                if i.text == "(Add(ed) to Waitlist)":
                    r_click(i)
            class_search_button = driver.find_elements(By.NAME, "REG_BTN")[-1]
            submit_change_button = driver.find_elements(By.NAME, "REG_BTN")[-2]
            r_click(submit_change_button)
            time.sleep(10)
            r_click(class_search_button)
        print(f"Added CRN {crn}")
        WANTED_CRN.remove(int(crn))

        
        
        
    def choosing_class(Class):
        # Defining the Department and number
        
        Department = Class.split(" ")[0]
        Num = Class.split(" ")[1]
        print(Department)
        print(Num)
        #Choosing the department
        Department_Slider = driver.find_elements(By.TAG_NAME, "option")
        for i in Department_Slider:
            if i.text[:4] == Department:
                r_click(i)
        Course_Search_Button = driver.find_element(By.NAME, "SUB_BTN")
        Course_Search_Button.click()
        #Choosing the class
        class_grid = driver.find_elements(By.TAG_NAME, "td")
        counter = -1
        # Finding which order the class is in
        for line in class_grid:
            if len(line.text) == 3:
                counter += 1
                if line.text.strip().lower() == Num.strip().lower():
                    break
        # Click on the n'th button
        Class_Submit_Buttons = driver.find_elements(By.NAME, "SUB_BTN")
        r_click(Class_Submit_Buttons[counter])
        # Finding and storing Class data
        class_grid2 = driver.find_elements(By.TAG_NAME, "td")
        Storing = False
        Full_availability_list = []
        '''
        Starts storing data when it detects the department name and stops storing
        when encountering the words Cancelled... from a set list
        '''
        Temp_storage = []
        for line in class_grid2:
            Temp_storage.append(line.text)
            if len(Temp_storage) == 4:
                Temp_storage.pop(0)
            if Storing is True:
                class_data.append(line.text)
            if line.text == Department:
                Storing, class_data = True, [i for i in Temp_storage]
            if line.text == "Active":
                Full_availability_list.append(class_data)
                Storing = False
            elif line.text in ["Cancelled", "Closed", "Temporarily closed"]:
                Storing = False
        
        moved = False
        for lecture in Full_availability_list:
            if lecture[0] != "C" and int(lecture[12]) > 3 and int(lecture[1]) in WANTED_CRN:# If there are still vacant spotslecture[1] or int(lecture[1]) in WANTED_CRN:
                take_class(lecture[1], False)
                moved = True
                break
            elif int(lecture[15]) > 0 and int(lecture[1]) in WANTED_CRN:# If there are still vacant spotslecture[1] or int(lecture[1]) in WANTED_CRN:
                print("AVAILABLEEEEE\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nAVAILABLE")
                take_class(lecture[1], True)
                moved = True
                break
        # Resetting for New search
        if not moved:
            New_Search_Button = driver.find_elements(By.NAME, "ADD_BTN")[-1]
            r_click(New_Search_Button)
        return Full_availability_list
        
    final_output = ""
    for classes in CLASSES:
        # Making the output more readable
        availability_list = choosing_class(classes)
        # Print class number
        final_output = final_output + f"{availability_list[0][2]} {availability_list[0][3]}\n"
        print(f"{availability_list[0][2]} {availability_list[0][3]}")
        for lecture in availability_list:
            #if (lecture[0] != "C"):
            if (float(lecture[12]) > 0): # If there are still vacant spots
                final_output = final_output + f"Sect:{lecture[4]} {lecture[5]} Rem:{lecture[12]} Chosen\n"
                print(f"Sect:{lecture[4]} {lecture[5]} CRN: {lecture[1]} Rem:{lecture[12]} Chosen")
            else: # Only display sections with open positions
                final_output = final_output + f"Sect:{lecture[4]} {lecture[5]} Rem:{lecture[12]}\n"
                print(f"Sect:{lecture[4]} {lecture[5]} CRN: {lecture[1]} Rem:{lecture[12]}")
        print("------------------") 
    final_output = final_output + "-------------------------------------------------------------------\n"
    time.sleep(5)
    driver.close()
    time.sleep(TIMER)

    #Closing the code
