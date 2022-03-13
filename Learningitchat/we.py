# coding=utf8
import itchat
import time

'''
This python program calls itchat to group send greetings.
For all wechat friends, whose remarks (备注) modified to be of the format AAAAA-BBBB-X (ie, with two "-" and a last capital letter)
where BBBB will be used in the greetings as nickname and X specifies which group they each belongs
1. When testing,comment out line "#user_name = item['UserName'] #######!!!测试时需要comment out!" and all message will be sent to filehelper
2. Change single letter label in rank_list initalization to "xX" e.g. "xC", will disable sending message to that group.
'''

def happy_holiday(): 
    itchat.auto_login(hotReload=True)       ## 登录微信，要扫描登录
    users = itchat.get_friends(update=True)[0:] ## 获取所有的微信好友
    ## 一些统计变量
    num_total = 0 #微信好友总数
    num_send = 0 #信息发出个数   
    ## 一些应用变量
    user_name = 'filehelper'  #用于测试但实际运行时也不需要改变    
    rank_list = ['C', #customers
                 'D', #distributors
                 'F', #friends
                 'G', #government officials
                 'R', #relatives
                 'S', #seniors
                 'V', #vendors
                 'xT'] #for test only
                      
    mssg_list = ['早！节后第一天，开工大吉！祝新的一年生意兴隆，财源广进！', #C
                 '早！春节过得好吧，节后第一天，开工大吉！新的一年，咱们一起继续努力，生意更上层楼，祝幸运相伴，成功相随！', #D
                 '早！节后第一天，开工大吉！新的一年祝工作轻松愉快，身体健康平安，成就相伴相随！', #F
                 '早！节后第一天，开工大吉！新的一年祝工作轻松愉快，身体健康平安，事业随心而成！', #G
                 '早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！', #R
                 '早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！', #S
                 '早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！', #V
                 '早！节后开工第一天，祝新的一年工作轻松愉快，身体健康平安！']  #T                
                  
    sent_user_list = [] #用于检测防止出现重复发送

    ## 直接遍历每个好友，然后根据自己的需求设置一些相关的约束条件，决定是否发送以及发送什么内容
    for item in users:
 
        if "-" in item['RemarkName']:
            rank = item['RemarkName'].split("-")[-1]
            name = item['RemarkName'].split("-")[-2]
        else:
            name = ""
 
        ## 根据用户昵称发送祝福信息
        ## 备注无‘-’的用户：其昵称默认为空字符串并且不发消息
        
        try:
            num_total += 1
            #user_name = item['UserName'] #######!!!测试时需要comment out!
            name = name.split()[0] ## 排除一些奇奇怪怪的昵称以及空字符串
            
            if name != "":         
                print("UserName = {}, name = {}".format(item['UserName'], name))
                
                if (rank in rank_list) and (item['UserName'] not in sent_user_list):
                  message = name
                  message += mssg_list[rank_list.index(rank)] #rank_list和mssg_list中各项准确对应同样序号
                  itchat.send(msg=message, toUserName = user_name) 
                  num_send += 1
                  sent_user_list.append(item['UserName'])
                                
            else:
              print("Empty Remarks! UserName = {}, name = {}".format(item['UserName'], name))                        
            time.sleep(2)   ## 不要发得太频繁，以免发生一些不必要的麻烦
 
        except Exception as e:
            print("Not Send{}: {}".format(item['UserName'], e))
            print("Not Send{}: {}".format(item['RemarkName'], e))
            
    print(num_total, num_send)
 
### main program
if __name__ == '__main__':
 
    print('... start ...')
    happy_holiday()
    print("... end ...")
