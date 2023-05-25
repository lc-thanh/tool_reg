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
from reg_fb import reg_fb
from reg_reddit import reg_reddit
from reg_insta import reg_insta
from reg_tiktok import reg_tiktok
from reg_garena import reg_garena


def init_tool(name_sheet, group_gpm, screen_size, is_reg_fb, is_reg_insta, is_reg_reddit, is_reg_tiktok, is_reg_garena):
    print("init tool")
    wks = start_sheet(name_sheet, "main")

    while True:
        index_proxy, proxy = get_proxy_first(name_sheet)
        if proxy is None or proxy == "":
            print("cannot get proxy")
            break

        index_account_on_sheets, account = get_account(wks)
        if account is None:
            print("account is None, exit..")
            refresh_proxy_status(name_sheet)
            break

        start_tool(group_gpm, screen_size, wks, index_account_on_sheets, account, is_reg_fb, is_reg_insta,
                   is_reg_reddit, is_reg_tiktok, is_reg_garena, proxy)

        refresh_proxy_status(name_sheet)
        sleep(3)


def start_tool(group_gpm, screen_size, wks, index_account_on_sheets, account, is_reg_fb, is_reg_insta,
               is_reg_reddit, is_reg_tiktok, is_reg_garena, proxy):
    print("start tool")

    if account is not None:
        account_id = str(account.get("ID"))
        profile_id = str(account.get("Profile ID"))

        browser = None
        try:
            if len(profile_id) < 2:
                """ Nếu trên sheet chưa có đường dẫn Profile thì tạo Profile mới """

                profile_id = create_profile(account_id, group_gpm, proxy)
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

            width = int(screen_size.split('x')[0])
            height = int(screen_size.split('x')[1])
            browser.set_window_rect(0, 0, width, height-60)
            sleep(2)

            have_error = False

            if is_reg_fb:
                if not reg_fb(browser, wks, index_account_on_sheets, account):
                    have_error = True

            if is_reg_insta:
                if not reg_insta(browser, wks, index_account_on_sheets, account):
                    have_error = True

            if is_reg_reddit:
                if not reg_reddit(browser, wks, index_account_on_sheets, account):
                    have_error = True

            if is_reg_tiktok:
                if not reg_tiktok(browser, wks, index_account_on_sheets, account):
                    have_error = True

            if is_reg_garena:
                if not reg_garena(browser, wks, index_account_on_sheets, account):
                    have_error = True

            close_profile(browser)

            if not have_error:
                wks.update(COL_STATUS + index_account_on_sheets, "GOOD")
                sleep(2)

                today = date.today()
                # dd/mm/YY
                d1 = today.strftime("%d/%m/%Y")
                wks.update(COL_DATE + index_account_on_sheets, str(d1))
            else:
                wks.update(COL_STATUS + index_account_on_sheets, "FAIL")

        except Exception as ex:
            print(str(ex))
            wks.update(COL_STATUS + str(index_account_on_sheets), "FAIL")
            if browser is not None:
                close_profile(browser)
            return


# if __name__ == '__main__':
#     init_tool("tool reg")
