import json
import time
import os

import websocket
from win32com.client import GetObject
import MySQLdb
import jh
import threading
import pythoncom
#查看检测设备程序是否在运行
def wmi_sql_all_name(pname):
    #子线程中执行wmi需要加初始化
    #pythoncom.CoInitialize()
    _wmi = GetObject('winmgmts:')
    processes = _wmi.ExecQuery("Select * from win32_process where name = '%s'" % (pname))
    #print(len(processes))
    if len(processes) >0:
        # 子线程中执行wmi需要去初始化
        #pythoncom.CoUninitialize()
        return True
    else:
        #pythoncom.CoUninitialize()
        return False
findtarget = wmi_sql_all_name('checkDevice.exe')
#检测设备没有运行则退出主程序
if findtarget ==False:
    #exit()
    print("这里要退出程序")
#开始
#是否正在转账标志
transferFlag = False
#转账信息
transferInfo ={
    "client_name":"none",
    "from_card":"none",
    "total_card":"62170001",
    "money":100.02,
    "total_card_name":"none",
    "total_bank":"none"
}
bankobject = jh.Cbc()
def on_message(ws,message):
    global transferFlag
    #print(json.loads(message))
    rec_result = json.loads(message)
    print(rec_result)
    #time.sleep(200)
    r_type = rec_result['type']
    if r_type == 'submit_data':
        if transferFlag == True:
            print("正在执行上一笔订单")
            p =  {
                     "type": "reply",
                     "content": "订单失败，上一订单未完成",
                     "code":"401",
                     "to_uid":rec_result['from_uid'],
                     "from_uid":rec_result['to_uid']
            }
            ws.send(json.dumps(p))
        else:

            global bankobject
            global waitingcode
            global isverify
            transferFlag = True
            transferInfo['from_uid'] = rec_result['from_uid']
            transferInfo['from_card'] = rec_result['from_card']
            transferInfo['total_card'] = rec_result['total_card']
            transferInfo['money'] = rec_result['money']
            transferInfo['total_card'] = rec_result['total_card']
            transferInfo['total_bank'] = rec_result['total_bank']
            transferInfo['to_uid'] = rec_result['to_uid']
            transferInfo['from_card_bank'] = rec_result['from_bank']
            try:
                db = MySQLdb.connect(host="59.110.174.196",user="root",passwd="17965290",db="fastadmin",charset="utf8")
                cursor = db.cursor()
                sql = "SELECT * FROM fa_user_card where cardNumber = " + transferInfo['from_card']
                cursor.execute(sql)
                data = cursor.fetchone()
                print(data)
                #transferInfo['from_card_bank'] = data[6]
                transferInfo['from_card_password'] = data[3]
                transferInfo['from_card_ukeypassword'] = data[4]
            except Exception as e:
                print(e)
            print("from_card_bank",transferInfo['from_card_bank'])
            if transferInfo['from_card_bank'] == 1:
                print("建行")
                bankobject = jh.Cbc()
            if transferInfo['from_card_bank'] == 2:
                print("工行")
            if bankobject.openweb() == True:
                bankobject.input_username()
                bankobject.input_password()
            #登录需要验证码
            need_verify = bankobject.need_verify()
            if need_verify ==True:
                vcode = bankobject.get_verify()
                print("vcode",vcode)
                contents = {
                    "type":"reply",
                    "content":vcode,
                    "from_uid":transferInfo['to_uid'],
                    "to_uid":transferInfo['from_uid'],
                    "code":"405"
                }
                print(contents)
                ws.send(json.dumps(contents))
            else:
                bank_login = bankobject.login()
                if bank_login == True:
                    input_t = bankobject.input_transfer()
                if input_t == True:
                    bankobject.input_ukey_password()
                if bankobject.ukey_push() == True:
                    print("转账完成")
                    transferFlag = False
                    print("transferFlg:", transferFlag)
                    content = {
                        "type": "reply",
                        "content": "订单完成,order complete",
                        "code": "201",
                        "to_uid": rec_result['from_uid'],
                        "from_uid": rec_result['to_uid']
                    }
                    ws.send(json.dumps(content))
    if r_type =="verification_code":
        if transferFlag == True:
            waitingcode = rec_result['content']
            isRight=bankobject.input_verify_code(waitingcode)
            if isRight == False:
                print("验证码错误，重新输入")
                content={
                    "type": "reply",
                    "content": "验证码错误",
                    "code": "402",
                    "to_uid": rec_result['from_uid'],
                    "from_uid": rec_result['to_uid']
                }
                ws.send(json.dumps(content))
            else:
                bank_login = bankobject.login()
                if bank_login == True:
                    input_t = bankobject.input_transfer()
                if input_t == True:
                    bankobject.input_ukey_password()
                if bankobject.ukey_push() == True:
                    print("转账完成")
                    transferFlag = False
                    print("transferFlg:", transferFlag)
                    content = {
                        "type":"reply",
                        "content":"订单完成,order complete",
                        "code":"201",
                        "to_uid":rec_result['from_uid'],
                        "from_uid":rec_result['to_uid']
                    }
                    ws.send(json.dumps(content))
    if r_type =="get_new_verification_code":
        if transferFlag == True:
            print("重新获取验证码发送给客户端")
            vcode = bankobject.get_verify()
            content = {
                "type": 'verifycode',
                "content": vcode,
                "from_uid": transferInfo['to_uid'],
                "to_uid": transferInfo['client_name']
            }
            ws.send(json.dumps(content))
def on_error(ws,error):
    print(error)
def on_close(ws):
    print("closed!")
def on_open(ws):
    params = {"type":"login","client_name":"028106a4c04e","group_id": '1'}
    ws.send(json.dumps(params))
def th1():
    ws = websocket.WebSocketApp("ws://59.110.174.196:7272", on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=30)
if __name__ == '__main__':
    th1_ = threading.Thread(target=th1)
    th1_.start()
    #webbrowser.open("http://www.163.com")
    print("complete")