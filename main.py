import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

random_sleep_short = [1, 2, 3]
random_sleep_little_long = [5, 6, 7]


# creating chrome driver
def setting_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=options)


def accept_cookies():
    # random time sleep [1, 2, 3]
    time.sleep(random.choice(random_sleep_short))
    # accept cookies
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button/div[2]/div[2]').click()
    except NoSuchElementException:
        pass


# access tinder website
def access_tinder_website():
    driver.maximize_window()
    driver.get("https://tinder.com/")
    accept_cookies()


def login_to_facebook():
    time.sleep(random.choice(random_sleep_short))
    # click on login
    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]').click()
    time.sleep(random.choice(random_sleep_short))
    # click login with facebook
    driver.find_element(By.XPATH,
                        '/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]/div/div').click()

    time.sleep(random.choice(random_sleep_little_long))
    # switch to Facebook window
    driver.switch_to.window(window_name=driver.window_handles[1])
    # enter facebook credentials
    driver.find_element(By.NAME, "email").send_keys(os.environ['MAIL'] + Keys.TAB + os.environ['PASSWORD'])
    time.sleep(random.choice(random_sleep_little_long))
    # click facebook login
    driver.find_element(By.NAME, 'login').click()


# location and notification pop up
def handle_tinder_extra_pop_up():
    driver.switch_to.window(window_name=driver.window_handles[0])
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]')))

    # switch back to tinder window
    # Allow location and enable notifications
    for i in range(2):
        time.sleep(random.choice(random_sleep_short))
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]').click()


# swiping in tinder left/right
def tinder_swipe(swipe_direction, number_of_swipes):
    if swipe_direction == 2:
        WebDriverWait(driver, 20).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, f'/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[{swipe_direction}]/button/span')))
    else:
        time.sleep(random.choice([10, 12]))

    for _ in range(number_of_swipes):
        time.sleep(random.choice([2, 3]))
        try:
            driver.find_element(By.XPATH,
                                f'/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[4]/div/div[{swipe_direction}]/button/span').click()
        # for the first swipe div is div[3]
        except (ElementNotInteractableException, NoSuchElementException):
            driver.find_element(By.XPATH,
                                f'/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[{swipe_direction}]/button/span').click()
        # for extra pop up (Home Screen, MATCH)
        except ElementClickInterceptedException:
            try:
                driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/button[2]/div[2]/div[2]').click()
            # if we get a match
            except NoSuchElementException:
                match_info = driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div').text.split(
                    '\n')
                print(f"you have a match with {match_info[0]}, age {match_info[1]}")
                driver.find_element(By.CSS_SELECTOR, 'itsAMatch a').click()

# CODE START HERE #
driver = setting_chrome_driver()
access_tinder_website()
login_to_facebook()
handle_tinder_extra_pop_up()
# swipe left (div # 2 for swipe left)
tinder_swipe(swipe_direction=2, number_of_swipes=10)
# swipe right (div # 4 for swipe left)
tinder_swipe(swipe_direction=4, number_of_swipes=10)

# close the browser after 100 seconds
time.sleep(100)
driver.quit()