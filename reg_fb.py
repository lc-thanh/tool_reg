import string

from common_element import *
from read_hotmail import getCodeMail
from CONSTANT_gspread import *

import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
import names


# =================== FACEBOOK REG ACCOUNT ====================

def tao_ngay_sinh_random():
    nam_sinh = random.randint(1985, 2004)
    thang = random.randint(1, 12)

    if thang == 2:
        if nam_sinh % 4 == 0 and (nam_sinh % 100 != 0 or nam_sinh % 400 == 0):
            ngay = random.randint(1, 29)
        else:
            ngay = random.randint(1, 28)
    elif thang in [4, 6, 9, 11]:
        ngay = random.randint(1, 30)
    else:
        ngay = random.randint(1, 31)

    ngay_sinh = f"{ngay:02d}/{thang:02d}/{nam_sinh}"  # Định dạng ngày: dd/mm/yyyy
    return ngay_sinh


def generate_name_by_letters(letters):
    vowels = "aeiou"
    consonants = "".join(set(letters) - set(vowels))
    name = ""
    for i in range(random.randint(4, 6)):
        if i % 2 == 0:
            name += random.choice(consonants)
        else:
            name += random.choice(vowels)
    return name.capitalize()


def generate_name(random_string: str, gender='male'):
    first_name = ""
    last_name = ""

    def isVowels(letter):
        return letter in "aeiouy"

    def vowels_count(count_string: str):
        count = 0
        for char_check in count_string:
            if isVowels(char_check):
                count += 1
        return count

    # Hàm kiểm tra xem chuỗi 'name' có sử dụng để đặt tên được hay không?
    def can_name(name):
        name_vowels_count = vowels_count(name)
        if ((len(name) >= 3) and (name_vowels_count >= int(len(name) / 2))) or \
                ((len(name) >= 4) and (name_vowels_count >= int(len(name) / 2) - 1)):
            return True

        return False

    letters = ""
    random_string += '@'  # Dùng '@' để làm phần tử kết thúc chuỗi
    for char in random_string:
        char = char.lower()

        if (char in string.ascii_lowercase) and (len(letters) < 10):
            letters += char
            continue

        # Nếu first_name chưa được tạo
        if first_name == "":
            # Có thỏa mãn để đặt tên hay không?
            if can_name(letters):
                first_name = letters
                letters = ""
                continue
            else:
                # Nếu không đặt được tên với từ này, thì reset lại letters và chạy tiếp
                letters = ""

        elif last_name == "":  # Nếu first_name tạo rồi, thì tạo last_name
            # Có thỏa mãn để đặt tên hay không?
            if can_name(letters):
                last_name = letters
                return first_name.capitalize(), last_name.capitalize()
            else:
                # Nếu không đặt được tên với từ này, thì reset lại letters và chạy tiếp
                letters = ""

    if first_name != "":
        last_name = names.get_last_name()
        return first_name.capitalize(), last_name.capitalize()

    letters = ""
    for char in random_string:
        char = char.lower()

        if char in string.ascii_lowercase:
            letters += char
            continue
    if len(letters) >= 9:
        first_name = letters[0:int(len(letters) / 2)]
        last_name = letters[int(len(letters) / 2):len(letters)]

    if not can_name(first_name):
        first_name = names.get_first_name(gender=gender)
    if not can_name(last_name):
        last_name = names.get_last_name()

    return first_name.capitalize(), last_name.capitalize()


def reg_fb(browser, wks, index_account, account):
    print("Starting reg Fb...")
    sleep(3)
    error = 0

    account_id = str(account.get("ID"))
    account_password = str(account.get("Password"))

    account_birthday = account.get("Birth day")
    if account_birthday is None or account_birthday == "":
        account_birthday = tao_ngay_sinh_random()

    account_gender = account.get("Sex")
    if account_gender is None or account_gender == "":
        account_gender = (random.randint(0, 100) % 2 != 0) and 'male' or 'female'
        print("Gender: " + str(account_gender))
        wks.update(COL_SEX + str(index_account), str(account_gender))
        sleep(2)

    account_name = account.get("Name")
    if account_name is None or account_name == "":
        account_firstName, account_lastName = generate_name(account_id.split("@")[0], account_gender)
        print("Name: " + str(account_firstName) + " " + str(account_lastName))
        wks.update(COL_NAME + str(index_account), str(account_firstName) + " " + str(account_lastName))
        sleep(2)
    else:
        account_firstName = str(account_name).strip().split(" ")[0]
        account_lastName = str(account_name).strip().split(" ")[1]

    while True:
        if error > 3:
            print("signUp error, exit..")
            return False
        try:

            # Truy cập Facebook
            browser.get("http://facebook.com/me")
            sleep(10)

            # Kiểm tra xem đã login chưa
            try:
                url_check = browser.current_url
                if "profile.php" in url_check:
                    print("logged in")
                    wks.update(COL_LINK_FACEBOOK + str(index_account), str(url_check))
                    if account.get("2FA") is None or account.get("2FA") == "":
                        account_2fa = get_2FA(browser, account)
                        if account_2fa:
                            wks.update(COL_2FA + str(index_account), str(account_2fa))
                            sleep(2)
                            print(f"Done! Close browser: {account_id}")
                            sleep(3)
                            return True
                        else:
                            return False
                    else:
                        return True
            except Exception as ex:
                print(str(ex))

            # Click vào nút Tạo tài khoản mới
            # button_register = browser.find_element(By.XPATH, '//a[@data-testid="open-registration-form-button"]')
            # button_register.click()
            if has_element_xpath(browser, '//a[@data-testid="open-registration-form-button"]'):
                click_elment_xpath(browser, '//a[@data-testid="open-registration-form-button"]', 1)
                sleep(2)
                if not has_element(browser, '#reg_box'):
                    print("retry registration...")
                    error += 1
                    sleep(1)
                    continue

                # Nhập họ, tên
                input_value_by_xpath(browser, '//input[@name="lastname"]', account_lastName)

                input_value_by_xpath(browser, '//input[@name="firstname"]', account_firstName)

                # Nhập sđt/email
                input_value_by_xpath(browser, '//form[@id="reg"]/div[1]/div[2]/div/div[1]/input', account_id)
                sleep(1)
                input_value_by_xpath(browser, '//form[@id="reg"]/div[1]/div[3]/div/div/div[1]/input', account_id)

                # Nhập mật khẩu
                input_value_by_xpath(browser, '//input[@id="password_step_input"]', account_password)
                sleep(random.uniform(1.8, 3.0))
                # Chọn birthday
                try:
                    selectBirthday = Select(WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//select[@name="birthday_year"]'))))
                    year = account_birthday.split("/")[2]
                    selectBirthday.select_by_visible_text(str(year))
                    sleep(random.uniform(1.8, 3.0))
                except Exception as ex:
                    print("select birthday_year error")
                    print(str(ex))

                # Chọn tháng
                try:
                    selectBirthday = Select(WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//select[@name="birthday_month"]'))))
                    month = int(account_birthday.split("/")[1]) - 1
                    selectBirthday.select_by_index(month)
                    sleep(random.uniform(1.8, 3.0))
                except Exception as ex:
                    print("select birthday_month error")
                    print(str(ex))

                # Chọn ngày
                try:
                    selectBirthday = Select(WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//select[@name="birthday_day"]'))))
                    x = int(account_birthday.split("/")[0])
                    selectBirthday.select_by_visible_text(str(x))
                    sleep(random.uniform(1.8, 3.0))
                except Exception as ex:
                    print("select birthday_day error")
                    print(str(ex))

                # Chọn giới tính
                if account_gender == 'female':
                    click_elment_xpath(browser, '//span[@data-name="gender_wrapper"]/span[1]/input')
                else:
                    click_elment_xpath(browser, '//span[@data-name="gender_wrapper"]/span[2]/input')

                # Submit
                click_elment_xpath(browser, '//button[@name="websubmit"]')
                sleep(10)
                waitWebLoading(browser, 5)

                # Nếu có thông báo đăng ký không thành công
                if has_element(browser, '#reg_error_inner'):
                    if has_element_xpath(browser, "//div[contains(text(), 'use the name that')]", 1):
                        print("name error")
                        # account_firstName, account_lastName = generate_name(account_id.split("@")[0], account_gender)
                        account_firstName = names.get_first_name(account_gender)
                        account_lastName = names.get_last_name()
                        print("New name: " + str(account_firstName) + " " + str(account_lastName))
                        wks.update(COL_NAME + str(index_account), str(account_firstName) + " " + str(account_lastName))
                        sleep(2)
                        error += 1
                        continue
                    print("have #reg_error_inner, trying again...")
                    error += 1
                    sleep(2)
                    continue

                # Sau khi bấm nút Submit đăng ký
                # Nếu dính checkpoint
                if "checkpoint" in browser.current_url:
                    print("Facebook checkpoint => Fail, sleep 10s and exit..")
                    sleep(10)
                    wks.update(COL_LINK_FACEBOOK + str(index_account), "checkpoint FAIL")
                    return False

                # Điền email code
                error_code = 0
                while True:
                    if has_element(browser, "#code_in_cliff"):
                        print("have element #code_in_cliff, starting getCodeMail()")

                        fb_code = getCodeMail(account_id, account_password, "registration@facebookmail.com")
                        if fb_code is not None:
                            fb_code = str(fb_code)
                            print("Code is: " + fb_code)
                            input_value_by_xpath(browser,
                                                 '//*[@id="conf_dialog_middle_components"]/div/label/div/input',
                                                 fb_code)
                            sleep(5)
                            if click_elment_xpath(browser, '//button[@name="confirm" and @type="submit"]'):
                                sleep(10)
                                # click_elment_xpath(browser, "//a[contains(text(),'Ok')]")
                                # sleep(5)
                                browser.get("https://www.facebook.com/me")
                                sleep(5)
                                url_check = browser.current_url
                                if "profile.php" in url_check:
                                    print("Reg Account Successfully")
                                    wks.update(COL_LINK_FACEBOOK + str(index_account), str(url_check))

                                    account_2fa = get_2FA(browser, account)
                                    if account_2fa:
                                        wks.update(COL_2FA + str(index_account), str(account_2fa))
                                        sleep(2)
                                        print(f"Done Reg Fb! Account: {account_id}")
                                        sleep(3)
                                        return True
                                    else:
                                        return False

                                elif "checkpoint" in url_check:
                                    print("Facebook checkpoint => Fail, sleep 10s and exit..")
                                    sleep(10)
                                    wks.update(COL_LINK_FACEBOOK + str(index_account), "checkpoint FAIL")
                                    return False

                        else:
                            print("get Fb code error, click to 'Send Email Again' and try again..")
                            if error_code > 3:
                                print("cannot get email code, exit reg...")
                                wks.update(COL_EMAIL_STATUS + str(index_account), "Account FAIL")
                                return False

                            error_code += 1
                            sleep(2)
                            if click_elment_xpath(browser, "//a[contains(@href,'/confirm/resend_code/')]", 2):
                                sleep(10)
                                if has_element_xpath(browser, "//*[contains(text(),'To confirm your email')]"):
                                    click_elment_xpath(browser,
                                                       "(//a[contains(@href,'/change_contactpoint/dialog/')])[2]/../a[2]")
                                    sleep(3)
                                else:
                                    print("can not access to 'Resend email code' site, retry reg...")
                                    sleep(2)
                                    error += 1
                                    break
                            else:
                                error_code += 1
                                browser.get("https://www.facebook.com/")
                                sleep(10)

                    else:
                        print('cannot enter code confirm email, trying again..')
                        sleep(3)
                        error += 1
                        break

        except:
            error += 1
            print(f"signUp error, sleep(5s) and retry..")
            sleep(5)


def get_approvals_code(code):
    totp = pyotp.TOTP(str(code).strip().replace(" ", "")[:32])
    sleep(2)
    return totp.now()


def get_2FA(browser, account):
    print("get_2FA")
    account_password = account.get("Password")
    error = 0
    while True:
        if error > 2:
            print("get 2FA code error, exit..")
            return False

        browser.get("https://www.facebook.com/security/2fac/setup/intro")
        sleep(10)

        if click_elment_xpath(browser, "//a[contains(@href,'2fac/setup/qrcode/generate/')]"):
            sleep(3)
            input_value_by_xpath(browser, '//input[@class="inputpassword autofocus"]', account_password)
            sleep(2)
            click_elment_xpath(browser, "//button[contains(text(),'Submit')]")
            sleep(7)
            code_2fa = get_value_element(browser, "//div[contains(text(), 'Or enter this code')]/../../span[2]")
            if code_2fa:
                if click_elment_xpath(browser, "//div[contains(text(), 'Continue')]"):
                    sleep(5)
                    app_code = get_approvals_code(code_2fa)
                    input_value_by_xpath(browser, '//input[@data-key="0"]', app_code)
                    sleep(10)
                    click_elment_xpath(browser, "//a[contains(@href, '/security/2fac/settings/')]")
                    if has_element_xpath(browser, "//h1[contains(text(), 'Two-factor authentication is on')]"):
                        return code_2fa

        error += 1
        continue
