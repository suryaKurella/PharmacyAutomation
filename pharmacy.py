from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

course_name = "F21 PHAR 5195 Sterile Products Checkoff"

# PATHS
user_id_homepage = 'userid'
password_id_homepage = 'password'
login_homepage_click = "//a[@id='emLoginLink']"

# After login PATHS
after_login_headline = "//th[@class='ugheadline']"
assesments_ref_path = "Assessments"

# Selecting the course
course_headline = "//div[@class='headline']"
course_headline_current_text = "//div[@class='headline'][contains(text(),'" + course_name + "')]"
grade_link = 'gradingLink'
loading_after_grade_click = 'animationCancelText'

# edit clicks
first_time_edit_click = "(//img[contains(@src, 'edit-green')])[2]"
all_edit_pencils_grader_tab = "//div[@id='selectGradersTable_wrapper']//img[contains(@src,'edit-green')]"

# after form open
grade_first_checkBox_clicked = "//div[@id='availableETsTable_wrapper']//input[@checked='checked']"
save_btn_assign = "saveETAssignmentBtn"
# commons
common_time = 10


# Functions
def waiter(by_type, path, time):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located((by_type, path)))


def sen_keys(by_type, path, time, text):
    waiter(by_type, path, time)
    driver.find_element(by_type, path).send_keys(text)


def just_clicker(by_type, path, time=common_time):
    waiter(by_type, path, time)
    driver.find_element(by_type, path).click()


def text_getter(by_type, path, time=common_time):
    waiter(by_type, path, time)
    return driver.find_element(by_type, path).text


def wait_till_invisibility(by_type, path, time=common_time):
    wait = WebDriverWait(driver, time)
    wait.until(EC.invisibility_of_element_located((by_type, path)))


username = 'skurella'
password = 'Aug@2021'

driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe')

driver.get('https://ei.examsoft.com/GKWeb/login/uhpharm')

sen_keys(By.ID, user_id_homepage, common_time, username)
sen_keys(By.ID, password_id_homepage, common_time, password)

just_clicker(By.XPATH, login_homepage_click, common_time)

waiter(By.XPATH, after_login_headline, 2 * common_time)

just_clicker(By.LINK_TEXT, assesments_ref_path)

waiter(By.XPATH, course_headline_current_text, 4 * common_time)

print(text_getter(By.XPATH, course_headline_current_text))

if course_name in text_getter(By.XPATH, course_headline_current_text):
    print("Yay course name found")
    just_clicker(By.ID, grade_link)
    wait_till_invisibility(By.ID, loading_after_grade_click, 3 * common_time)
    just_clicker(By.XPATH, first_time_edit_click)
    wait_till_invisibility(By.ID, loading_after_grade_click, 3 * common_time)
    sleep(5)

    all_pencil_boxes = driver.find_elements(By.XPATH, all_edit_pencils_grader_tab)

    for i in range(len(all_pencil_boxes)):
        waiter(By.XPATH, all_pencil_boxes[i], 4 * common_time)
        all_pencil_boxes[i].click()

        wait_till_invisibility(By.ID, loading_after_grade_click, 3 * common_time)
        just_clicker(By.XPATH, grade_first_checkBox_clicked)
        just_clicker(By.ID, save_btn_assign)
        driver.execute_script("arguments[0].focus();", all_pencil_boxes[i])
