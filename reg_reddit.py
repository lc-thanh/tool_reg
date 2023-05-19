import random
from common_element import *
from CONSTANT_gspread import *
from captcha import by_captcha
from read_hotmail import get_verify_link


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
                                scroll_into_view(browser, button)
                                sleep(2)
                                button.click()
                                sleep(2)

                            click_elment_xpath(browser, "//button[text()='Continue']")
                            sleep(5)

                            select_all_buttons = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
                                (By.XPATH, "//button[contains(text(),'Select All')]")))
                            for _ in range(random.randint(1, 3)):
                                button = random.choice(select_all_buttons)
                                sleep(0.5)
                                scroll_into_view(browser, button)
                                sleep(2)
                                button.click()
                                sleep(2)

                            click_elment_xpath(browser, "//button[text()='Continue']")
                            sleep(5)

                        if has_element_xpath(browser, "//div[contains(text(),'Style your avatar')]"):
                            click_elment_xpath(browser, "//button[contains(text(),'Randomize')]")
                            sleep(7)
                            click_elment_xpath(browser, "//button[contains(text(),'Continue')]")
                            sleep(10)

                        click_elment_xpath(browser, "//button[contains(text(),'Got it')]", 1)
                        sleep(5)
                        click_elment_xpath(browser, "//button[contains(text(),'Got it')]", 1)
                        sleep(5)

                        verify_link = get_verify_link(email, password, "noreply@reddit.com")
                        browser.get(verify_link)
                        waitWebLoading(browser, 5)
                        browser.get("https://www.reddit.com/settings/")
                        waitWebLoading(browser)
                        error_verify = 0
                        while has_element_xpath(browser, "//button[contains(text(), 'resend')]"):
                            if error_verify > 2:
                                wks.update(COL_LINK_REDDIT + str(index_account), "not verify")
                                return False
                            click_elment_xpath(browser, "//button[contains(text(), 'resend')]")
                            sleep(3)
                            verify_link = get_verify_link(email, password, "noreply@reddit.com")
                            browser.get(verify_link)
                            waitWebLoading(browser, 5)
                            browser.get("https://www.reddit.com/settings/")
                            waitWebLoading(browser)
                            error_verify += 1
                        print("email verified")

                        browser.get("https://www.reddit.com/user/me/")
                        waitWebLoading(browser, 5)
                        wks.update(COL_LINK_REDDIT + str(index_account), str(browser.current_url))
                        sleep(2)
                        return True

        error += 1
        continue
