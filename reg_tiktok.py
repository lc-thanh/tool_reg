from common_element import *
from CONSTANT_gspread import *
from read_hotmail import getCodeMail
from reg_insta import tao_ngay_sinh_random
import bypass_captcha
import cv2
import numpy as np


def reg_tiktok(browser, wks, index_account, account):
    print("Starting reg Tiktok...")

    def tiktok_captcha():
        def get_slider(img1, img2):
            img_boder = bypass_captcha.link_to_img(img1)
            img_in = bypass_captcha.link_to_img(img2)
            pixel = bypass_captcha.Bypass_captcha().rotate(img_boder, img_in)
            print(pixel)
            return int(float(pixel))

        def Drag(pixel):
            slider = browser.find_element(By.XPATH, '//div[@id="secsdk-captcha-drag-wrapper"]/div[2]/div')
            ActionChains(browser).click_and_hold(slider).perform()
            ActionChains(browser).move_by_offset(pixel * 0.25, 0).perform()
            ActionChains(browser).move_by_offset(pixel * 0.25, 0).perform()
            ActionChains(browser).move_by_offset(pixel * 0.25, 0).perform()
            ActionChains(browser).move_by_offset(pixel * 0.25, 0).perform()
            ActionChains(browser).click(slider).perform()

        error_captcha = 0
        while has_element_xpath(browser, '//div[@id="captcha_container" and contains(@style, "display: block")]', 1):
            if error_captcha > 3:
                return False

            print("waiting for captcha")
            # by pass captcha tiktok
            try:
                while True:
                    imgs = browser.find_elements(By.XPATH, '//img[@draggable="false"]')
                    left = get_slider(imgs[0].get_attribute('src'), imgs[1].get_attribute('src'))
                    Drag(left)
                    sleep(2)
                    slider2 = browser.find_element(By.XPATH, '//div[@id="secsdk-captcha-drag-wrapper"]/div')
                    if slider2.is_displayed():
                        continue
                    else:
                        break
            except Exception as ex:
                print(ex)

            try:
                img_captcha = browser.find_element(By.ID, 'captcha-verify-image')
                link = str(img_captcha.get_attribute('src'))
                print("link captcha " + link)

                index_random = random.randint(100, 9999999)
                filename = "captcha_object" + str(index_random) + ".png"
                bypass_captcha.download_img(link, filename)
                sleep(4)
                try:
                    with open(filename, "rb") as image:
                        file = image.read()
                        # convert to numpy array
                        image = np.asarray(bytearray(file))

                        # RGB to Grayscale
                        image = cv2.imdecode(image, -1)[:, :, :3][:, :, ::-1]
                        # image = bypass_captcha.link_to_img(img_link)
                        position1, position2 = bypass_captcha.Bypass_captcha().object(image)
                        # print(position1, position2)
                        sleep(5)
                        print("position1 " + str(position1))
                        print("position2 " + str(position2))
                        ac = ActionChains(browser)
                        ac.move_to_element(img_captcha).move_by_offset(position1[0],
                                                                       position1[1]).click().perform()
                        sleep(1)
                        ac = ActionChains(browser)
                        ac.move_to_element(img_captcha).move_by_offset(position2[0],
                                                                       position2[1]).click().perform()
                        sleep(1)
                        browser.find_element(By.XPATH, '//*[@id="captcha_container"]/div/div[3]/div[2]').click()
                        sleep(5)
                        return True
                except Exception as ex:
                    print("error " + ex)
                    error_captcha += 1
                    sleep(3)
                    continue
            except Exception as ex:
                print(str(ex))
                error_captcha += 1
                sleep(10)
                continue

    def click_send_code(index_resend_code=0):
        click_elment_xpath(browser, '//input[@placeholder="Enter 6-digit code"]')
        sleep(1)
        # Nhấn nút "Send code"
        if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
            sleep(5)
            # Nếu nhấn "Send code" xong bị lỗi
            while has_element_xpath(browser, '//div[@type="error"]', 1):
                print("has error notification")
                print("index_resend_code = " + str(index_resend_code))
                if index_resend_code > 7:
                    return False
                click_elment_xpath(browser, '//input[@placeholder="Enter 6-digit code"]')
                sleep(1)
                # Nhấn nút "Send code"
                if click_elment_xpath(browser, '//button[@data-e2e="send-code-button"]'):
                    sleep(5)
                    tiktok_captcha()

                index_resend_code += 1

            tiktok_captcha()
            if has_element_xpath(browser, '//div[@type="error"]', 1):
                click_send_code(index_resend_code + 1)
            return True
        else:
            click_send_code(index_resend_code + 1)

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
                    if not click_send_code():
                        print("click_send_code error, trying reg again... ")
                        error += 1
                        sleep(2)
                        break
                    error_code += 1
                    continue

                input_value_by_xpath(browser, '//input[@name="new-username"]', email.split('@')[0])
                click_elment_xpath(browser, '//button[@type="submit"]')
                sleep(5)
                waitWebLoading(browser, 7)

                hover_on_xpath(browser, '//div[@data-e2e="profile-icon"]')
                click_elment_xpath(browser, '//li[@data-e2e="profile-info"]')
                waitWebLoading(browser, 5)

                profile_url = str(browser.current_url).split('?')[0]
                wks.update(COL_LINK_TIKTOK + str(index_account), profile_url)
                return True

            else:
                print("code is None, trying again...")
                error_code += 1
                if not click_send_code():
                    print("click_send_code error, trying reg again... ")
                    error += 1
                    sleep(2)
                    break
