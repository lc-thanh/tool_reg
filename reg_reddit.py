import random
from common_element import *
from CONSTANT_reddit_gspread import *
from captcha import by_captcha


def reg_reddit(browser, wks, index_account, account):
    browser.get("https://www.reddit.com/account/register/")
    waitWebLoading(browser)

    email = str(account.get("ID"))
    password = str(account.get("Password"))
    error = 0
    while True:
        if error > 3:
            print("reg error > 3. exit...")
            return False
        if input_value_by_xpath(browser, '//input[@id="regEmail"]', email):
            if click_elment_xpath(browser, '//button[@data-step="email"]'):
                waitWebLoading(browser, 5)
                if input_value_by_xpath(browser, '//input[@id="regUsername"]', email.split("@")[0]):
                    if input_value_by_xpath(browser, '//input[@id="regPassword"]', password):
                        # print("captcha")
                        # by_captcha(browser)
                        # sleep(5)
                        print("waiting for captcha")
                        sleep(30)
                        if not click_elment_xpath(browser, '//button[@data-step="username-and-password"]'):
                            error += 1
                            continue

                        waitWebLoading(browser, 10)
                        gender = account.get("Sex")
                        if gender is None or gender == "":
                            gender = random.choice([True, False]) and 'male' or 'female'
                            wks.update(COL_SEX + str(index_account), gender)

                        if gender == 'male':
                            click_elment_xpath(browser, '//input[@data-testid="MALE"]/..')
                        else:
                            click_elment_xpath(browser, '//input[@data-testid="FEMALE"]/..')

                        sleep(5)
                        if has_element_xpath(browser, "//div[contains(text(),'Interests')]"):
                            interest_buttons = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
                                (By.XPATH, "//div[contains(text(),'Interests')]/../../button")))
                            for _ in range(random.randint(5, 10)):
                                button = random.choice(interest_buttons)
                                sleep(0.5)
                                button.click()
                                sleep(2)
                            sleep(7000)

                            select_all_buttons = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
                                (By.XPATH, "//button[contains(text(),'Select All')]")))
                            for _ in range(random.randint(1, 3)):
                                button = random.choice(select_all_buttons)
                                sleep(0.5)
                                button.click()
                                sleep(2)
                            sleep(7)

                        if has_element_xpath(browser, "//div[contains(text(),'Style your avatar')]"):
                            click_elment_xpath(browser, "//button[contains(text(),'Randomize')]")
                            sleep(7)
                            click_elment_xpath(browser, "//button[contains(text(),'Continue')]")

                        sleep(10)
                        click_elment_xpath(browser, "//button[contains(text(),'Got it')]")
                        sleep(5)
                        click_elment_xpath(browser, "//button[contains(text(),'Got it')]")
                        sleep(2000)
                        return True

        error += 1
        continue
