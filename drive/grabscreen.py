import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api   #操作窗口的包

#截取桌面指定位置、宽度、高度的图片
def grab_screen(region=None):           #此时的形参为一个空值对象（实参可以赋值）

    hwin = win32gui.GetDesktopWindow()  # 获取桌面

    if region:
            left,top,x2,y2 = region     # 获取最左侧，最上面，最右面，最下面的值
            width = x2 - left + 1       # 获取宽度
            height = y2 - top + 1       # 获取高度
    else:   #对整个桌面进行截图
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        # 分辨率适应

    hwindc = win32gui.GetWindowDC(hwin)
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    # 创建设备描述表
    memdc = srcdc.CreateCompatibleDC()
    # 创建内存设备描述表
    bmp = win32ui.CreateBitmap()
    # 创建位图对象准备保存图片
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    # 为bitmap开辟存储空间
    memdc.SelectObject(bmp)
    # 创建位图对象


    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    # 截图指定坐标和宽度高度的图像至内存设备描述表
    signedIntsArray = bmp.GetBitmapBits(True)
    # 获取位图信息
    img = np.fromstring(signedIntsArray, dtype='uint8')
    # 加载图片信息转成numpy数组
    img.shape = (height,width,4)
    # 对图片进行reshape处理，变成3维结构每个维度分别是高度，宽度，通道数

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    # 内存释放

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    # 色彩空间转换将4通道图片转成RGB3通道图片