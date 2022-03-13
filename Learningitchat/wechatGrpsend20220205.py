# coding=utf8
import itchat
import time

'''
This python program calls itchat to group send greetings.
For all wechat friends, whose remarks (备注) modified to be of the format AAAAA-BBBB-X (ie, with two "-" and a last capital letter)
where BBBB will be used in the greetings as nickname and X specifies which group they each belongs
Delete the "x" in one of the items in rank_list will enable the corresponding group to be sent greetings (this is the only switch controls sending)
'''
def happy_holiday(): 
    itchat.auto_login(hotReload=True)       ## 登录微信，要扫描登录
    users = itchat.get_friends(update=True)[0:] ## 获取所有的微信好友
    ## 一些统计变量
    num_total = 0 #微信好友总数
    num_send = 0 #信息发出个数   
    ## 一些应用变量
    user_name = 'filehelper'  #用于测试但实际运行时也不需要改变    
    rank_list = ['xC', #customers
                      'xD', #distributors
                      'xF', #friends
                      'xG', #government officials
                      'xR', #relatives
                      'xS', #seniors
                      'xV', #vendors
                      'T'] #for test only
                      
    mssg_list = ['c新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #C
                      'd新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #D
                      'f新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #F
                      'g新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #G
                      'r新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #R
                      's新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #S
                      'v新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞', #V
                      't新年好！细雨吟春诗醉酒，和风吻柳虎呈祥。在壬寅虎年到来之际，愿岁序常易,福悦日新！感恩您一直以来的支持和帮助，祝愿您和家人节日快乐、健康平安！— 鹏飞']  #T                
                  
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
            user_name = item['UserName'] #测试时需要comment out
            name = name.split()[0] ## 排除一些奇奇怪怪的昵称以及空字符串
            
            if name != "":         
                print("UserName = {}, name = {}".format(item['UserName'], name))
                
                if rank in rank_list:
                  message = name
                  message += mssg_list[rank_list.index(rank)] #rank_list和mssg_list中各项准确对应同样序号
                  itchat.send(msg=message, toUserName = user_name) 
                  num_send += 1
                                
            else:
              print("Empty Remarks! UserName = {}, name = {}".format(item['UserName'], name))                        
            time.sleep(.5)   ## 不要发得太频繁，以免发生一些不必要的麻烦
 
        except Exception as e:
            print("Not Send{}: {}".format(item['UserName'], e))
            
    print(num_total, num_send)
 
### main program
if __name__ == '__main__':
 
    print('... start ...')
    happy_holiday()
    print("... end ...")
