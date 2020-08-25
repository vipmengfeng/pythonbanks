#coding = utf-8
#通过每秒ping设备ip进行监测设备是否在线，设备如果在线则打开转账程序进行websocket链接服务器，通知前端应用设备上线，并接受信息
from tools.ping import *
from win32com.client import GetObject
import pythoncom
#设备在线标识，默认False，如果在线则设置其值为 1，离线则设置为 2
onlineFlag = False
#杀死转账程序
def end_program(pname):
    os.system('%s%s' % ("taskkill /F /IM ",pname))
#查询任务管理器是否有转账程序在运行，如果有则返回True（不需要重复打开进程），如果没有则返回False
def wmi_sql_all_name(pname):
    #子线程中执行wmi需要加初始化
    pythoncom.CoInitialize()
    _wmi = GetObject('winmgmts:')
    processes = _wmi.ExecQuery("Select * from win32_process where name = '%s'" % (pname))
    #print(len(processes))
    if len(processes) >0:
        # 子线程中执行wmi需要去初始化
        pythoncom.CoUninitialize()
        return True
    else:
        pythoncom.CoUninitialize()
        return False
    # try:
    #     print(processes[0].ProcessID)
    #     # 子线程中执行wmi需要去初始化
    #     pythoncom.CoUninitialize()
    #     return True
    # except:
    #     print("没有发现程序")
    #     # 子线程中执行wmi需要去初始化
    #     pythoncom.CoUninitialize()
    #     return False
    #     return False
#关闭进程
def shutdown(pname):
    print("====查询任务管理器进程中是否有转账程序在运行===")
    result = wmi_sql_all_name(pname)
    #如果有则关闭
    if result == True:
        print('get it  and ready to shutdown')
        end_program(pname)
    else:
        #没有则不执行任何操作
        print("not found")
#如果进程中没有在运行的转账程序则打开进程，如果有则不进行操作
def open_program(pname):
    if wmi_sql_all_name(pname) == False:
        os.popen(pname)
    else:
        print("设备在线并且程序已经在运行")
        #print()
#ping设备
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
        #设备在线的时候
        onlineFlag = 1
        print("yes，设备在线准备就绪")
        open_program('testexe.exe')
    else:
        #设备离线的时候
        onlineFlag = 2
        print("no","设备离线，请打开设备")
        shutdown('testexe.exe')
    timer = threading.Timer(1,get_alive_ip)
    timer.start()


if __name__ == '__main__':
    timer = threading.Timer(1, get_alive_ip)
    timer.start()