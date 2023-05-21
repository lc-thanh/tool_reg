from common_element import *
from CONSTANT_gspread import *
from read_hotmail import getCodeMail
from reg_insta import tao_ngay_sinh_random


def reg_tiktok(browser, wks, index_account, account):
    print("Starting reg Tiktok...")

    def click_send_code():
        click_elment_xpath(browser, '//input[@placeholder="Enter 6-digit code"]')
        sleep(1)
        # Nhấn nút "Send code"
        if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
            sleep(5)
            index_resend_code = 0  # Số lần bấm resend code
            # Nếu nhấn "Send code" xong bị lỗi
            while has_element_xpath(browser, '//div[@type="error"]', 1):
                print("has error notification")
                if index_resend_code > 7:
                    return False
                click_elment_xpath(browser, '//input[@placeholder="Enter 6-digit code"]')
                sleep(1)
                # Nhấn nút "Send code"
                if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
                    sleep(2)
                    if has_element_xpath(browser, '//div[@id="captcha_container"]', 1):
                        print("waiting for captcha")
                        sleep(10)

                index_resend_code += 1

            return True
        else:
            click_send_code()

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
        if click_elment_xpath(browser, '//div[@id="Month-options-list-container"]/..'):
            sleep(1)
            index_month = int(birthday.split("/")[1]) - 1
            if not click_elment_id(browser, f'Month-options-item-{index_month}'):
                error += 1
                print("trying again...")
                sleep(2)
                continue
            sleep(random.uniform(1.8, 3.0))
        else:
            error += 1
            print("trying again...")
            sleep(2)
            continue

        # Chọn ngày
        if click_elment_xpath(browser, '//div[@id="Day-options-list-container"]/..'):
            sleep(1)
            index_day = int(birthday.split("/")[0]) - 1
            if not click_elment_id(browser, f'Day-options-item-{index_day}'):
                error += 1
                print("trying again...")
                sleep(2)
                continue
            sleep(random.uniform(1.8, 3.0))
        else:
            error += 1
            print("trying again...")
            sleep(2)
            continue

        # Chọn năm
        if click_elment_xpath(browser, '//div[@id="Year-options-list-container"]/..'):
            sleep(1)
            year = birthday.split("/")[2]
            if not click_elment_xpath(browser, f'//div[contains(@id,"Year-options-item-") and text()="{year}"]'):
                error += 1
                print("trying again...")
                sleep(2)
                continue
            sleep(random.uniform(1.8, 3.0))
        else:
            error += 1
            print("trying again...")
            sleep(2)
            continue

        if input_value_by_xpath(browser, '//input[@name="email"]', email):
            if input_value_by_xpath(browser, '//input[@type="password"]', password + "#"):
                sleep(2)
                if not click_send_code():
                    print("click_send_code error, trying again... ")
                    error += 1
                    sleep(2)
                    continue
            else:
                error += 1
                print("trying again...")
                sleep(2)
                continue
        else:
            error += 1
            print("trying again...")
            sleep(2)
            continue

        error_code = 0
        while True:
            if error_code > 3:
                wks.update(COL_EMAIL_STATUS + str(index_account), 'Account FAIL')
                return False

            code = getCodeMail(email, password, "noreply@account.tiktok.com")
            if code is not None:
                input_value_by_xpath(browser, '//input[@placeholder="Enter 6-digit code"]', code)
                click_elment_xpath(browser, '//button[@type="submit"]')
                sleep(7)
                if has_element_xpath(browser, '//div[@type="error"]'):
                    click_send_code()
                    error_code += 1
                    continue

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
                print("code is None, trying again...")
                error_code += 1
                click_send_code()
