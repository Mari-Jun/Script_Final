from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import datetime

#폰트 저장소
font_dic = {}

def LoadFonts():
    print(list(font.families()))
    font_dic["Forte"] = font.Font(family="Forte", size=30, weight="bold")
    font_dic["Forte20"] = font.Font(family="Forte", size=20, weight="bold")
    font_dic["Cooper"] = font.Font(family="Cooper Black", size=16, weight="bold")
    font_dic["CooperSmall"] = font.Font(family="Cooper Black", size=10, weight="bold")

#이미지들은 여기에 저장
image_dic = {}
image_list = []

def LoadImageDir(dir, width=None, height=None):
    img = Image.open(dir)
    if width != None and height != None:
        img = img.resize((width, height), Image.ANTIALIAS)
    b_image = ImageTk.PhotoImage(img)
    image_dic[dir] = b_image

#canvas에서 alpha rectangle을 사용하고 싶을 때 사용
def CreateAlphaRectangle(gui, canvas, x1, y1, x2, y2, **kwargs):
    if "alpha" in kwargs:
        alpha = int(kwargs.pop("alpha") * 255)
        color = kwargs.pop("color")
        color = gui.winfo_rgb(color) + (alpha,)
        image = Image.new("RGBA", (x2-x1, y2-y1), color)
        image_list.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=image_list[-1], anchor="nw")
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


#unix 시간을 우리가 알아볼 수 있는 시간으로 바꿔준다.
cg_unix = lambda ts: (datetime.datetime.utcfromtimestamp(ts) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
#unix 시간을 날짜만 있게 바꾼다.
cg_unix_mdh = lambda ts: (datetime.datetime.utcfromtimestamp(ts) + datetime.timedelta(hours=9)).strftime('%m-%d / %Hh')
cg_unix_md = lambda ts: (datetime.datetime.utcfromtimestamp(ts) + datetime.timedelta(hours=9)).strftime('%m-%d')
#Sunday, Monday....
cg_unix_d = lambda ts: (datetime.datetime.utcfromtimestamp(ts) + datetime.timedelta(hours=9)).strftime('%A')
