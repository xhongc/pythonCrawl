import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])
    return 'nihao'

itchat.auto_login(hotReload=True)
itchat.run()