#!/usr/bin/env python3

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from settings import GetSettings


def send_mail(send_from, send_to, subject, text, attachment,
              server="127.0.0.1"):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open(attachment, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(attachment)
        )
        # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
    msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__ == "__main__":
    settings = GetSettings()
    send_from = settings.send_from
    send_to = settings.email
    subject = settings.subject
    text = settings.text
    attachment = settings.result_file

    send_mail(send_from, send_to, subject, text, attachment)