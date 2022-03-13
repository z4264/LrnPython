import itchat
from time import time, ctime
from pprint import pprint

# user_name = 'filehelper'  #这是文件传输助手的UserName可用作测试

# 登录微信
# itchat.auto_login(hotReload=True) #第一次扫码登录后下次不需扫码但容易死机
itchat.auto_login()

# 获取所有的微信好友
users = itchat.get_friends(update=True)[0:]
list_to_greet = []

# Greeting messages for each group of diff type of friends
messages = {
    "C": "早！节后第一天，开工大吉！祝新的一年生意兴隆财源广进！",
    "D": "早！新的一年继续努力，生意更上层楼，祝幸运相伴，成功相随！",
    "F": "早！节后第一天，开工大吉！新的一年祝工作轻松愉快!",
    "G": "早！新的一年祝工作轻松愉快，身体健康平安，事业随心而成！",
    "R": "早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！",
    "S": "早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！",
    "V": "早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！",
    "T": "测试一下",
}

# For information only, not used in program
type_keys = [
    "C",  # customers
    "D",  # distributors
    "F",  # friends
    "G",  # government officials
    "R",  # relatives
    "S",  # seniors
    "V",  # vendors
    "T",  # for test only
]

# Collect all friends to greet and construct the sorted List
for user in users:

    if len(user["RemarkName"].split("-")) == 3:

        user_type = user["RemarkName"].split("-")[-1]
        user_salute = user["RemarkName"].split("-")[-2]
        user_msg = f"{user_salute}{messages[user_type]}"

        user_realname = user["RemarkName"].split("-")[0]
        user_name = user["UserName"]

        friend_to_greet = {
            "fType": user_type,
            "fRealName": user_realname,
            "fMsg": user_msg,
            "fName": user_name,
        }

        list_to_greet.append(friend_to_greet)

list_sorted = sorted(list_to_greet, key=lambda i: i["fType"])
# pprint(list_sorted)

# Write the list with messages to a file
with open("List_of_Greetings.txt", "a", encoding="utf-8") as f:
    f.write(ctime() + "\n")  # record current time
    for each in list_sorted:
        f.write(
            f"Type={each['fType']}, 姓名={each['fRealName']}, Message={each['fMsg']} \n"
        )

# Sending Greetings
for item in list_sorted:
    # itchat.send(
    #    msg=item["fMsg"], toUserName=item["fName"]
    # )  # only enabled when ready to send

    # for test
    pprint(f"msg={item['fMsg']}, toUserName={item['fName']}")
    if item["fType"] == "T":
        itchat.send(msg=item["fMsg"], toUserName=item["fName"])