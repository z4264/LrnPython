# coding=utf8
import itchat
import time
## python2 需要加上如下语句：中文问题
# import sys
# from imp import reload
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
 
#### 核心部分
## 安装 itchat: pip install itchat （本文是基于 Anaconda3 进行安装的）
## 获取所有的微信好友：users = itchat.get_friends(update=True)[0:]
## users 是一个list。list中的每个元素都是个字典，本文用到的键值如下：
### RemarkName：你给好友备注的昵称
### UserName：好友的用户名，是个主键
## itchat.send(msg, toUserName = user_name)     ## 根据用户名发送给指定的好友
 
 
def happy_holiday():
 
    itchat.auto_login(hotReload=True)       ## 登录微信，要扫描登录
    users = itchat.get_friends(update=True)[0:] ## 获取所有的微信好友
 
    ## 一些统计变量
    num_total = 0
    num_send = 0
 
    ## 直接遍历每个好友，然后根据自己的需求设置一些相关的约束条件，决定是否发送以及发送什么内容
    for item in users:
 
        if "-" in item['RemarkName']:
            #pfz name = item['RemarkName'].split("-")[-1]
            name = item['RemarkName'].split("-")[-1]
        else:
           #pfz name = item['RemarkName']
            name = ""
 
        ## 根据用户昵称发送祝福信息
        ## 没给备注的用户：其昵称默认为空字符串
        ## 发送消息时，获取键值为 UserName 的主键（获取指定的用户）
        ## 测试时，可发送给 filehelper 文件传输助手: toUserName='filehelper'
        ## itchat.send(u"祝{}2019除夕&&新年快乐哈，身体健康，顺顺利利~".format(name), toUserName='filehelper')
        try:
            num_total += 1
            user_name = item['UserName']
            name = name.split()[0] ## 排除一些奇奇怪怪的昵称以及空字符串, hhhh
            if name != "":  ## 
                num_send += 1
                print("UserName = {}, name = {}".format(item['UserName'], name))
                #pfz itchat.send(u"^^祝{}: 2019除夕&&新年快乐哈，身体健康，顺顺利利~".format(name), toUserName = user_name)     
                itchat.send(u"^^祝{}: 2019除夕&&新年快乐哈，身体健康，顺顺利利~".format(name), toUserName = 'filehelper')               
            # else:
            #     print("UserName = {}, name = {}".format(item['UserName'], name))
            #     # itchat.send(u'%s %s %s'%("祝 ", item['NickName'], " 2018除夕&&新年快乐哈~"), toUserName = user_name)
            
            time.sleep(.5)   ## 不要发得太频繁，以免发生一些不必要的麻烦
 
        except Exception as e:
            print("Not Send{}: {}".format(item['UserName'], e))
 
 
    print(num_total, num_send)
 
### main program
if __name__ == '__main__':
 
    print('... start ...')
    happy_holiday()
    print("... end ...")
