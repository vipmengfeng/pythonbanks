#coding=utf-8
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tools.ping import *
import websocket
import json
onlineFlag = 0
threadState = {}
params={
    "type":"login",
    "client_name":"meng",
    "room_id":1
}
def on_message(ws,message):
    print(json.loads(message))
def on_error(ws,error):
    print(error)
def on_close(ws):
    print("closed!")
def on_open(ws):
    params = {"type":"login","client_name":"meng","room_id": '1'}
    ws.send(json.dumps(params))
def get_alive_ip():
    global onlineFlag
    s = AliveScan()
    ipPool = set()
    with open('ip.txt') as file_obj:
        ips = file_obj.read()
        ips_list = ips.split('\n')
        ipPool = set(ips_list[:20])
        # print ipPool
        alive_ip_set = set()
        for ip in ipPool:
            alive_ips = s.hot_ping(set([ip, ]))
            if alive_ips:
                alive_ip_set = alive_ip_set | alive_ips
    l = alive_ip_set
    l2 = len(l)
    if l2 > 0:
        onlineFlag = 1
        print("yes")
    else:
        onlineFlag = 2
        print("no")
    timer = threading.Timer(5,get_alive_ip)
    timer.start()
    #return alive_ip_set

def thread_two(tid):
    global onlineFlag
    global ws
    while True and threadState[tid]:
        ws = websocket.WebSocketApp("ws://59.110.174.196:7272", on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever(ping_timeout=30)
        ws.keep_running = False
        if onlineFlag == True:
            print("it is online")


        else:

            print("it is offline")
class testingThread(threading.Thread):
    def __init__(self,threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        print(str(self.threadID) + " Starting thread")
        print(threading.current_thread().getName())
        self.ws = websocket.WebSocketApp("ws://59.110.174.196:7272", on_message=on_message, on_error=on_error,on_open=on_open, on_close=on_close)
        self.ws.keep_running = True
        self.wst = threading.Thread(target=self.ws.run_forever)
        #self.wst.daemon = True
        self.wst.start()
        running = True;
        testNr = 0;
        time.sleep(3.1)
        while True:
            time.sleep(0.01)
            if onlineFlag == 2:
                self.ws.keep_running = False
                print(str(self.threadID) + " Exiting thread")
                break
        # #
        # global onlineFlag
        # print("线程内部onlineglag",onlineFlag)
        # if onlineFlag == 2:
        #     self.ws.keep_running = False
        #     print(str(self.threadID) + " Exiting thread")
        print("线程运行完毕结束")
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print("开始线程：")
        threadState[self.ident] = True
        thread_two(self.ident)
        print("退出线程")
    def stop(self):
        threadState[self.ident] = False
        while self.isAlive():
            time.sleep(0.001)
        return 'stoped'
    def restart(self):
        if self.stop() == 'stoped':
            self.run()
def test(tid):
    a = 0
    while True and threadState[tid]:
        a +=1
        print('-'*10+str(a)+'-'*10)
        time.sleep(0.5)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # websocket.enableTrace(True)
    timer = threading.Timer(5, get_alive_ip)
    timer.start()
    t = testingThread("222")

    while True:
        time.sleep(5)
        print(onlineFlag)

        if onlineFlag == 1:
            print("线程是否存活",t.is_alive())
            if t.is_alive() == True:
                print("already running")
            else:
                print("没有运行，现在开始")
                t.start()
                print("是否存活" , t.is_alive())
            print(t.ident)
            #break
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
