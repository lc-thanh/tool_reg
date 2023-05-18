import os
import random
import threading
from time import sleep
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common_element import click_elment_xpath, has_element
# from gpm_v2.start_gpm_v2 import create_profile, close_profile, get_ip_proxy, delete_profile
from common_gspread import *
from test_Fb_tools import signUp
from profile import open_profile, close_profile


def init_tool(name_sheet):
    print("init tool")
    wks = start_sheet(name_sheet, "Sheet5")

    while True:
        index_account_on_sheets, account = get_account(wks)
        if account is None:
            print("account is None, exit..")
            break

        start_tool(wks, index_account_on_sheets, account)

        sleep(3)

    # index_account_on_sheets, account = get_account_by_index(wks, 81)
    # if account is None:
    #     print("account is None, exit..")
    #     return
    #
    # start_tool(name_sheet, index_account_on_sheets, account)
    #
    # refresh_proxy_status(name_sheet)
    # sleep(3)


def start_tool(wks, index_account_on_sheets, account):
    print("start tool")

    if account is not None:
        account_id = str(account.get("ID"))
        profile_id = str(account.get("Profile ID"))

        try:
            if len(profile_id) < 2:
                print("account does not have profile_id")
                return
            else:
                """ Nếu có đường dẫn Profile rồi thì vào Profile đấy """
                browser = open_profile(str(profile_id))

            if browser is None:
                print("browser error")
                sleep(5)
                # delete_profile(profile_id)
                return

            # sleep(3)
            # browser.set_window_rect(0, 0, 1920, 1080)
            sleep(2)

            if signUp(browser, wks, index_account_on_sheets, account):
                wks.update(COL_STATUS + index_account_on_sheets, "GOOD")
                sleep(2)

                today = date.today()
                # dd/mm/YY
                d1 = today.strftime("%d/%m/%Y")
                wks.update(COL_DATE + index_account_on_sheets, str(d1))
                return
            else:
                wks.update(COL_STATUS + index_account_on_sheets, "FAIL")
                return
        except Exception as ex:
            print(str(ex))
            wks.update(COL_STATUS + str(index_account_on_sheets), "FAIL")
            return


if __name__ == '__main__':
    init_tool("tool reg")
