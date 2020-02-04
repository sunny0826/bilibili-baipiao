#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSend(object):
    def __init__(self):
        self.port = 25
        self.smtp_server = "smtp.163.com"
        self.sender_email = os.getenv('SENDER')
        self.receiver_email = os.getenv('RECEIVER')
        self.password = os.getenv('PASS')
        self.message = MIMEMultipart("alternative")
        self.title = ""
        self.html = ""

    def login(self):
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.port)
            self.server.login(self.sender_email, self.password)
        except Exception as e:
            print('邮箱登录错误，原因：{0}'.format(e))

    def send_email(self, img_list):
        self.login()
        self.message["Subject"] = self.title
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message.attach(MIMEText(self.html, "html"))
        if img_list != []:
            for i, img in enumerate(img_list):
                fp = open(img, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                msgImage.add_header('Content-ID', '<image{count}>'.format(count=i))
                self.message.attach(msgImage)
        try:
            self.server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
        except Exception as e:
            print('发送至 %s 失败( %s )' % (self.sender_email, e))
