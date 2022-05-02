import datetime
import smtplib
from email.mime.text import MIMEText
def send_email(message, to_send1, username, rand_id):
    sender = "ilyabudnikjb@gmail.com"
    password = "Budnik1987ss2002ss"


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f"Username: {username}. Почта: {to_send1}. Текст: {message}. Время отправления: {datetime.datetime.now()}. ID: {rand_id}")
        msg["Subject"] = "Обратная связь"
        server.sendmail(sender, sender, msg.as_string())

        return "The message was sent success!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

def main():
    message = ''
    to_send1 = ''
    username = ''
    rand_id = ''
    print(send_email(message=message, to_send1=to_send1, username=username, rand_id=rand_id))
if __name__ == "__main__":
    main()