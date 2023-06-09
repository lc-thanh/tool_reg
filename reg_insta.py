import string

from common_element import *
from read_hotmail import getCodeMail
from reg_fb import generate_name
from CONSTANT_gspread import *


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


def reg_insta(browser, wks, index_account, account):
    print("Starting reg Insta")
    error = 0
    username = str(account.get("ID")).split('@')[0]

    while True:
        if error > 2:
            print("REG INSTA ERROR, exit...")
            return False

        browser.get("https://www.instagram.com/")
        waitWebLoading(browser, 5)

        if not click_elment_xpath(browser, "//a[contains(@href, 'accounts/emailsignup/')]"):
            error += 1
            print("cannot click 'Sign up' button, trying again...")
            sleep(2)
            continue

        if not has_element_xpath(browser, '//input[@name="emailOrPhone"]', 2):
            if has_element_xpath(browser, "//a[contains(@href,'/direct/inbox/')]"):
                if after_reg(browser, wks, index_account):
                    return True

            error += 1
            continue

        email = str(account.get("ID"))
        password = str(account.get("Password"))

        gender = account.get("Sex")
        if gender is None or gender == "":
            gender = random.choice([True, False]) and 'male' or 'female'
            wks.update(COL_SEX + str(index_account), gender)
            sleep(1)

        fullName = account.get("Name")
        if fullName is None or fullName == "":
            name1, name2 = generate_name(email.split('@')[0], gender=gender)
            fullName = name1 + " " + name2
            wks.update(COL_NAME + str(index_account), fullName)
            sleep(1)

        birthday = account.get("Birth day")
        if birthday is None or birthday == "":
            birthday = tao_ngay_sinh_random()
            wks.update(COL_BIRTHDAY + str(index_account), birthday)

        input_value_by_xpath(browser, '//input[@name="emailOrPhone"]', email)
        input_value_by_xpath(browser, '//input[@name="fullName"]', fullName)
        input_value_by_xpath(browser, '//input[@name="username"]', username)
        input_value_by_xpath(browser, '//input[@name="password"]', password)

        click_elment_xpath(browser, '//input[@name="username"]')
        if not click_elment_xpath(browser, '//button[@type="submit"]'):
            error += 1
            print("cannot click submit button, trying reg again...")
            sleep(2)
            continue
        sleep(5)

        if has_element(browser, "#ssfErrorAlert"):
            if has_element_xpath(browser, '//input[@name="username" and @aria-describedby="ssfErrorAlert"]'):
                characters = string.ascii_letters + string.digits
                username += ''.join(random.choice(characters) for _ in range(3))
                print("username isn't available")
                print("new username: " + str(username))

            print("try again...")
            error += 1
            sleep(2)
            continue

        # Chọn birthday
        try:
            selectBirthday = Select(WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//select[@title="Year:"]'))))
            year = birthday.split("/")[2]
            selectBirthday.select_by_visible_text(str(year))
            sleep(random.uniform(1.8, 3.0))
        except Exception as ex:
            print("select birthday_year error")
            print(str(ex))

        # Chọn tháng
        try:
            selectBirthday = Select(WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//select[@title="Month:"]'))))
            month = int(birthday.split("/")[1]) - 1
            selectBirthday.select_by_index(month)
            sleep(random.uniform(1.8, 3.0))
        except Exception as ex:
            print("select birthday_month error")
            print(str(ex))

        # Chọn ngày
        try:
            selectBirthday = Select(WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//select[@title="Day:"]'))))
            x = int(birthday.split("/")[0])
            selectBirthday.select_by_visible_text(str(x))
            sleep(random.uniform(1.8, 3.0))
        except Exception as ex:
            print("select birthday_day error")
            print(str(ex))

        if not click_elment_xpath(browser, "//button[contains(text(),'Next')]"):
            print("cannot click 'Next' button")
            print('try again..')
            error += 1
            sleep(2)
            continue

        error_email_code = 0
        while has_element_xpath(browser, '//input[@name="email_confirmation_code"]'):
            if error_email_code > 2:
                wks.update(COL_EMAIL_STATUS + str(index_account), 'Account FAIL')
                break
            email_code = getCodeMail(email, password, "no-reply@mail.instagram.com")
            if email_code is not None:
                email_code = str(email_code)
                print("Code is: " + email_code)

                input_value_by_xpath(browser, '//input[@name="email_confirmation_code"]', email_code)
                sleep(2)
                click_elment_xpath(browser, '//button[@type="submit"]')
                sleep(5)

                if has_element_xpath(browser, "//*[contains(text(),\"That code isn't valid\")]") \
                        or has_element_xpath(browser, "//*[contains(text(),'something went wrong')]"):
                    click_elment_xpath(browser, "//div[contains(text(),'Resend Code.')]")
                    sleep(5)
                    continue

                if "suspended" in browser.current_url:
                    print("checkpoint => Fail, sleep 10s and exit..")
                    sleep(10)
                    wks.update(COL_LINK_INSTA + str(index_account), "checkpoint")
                    return False

                wks.update(COL_LINK_INSTA + str(index_account), "Reg Success")

                if after_reg(browser, wks, index_account):
                    return True
                else:
                    error += 1
                    break

            else:
                print("cannot get email code")
                error_email_code += 1
                sleep(3)
                print("try get code again..")
                click_elment_xpath(browser, "//div[contains(text(),'Resend Code.')]")
                sleep(5)
                continue

        error += 1
        print("try again..")
        continue


def after_reg(browser, wks, index_account):
    click_elment_xpath(browser, "//button[contains(text(),'Not Now')]")

    try:
        follow_buttons = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[text()='Follow']/../..")))
        for _ in range(random.randint(5, 10)):
            button = random.choice(follow_buttons)
            sleep(0.5)
            scroll_into_view(browser, button)
            sleep(2)
            button.click()
            sleep(2)

    except Exception as ex:
        print(str(ex))
        return False

    sleep(3)
    click_elment_xpath(browser, "//div[contains(text(), 'Profile')]/../../..")
    waitWebLoading(browser, 5)
    if has_element_xpath(browser, '//a[@href="/accounts/edit/"]'):
        wks.update(COL_LINK_INSTA + str(index_account), browser.current_url)
        sleep(1)

    return True
