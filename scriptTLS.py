import math
import os
import sys
import smtplib
import requests

print(sys.version)
print(sys.executable)


def greet(who_to_greet):
    greeting = "Hello, {}!".format(who_to_greet)
    return greeting


print(greet("world"))

r = requests.get("http://www.bekencorp.com")
print(r.status_code)

#environment variables needs to be added to ~/.zshrc
my_usrname=os.environ.get('GM_USR')
my_passwd=os.environ.get('GM_PWD')
print(my_usrname)
print(my_passwd)

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(my_usrname, my_passwd)

    subject = 'How about dinner'
    body = 'Can we go dinner together ?'

    msg = f'Subject: {subject}\n\n{body}'
    smtp.sendmail(my_usrname, 'pengfei@bekencorp.com',msg)

