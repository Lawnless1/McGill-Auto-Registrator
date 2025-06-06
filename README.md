# McGill-Auto-Registrator

## Overview

McGill-Auto-Registrator is a Python-based software designed to automatically register you for your selected classes as soon as they become available. It uses **headless web scraping with Selenium** to interact with McGill's registration system, allowing for automated and seamless course enrollment. The program supports login either through saved Microsoft cookies (for returning students) or direct credential input (for new students).

By saving your login cookies locally, the program can run without repeatedly prompting you for credentials, enhancing security and convenience.

---

## Usage Instructions

### Prerequisites

- Ensure you have **Python** installed.
- Basic familiarity with running Python scripts.
- Extract all the files into a new folder and perform every step from within this folder.

### Step 1: Install Required Packages

Open your terminal and run:

``` pip install selenium ```

``` pip install json ```

### Step 2: Save Login Cookies (For Returning Students Only)

If you have already completed a semester at McGill:

- Run `save_cookies.py`.
- A browser window will pop up.
- Log in with your McGill credentials and navigate to Minerva within one minute.
- The window will automatically close after one minute.
- This process saves your login cookies to a local file `cookies.txt`, which allows the program to authenticate automatically in future runs.

If you are a **new student**, you can skip this step.

### Step 3: Configure Your Settings

Open `config.py` in your preferred code editor and fill in the following:

- `IS_NEW_STUDENT` = Set to `True` if you are a new student; `False` if returning.
- `USERNAME` = Your McGill ID as a string (only required if `IS_NEW_STUDENT` is `True`, leave empty `""` if returning).
- `PASSWORD` = Your McGill password as a string (only required if `IS_NEW_STUDENT` is `True`, leave empty `""` if returning).
- `SEMESTER` = The semester you want to register for, e.g., `"Winter 2025"`.
- `CLASSES` = A list of course codes you want to register for, e.g., `["COMP 202", "FACC 100"]`.
- `WANTED_CRN` = A set of CRNs for the specific sections you want to lock in, e.g., `{1800}`.  
  **Warning:** Filling this will automatically lock you into these sections as soon as they are available.
- `TIMER` = Time delay in seconds between subsequent program runs (default example: `300`).

### Step 4: Run the Program

Run the main script:

``` python Mcgill_registration_main.py ```

The program will run continuously, checking for openings and automatically registering you when spots become available.

---

## FAQ

**Q: I am a returning student and the credentials saved in cookies do not work. What should I do?**  
A: Simply redo Step 2 (`save_cookies.py`) to refresh your saved credentials.

---

Enjoy hassle-free registration with McGill-Auto-Registrator!
