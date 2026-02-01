# Software Testing & Quality Assurance Project: Moodle LMS
**Student Name:** S.M.Chalani Sankalpana  
**Registration Number:** 22ug1-0481  
**Degree:** BSc (Hons) in Engineering in Information and Communication Engineering  

---

## 1. Project Overview
This project demonstrates an end-to-end software testing lifecycle for the **Moodle LMS (v4.3.12)**. It covers requirement analysis, manual testing, UI automation, API testing, performance evaluation, and security auditing.

*   **Target Application:** https://github.com/moodle/moodle
*   **Version:** 4.3.12 (Stable)
*   **Environment:** Localhost via XAMPP (Apache, MySQL, PHP)
*   **Training Video:** [PASTE YOUR GOOGLE DRIVE OR YOUTUBE LINK HERE]

---

## 2. Testing Environment
*   **OS:** Windows 10
*   **Web Server:** Apache (XAMPP)
*   **Database:** MySQL / phpMyAdmin
*   **Browsers:** Google Chrome
*   **Testing Tools:** 
    *   **UI Automation:** Selenium (Python)
    *   **API Testing:** Postman
    *   **Performance:** Apache JMeter 5.6.3
    *   **Security:** OWASP ZAP
    *   **Accessibility:** WAVE Evaluation Tool

---

## 3. Repository Structure
*   📂 `01_Requirements_TestPlan/`: RTM and Test Plan.
*   📂 `02_Manual_Testing/`: Excel sheet with 50+ Test Cases.
*   📂 `03_Automation_Scripts/`: Selenium Python scripts.
*   📂 `04_API_Testing/`: Postman Collections.
*   📂 `05_Performance_Testing/`: JMeter scripts and reports.
*   📂 `06_Security_Accessibility/`: OWASP and WCAG checks.
*   📂 `07_Evidence/`: Screenshots of results and defects.

---

## 4. How to Run the Tests
### UI Automation
Run: `python test_create_course_admin.py` in the automation folder.

### API Testing
Import the `.json` collection from the API folder into Postman.

### Performance Testing
Open the `.jmx` file in JMeter and click 'Start'.
