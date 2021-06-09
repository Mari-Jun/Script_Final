
from TKHelper import *
from SunInfo import *
T_POS_X, T_POS_Y = 10, 10
F_WIDTH, F_HEIGHT = 800, 600
B_Size = 75
class DetailGUI:
    is_open = False
    def __init__(self,MainGUI):
        if DetailGUI.is_open:
            return
        self.main_gui = MainGUI
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("상세정보")
        self.gui.geometry("{width}x{height}".format(width=F_WIDTH, height=F_HEIGHT))
        self.canvas = Canvas(self.gui, height=F_HEIGHT, width=F_WIDTH, background="pale green")
        self.canvas.pack()
        self.location = self.main_gui.cur_serach_location
        self.InitRenderText()
        self.TopInfo()
        self.RenderTwilight()
        self.InitSun()
        self.RenderSunDetail()


        self.gui.protocol("WM_DELETE_WINDOW", self.Closing)
        DetailGUI.is_open = True

        self.gui.mainloop()

    def InitRenderText(self):
        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X, T_POS_Y , T_POS_X + 780, T_POS_Y + 150, \
                             color="white", alpha=0.6)
        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X, T_POS_Y + 160, T_POS_X + 780, T_POS_Y + 320, \
                             color="white", alpha=0.6)

        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X, T_POS_Y + 330, T_POS_X + 250, T_POS_Y + 580, \
                             color="white", alpha=0.6)
        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X+260, T_POS_Y + 330, T_POS_X + 520, T_POS_Y +580, \
                             color="white", alpha=0.6)
        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X+530, T_POS_Y + 330, T_POS_X + 780, T_POS_Y + 580, \
                             color="white", alpha=0.6)

        self.date_text = self.canvas.create_text((T_POS_X+400, T_POS_Y + 20), font=font_dic["Forte"], \
                                                 anchor=CENTER)
        self.location_text = self.canvas.create_text((T_POS_X+400, T_POS_Y + 80), font=font_dic["Forte"], \
                                                     anchor=CENTER)
        self.longitude_text = self.canvas.create_text((T_POS_X+400, T_POS_Y + 130), font=font_dic["Forte20"], \
                                                      anchor=CENTER)


        self.risetime_text = self.canvas.create_text((T_POS_X+120, T_POS_Y + 530), font=font_dic["Forte"], \
                                                     anchor=CENTER,fill="tomato")
        self.transittime_text = self.canvas.create_text((T_POS_X + 390, T_POS_Y + 530), font=font_dic["Forte"], \
                                                     anchor=CENTER, fill="tomato")
        self.settime_text = self.canvas.create_text((T_POS_X + 660, T_POS_Y + 530), font=font_dic["Forte"], \
                                                     anchor=CENTER, fill="tomato")

        self.TW_text = self.canvas.create_text((T_POS_X + 400, T_POS_Y + 180), font=font_dic["Forte"], \
                                                 anchor=CENTER)
        self.civil_text = self.canvas.create_text((T_POS_X+400, T_POS_Y + 220), font=font_dic["Forte20"], \
                                                     anchor=CENTER, fill="cornflower blue")
        self.naut_text = self.canvas.create_text((T_POS_X+400, T_POS_Y + 260), font=font_dic["Forte20"], \
                                                  anchor=CENTER, fill="royal blue")
        self.ast_text = self.canvas.create_text((T_POS_X+400, T_POS_Y + 300), font=font_dic["Forte20"], \
                                                  anchor=CENTER, fill="navy")
    def InitSun(self,):
        LoadImageDir("asset/sun.png",B_Size,B_Size)
        self.rise_image=self.canvas.create_image((100, 360), image=image_dic["asset/sunrise.png"], anchor=N+W)
        self.transit_image=self.canvas.create_image((365, 370), image=image_dic["asset/sun.png"], anchor=N+W)
        self.set_image=self.canvas.create_image((630, 360), image=image_dic["asset/sunset.png"], anchor=N+W)

        self.canvas.create_text(50,450,font=font_dic["Forte20"],anchor=N+W,text="해뜨는 시각(일출)")
        self.canvas.create_text(315, 450, font=font_dic["Forte20"], anchor=N + W, text="한낮의 시각(남중)")
        self.canvas.create_text(575, 450, font=font_dic["Forte20"], anchor=N + W, text="해지는 시각(일몰)")

    def TopInfo(self):
        self.travel_date=self.main_gui.travel_date
        self.canvas.itemconfig(self.date_text, text="날짜: " + self.travel_date.strftime("%Y-%m-%d"))


        self.canvas.itemconfig(self.location_text, text="지역: " +self.location)

        self.sun_info = Suninfo(self.location, self.travel_date.strftime("%Y%m%d"))
        longitude = self.sun_info.LoadLongitude()
        latitude = self.sun_info.LoadLatitude()
        self.canvas.itemconfig(self.longitude_text,
                               text="위치: 동경 {0}도{1}분 / 북위 {2}도{3}분".format(longitude[0], longitude[1], latitude[0],
                                                                           latitude[1]))

    def RenderTwilight(self):

        locdate = self.travel_date.strftime("%Y%m%d")

        self.sun_info = Suninfo(self.location, locdate)
        tw_civil = self.sun_info.LoadTimes(Suninfo.CategoryDict["시민박명(아침)"]) + self.sun_info.LoadTimes(
            Suninfo.CategoryDict["시민박명(저녁)"])
        tw_naut = self.sun_info.LoadTimes(Suninfo.CategoryDict["항해박명(아침)"]) + self.sun_info.LoadTimes(
            Suninfo.CategoryDict["항해박명(저녁)"])
        tw_ast = self.sun_info.LoadTimes(Suninfo.CategoryDict["천문박명(아침)"]) + self.sun_info.LoadTimes(
            Suninfo.CategoryDict["천문박명(저녁)"])


        self.canvas.itemconfig(self.TW_text, text="박명시각")
        self.canvas.itemconfig(self.civil_text,
                               text="시민박명(아침/저녁) :  아침-{0}시{1}분  /  저녁- {2}시{3}분".format(tw_civil[0], tw_civil[1],
                                                                                     tw_civil[2],
                                                                                     tw_civil[3]))
        self.canvas.itemconfig(self.naut_text,
                               text="항해박명(아침/저녁) : 아침-{0}시{1}분  /  저녁- {2}시{3}분".format(tw_naut[0], tw_naut[1],
                                                                                     tw_naut[2],
                                                                                     tw_naut[3]))
        self.canvas.itemconfig(self.ast_text,
                               text="천문박명(아침/저녁) : 아침-{0}시{1}분  /  저녁- {2}시{3}분".format(tw_ast[0], tw_ast[1],
                                                                                     tw_ast[2],
                                                                                     tw_ast[3]))
    def RenderSunDetail(self):

        locdate=self.travel_date.strftime("%Y%m%d")
        category1=Suninfo.CategoryDict["일출"]
        category2 = Suninfo.CategoryDict["일중"]
        category3 = Suninfo.CategoryDict["일몰"]
        self.sun_info=Suninfo(self.location,locdate)

        time1=self.sun_info.LoadTimes(category1)
        time2 = self.sun_info.LoadTimes(category2)
        time3 = self.sun_info.LoadTimes(category3)

        self.canvas.itemconfig(self.risetime_text, text="{0}시 {1}분".format(time1[0],time1[1]) )
        self.canvas.itemconfig(self.transittime_text, text="{0}시 {1}분".format(time2[0], time2[1]))
        self.canvas.itemconfig(self.settime_text, text="{0}시 {1}분".format(time3[0], time3[1]))

    def Closing(self):
        DetailGUI.is_open = False
        self.gui.destroy()