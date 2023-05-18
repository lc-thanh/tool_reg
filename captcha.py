import requests
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def convert_captcha():
    print("convert_captcha")
    index_loop = 0
    while True:
        index_loop = index_loop + 1
        if index_loop > 3:
            return False

        url = "http://14.225.44.214:5555/recaptcha/v2"
        payload = {}
        files = [
            ('file', ('captcha_file.mp3', open('captcha_file.mp3', 'rb'), 'audio/mpeg'))
        ]
        response = requests.request("POST", url, data=payload, files=files)
        response_text = str(response.text).strip()
        print("response " + response_text)

        if "None" == response_text or response.status_code != 200:
            continue

        return str(response.text)

print(convert_captcha())


def by_captcha(browser):
    print("by_captcha")
    sleep(2)
    try:
        # browser.switch_to.frame(browser.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]'))
        browser.switch_to.frame(WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]'))))
        sleep(3)
        print("reCAPTCHA")
        browser.find_element(By.ID, 'recaptcha-anchor').click()
        sleep(3)
        browser.switch_to.default_content()
        sleep(2)
        try:
            browser.switch_to.frame(
                browser.find_element(By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]'))
            sleep(2)
            bt_audio = browser.find_element(By.ID, 'recaptcha-audio-button')
            bt_audio.click()
            sleep(6)
            # audio-source
            audio_src = browser.find_element(By.ID, 'audio-source').get_attribute('src')
            content = requests.get(audio_src).content
            # save the content into a file where you would want to
            open('captcha_file.mp3', 'wb').write(content)
            value = convert_captcha()
            input_result = browser.find_element(By.ID, 'audio-response')
            input_result.click()
            sleep(2)
            input_result.send_keys(value)
            sleep(2)
            input_result.send_keys(Keys.ENTER)
            print("CLICKw")
            sleep(3)
            browser.switch_to.default_content()
            return True
        except Exception as ex:
            print("try again " + ex)
            browser.get(str(browser.current_url))
            sleep(20)
            return by_captcha(browser)
            # browser.switch_to.default_content()

    except Exception as ex:
        print("error 2 " + str(ex))
        browser.switch_to.default_content()
        sleep(2)

    return False
