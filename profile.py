import os
import shutil
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import zipfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from subprocess import CREATE_NO_WINDOW
from webdriver_manager.chrome import ChromeDriverManager

dir_path = os.getcwd()
canvas = dir_path + "/data/ex/canvas"
font = dir_path + "/data/ex/font"
webgl = dir_path + "/data/ex/webgl"
audio = dir_path + "/data/ex/audio"
pathchrome = dir_path + r"\GoogleChromePortable\App\Chrome-bin\chrome.exe"


def open_profile(profile_id, proxy=None):
    index_error = 0
    while True:
        index_error = index_error + 1
        if index_error > 3:
            return None
        try:
            options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 1,
                     "credentials_enable_service": False,
                     "profile.password_manager_enabled": False
                     }
            options.add_experimental_option("prefs", prefs)
            options.add_argument('--disable-notifications')
            options.add_argument("--disable-infobars")
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("start-maximized")
            options.add_experimental_option("detach", True)
            options.add_argument("--disable-extensions")
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            options.add_argument(r"user-data-dir=C:\testProject\profiles" + "\\" + str(profile_id))
            # options.add_argument("--user-data-dir=" + pathprofile)
            # options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('--autoplay-policy=no-user-gesture-required')
            # options.add_argument('--force-dark-mode')
            # if proxy is not None:
            #     proxys = str(proxy).split(":")
            #     if len(proxys) < 3:
            #         options.add_argument(f'--proxy-server={proxy}')
            #     else:
            #         PROXY_HOST = str(proxys[0]).strip()
            #         PROXY_PORT = str(proxys[1]).strip()
            #         PROXY_USER = str(proxys[2]).strip()
            #         PROXY_PASS = str(proxys[3]).strip()
            #         manifest_json = """
            #                                         {
            #                                             "version": "1.0.0",
            #                                             "manifest_version": 2,
            #                                             "name": "Chrome Proxy",
            #                                             "permissions": [
            #                                                 "proxy",
            #                                                 "tabs",
            #                                                 "unlimitedStorage",
            #                                                 "storage",
            #                                                 "<all_urls>",
            #                                                 "webRequest",
            #                                                 "webRequestBlocking"
            #                                             ],
            #                                             "background": {
            #                                                 "scripts": ["background.js"]
            #                                             },
            #                                             "minimum_chrome_version":"22.0.0"
            #                                         }
            #                                         """
            #
            #         background_js = """
            #                                         var config = {
            #                                                 mode: "fixed_servers",
            #                                                 rules: {
            #                                                   singleProxy: {
            #                                                     scheme: "http",
            #                                                     host: "%s",
            #                                                     port: parseInt(%s)
            #                                                   },
            #                                                   bypassList: ["localhost"]
            #                                                 }
            #                                               };
            #
            #                                         chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            #
            #                                         function callbackFn(details) {
            #                                             return {
            #                                                 authCredentials: {
            #                                                     username: "%s",
            #                                                     password: "%s"
            #                                                 }
            #                                             };
            #                                         }
            #
            #                                         chrome.webRequest.onAuthRequired.addListener(
            #                                                     callbackFn,
            #                                                     {urls: ["<all_urls>"]},
            #                                                     ['blocking']
            #                                         );
            #                                         """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
            #
            #         pluginfile = pathprofile + fr"\proxy_auth_plugin.zip"
            #         with zipfile.ZipFile(pluginfile, 'w') as zp:
            #             zp.writestr("manifest.json", manifest_json)
            #             zp.writestr("background.js", background_js)
            #
            #         fantasy_zip = zipfile.ZipFile(pluginfile)
            #         fantasy_zip.extractall(pathprofile)
            #         fantasy_zip.close()
            #         options.add_argument(
            #             '--load-extension=' + canvas + ',' + font + ',' + webgl + ',' + audio + ',' + pathprofile)

            driver = webdriver.Chrome(r"C:\testProject\chromedriver.exe", options=options)
            sleep(5)
            return driver
        except Exception as ex:
            print("error " + str(ex))


def close_profile(browser):
    print("close_browser")
    try:
        sleep(1)
        browser.close()
        print("browser closed")
    except Exception as ex:
        print("close error")
        print(str(ex))
        sleep(5)
