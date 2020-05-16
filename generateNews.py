#!/usr/bin/env python3
#-*- coding:utf8 -*-
# CCTV News generater
# by MeroMoon
# last edit: 2020.5.16

import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

NEWSBACK_IMG = sys.path[0] + "/bin/back.png"
NEWS_IMG = sys.path[0] + "/bin/in.png"
SAVE_DIR = sys.path[0] + "/output/"
IMG_DIR = sys.path[0] + "/bin/"
# MAX_SIZE = (195, 160)
TITLE_POS = (90, 295)
DOWN_POS = (90, 331)
TITLE_COLOR = (225, 193, 12, 255)
DOWN_COLOR = (247, 255, 247, 255)


def scan_img():
    print('scanning...')
    for file in os.listdir(IMG_DIR):
        if file != "back.png":
            f, h = os.path.splitext(file)
            if h == '.png' or h == '.jpg':
                print('img found: ', file)
                return file
    print('Error: 没有找到新闻图片\n')
    exit(0)





def add_font():
    img = Image.open(NEWSBACK_IMG)
    drawObj = ImageDraw.Draw(img)

    title_font = ImageFont.truetype('C:/Windows/Fonts/AdobeHeitiStd-Regular.otf',25)
    down_font = ImageFont.truetype('C:/Windows/Fonts/AdobeHeitiStd-Regular.otf',15)
    title_text = input('请输入标题')
    down_text = input('请输入底端文字')
    
    drawObj.text(TITLE_POS,title_text,TITLE_COLOR,font=title_font)
    drawObj.text(DOWN_POS,down_text,DOWN_COLOR,font=down_font)
    
    return img

def deal_img():
    news = Image.open(IMG_DIR + scan_img())
    img = add_font()
    # drawit = ImageDraw.Draw(news)
    w, h = news.size
    blank = Image.new('RGBA', img.size, 'white')
    if w >= h:
        news = news.resize((int(w/h*160), 160))
    else:
        news = news.resize((195, int(h/w*195)))
    blank.paste(news, (5, 35))
    out = Image.alpha_composite(blank, img)
    out.save(SAVE_DIR + 'output.png','png')
    out.show()



if __name__ == "__main__":
    deal_img()
    """
    print("abspath = ", os.path.abspath(__file__))
    print("realpath = ", os.path.realpath(__file__))
    print("getcwd = ", os.getcwd())
    print("argv = ", sys.argv[0])
    print("path = ", sys.path[0])
    """