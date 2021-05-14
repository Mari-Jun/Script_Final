from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from GUI import Calendar
import datetime

T_POS_X, T_POS_Y = 100, 150
B_Size = 80
B_POS_X, B_POS_Y = 1100, 100

class MainGUI:
    def __init__(self):
        self.gui = Tk()
        self.gui.title("해가 뜰 때까지")
        self.gui.geometry("1280x720")
        self.gui.resizable(width=False, height=False)
        self.canvas = Canvas(self.gui, height=720, width=1280)
        self.canvas.pack()

        self.LoadFonts()
        self.SetBackGround()
        self.SetMainTexts()
        self.SetButtons()

        self.gui.mainloop()

    def LoadFonts(self):
        self.font_dic = {}
        print(list(font.families()))
        self.font_dic["Forte"] = font.Font(family="Forte", size=30, weight="bold")
        self.font_dic["Cooper"] = font.Font(family="Cooper Black", size=16, weight="bold")

    def SetBackGround(self):
        self.bgImg = PhotoImage(file="asset/bg_sunset.png")
        self.canvas.create_image((0, 0), image=self.bgImg, anchor=N+W)

    def SetMainTexts(self):
        self.travel_date = datetime.datetime(2021, 5, 15, 20, 30)
        self.cur_location = "서울"

        self.subtitle = self.canvas.create_text((T_POS_X, T_POS_Y), font=self.font_dic["Forte"],\
                                                text="해가 뜰 때까지", anchor=W)
        now = datetime.datetime.now()
        time_remaining = self.travel_date - now
        self.time_remaing_text = self.canvas.create_text((T_POS_X, T_POS_Y + 80), font=self.font_dic["Forte"],\
                                text=str(time_remaining), anchor=W)
        self.cur_time_text = self.canvas.create_text((T_POS_X, T_POS_Y + 180), font=self.font_dic["Cooper"],\
                                text=("현재 시간: " + now.strftime("%Y-%m-%d %H:%M:%S")), anchor=W)
        self.travel_date_text = self.canvas.create_text((T_POS_X, T_POS_Y + 230), font=self.font_dic["Cooper"],\
                                text=("일출 시간: " + self.travel_date.strftime("%Y-%m-%d %H:%M:%S")), anchor=W)
        self.cur_location_text = self.canvas.create_text((T_POS_X, T_POS_Y + 280), font=self.font_dic["Cooper"],\
                                text=("지역: " + self.cur_location), anchor=W)
        self.UpdateTime()

    def UpdateTime(self):
        now = datetime.datetime.now()
        time_remaining = self.travel_date - now
        self.canvas.itemconfig(self.time_remaing_text, text=str("{0} Day {1} Hours {2} Minutes {3} Seconds")\
                              .format(time_remaining.days, time_remaining.seconds // 3600,\
                                      time_remaining.seconds % 3600 // 60, time_remaining.seconds % 60))
        self.canvas.itemconfig(self.cur_time_text, text=("현재 시간: " + now.strftime("%Y-%m-%d %H:%M:%S")))
        self.canvas.itemconfig(self.travel_date_text, text=("일출 시간: " + self.travel_date.strftime("%Y-%m-%d %H:%M:%S")))
        self.gui.after(500, self.UpdateTime)

    def SetButtons(self):
        self.b_image_list = []
        self.SetMainButton("asset/magnifier.png", B_POS_X, B_POS_Y)
        self.SetMainButton("asset/map.png", B_POS_X, B_POS_Y + B_Size)
        self.SetMainButton("asset/calendar.png", B_POS_X, B_POS_Y + B_Size * 2, self.CreateCalendar)
        self.SetMainButton("asset/sunset.png", B_POS_X, B_POS_Y + B_Size * 3)
        self.SetMainButton("asset/detail.png", B_POS_X, B_POS_Y + B_Size * 4)
        self.SetMainButton("asset/gmail.png", B_POS_X, B_POS_Y + B_Size * 5)
        self.SetMainButton("asset/telegram.png", B_POS_X, B_POS_Y + B_Size * 6)


    def SetMainButton(self, dir, x_pos, y_pos, cmd = None):
        img = Image.open(dir)
        img = img.resize((B_Size, B_Size), Image.ANTIALIAS)
        b_image = ImageTk.PhotoImage(img)
        self.b_image_list.append(b_image)
        Button(self.canvas, image=b_image, width=B_Size, height=B_Size, command=cmd).place(x=x_pos, y=y_pos)

    def CreateCalendar(self):
        Calendar.Cal(self)



