Here is a Software to automaticaly lock in your classes:

Purpose: 
    This Software allows you to pick classes and let the program automatically them in as soon as they are available

Note: this manual assumes you have Python already installed and know how to run different scripts

1. Extract all the files within this folder and perform every step from within the new folder

2. Run the following commands in your terminal:
        1. pip install selenium
        2. pip install json


3. If you have already completed a semester:
    please run save_cookies.py:
        A page will pop up:
            Within it, you will have to fill in your login credentials and enter minerva within a minute
            The page will automatically close once a minute has passed.
        explanation:
            This will save your credentials locally within a new file named cookies.txt, which the other programs will be able to access

    If you are a new student:
        nothing of note to do


4. Enter your code editor and look at config.py
You will have to fill in the following constants:
    IS_NEW_STUDENT = (True for new students and False for returning students)
    USERNAME = "Write down your Mcgill ID as a string" (Only required for new student, leave "" if returning)
    PASSWORD = "Write down your Mcgill Password as string" (Only required for new student, leave "" if returning)
    SEMESTER = Example: "Winter 2025" -Which semester do you want to check?
    CLASSES = ["COMP 202", "FACC 100] -In the following format
    WANTED_CRN = {1800} -the CRN of the sections you would like to LOCK In
        WARNING: Filling this section will automatically lock in the section for you when available
    TIMER = 300 -- The time delay between subsequent runs of the program in seconds

5. you are now ready to run the program!
    simply run Mcgill_registration_main.py, and wait for an opening!




Q&A:
    I am a returning student and the credentials don't work:
        Simply redo step 4