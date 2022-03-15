# coding=utf8
import itchat
import time

'''
This python program calls itchat to print out all friends and write to a comma
separated file
'''

itchat.auto_login(hotReload=True)       ## 登录微信，要扫描登录
users = itchat.get_friends(update=True)[0:] ## 获取所有的微信好友
## 一些统计变量
num_total = 0 #微信好友总数

with open('用户总表.txt', 'a', encoding='utf-8')as f:
  for item in users:
    remark_name = item['RemarkName']
    user_name = item['UserName']
    nick_name = item['NickName']
    prov_name = item['Province']
    city_name = item['City']
    sign_name = item['Signature']
    f.write('Nick=' + nick_name + ',Remark=' + remark_name + ',Province=' + prov_name + ',City=' + city_name + ',User=' + user_name + ',Signature=' + sign_name + '\n')
    num_total += 1
    print(num_total)
    print('Nick=' + nick_name + ',Remark=' + remark_name + ',Province=' + prov_name + ',City=' + city_name + ',User=' + user_name + ',Signature=' + sign_name + '\n')
    #print(remark_name, nick_name, prov_name, city_name, user_name, sign_name)
    #time.sleep(.2)   ## 不要发得太频繁，以免发生一些不必要的麻烦
  
f.close()
