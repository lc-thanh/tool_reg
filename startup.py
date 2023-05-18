import os
import random
import threading
from time import sleep
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common_element import click_elment_xpath, has_element
from gpm_v2.start_gpm_v2 import create_profile, open_profile, close_profile, get_ip_proxy, delete_profile
from common_gspread import *
from reg_fb import fb_signUp, get_2FA
from reg_reddit import reg_reddit
from reg_insta import regInsta


def init_tool(name_sheet):
    print("init tool")
    wks = start_sheet(name_sheet, "reg insta")

    while True:
        # index_proxy, proxy = get_proxy_first(name_sheet)
        # if proxy is None or proxy == "":
        #     print("cannot get proxy")
        #     break

        index_account_on_sheets, account = get_account(wks)
        if account is None:
            print("account is None, exit..")
            refresh_proxy_status(name_sheet)
            break

        # start_tool(wks, index_account_on_sheets, account, proxy)
        start_tool(wks, index_account_on_sheets, account, proxy=None)

        refresh_proxy_status(name_sheet)
        sleep(3)


def start_tool(wks, index_account_on_sheets, account, proxy=None):
    print("start tool")

    if account is not None:
        account_id = str(account.get("ID"))
        profile_id = str(account.get("Profile ID"))

        browser = None
        try:
            if len(profile_id) < 2:
                """ Nếu trên sheet chưa có đường dẫn Profile thì tạo Profile mới """

                profile_id = create_profile(account_id, "reg", proxy)
                wks.update(COL_PROFILE_ID + str(index_account_on_sheets), str(profile_id))
                sleep(3)
                browser = open_profile(profile_id)
            else:
                """ Nếu có đường dẫn Profile rồi thì vào Profile đấy """
                browser = open_profile(profile_id)

            if browser is None:
                print("browser error")
                sleep(5)
                delete_profile(profile_id)
                return

            browser.set_window_rect(0, 0, 1920, 1080)
            sleep(2)

            if regInsta(browser, wks, index_account_on_sheets, account):
                wks.update(COL_STATUS + index_account_on_sheets, "GOOD")
                sleep(2)

                today = date.today()
                # dd/mm/YY
                d1 = today.strftime("%d/%m/%Y")
                wks.update(COL_DATE + index_account_on_sheets, str(d1))
            else:
                wks.update(COL_STATUS + index_account_on_sheets, "FAIL")

            close_profile(browser)

        except Exception as ex:
            print(str(ex))
            wks.update(COL_STATUS + str(index_account_on_sheets), "FAIL")
            if browser is not None:
                close_profile(browser)
            return


if __name__ == '__main__':
    init_tool("tool reg")
