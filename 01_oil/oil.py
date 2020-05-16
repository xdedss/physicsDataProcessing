
# coding=utf-8

# 根据给定期望值和标准差生成正态分布

import numpy as np
from sympy import *

import win32con
import win32api
import time

key_map = {
    "0": 96, "1": 97, "2": 98, "3": 99, "4": 100, "5": 101, "6": 102, "7": 103, "8": 104, "9": 105,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, ".": 110, "-": 109, "TAB": 9, "BACK": 8
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
        time.sleep(0.05)

def enter_value(f, fpnum):
    key_string(('%%.%df' % fpnum) % f)

typeNum = type(0.0)

pi = 3.141592653589793

r_oil = 981
r_air = 1.205
g = 9.794
eta = 1.83e-5
b = 8.22e-3
p = 1.0133e5
d = 5.00e-3
l = 2.0e-3

rg2 = (2*(r_oil-r_air)*g)

e0 = 1.6021773e-19

tg = Symbol('tg')
te = Symbol('te')
U = Symbol('U')

#[round(tg*100)/100 for tg in numpy.random.normal(loc=xx.xx, scale=0.25, size=8)]

r = 3 * (eta * l / tg / rg2)**(1/2)
K = simplify(18 * pi / (rg2**(1/2)) * (eta * l / (1 + b /(p*r)))**(3/2) * d)
q_static = simplify(K / U * (1/tg)**(3/2))
q_dynamic = simplify(K / U * (1/te + 1/tg) * (1/tg)**(1/2))

sigma = 0.22

def gen_static(Uf, tgf, sim_key=false):
    tg_arr = np.random.normal(size=8) * sigma + tgf
    tg_arr = np.array([round(i*100)/100 for i in tg_arr])
    tgf = tg_arr.mean()
    subs={
        U:Uf,
        tg:tgf
    }
    
    res = q_static.evalf(subs=subs)
    rese0 = res / round(res/e0)

    print('U:\t' + str(Uf))
    print('\t'.join([str(i) for i in tg_arr]))
    print(tgf)
    print('q\t' + str(res))
    print('e0\t' + str(rese0))
    print('ratio\t' + str(res/e0))
    print('error:\t%.2f%%' % ((rese0-e0)/rese0 * 100))
    
    if not sim_key:
        return
    time.sleep(3)
    for i in range(8):
        for j in range(5):
            time.sleep(0.01)
            key_press("back")
        time.sleep(0.05)
        key_string(str(Uf))
        time.sleep(0.05)
        key_press("tab")
        time.sleep(0.05)
        for j in range(5):
            time.sleep(0.01)
            key_press("back")
        time.sleep(0.1)
        key_string(str(tg_arr[i]))
        time.sleep(0.05)
        key_press("tab")
        time.sleep(0.05)
        
    key_string(str(Uf))
    key_press("tab")
    key_string(str(tgf))
    key_press("tab")
    key_string('%.5f'%(res*1.0e19))
    key_press("tab")
    key_string('%.5f'%(rese0*1.0e19))
    key_press("tab")
    key_string('%.1f' % ((rese0-e0)/rese0 * 100))
    
def gen_dynamic(Uf, tgf, tef, sim_key=false):
    tg_arr = np.random.normal(size=8) * sigma + tgf
    tg_arr = np.array([round(i*100)/100 for i in tg_arr])
    tgf = tg_arr.mean()
    te_arr = np.random.normal(size=8) * sigma + tef
    te_arr = np.array([round(i*100)/100 for i in te_arr])
    tef = te_arr.mean()

    subs={
        U:Uf,
        tg:tgf,
        te:tef
    }

    res = q_dynamic.evalf(subs=subs)
    rese0 = res / round(res/e0)

    print('U:\t' + str(Uf))
    print('\t'.join([str(i) for i in te_arr]))
    print(tef)
    print('\t'.join([str(i) for i in tg_arr]))
    print(tgf)
    print('q:\t' + str(res))
    print('e0:\t' + str(rese0))
    print('ratio:\t' + str(res/e0))
    print('error:\t%.2f%%' % ((rese0-e0)/rese0 * 100))
    
    if not sim_key:
        return
        
    time.sleep(3)
    key_string(str(Uf))
    key_press("tab")
    for i in range(8):
        for j in range(5):
            time.sleep(0.01)
            key_press("back")
        time.sleep(0.05)
        key_string(str(te_arr[i]))
        time.sleep(0.05)
        key_press("tab")
        time.sleep(0.05)
        for j in range(5):
            time.sleep(0.01)
            key_press("back")
        time.sleep(0.05)
        key_string(str(tg_arr[i]))
        time.sleep(0.05)
        key_press("tab")
        time.sleep(0.05)
    
    
    key_string(str(tef))
    key_press("tab")
    key_string(str(tgf))
    key_press("tab")
    key_string('%.5f'%(res*1.0e19))
    key_press("tab")
    key_string('%.5f'%(rese0*1.0e19))
    key_press("tab")
    key_string('%.1f' % ((rese0-e0)/rese0 * 100))


#gen_dynamic(292, 19.2, 35.25)
#gen_static(196, 14.81)


import sys
if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'static':
            if len(sys.argv) > 3:
                gen_static(int(sys.argv[2]), float(sys.argv[3]), true)
        if sys.argv[1] == 'dynamic':
            if len(sys.argv) > 4:
                gen_dynamic(int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), true)
                
                
# python ./oil.py -i