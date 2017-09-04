# -- coding:utf-8
import smtplib
from email.mime.text import MIMEText

class BeaverBotSender(object):
    def __init__(self):
        self.sender = 'beaver4276@daum.net'
        self.receivers = ['sunkyu4276@gmail.com']

        self.server = smtplib.SMTP_SSL('smtp.daum.net', port=465)
        self.server.ehlo()

        self.server.login('beaver4276',"")

    def send(self, subject, message):
        subject = "[BeaverBot] " + subject
        msg = MIMEText(message)
        msg['Subject'] = subject
        self.server.sendmail(self.sender, self.receivers, msg.as_string())
        self.server.quit()
        print("Successfully sent email")

    def test(self):
        subject = "[BeaverBot] SMTP TEST"
        message = """
        SMTP TEST 테스트 입니다.
        """
        msg = MIMEText(message)
        msg['Subject'] = subject
        self.server.sendmail(self.sender, self.receivers, msg.as_string())
        self.server.quit()
        print("Successfully sent email")