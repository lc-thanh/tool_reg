# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess
import imaplib
import email

from email.header import decode_header


# Subject: FB-56099 is your Facebook confirmation code
def get_code_fb(sub):
    print("get_code_fb")
    sub = str(sub).strip()
    try:
        sub_slipt = str(sub).split(" ")[0]
        return int(str(sub_slipt.split("-")[1]).strip())
    except:
        return None


def getCodeMail(username, password, email_code):
    username = str(username)
    app_password = str(password)
    gmail_host = 'imap-mail.outlook.com'
    mail = imaplib.IMAP4_SSL(gmail_host)
    try:
        mail.login(username, app_password)
        mail.select("INBOX")
        _, selected_mails = mail.search(None, '(UNSEEN FROM "' + email_code + '")')

        print("Total Messages from ", len(selected_mails[0].split()))
        for num in selected_mails[0].split():
            rv, data = mail.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return
            for response_part in data:
                print("response_part " + str(response_part))
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                        # decode the email subject
                    print("From:", From)
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    print("Subject:", subject)
                    if 'facebook' in str(email_code):
                        print("Subject:", subject)
                        if "is your Facebook confirmation code" in str(subject).strip():
                            code = get_code_fb(subject)
                            return code
        return None
    except Exception as ex:
        print("ex " + str(ex))
        return None


# username = "latrinas1671@outlook.com"
# password = "XiUIljVpe7"
# email_code = "registration@facebookmail.com"
# getCodeMail(username, password, email_code)
