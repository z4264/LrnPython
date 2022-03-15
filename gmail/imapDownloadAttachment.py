# %%
import imaplib, email, os
from email.header import decode_header

imap_url = "imap.gmail.com"
# Environment variables set in ~/.zshrc
usrname = os.environ.get("GM_USR")
passwd = os.environ.get("GM_PWD")
# Where you want your attachments to be saved (ensure this directory exists)
#When there is space in path use "r" string
attachment_dir = r'/Users/pengfeimacbook18/Library/CloudStorage/OneDrive-Personal/Workspace 2/LrnPython/gmail/attatchment' 

# %%
# sets up the auth
def auth(usrname, passwd,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(usrname, passwd)
    return con

# %%
con = auth(usrname, passwd,imap_url)

# %%
con.list()

# %%

con.select('PerformanceReview')

# %%
#search for a particular email
def search(key,value,con):
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data

# %%

msgb = search('From', 'roy.peng@bekencorp.com', con)
msgb

# %%
#extracts emails from byte array
def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

# %%
# allows you to download attachments
def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        #处理一下中文附件名
        if decode_header(fileName)[0][1] == 'utf-8':
            fileName = decode_header(fileName)[0][0].decode("utf-8")
        # print(fileName)
        # print(type(fileName))
        # print(decode_header(fileName))
        # print(type(decode_header(fileName)))
        # print(decode_header(fileName)[0][0].decode("utf-8"))
        # print(type(decode_header(fileName)[0][0]))
        
        if bool(fileName):
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))


# %%
msgs = get_emails(msgb)
for msg in msgs:
    raw = email.message_from_bytes(msg[0][1])
    get_attachments(raw)


# %%
# extracts the body from the email
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)


# %%
get_body(raw)

# %%
con.select('test')
msgb = search('From', 'sam@bekencorp.com', con)
msgb
msgs = get_emails(msgb)
for msg in msgs:
    raw = email.message_from_bytes(msg[0][1])
    get_attachments(raw)


