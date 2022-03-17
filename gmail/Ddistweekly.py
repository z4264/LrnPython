
import imaplib, email, os
from email.header import decode_header

imap_url = "imap.gmail.com"
# Environment variables set in ~/.zshrc
usrname = os.environ.get("GM_USR")
passwd = os.environ.get("GM_PWD")
# Where you want your attachments to be saved (ensure this directory exists)
#When there is space in path use "r" string
attachment_dir = r'/Users/pengfeimacbook18/Library/CloudStorage/OneDrive-Personal/Workspace 2/DistWeekly' 

# sets up the auth
def auth(usrname, passwd,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(usrname, passwd)
    return con

#search for a particular email
def search(key,value,con):
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data


#extracts emails from byte array
def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

# allows you to download attachments
def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        #When filename of attachment is chinese
        if decode_header(fileName)[0][1] == 'utf-8':
            fileName = decode_header(fileName)[0][0].decode("utf-8")
        if decode_header(fileName)[0][1] == 'gb2312':
            fileName = decode_header(fileName)[0][0].decode("gb2312")
        
        if bool(fileName):
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))

con = auth(usrname, passwd,imap_url)
con.select('Weekly')
msgb = search('Subject', '*', con)
msgs = get_emails(msgb)
for msg in msgs:
    raw = email.message_from_bytes(msg[0][1])
    get_attachments(raw)