from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid

# ====== CONFIGURE BEFORE RUNNING ======
BASE_URL = "http://localhost/moodle"   # adjust to your local Moodle base URL
ADMIN_USERNAME = "admin"               # admin username
ADMIN_PASSWORD = "Chalani123@" # admin password
CATEGORY_ID = 1                        # the category id where the course will be created (default 1)
HEADLESS = False                       # set True to run headless
# ======================================

def unique_shortname(base="COURSE"):
    # generate a short unique shortname to avoid collisions
    return f"{base}_{uuid.uuid4().hex[:8]}"

def main():
    chrome_opts = Options()
    if HEADLESS:
        chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--window-size=1400,1000")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
    wait = WebDriverWait(driver, 15)

    try:
        # 1) Open site and go to login page
        driver.get(BASE_URL)
        try:
            # Try to click the "Log in" link (theme-dependent)
            login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in")))
            login_link.click()
        except Exception:
            # Fallback: navigate directly to Moodle login page
            driver.get(BASE_URL.rstrip("/") + "/login/index.php")

        # 2) Log in as admin
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = driver.find_element(By.NAME, "password")
        username_input.clear()
        username_input.send_keys(ADMIN_USERNAME)
        password_input.clear()
        password_input.send_keys(ADMIN_PASSWORD)

        # Submit the login form (try to find a submit button first)
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            submit_button.click()
        except Exception:
            # fallback to executing form submit
            form = driver.find_element(By.XPATH, "//form[contains(@id,'login') or contains(@id,'mform') or contains(@action,'login')]")
            driver.execute_script("arguments[0].submit();", form)

        # Wait until login completes. Many Moodle sites redirect to /my/
        wait.until(lambda d: d.current_url != BASE_URL and "login" not in d.current_url.lower())

        # 3) Navigate to the "Add a new course" page for the selected category
        add_course_url = f"{BASE_URL.rstrip('/')}/course/edit.php?category={CATEGORY_ID}"
        driver.get(add_course_url)

        # Wait for the course creation form to appear
        form = wait.until(EC.presence_of_element_located((By.XPATH, "//form[contains(@id,'mform') or contains(@id,'course-edit-form')]")))

        # 4) Fill course fullname and shortname
        course_fullname = f"Automated Test Course {int(time.time())}"
        try:
            fullname = driver.find_element(By.NAME, "fullname")
            fullname.clear()
            fullname.send_keys(course_fullname)
        except Exception:
            raise RuntimeError("Could not find 'fullname' field on the Add course page. Inspect your Moodle theme/fields.")

        try:
            shortname = driver.find_element(By.NAME, "shortname")
            shortname_value = unique_shortname("ATC")
            shortname.clear()
            shortname.send_keys(shortname_value)
        except Exception:
            # If shortname doesn't exist for some reason, ignore (Moodle usually requires it)
            shortname_value = None

        # Optionally you can set other fields here (summary, format, start date, etc.)
        # e.g. find by name="summary" and send_keys("...")

        # 5) Submit the form
        # Try to click one of the expected save buttons; if not found, submit the form element.
        submitted = False
        try:
            # common ids: id_saveanddisplay, id_savechanges, id_submitbutton
            for btn_id in ("id_saveanddisplay", "id_savechanges", "id_submitbutton"):
                try:
                    btn = driver.find_element(By.ID, btn_id)
                    btn.click()
                    submitted = True
                    break
                except Exception:
                    continue
            if not submitted:
                # Try to find by button text (language dependent), fallback to form submit
                try:
                    btn = driver.find_element(By.XPATH, "//button[contains(., 'Save and display') or contains(., 'Save changes') or contains(., 'Save')]")
                    btn.click()
                    submitted = True
                except Exception:
                    pass
        except Exception:
            pass

        if not submitted:
            # final fallback: submit the form via JS
            driver.execute_script("arguments[0].submit();", form)

        # 6) Wait for creation success: usually Moodle redirects to course/view.php?id=...
        wait.until(lambda d: "/course/view.php" in d.current_url or "view.php" in d.current_url.lower())

        created_url = driver.current_url
        # verify the page contains our course name in an h1 or title
        try:
            h1 = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            found_title = h1.text.strip()
        except Exception:
            found_title = ""

        # Quick assertion/print
        if course_fullname in found_title or "/course/view.php" in created_url:
            print("Course created successfully!")
            print("Course fullname: ", course_fullname)
            print("Course shortname: ", shortname_value)
            print("Course URL: ", created_url)
        else:
            print("Course creation may have failed. Current URL:", created_url)
            print("Page h1/title:", found_title)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()