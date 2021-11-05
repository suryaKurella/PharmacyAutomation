from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

course_name = "F21 PHAR 5195 Sterile Products Checkoff"
file_path = "./Files/IAGrader Assignment in ExamSoft PHAR5158.xlsx"
print("Reading File ", file_path)

df = pd.read_excel(file_path, usecols="A, B, E")

print("File Reading Done!")

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

# Grader name getters, this only get names when u have 0 people in grader group
available_grader_rows = "//div[@id='selectGradersTable_wrapper']//img[contains(@src,'add')]//parent::a//parent::td//parent::tr//td//input[@checked='checked']//parent::td//parent::tr"
available_grader_name = "//div[@id='selectGradersTable_wrapper']//img[contains(@src,'add')]//parent::a//parent::td//parent::tr//td[2]"

# after open grader events

grader_name_on_ui = "//span[@class='graderName']"
student_rows_unchecked = "//div[@id='availableETsTable_wrapper']//input[@type='checkbox'][not(contains(@checked,'checked'))]//parent::td//parent::tr"
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

driver.implicitly_wait(common_time)

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
        all_pencil_boxes[i].click()

        wait_till_invisibility(By.ID, loading_after_grade_click, 3 * common_time)
        just_clicker(By.XPATH, grade_first_checkBox_clicked)
        just_clicker(By.ID, save_btn_assign)
        driver.execute_script("arguments[0].focus();", all_pencil_boxes[i])

    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    all_available_grader_rows = driver.find_elements(By.XPATH, available_grader_rows)

    # print("======================================")
    # for i in range(len(all_available_grader_rows)):
    #     print((driver.find_elements(By.XPATH, available_grader_rows + "//td[2]")[i]).text.strip())
    # print("======================================")

    # print("The row num is ")
    # print("length of rows = ", len(all_available_grader_rows))

    for i in range(len(all_available_grader_rows)):
        # print(f'i value main loop = {i}')

        current_grader = (driver.find_element(By.XPATH, ("(" + available_grader_rows + "//td[2])[1]"))).text.strip()

        # print(("(" + available_grader_rows + "//td[2])[1]"))
        # print("Current grader on main loop = ", current_grader)
        # current_grader = text_getter(By.XPATH, available_grader_rows+"//td[2]")
        # print(available_grader_rows[i]+"//td[2]")

        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, available_grader_rows + "//td[3]//a"))))

            # driver.find_elements(By.XPATH, available_grader_rows + "//td[3]//a")[i].click()
        except:
            print('lol')

        wait_till_invisibility(By.ID, loading_after_grade_click, 3 * common_time)
        waiter(By.XPATH, grader_name_on_ui, 4 * common_time)

        # print('current_grader on front page   = ', current_grader)
        # print('current_grader on grder open page    = ', text_getter(By.XPATH, grader_name_on_ui))

        if text_getter(By.XPATH, grader_name_on_ui) == current_grader:
            for index, row in df.iterrows():
                candidate_last_name_excel = row['Last Name'].strip()
                candidate_first_name_excel = row['First Name'].strip()
                candidate_corresponding_grader_excel = row['Grader Assignment'].strip()

                # print('candidate_corresponding_grader_excel = ', candidate_corresponding_grader_excel)
                # print('current grader on open page = ', text_getter(By.XPATH, grader_name_on_ui))

                if candidate_corresponding_grader_excel == current_grader:

                    for num in range(len(driver.find_elements(By.XPATH, "//div[@id='availableETsTable_length']//a"))):
                        try:
                            # WebDriverWait(driver, 2).until(
                            #     EC.element_to_be_clickable(
                            #         (By.XPATH, "(//div[@id='availableETsTable_length']//a)[" + str((num + 1)) + "]")))

                            # just_clicker(By.XPATH, "(//div[@id='availableETsTable_length']//a)[" + str((num + 1)) + "]")
                            just_clicker(By.XPATH, "(//div[@id='availableETsTable_length']//a)[2]")

                            wait_till_invisibility(By.ID, loading_after_grade_click, common_time)
                        except:
                            print("In excepter for " + str(num) + " th time")
                            break

                    html = driver.find_element_by_tag_name('html')
                    html.send_keys(Keys.END)
                    # just_clicker(By.XPATH, "//th[contains(@aria-label,'Last Name')]")
                    # wait_till_invisibility(By.ID, loading_after_grade_click, common_time)

                    all_available_unchecked_student_rows = driver.find_elements(By.XPATH, student_rows_unchecked)

                    for j in range(len(all_available_unchecked_student_rows)):
                        # print(f'j value = {j}')
                        last_name_on_ui = (driver.find_elements(By.XPATH, student_rows_unchecked + "//td[2]"))[
                            j].text.strip()
                        first_name_on_ui = driver.find_elements(By.XPATH, student_rows_unchecked + "//td[3]")[
                            j].text.strip()

                        # print(f'last_name_on_ui = {last_name_on_ui}')
                        # print(f'first_name_on_ui  = {first_name_on_ui}')
                        # print(f'candidate_first_name_excel = {candidate_first_name_excel}')
                        # print(f'candidate_last_name_excel = {candidate_last_name_excel}')

                        if first_name_on_ui.lower() == candidate_first_name_excel.lower() and last_name_on_ui.lower() == candidate_last_name_excel.lower():
                            # print(f'first_name_on_ui and candidate_first_name_excel matches')

                            WebDriverWait(driver, 3).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, student_rows_unchecked + "//td[1]//input")))

                            driver.execute_script("arguments[0].scrollIntoView();", (
                                driver.find_elements(By.XPATH, student_rows_unchecked + "//td[1]//input"))[j])

                            driver.execute_script("arguments[0].click();", (
                                driver.find_elements(By.XPATH, student_rows_unchecked + "//td[1]//input"))[j])
                            # (driver.find_elements(By.XPATH, student_rows_unchecked + "//td[1]//input"))[j].click()
                            break

                        # sleep(1)

            try:
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.ID, save_btn_assign))))
                wait_till_invisibility(By.ID, loading_after_grade_click, 3 * common_time)
            except:
                print('lel')

                break

                # break

                # if
                #
                # print(candidate_last_name_excel, candidate_first_name_excel, candidate_corresponding_grader_excel)
