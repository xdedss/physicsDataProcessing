#截屏识别万用表的示数并记录


import time
import win32gui, win32ui, win32con, win32api
import cv2
import matplotlib.pyplot as plot
import numpy as np
import numpy.linalg as npl

#简化数组写法
def arr(*a):
    return np.array(a)

#屏幕截图
def window_capture(filename, w=1920, h=1080):
    hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    #MoniterDev = win32api.EnumDisplayMonitors(None, None)
    #w = MoniterDev[0][2][2]
    #h = MoniterDev[0][2][3]
    print(w,h) #图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def get_corner(img):
    window_color = (35, 157, 199)
    imgshape = img.shape
    for y in range(imgshape[0]):
        #print(img[y, int(imgshape[1]/2)])
        if (img[y, int(imgshape[1]/2)] == window_color).all():
            print(y)
            for x in range(imgshape[1]):
                if (img[y, x] == window_color).all():
                    break
            break
    return (x, y)

#提取单个数字
def id_digit(img_sl, corner):
    thr = arr(120,120,120)
    (xc, yc) = corner
    #关键点位置
    a = arr(6, 1) + corner
    b = arr(10, 6) + corner
    c = arr(10, 16) + corner
    d = arr(6, 21) + corner
    e = arr(1, 16) + corner
    f = arr(1, 6) + corner
    g = arr(6, 11) + corner
    #关键点检测结果
    a_b = (img_sl[a[1], a[0]] < thr).all()
    b_b = (img_sl[b[1], b[0]] < thr).all()
    c_b = (img_sl[c[1], c[0]] < thr).all()
    d_b = (img_sl[d[1], d[0]] < thr).all()
    e_b = (img_sl[e[1], e[0]] < thr).all()
    f_b = (img_sl[f[1], f[0]] < thr).all()
    g_b = (img_sl[g[1], g[0]] < thr).all()
    res = arr(a_b, b_b, c_b, d_b, e_b, f_b, g_b)
    #debug
    img_sl[a[1], a[0]] = thr
    img_sl[b[1], b[0]] = thr
    img_sl[c[1], c[0]] = thr
    img_sl[d[1], d[0]] = thr
    img_sl[e[1], e[0]] = thr
    img_sl[f[1], f[0]] = thr
    img_sl[g[1], g[0]] = thr
    #print(res)
    #字符
    reference = [
        arr(1,1,1,1,1,1,0),arr(0,1,1,0,0,0,0), 
        arr(1,1,0,1,1,0,1),arr(1,1,1,1,0,0,1),
        arr(0,1,1,0,0,1,1),arr(1,0,1,1,0,1,1),
        arr(1,0,1,1,1,1,1),arr(1,1,1,0,0,0,0),
        arr(1,1,1,1,1,1,1),arr(1,1,1,1,0,1,1)]
    for i in range(10):
        if ((reference[i] == 1) == res).all():
            return i
    return None

#从切片里提取数字
def id_num(img_sl):
    corner1 = arr(58, 8)
    corner2 = arr(40, 8)
    corner3 = arr(22, 8)
    corner4 = arr(4, 8)
    d1 = (id_digit(img_sl, corner1))
    d2 = (id_digit(img_sl, corner2))
    d3 = (id_digit(img_sl, corner3))
    d4 = (id_digit(img_sl, corner4))
    print(d1,d2,d3,d4)
    return d1 + 10*(0 if d2==None else d2) + 100*(0 if d3==None else d3) + 1000*(0 if d4==None else d4)
    
#截屏并识别电压、电流值
def get_number():
    window_capture('temp.png')
    
    img = cv2.imread('temp.png')[:,:,::-1]
    
    (xc, yc) = get_corner(img)
    print(xc, yc)
    
    #切片
    img_sl1 = img[yc+289:yc+327, xc+206:xc+277, :]
    img_sl2 = img[yc+289:yc+327, xc+1303:xc+1374, :]
    
    I = (id_num(img_sl1)) / 10.0
    U = (id_num(img_sl2)) / 100.0
    
    
    print(I, U)
    
    ## debug
    #plot.imshow(img_sl1)
    #plot.imshow(img_sl2)
    #plot.show()
    
    return arr(I, U)

results = []
results_sc = []
time.sleep(2)
for i in range(300):
    time.sleep(0.1)
    res = get_number()
    res_sc = arr(res[0]/10, res[1])
    if len(results) != 0 and npl.norm(results_sc[-1] - res_sc) < 0.1: #相同/相近数据跳过
        continue
    results.append(res)
    results_sc.append(res_sc)


print(results)
print(len(results))

with open('./res.txt', 'w') as f:
    for i in range(len(results)):
        f.write(str(results[i][0]) + '\t')
    f.write('\n')
    for i in range(len(results)):
        f.write(str(results[i][1]) + '\t')
    