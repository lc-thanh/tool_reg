import datetime
import json
import threading
from tkinter import *
from tkinter import messagebox

from startup import init_tool
from read_hotmail import getCodeMail, get_verify_link


def main():
    window = Tk()
    window.title("Tool Reg")
    window.geometry("750x310")
    text_button_start = StringVar()
    text_button_start.set("Start")

    label_name_sheet = Label(window, text="Name sheet:  ", font=("Arial", 13))
    label_name_sheet.grid(column=0, row=1)
    label_name_sheet.grid(padx=20, pady=10)
    # path_profile
    txt_name_sheet = Entry(window, font=("Arial", 13), width=50)
    txt_name_sheet.grid(column=1, row=1, columnspan=2)

    label_group_gpm = Label(window, text="Group gpm:", font=("Arial", 13))
    label_group_gpm.grid(column=0, row=2)
    label_group_gpm.grid(padx=20, pady=10)
    txt_group_gpm = Entry(window, font=("Arial", 13), width=50)
    txt_group_gpm.grid(column=1, row=2, columnspan=2)

    label_screen_size = Label(window, text="Screen size:", font=("Arial", 13))
    label_screen_size.grid(column=0, row=3)
    label_screen_size.grid(padx=20, pady=10)
    txt_screen_size = Entry(window, font=("Arial", 13), width=50)
    txt_screen_size.grid(column=1, row=3, columnspan=2)

    checkbox_reg_fb = BooleanVar()
    checkbox_reg_insta = BooleanVar()
    checkbox_reg_reddit = BooleanVar()
    checkbox_reg_tiktok = BooleanVar()
    checkbox_reg_garena = BooleanVar()

    Checkbutton(window, text="Reg Facebook", variable=checkbox_reg_fb, padx=10, pady=10, font=("Arial", 13)).grid(
        column=0,
        row=4)
    Checkbutton(window, text="Reg Instagram", variable=checkbox_reg_insta, padx=10, pady=10, font=("Arial", 13)).grid(
        column=1,
        row=4)
    Checkbutton(window, text="Reg Reddit", variable=checkbox_reg_reddit, padx=10, pady=10, font=("Arial", 13)).grid(
        column=2,
        row=4)
    Checkbutton(window, text="Reg Tiktok", variable=checkbox_reg_tiktok, padx=10, pady=10, font=("Arial", 13)).grid(
        column=0,
        row=5)
    Checkbutton(window, text="Reg Garena", variable=checkbox_reg_garena, padx=10, pady=10, font=("Arial", 13)).grid(
        column=1,
        row=5)

    class thread(threading.Thread):
        def __init__(self, name_sheet, group_gpm, screen_size, is_reg_fb, is_reg_insta, is_reg_reddit, is_reg_tiktok,
                     is_reg_garena):
            super().__init__()
            self.name_sheet = name_sheet
            self.group_gpm = group_gpm
            self.screen_size = screen_size
            self.is_reg_fb = is_reg_fb
            self.is_reg_insta = is_reg_insta
            self.is_reg_reddit = is_reg_reddit
            self.is_reg_tiktok = is_reg_tiktok
            self.is_reg_garena = is_reg_garena

        def run(self):
            print("run")
            init_tool(self.name_sheet, self.group_gpm, self.screen_size, self.is_reg_fb, self.is_reg_insta,
                      self.is_reg_reddit, self.is_reg_tiktok, self.is_reg_garena)

    def start():
        print("start")
        name_sheet = txt_name_sheet.get()
        group_gpm = txt_group_gpm.get()
        screen_size = txt_screen_size.get()
        is_reg_fb = checkbox_reg_fb.get()
        is_reg_insta = checkbox_reg_insta.get()
        is_reg_reddit = checkbox_reg_reddit.get()
        is_reg_tiktok = checkbox_reg_tiktok.get()
        is_reg_garena = checkbox_reg_garena.get()

        if not name_sheet or name_sheet is None or \
                not group_gpm or group_gpm is None or \
                not screen_size or screen_size is None:
            messagebox.showerror("Error", "Input is empty!!")
        else:
            thread_start = thread(name_sheet, group_gpm, screen_size, is_reg_fb, is_reg_insta, is_reg_reddit,
                                  is_reg_tiktok, is_reg_garena)
            thread_start.start()

    def save():
        print("save")
        name_sheet = txt_name_sheet.get()
        group_gpm = txt_group_gpm.get()
        screen_size = txt_screen_size.get()
        is_reg_fb = checkbox_reg_fb.get()
        is_reg_insta = checkbox_reg_insta.get()
        is_reg_reddit = checkbox_reg_reddit.get()
        is_reg_tiktok = checkbox_reg_tiktok.get()
        is_reg_garena = checkbox_reg_garena.get()

        if not name_sheet or name_sheet is None or \
                not group_gpm or group_gpm is None or \
                not screen_size or screen_size is None:
            messagebox.showerror("Error", "Input is empty!!")
        else:
            data = {
                "name_sheet": name_sheet,
                "screen_size": screen_size,
                "group_gpm": group_gpm,
                "is_reg_fb": bool(is_reg_fb),
                "is_reg_insta": bool(is_reg_insta),
                "is_reg_reddit": bool(is_reg_reddit),
                "is_reg_tiktok": bool(is_reg_tiktok),
                "is_reg_garena": bool(is_reg_garena)
            }
            with open("cache.json", "w") as outfile:
                json.dump(data, outfile)
            messagebox.showinfo("Info", "Save Success!!")

    # handle close
    # def on_closing():
    #     name_sheet = txt_name_sheet.get()
    #     try:
    #         if name_sheet is not None or name_sheet:
    #             get_update_close(name_sheet, "account")
    #     except Exception as ex:
    #         print("update " + str(ex))
    #         pass
    #     window.destroy()

    # window.protocol("WM_DELETE_WINDOW", on_closing)

    import os.path
    file_exists = os.path.exists('cache.json')
    if file_exists:
        cache = open('cache.json')
        # a dictionary
        data_cache = json.load(cache)
        txt_name_sheet.delete(0, END)
        txt_name_sheet.insert(0, data_cache['name_sheet'])
        txt_screen_size.delete(0, END)
        txt_screen_size.insert(0, data_cache['screen_size'])
        txt_group_gpm.delete(0, END)
        txt_group_gpm.insert(0, data_cache['group_gpm'])
        checkbox_reg_fb.set(data_cache['is_reg_fb'])
        checkbox_reg_insta.set(data_cache['is_reg_insta'])
        checkbox_reg_reddit.set(data_cache['is_reg_reddit'])
        checkbox_reg_tiktok.set(data_cache['is_reg_tiktok'])
        checkbox_reg_garena.set(data_cache['is_reg_garena'])

    bt_start = Button(window, textvariable=text_button_start, font=("Arial", 19), width=15, bg="green", command=start)
    bt_start.grid(column=0, row=19)
    bt_start.grid(padx=10, pady=10)

    bt_save = Button(window, text="Save", font=("Arial", 19), width=15, bg="yellow", command=save)
    bt_save.grid(column=2, row=19, sticky=E)
    bt_save.grid(padx=10, pady=10)
    window.mainloop()


if __name__ == '__main__':
    main()
    # getCodeMail("bertrandfittingusfx@hotmail.com", "F8PvEK3sLR", "noreply@account.tiktok.com")
    # print("sturkeyhanneloresus"[0:12])
    # get_verify_link("christina_ox292.eser@outlook.com", "a60fs2Ul5", "account@garena.com")
