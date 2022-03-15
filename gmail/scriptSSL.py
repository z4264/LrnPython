
import os
import smtplib
import imghdr
from email.message import EmailMessage

#Environment variables set in ~/.zshrc
my_usrname=os.environ.get('GM_USR')
my_passwd=os.environ.get('GM_PWD')

msg = EmailMessage()
msg['Subject'] = 'How about dinner'
msg['From'] = my_usrname
msg['To'] = 'pengfei@bekencorp.com'
msg.set_content('Can we go dinner together ?')

#attach multiple image files
files = ['sample.png', '样品.jpg']

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name
        file_type = imghdr.what(file_name)
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    
#attach pdf file
files = ['combinedminutes.pdf']

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(my_usrname, my_passwd)
    smtp.send_message(msg)

