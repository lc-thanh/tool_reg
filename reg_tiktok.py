from common_element import *
from CONSTANT_gspread import *
from read_hotmail import getCodeMail
from reg_insta import tao_ngay_sinh_random


def reg_tiktok(browser, wks, index_account, account):
    error = 0
    while True:
        if error > 3:
            print("reg_tiktok error, exit...")
            return False

        browser.get("https://www.tiktok.com/signup/phone-or-email/email")
        waitWebLoading(browser)

        email = str(account.get("ID"))
        password = str(account.get("Password"))

        birthday = account.get("Birth day")
        if birthday is None or birthday == "":
            birthday = tao_ngay_sinh_random()

        # Chọn tháng
        click_elment_xpath(browser, '//div[@id="Month-options-list-container"]/..')
        sleep(1)
        index_month = int(birthday.split("/")[1]) - 1
        click_elment_id(browser, f'Month-options-item-{index_month}')
        sleep(random.uniform(1.8, 3.0))

        # Chọn ngày
        click_elment_xpath(browser, '//div[@id="Day-options-list-container"]/..')
        sleep(1)
        index_day = int(birthday.split("/")[0]) - 1
        click_elment_id(browser, f'Day-options-item-{index_day}')
        sleep(random.uniform(1.8, 3.0))

        # Chọn năm
        click_elment_xpath(browser, '//div[@id="Year-options-list-container"]/..')
        sleep(1)
        year = birthday.split("/")[2]
        click_elment_xpath(browser, f'//div[contains(@id,"Year-options-item-") and text()="{year}"]')
        sleep(random.uniform(1.8, 3.0))

        input_value_by_xpath(browser, '//input[@name="email"]', email)

        input_value_by_xpath(browser, '//input[@type="password"]', password + "#")

        click_elment_xpath(browser, '//input[@placeholder="Enter 6-digit code"]')
        sleep(3)
        if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
            sleep(5)
            while has_element_xpath(browser, '//div[@type="error"]'):
                if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
                    sleep(5)

        print("waiting for captcha")
        sleep(10)

        error_code = 0
        while True:
            code = getCodeMail(email, password, "noreply@account.tiktok.com")
            if code is not None:
                input_value_by_xpath(browser, '//input[@placeholder="Enter 6-digit code"]', code)
                click_elment_xpath(browser, '//button[@type="submit"]')
                sleep(10)

                input_value_by_xpath(browser, '//input[@name="new-username"]', email.split('@')[0])
                click_elment_xpath(browser, '//button[@type="submit"]')
                sleep(10)

                hover_on_xpath(browser, '//div[@data-e2e="profile-icon"]')
                click_elment_xpath(browser, '//li[@data-e2e="profile-info"]')
                waitWebLoading(browser, 5)

                profile_url = str(browser.current_url).split('?')[0]
                wks.update(COL_LINK_TIKTOK + str(index_account), profile_url)
                return True

            else:
                print("get code fail, try again...")
                error_code += 1
                if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
                    sleep(5)
                    while has_element_xpath(browser, '//div[@type="error"]'):
                        if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
                            sleep(5)