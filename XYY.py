# -*- coding:utf-8 -*-
import wx
import os
import winreg
import sys
import json
import requests
##########################                变量初始化
login_url = 'http://222.197.192.59:9090/zportal/login/do'    #校园网认证地址
app_path = sys.argv[0]  #获取当前文件地址
reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"     #注册表地址
name = 'xyw_kust'  # 注册表项值
path = os.path.join(os.path.expanduser("~"), 'Documents')#用户文档文件夹地址
xyw_json = path + '\kmust-xyw.json'  # 配置文件地址
# startup_studio = ''    #开机自启动配置
remember_studio = 0   # 记住密码配置
auto_login_studio = 0 # 自动登录配置
username = ''         # 用户名
password = ''            # 密码
config_dict = dict()        #配置字典
config_dict["remember_studio"] = remember_studio
config_dict["auto_login_studio"] = auto_login_studio
###################################     自启动函数

def startup_on():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, app_path)
        global startup_studio
        startup_studio = 1
    except:
        print('添加失败')
    print('添加成功')
    winreg.CloseKey(key)

def startup_off():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    winreg.DeleteValue(key,name)
    print('删除完成')
    global startup_studio
    startup_studio = 0
    winreg.CloseKey(key)

#############################            获取配置文件

#判断是否已经设置了启动
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
try:
    value, type = winreg.QueryValueEx(key, name)
    print('键值存在')
    print(value, type)
    startup_studio = 1
except:
    print('键值不存在')
    startup_studio = 0
winreg.CloseKey(key)



# 获取配置文件
if os.path.exists(xyw_json):
    print('配置文件存在')
    with open(xyw_json,'r') as f:
        config_dict.update(json.load(f))
        print('配置',config_dict)
        # 初始化参数
        auto_login_studio = config_dict['auto_login_studio']
        remember_studio = config_dict['remember_studio']
        username = config_dict['username']
        password = config_dict['password']
else:
    print('配置文件不存在')


#认证请求体
params = {
'qrCodeId': '请输入编号',
'username': username,
'pwd': password,
'validCode': '验证码',
'validCodeFlag': 'false',
'serviceId': '00b5544a36f9483b968a1b62c4263195',
'ssid': 'bfd0fd2d574e31c6ba728e0a908cdb8f',
'mac': 'a58d9095f45c5a441d27fcdb25878076',
't': 'wireless-v2',
'wlanacname': 'c8c9622958c8e70501e9284a0abec0fc',
# 'url': '00934593e7571f42045dd99e38fa63e2c6f27e15e5c9af77',
'nasip': 'cbde5ddbb5eb03be513e83acf881fb36',
'wlanuserip': '0248bc8e89ffc645550f89422242acca'
}





###############################################################
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='登录器', size=(301, 299),name='frame',style=541072960)
        icon = wx.Icon(r'C:\Users\59673\Pictures\图标\UFO.png')
        self.SetIcon(icon)
        self.qdck = wx.Panel(self)
        self.qdck.SetOwnBackgroundColour((240, 240, 240, 255))
        self.Centre()
        self.an1 = wx.Button(self.qdck,size=(80, 32),pos=(139, 208),label='登录',name='button')

        self.bq1 = wx.StaticText(self.qdck,size=(70, 20),pos=(10, 110),label='    账号:',name='staticText',style=2321)
        self.bq2 = wx.StaticText(self.qdck,size=(70, 20),pos=(10, 150),label='    密码:',name='staticText',style=2321)

        self.bjk1 = wx.TextCtrl(self.qdck,size=(110, 24),pos=(90, 106),value='',name='text',style=0)
        self.bjk1.SetOwnBackgroundColour((224, 224, 224, 255))

        self.bjk2 = wx.TextCtrl(self.qdck,size=(110, 24),pos=(91, 147),value='',name='text',style=wx.TE_PASSWORD)
        self.bjk2.SetOwnBackgroundColour((224, 224, 224, 255))

        self.dxk1 = wx.CheckBox(self.qdck,size=(80, 24),pos=(10, 195),name='remember',label='记住密码')
        self.Bind(wx.EVT_CHECKBOX, self.remember, self.dxk1)
        self.dxk1.SetValue(remember_studio)

        self.dxk2 = wx.CheckBox(self.qdck,size=(80, 24),pos=(10, 215),name='autostart',label='开机自启')
        self.Bind(wx.EVT_CHECKBOX, self.auto_start, self.dxk2)
        self.dxk2.SetValue(startup_studio)

        self.dxk3 = wx.CheckBox(self.qdck,size=(80, 24),pos=(10, 235),name='autologin',label='自动登录')
        self.Bind(wx.EVT_CHECKBOX, self.auto_login, self.dxk3)
        self.dxk3.SetValue(auto_login_studio)

        tpk2_img = wx.Image(r'C:\Users\59673\Pictures\图标\UFO.png').ConvertToBitmap()
        self.tpk2 = wx.StaticBitmap(self.qdck, bitmap=tpk2_img,size=(64, 64),pos=(105, 25),name='staticBitmap',style=0)
        self.Bind(wx.EVT_BUTTON,self.login,self.an1)

###################################################################
        self.bjk1.SetValue(username)
        self.bjk2.SetValue(password)
######################################################################
        #登录函数
    def login(self,event):
        name = self.bjk1.GetValue()
        password = self.bjk2.GetValue()
        print(name,password,'登录')
        config_dict["username"] = name
        config_dict["password"] = password
        with open(xyw_json,'w') as f:
            json.dump(config_dict,f,ensure_ascii=False)
        print("文件地址：",xyw_json)
        resp = requests.post(url=login_url, params=params)
        print(resp)


        # 记住密码函数
    def remember(self,event):
        statue = self.dxk1.GetValue()
        print(statue)
        if statue == False:
            config_dict["remember_studio"] = 0
            print('未选中')
        else:
            print('选中')
            config_dict["remember_studio"] = 1
    # 自启函数
    def auto_start(self,event):
        statue = self.dxk2.GetValue()
        print(statue)
        if statue == False:
            print('未选中')
            startup_off()
        else:
            print('选中')
            startup_on()

    # 自动登录函数
    def auto_login(self,event):
        statue = self.dxk3.GetValue()
        print(statue)
        if statue == False:
            print('未选中')
            config_dict["auto_login_studio"] = 0
        else:
            print('选中')
            config_dict["auto_login_studio"] = 1

class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()