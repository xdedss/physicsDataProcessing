

import win32con
import win32api
import time
import sys
from pynput.keyboard import Listener

key_map = {
    "0": 96, "1": 97, "2": 98, "3": 99, "4": 100, "5": 101, "6": 102, "7": 103, "8": 104, "9": 105,
    ".": 110, "-": 109, "TAB": 9, "BACK": 8
}

def key_down(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)

def key_up(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)

def key_press(key):
    key_down(key)
    time.sleep(0.01)
    key_up(key)

def key_string(s):
    for c in s:
        key_press(c)
        time.sleep(0.01)

def enter_value(f, fpnum):
    key_string(('%%.%df' % fpnum) % f)

def key_clear(num):
    for i in range(num):
        key_press("back")


fcontent = []
if __name__ == '__main__':
    #print(sys.argv)
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        print('file name?')
        fname = input()
    
    with open(fname) as f:
        time.sleep(0.5)
        while True:
            ln = f.readline()
            if ln == None:
                break
            ln = ln.split('\t')
            if len(ln) <= 1:
                break
            fcontent.append(ln)
            
    def pressed(key):
        print(str(key))
        listener.stop()

    with Listener(on_press = pressed) as listener:
        print('按任意键开始...')
        listener.join()

    for i in range(len(fcontent[0])):
        for j in range(len(fcontent)):
            key_clear(10)
            key_string(fcontent[j][i].strip())
            key_press("tab")