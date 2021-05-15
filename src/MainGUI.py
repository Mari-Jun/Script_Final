from TKHelper import *
from Calendar import *
from Weather import *
import datetime

T_POS_X, T_POS_Y = 100, 150
B_Size = 75
B_POS_X, B_POS_Y = 1150, 50

class MainGUI:
    def __init__(self):
        self.gui = Tk()
        self.gui.title("해가 뜰 때까지")
        self.gui.geometry("1280x720")
        self.gui.resizable(width=False, height=False)
        self.canvas = Canvas(self.gui, height=720, width=1280)
        self.canvas.pack()

        self.text=StringVar()#아무쓸모 없지만 켈린더 갔다가 쓰려고 어쩔수없이 만듬 ㅠㅠ
        self.LoadFonts()
        self.SetBackGround()

        LoadFonts()
        LoadIconData()

        self.SetBackGround("asset/bg_sunrise.png", "asset/bg_sunset.png")
        self.SetMainTexts()
        self.SetMainWeather()
        self.SetButtons()

        self.gui.mainloop()

    def SetBackGround(self, dir, dir2):
        LoadImageDir(dir, 1280, 720)
        LoadImageDir(dir2, 1280, 720)
        self.bg_image = self.canvas.create_image((0, 0), image=image_dic[dir], anchor=N+W)

    def SetMainTexts(self):
        self.travel_date = datetime.datetime(2021, 6, 1, 20, 30)
        self.cur_location = "서울"

        self.subtitle = self.canvas.create_text((T_POS_X, T_POS_Y), font=font_dic["Forte"],\
                                                text="해가 뜰 때까지", anchor=W)

        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X - 30, T_POS_Y + 150, T_POS_X + 450, T_POS_Y + 310, \
                             color="white", alpha=0.7)

        self.time_remaing_text = self.canvas.create_text((T_POS_X, T_POS_Y + 80), font=font_dic["Forte"],\
                                anchor=W)
        self.cur_time_text = self.canvas.create_text((T_POS_X, T_POS_Y + 180), font=font_dic["Cooper"],\
                                anchor=W, fill="dim gray")
        self.sun_rs_text = "일출"
        self.travel_date_text = self.canvas.create_text((T_POS_X, T_POS_Y + 230), font=font_dic["Cooper"],\
                                anchor=W, fill="dim gray")
        self.cur_location_text = self.canvas.create_text((T_POS_X, T_POS_Y + 280), font=font_dic["Cooper"],\
                                text=("지역: " + self.cur_location), anchor=W, fill="dim gray")
        self.UpdateTime()


    def SetMainWeather(self):
        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X - 30, T_POS_Y +350, T_POS_X + 450, T_POS_Y + 460,\
                             color="white", alpha=0.7)

        self.cur_weather_text = self.canvas.create_text((T_POS_X, T_POS_Y + 380), font=font_dic["Cooper"], \
                                                       text="", anchor=W, fill="dim gray")
        self.cur_weather_icon = self.canvas.create_image((T_POS_X, T_POS_Y + 430), image=None, anchor=W)
        self.UpdateWeather()

    def UpdateTime(self):
        now = datetime.datetime.now()
        time_remaining = self.travel_date - now
        self.canvas.itemconfig(self.time_remaing_text, text=str("{0} Day {1} Hours {2} Minutes {3} Seconds")\
                              .format(time_remaining.days, time_remaining.seconds // 3600,\
                                      time_remaining.seconds % 3600 // 60, time_remaining.seconds % 60))
        self.canvas.itemconfig(self.cur_time_text, text=("현재 시간: " + now.strftime("%Y-%m-%d %H:%M:%S")))
        self.canvas.itemconfig(self.travel_date_text,\
                               text=(self.sun_rs_text + " 시간: " + self.travel_date.strftime("%Y-%m-%d %H:%M:%S")))
        self.gui.after(500, self.UpdateTime)

    def UpdateWeather(self):
        LoadCurrentWeather("seoul,KR")
        w_data = ShowCurrentWeather()
        self.canvas.itemconfig(self.cur_weather_text, text=("날씨: {0}, 기온: {1}, 구름양: {2}").format(\
            w_data[0], w_data[1], w_data[2]))
        self.canvas.itemconfig(self.cur_weather_icon, image=w_data[3])
        self.gui.after(60000, self.UpdateWeather)

    def SetButtons(self):
        self.SetMainButton("asset/magnifier.png", B_POS_X, B_POS_Y)
        self.sun_button = self.SetMainButton("asset/sunrise.png", B_POS_X, B_POS_Y + B_Size, self.ChangeSunRiseSunSet)
        self.is_sunrise = True
        LoadImageDir("asset/sunset.png", B_Size, B_Size)
        self.SetMainButton("asset/map.png", B_POS_X, B_POS_Y + B_Size * 2, self.CreateMap)
        self.SetMainButton("asset/calendar.png", B_POS_X, B_POS_Y + B_Size * 3, self.CreateCalendar)
        self.SetMainButton("asset/forecast.png", B_POS_X, B_POS_Y + B_Size * 4, self.CreateForecast)
        self.SetMainButton("asset/detail.png", B_POS_X, B_POS_Y + B_Size * 5)
        self.SetMainButton("asset/gmail.png", B_POS_X, B_POS_Y + B_Size * 6)
        self.SetMainButton("asset/telegram.png", B_POS_X, B_POS_Y + B_Size * 7)

    def SetMainButton(self, dir, x_pos, y_pos, cmd=None):
        LoadImageDir(dir, B_Size, B_Size)
        button = Button(self.canvas, image=image_dic[dir], width=B_Size, height=B_Size, command=cmd)
        button.place(x=x_pos, y=y_pos)
        return button

    def ChangeSunRiseSunSet(self):
        self.is_sunrise = not self.is_sunrise
        self.sun_button.configure(image=image_dic["asset/sunrise.png"] if self.is_sunrise else image_dic["asset/sunset.png"])
        self.canvas.itemconfig(self.subtitle, text="해가 뜰 때까지" if self.is_sunrise else "해가 질 때까지")
        self.sun_rs_text = "일출" if self.is_sunrise else "일몰"
        self.canvas.itemconfig(self.travel_date_text,\
                    text=(self.sun_rs_text + " 시간: " + self.travel_date.strftime("%Y-%m-%d %H:%M:%S")))
        self.canvas.itemconfig(self.bg_image,\
                    image=image_dic["asset/bg_sunrise.png"] if self.is_sunrise else image_dic["asset/bg_sunset.png"])

    def CreateMap(self):
        #이 부분에서 self.cur_location을 설정해서 다른 부분을 수정해야함. 따로 MapGUI 클래스 생성해서 만들자.
        pass

    def CreateCalendar(self):
        CalendarGUI(self)

    def CreateForecast(self):
        ForecastGUI(self)