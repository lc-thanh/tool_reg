import string

from common_element import *
from CONSTANT_gspread import *
from selenium.webdriver.support.select import Select


def reg_garena(browser, wks, index_account, account):
    print("Starting reg Garena...")
    email = str(account.get("ID"))
    password = str(account.get("Password")) + "#"
    username = email.split("@")[0]
    error = 0
    while True:
        if error > 4:
            print("reg error > 3. exit...")
            return False

        browser.get("https://sso.garena.com/universal/register")
        waitWebLoading(browser)

        if not input_value_by_xpath(browser, '//input[@placeholder="Username"]', username):
            error += 1
            print("cannot input, trying reg again...")
            sleep(2)
            continue

        if not input_value_by_xpath(browser, '//input[@placeholder="Password"]', password):
            error += 1
            print("cannot input, trying reg again...")
            sleep(2)
            continue

        if has_element_xpath(browser, "//div[contains(text(),'between 6-15 characters')]"):
            username = username[0:12]
            print("new username: " + str(username))
            input_value_by_xpath(browser, '//input[@placeholder="Username"]', username)
        else:
            if has_element_xpath(browser, "//div[contains(text(),'username has been taken')]"):
                characters = string.ascii_letters + string.digits
                username += ''.join(random.choice(characters) for _ in range(2))
                print("username isn't available")
                print("new username: " + str(username))
                input_value_by_xpath(browser, '//input[@placeholder="Username"]', username)

        if not input_value_by_xpath(browser, '//input[@placeholder="Re-enter password"]', password):
            error += 1
            print("cannot input, trying reg again...")
            sleep(2)
            continue

        if has_element_xpath(browser, "//div[contains(text(),'username has been taken')]"):
            characters = string.ascii_letters + string.digits
            username += ''.join(random.choice(characters) for _ in range(2))
            print("username isn't available")
            print("new username: " + str(username))
            input_value_by_xpath(browser, '//input[@placeholder="Username"]', username)

        if not input_value_by_xpath(browser, '//input[@placeholder="Email"]', email):
            error += 1
            print("cannot input, trying reg again...")
            sleep(2)
            continue

        try:
            selectBirthday = Select(WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]/../../div[5]/select'))))
            selectBirthday.select_by_value("VN")
            sleep(random.uniform(1.8, 3.0))
        except Exception as ex:
            print("select country error")
            print(str(ex))
            error += 1
            continue

        click_elment_xpath(browser, '//button[@type="submit"]')
        if has_element_xpath(browser, "//div[contains(text(),'have been blocked')]"):
            error += 1
            print("have been blocked, trying reg again...")
            sleep(2)
            continue

        sleep(2000)
