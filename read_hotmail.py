import subprocess
import imaplib
import email
from bs4 import BeautifulSoup

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

        print("Total Messages from " + email_code + ": ", len(selected_mails[0].split()))
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
                    if 'instagram' in str(email_code):
                        print("Subject:", subject)
                        if "is your Instagram code" in str(subject).strip():
                            code = subject.strip().split(" ")[0]
                            return code
                    if "tiktok" in str(email_code):
                        print("Subject:", subject)
                        if "is your verification code" in str(subject).strip():
                            code = subject.strip().split(" ")[0]
                            return code
        return None
    except Exception as ex:
        print("ex " + str(ex))
        return None


# username = "latrinas1671@outlook.com"
# password = "XiUIljVpe7"
# email_code = "registration@facebookmail.com"
# getCodeMail(username, password, email_code)

def get_verify_link(username, password, from_email):
    username = str(username)
    app_password = str(password)
    gmail_host = 'imap-mail.outlook.com'
    mail = imaplib.IMAP4_SSL(gmail_host)
    try:
        mail.login(username, app_password)
        mail.select("INBOX")
        _, selected_mails = mail.search(None, '(FROM "' + from_email + '")')
        print("Total Messages from " + from_email + ": ", len(selected_mails[0].split()))
        # list_data = []
        # for num in selected_mails[0].split():
        #     # email_data = {}
        #     _, data = mail.fetch(num, '(RFC822)')
        #     _, bytes_data = data[0]
        #     email_message = email.message_from_bytes(bytes_data)
        #     for part in email_message.walk():
        #         if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
        #             message = part.get_payload(decode=True)
        #             data_text = str(message.decode())
        #             index = data_text.find('<p class="otp">')
        #             # code = data_text[index + 15] + data_text[index + 16] + data_text[index + 17] + data_text[
        #             #     index + 18] + data_text[index + 19] + data_text[index + 20]
        #             # list_data.append(int(code))
        #             print("Email Verified")
        #             return True

        for message_id in selected_mails[0].split():
            _, msg_data = mail.fetch(message_id, "(RFC822)")
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Trích xuất nội dung HTML từ email
            html_content = None
            for part in email_message.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True).decode("utf-8")
                    break

            if html_content:
                # Sử dụng BeautifulSoup để phân tích cú pháp HTML
                soup = BeautifulSoup(html_content, "html.parser")

                # Tìm phần tử <a> với href chứa chuỗi "reddit.com/verification/"
                link_element = soup.find("a", href=lambda href: href and "reddit.com/verification/" in href)
                if link_element:
                    # Trích xuất URL từ phần tử <a>
                    link_url = link_element["href"]
                    print("URL to click:", link_url)
                    print("-----")
                    return link_url

        print("cannot get verify link")
        return None
    except:
        print("cannot get verify link")
        return None
