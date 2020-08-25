import webbrowser
import time
from PIL import ImageGrab
import cv2
import aircv as ac
class Cbc:
    def __init__(self):
        print("jh class init")
        self.impath = "jh"
    #打开网页
    def openweb(self):
        isopen = False
        print("openweb")
        webbrowser.open("https://ibsbjstar.ccb.com.cn/CCBIS/V6/STY1/CN/login.jsp")
        time.sleep(1)
        while isopen == False:
            im = ImageGrab.grab()
            im.save("assets/"+self.impath+"/a.jpg")
            time.sleep(2)
            findimg = ac.imread("assets/"+self.impath+"/login.jpg")
            maiimg = ac.imread("assets/"+self.impath+"/a.jpg")
            pos = ac.find_template(maiimg, findimg,0.3)
            if pos:
                break
            time.sleep(3)
        print("find it")
        return True
    #输入用户名
    def input_username(self):
        print("input username")
        findimg = ac.imread("assets/jh/username.jpg")
        maiimg = ac.imread('assets/jh/a.jpg')
        pos = ac.find_template(maiimg, findimg, 0.3)
        print("this is username pos",pos)
        #this is username pos {'result': (920.0, 325.0), 'rectangle': ((910, 311), (910, 339), (930, 311), (930, 339)), 'confidence': 0.9712943434715271}
        print(pos['rectangle'][0])
        #(910, 311)

    #输入密码
    def input_password(self):
        print("input password")
    #输入验证码
    def input_verify_code(self,waitingcode):
        print("input verifycode",waitingcode)
        return True
    #登录
    def login(self):
        print("login")
        return True
    def need_verify(self):
        print("need verify")
        return True
    #获取验证码
    def get_verify(self):
        print("get verify")
        return '5678'
    def input_transfer(self):
        print("输入转账信息")
        return True
    def input_ukey_password(self):
        print("输入ukey密码")
    def ukey_push(self):
        print("按压ukey")
        return True

