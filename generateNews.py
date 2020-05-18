# !/usr/bin/env python3
#-*- coding:utf8 -*-
# CCTV News generater
# by MeroMoon
# last edit: 2020.5.17


import sys
import os
import random
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

NEWSBACK_IMG = "./bin/back01.png"
NEWSBACK02_IMG = "./bin/back02.png"
BACKDOWN_IMG = "./bin/backdown.png"
# FACE_DATA = "./bin/haarcascade_frontalcatface.xml"
FACE_DATA = "C:/Users/meromoon/AppData/Local/Programs/Python/Python38/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
SAVE_DIR = "./output/"
IMG_DIR = "./input/"
MAX_SIZE01 = (220, 180)
MAX_SIZE02 = (478, 359)
NAME_POS = (185, 531)
TITLE_POS = (90, 295)
DOWN_POS = (90, 331)
NAME_COLOR = (218, 217, 215, 255)
TITLE_COLOR = (225, 193, 12, 255)
DOWN_COLOR = (247, 255, 247, 255)  # same as titlecolor in method2



# 人脸识别 返回人脸坐标等信息
def face_get(file):
    print('人脸识别开始...')
    filepath = IMG_DIR + file
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  # 读取图片

    print(os.path.abspath(FACE_DATA))
    classifier = cv2.CascadeClassifier(FACE_DATA)
    faceRects = classifier.detectMultiScale(
    img, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

    if len(faceRects):  # 大于0则检测到人脸
        print('检测到人脸，开始裁剪...')
        x, y, h, w = faceRects[0]  # 只处理检测到的第一个人脸
        imgh, imgw = img.shape
        bc = 0.25  # 人脸补偿系数
        if imgw > imgh:
            a = int((x + w) * 0.5 - imgh * 0.6)
            if a < 0:
                a = 0
            a += int(bc * h)  
            b = int(a + 1.2 * imgh)
            return a, b, 1
        else:
            a = int(0.5 * (y+h) - imgw / 2.4)
            if a < 0:
                a = 0
            a += int(bc * h)
            b = int(imgw / 1.2 + a)
            return a, b, 2
    else:
        return 0, 0, 0
        
# 扫描目录中的图片
def scan_img():
    print('scanning...')
    for file in os.listdir(IMG_DIR):
        if not ('back' in file):
            h = os.path.splitext(file)
            if h[1] == '.png' or h[1] == '.jpg':
                print('img found: ', file)
                return file
    print('Error: 没有找到新闻图片，程序将自动生成空白图片\n')
    img = Image.new('RGBA', MAX_SIZE02, 'white')
    file = 'z_autogen.png'
    img.save(IMG_DIR + file)
    return file

# 合成新闻主界面添加文字信息
def add_font(c = 1):
    """
    c = 0 生成style01新闻图片
    c = 1 生成style02新闻图片
    """
    downimg = Image.open(BACKDOWN_IMG)
    drawdown = ImageDraw.Draw(downimg)
    title_font = ImageFont.truetype('C:/Windows/Fonts/AdobeHeitiStd-Regular.otf',26)
    down_font = ImageFont.truetype('C:/Windows/Fonts/AdobeHeitiStd-Regular.otf',15)
    if c == 1:
        title_color = TITLE_COLOR
        img = Image.open(NEWSBACK_IMG)
        drawObj = ImageDraw.Draw(img)
    elif c == 2:
        img = Image.open(NEWSBACK02_IMG)
        img = img.resize((img.size[0]*2, img.size[1]*2))
        print(img.size)
        drawObj = ImageDraw.Draw(img)
        title_color = DOWN_COLOR
        name_text = input('请输入采访人名字（可留空）：')
        if not name_text.isspace():
            name_font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',32)
            drawObj.text(NAME_POS, name_text, NAME_COLOR, name_font, None, 0, 'left', None, None, None, 1, 'black')
        img = img.resize(MAX_SIZE02)

    title_text = input('请输入标题：  ')
    down_text = input('请输入底端文字：  ')
    if title_text == '' and down_text == '':
        title_text = '默认标题这只是测试'
        down_text = '武汉卫健委回应集中核酸检测。  231省区市新增确诊5例本土3例。  安徽工程大学必不可能开学。'
    if len(down_text) >= 21:
        downpos = (DOWN_POS[0] - random.randint(5, 35), DOWN_POS[1])
    else:
        downpos = DOWN_POS
    drawObj = ImageDraw.Draw(img)
    drawObj.text(TITLE_POS, title_text, title_color, title_font, None, 0, 'left', None, None, None, 1, 'black')
    drawdown.text(downpos, down_text, DOWN_COLOR, down_font)
    img = Image.alpha_composite(downimg, img)

    return img

# 合成图片与新闻主界面
def deal_img(c = 1):
    imgfile = scan_img()
    news = Image.open(IMG_DIR + imgfile)
    img = add_font(c)
    w, h = news.size
    # drawit = ImageDraw.Draw(news)
    if w / h < 0.9 or w / h > 1.3:
        a, b, option = face_get(imgfile)
        if option:
            if option == 1:
                news = news.crop((a, 0, b, h))
            else:
                news = news.crop((0, a, w, b))
    # news.show()
    # os.system('pause')
    w, h = news.size
    if c == 1:
        newspos = (5, 30)
        maxsize = MAX_SIZE01
    elif c == 2:
        newspos = (0, 0)
        maxsize = MAX_SIZE02
    blank = Image.new('RGBA', img.size, 'white')
    news = news.resize((maxsize[0], int(h/w*maxsize[0])))
    blank.paste(news, newspos)
    out = Image.alpha_composite(blank, img)
    out.save(SAVE_DIR + 'output.png','png')
    out.show()

if __name__ == "__main__":
    """
    print("abspath = ", os.path.abspath(__file__))
    print("realpath = ", os.path.realpath(__file__))
    print("getcwd = ", os.getcwd())
    print("argv = ", sys.argv[0])
    print("path = ", sys.path[0])
    """
    c = int(input('输入你的选择（1 = sytle01, 2 = style02）： '))
    deal_img(c)