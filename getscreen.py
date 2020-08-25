import win32api,win32con
import time
import os
import pyautogui
import webbrowser
pyautogui.PAUSE=0.5
time.sleep(1)
#pyautogui.hotkey("win")
screenWidth,screenHeight = pyautogui.size()
currentMouseX,currentMouseY = pyautogui.position()
print(currentMouseX)
print(currentMouseY)
webbrowser.open("http://www.163.com")
#os.system(r'"C:/Program Files/Internet Explorer/iexplore.exe" http://www.163.com')
time.sleep(8)
pyautogui.moveTo(449,266)
pyautogui.click()

w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

while True:
    time.sleep(2)
    print(w)
    print(h)
    localtime = time.asctime(time.localtime((time.time())))
    file1 = open("C:/Users/meng/Desktop/test.txt","a")
    file1.writelines(str(w))
    file1.writelines(str(h))
    file1.writelines("----------------------")
    file1.writelines(localtime+"\n")
    file1.close()
