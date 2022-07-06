import smtplib
from email.mime.text import MIMEText
from email.header    import Header

service_email = 'service@dancinginfire.ru'
service_password = 'Swsu2016'


def sendmail(email, link):

    dest_email = email
    subject = 'Подтверждение регистрации на сайте dancinginfire.ru'
    email_text = "Перейдите, пожалуйста, по ссылке для подтверждения почты\n" + str(link)

    msg = MIMEText(email_text, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = service_email
    msg['To'] = dest_email

    server = smtplib.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(service_email, service_password)
    server.auth_plain()
    server.sendmail(service_email, dest_email, msg.as_string())

    server.quit()








