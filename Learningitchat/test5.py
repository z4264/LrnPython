import itchat,xlwt      #调用第三方库


def login_call():       #用来让我们知道登陆成功
    print('成功登陆')

itchat.auto_login(hotReload=True,loginCallback=login_call) #登陆微信
friend_data=itchat.get_friends(update=True)     #获取微信好友信息，参数为更新，可不写
#print(friend_data)  #可以把注释符号去掉看一下输出

'''总体来说就是这种  [{***},******] 列表里包含着很多个字典
每个好友就对应一个字典，每个字典用js格式存着各种信息'''
#'Sex','NickName','City','UserName','Signature'这是我想要的，你们也可以自己去字典找你们想用的

friend = []     #新建一个空列表
for i in range(len(friend_data)):   #循环*次，*为字典个数，也就是你好友的数量
    sex = friend_data[i].get('Sex')     #get到性别
    nickname = friend_data[i].get('NickName')   #get到昵称
    city = friend_data[i].get('City')    #get到次城市
    signature = friend_data[i].get('Signature')     #get到个性签名
    username = friend_data[i].get('UserName')   
    remarkname = friend_data[i].get('RemarkName')
    afdata = [sex,nickname,city,signature,username,remarkname]    #每次get到的都是一个好友的信息，把它们装进列表
    friend.append(afdata)   #把好友的列表信息装进上面建好的空列表
'''经过上面的for循环就把每个好友的信息装进friend中
大概是这个样子的  [[***],******]   '''
print(friend)

