from TKHelper import *
import tkinter.messagebox
from Calendar import *
import datetime
from SunInfo import *
B_Size = 35
T_POS_X, T_POS_Y = 20, 300
class SearchGUI:
    is_open=False
    def __init__(self,MainGui):
        if SearchGUI.is_open:
            return
        SearchGUI.is_open = True
        self.main_gui = MainGui
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("검색")
        self.gui.geometry("600x700")
        self.gui.resizable(width=False, height=False)
        self.canvas = Canvas(self.gui, height=720, width=1280)
        self.canvas.pack()
        self.travel_date = datetime.datetime(2021, 5, 15, 20, 30)
        self.TempFont=font.Font(self.gui, size=20, weight='bold', family="Consolas")
        self.sun_info=Suninfo()


        self.DataList=[]

        self.BackgroundImage("asset/Search.jpg")
        self.InitInputLabel()
        self.InitRenderText()
        self.InitSearchListBox()
        self.InitSearchButton()

        self.gui.protocol("WM_DELETE_WINDOW", self.Closing)



        self.gui.mainloop()
    def BackgroundImage(self,dir):
        LoadImageDir(dir,600,700)
        self.bg_image=self.canvas.create_image((0, 0), image=image_dic[dir], anchor=N+W)
    def SelectDate(self,date):
        self.travel_date = datetime.datetime(date.year, date.month, date.day)
        self.text.set(self.travel_date.strftime("%Y-%m-%d"))
    #너꺼 가져다 썼다 고맙다
    def CreateCalendar(self):
            self.calender=CalendarGUI(self, selectCommand=self.SelectDate)

    def SetMainButton(self, dir, x_pos, y_pos, cmd=None):
        img = Image.open(dir)
        img = img.resize((B_Size, B_Size), Image.ANTIALIAS)
        b_image = ImageTk.PhotoImage(img)
        image_list.append(b_image)
        Button(self.canvas, image=b_image, width=B_Size, height=B_Size, command=cmd).place(x=x_pos, y=y_pos)
    def resetText(self,TW=True):
        if TW:
            self.canvas.itemconfig(self.civil_text,
                               text="")
            self.canvas.itemconfig(self.naut_text,
                               text="")
            self.canvas.itemconfig(self.ast_text,
                               text="")
        else:
            self.canvas.itemconfig(self.risetime_text, text="")
    #날짜를 선택하면 나오게 함
    def InitInputLabel(self):
        my_x=20
        my_y=180
        #self.canvas.create_text(my_x,my_y,font=self.TempFont,text="날짜", anchor=W)
        self.text=StringVar()
        self.text.set("2021-05-06")

        self.RenderDate=Label(self.gui,textvariable=self.text,font=self.TempFont,bg='white')
        self.RenderDate.pack()
        self.RenderDate.place(x=my_x, y=my_y)
        self.SetMainButton("asset/calendar.png",my_x+180,my_y , self.CreateCalendar)

    #극한의 노가다로 콤보박스만듬
    def InitSearchListBox(self):

        self.SearchListBox = ttk.Combobox(self.gui,width=15,font=self.TempFont)
        self.SearchListBox['values']=('정보선택','일출시간','일몰시간','박명시간','태양고도')
        self.SearchListBox.pack()
        self.SearchListBox.place(x=20, y=32)
        self.SearchListBox.current(0)
        self.gui.option_add('*TCombobox*Listbox.font', self.TempFont)

        self.LocationBox = ttk.Combobox(self.gui, width=11, font=self.TempFont)
        self.LocationBox['values'] = ('지역','강릉', '강화도', '거제', '거창', '경산', '경주', '고성(강원)', '고양',
                                      '고흥', '광양','광주', '광주(경기)', '구미', '군산', '김천', '김해', '남원', '남해', '대관령', '대구', '대덕', '대전', '독도', '동해',
            '마산', '목포', '무안', '밀양', '변산', '보령', '보성', '보현산', '부산', '부안', '부천', '사천', '삼척', '상주', '서귀포', '서산', '서울', '서천', '성산일출봉', '세종', '소백산', '속초', '수원', '순천', '승주',
            '시흥', '아산', '안동', '안산', '안양', '양양', '양평', '여수', '여수공항', '여주', '영광', '영덕', '영월', '영주', '영천', '완도', '용인', '울릉도', '울산', '울진', '원주', '의성', '익산', '인천', '임실', '장수',
            '장흥', '전주', '정읍', '제주', '제주(레)', '제천', '주문진', '진도', '진주', '진해', '창원', '천안', '청주', '청주공항', '추풍령', '춘양', '춘천', '충주', '태백', '태안', '통영', '파주', '평택', '포항', '해남',
            '화성', '흑산도')


        self.LocationBox.pack()
        self.LocationBox.place(x=20, y=102)
        self.LocationBox.current(0)



    #검색 버튼
    def InitSearchButton(self):
        SearchButton = Button(self.canvas, image=image_dic["asset/magnifier.png"], width=B_Size+40, height=B_Size+40, command=self.SearchButtonAction)
        SearchButton.pack()
        SearchButton.place(x=500, y=110)


    #스크롤 박스고른걸로 작동
    def SearchButtonAction(self):
        #self.RenderText.configure(state='normal')
        #self.RenderText.delete(0.0, END)  # ?댁쟾 異쒕젰 ?띿뒪??紐⑤몢 ??젣
        iSearchIndex = self.SearchListBox.current()  # 由ъ뒪?몃컯???몃뜳??媛?몄삤湲?
        if iSearchIndex == 0:  # ?꾩꽌愿
            pass
        elif iSearchIndex == 1:  # 紐⑤쾾?뚯떇
            self.SearchSunRise()
        elif iSearchIndex == 2:  # 留덉폆
            self.SearchSunSet()
        elif iSearchIndex == 3:
            self.SearchTwilight()
        elif iSearchIndex == 4:
            self.SearchSunHeight()
        #self.RenderText.configure(state='disabled')

        #검색정보 나오게한다
    def InitRenderText(self):
        CreateAlphaRectangle(self.gui, self.canvas, T_POS_X-10, T_POS_Y , T_POS_X + 570, T_POS_Y + 350, \
                             color="white", alpha=0.8)
        self.date_text = self.canvas.create_text((T_POS_X+10, T_POS_Y + 40), font=font_dic["Forte20"], \
                                                 anchor=W)
        self.location_text = self.canvas.create_text((T_POS_X+10, T_POS_Y + 90), font=font_dic["Forte20"], \
                                                     anchor=NW)
        self.longitude_text = self.canvas.create_text((T_POS_X+10, T_POS_Y + 160), font=font_dic["Forte20"], \
                                                      anchor=NW)
        self.risetime_text = self.canvas.create_text((T_POS_X+70, T_POS_Y + 230), font=font_dic["Forte"], \
                                                     anchor=NW,fill="tomato")
        self.civil_text = self.canvas.create_text((T_POS_X, T_POS_Y + 210), font=font_dic["Forte20"], \
                                                     anchor=NW, fill="maroon")
        self.naut_text = self.canvas.create_text((T_POS_X, T_POS_Y + 250), font=font_dic["Forte20"], \
                                                  anchor=NW, fill="maroon")
        self.ast_text = self.canvas.create_text((T_POS_X, T_POS_Y + 290), font=font_dic["Forte20"], \
                                                  anchor=NW, fill="maroon")

    #일단 간단하게 만들어놨다 걱정 ㄴㄴ
    def SearchSunRise(self):
        self.resetText()
        locdate=self.travel_date.strftime("%Y%m%d")
        category=Suninfo.CategoryDict["일출"]
        self.sun_info=Suninfo(self.LocationBox.get(),locdate)
        longitude=self.sun_info.LoadLongitude()
        latitude=self.sun_info.LoadLatitude()
        time=self.sun_info.LoadTimes(category)
        self.canvas.itemconfig(self.date_text,text="날짜: "+self.travel_date.strftime("%Y-%m-%d"))
        self.canvas.itemconfig( self.location_text, text="지역: "+self.LocationBox.get())
        self.canvas.itemconfig(self.longitude_text, text="위치: 동경 {0}도{1}분 / 북위 {2}도{3}분" .format(longitude[0],longitude[1],latitude[0],latitude[1]))
        self.canvas.itemconfig(self.risetime_text, text="일출시간은 {0}시 {1}분 입니다".format(time[0],time[1]) )


    def SearchSunSet(self):
        self.resetText()
        locdate = self.travel_date.strftime("%Y%m%d")
        category = Suninfo.CategoryDict["일몰"]
        self.sun_info = Suninfo(self.LocationBox.get(), locdate)
        longitude = self.sun_info.LoadLongitude()
        latitude = self.sun_info.LoadLatitude()
        time = self.sun_info.LoadTimes(category)
        self.canvas.itemconfig(self.date_text, text="날짜: " + self.travel_date.strftime("%Y-%m-%d"))
        self.canvas.itemconfig(self.location_text, text="지역: " + self.LocationBox.get())
        self.canvas.itemconfig(self.longitude_text,
                               text="위치: 동경 {0}도{1}분 / 북위 {2}도{3}분".format(longitude[0], longitude[1], latitude[0],
                                                                           latitude[1]))
        self.canvas.itemconfig(self.risetime_text, text="일몰시간은 {0}시 {1}분 입니다".format(time[0], time[1]))

    def SearchTwilight(self):
        self.resetText(TW=False)
        locdate = self.travel_date.strftime("%Y%m%d")

        self.sun_info = Suninfo(self.LocationBox.get(), locdate)
        longitude = self.sun_info.LoadLongitude()
        latitude = self.sun_info.LoadLatitude()
        tw_civil=self.sun_info.LoadTimes( Suninfo.CategoryDict["시민박명(아침)"])+self.sun_info.LoadTimes( Suninfo.CategoryDict["시민박명(저녁)"])
        tw_naut=self.sun_info.LoadTimes( Suninfo.CategoryDict["항해박명(아침)"])+self.sun_info.LoadTimes( Suninfo.CategoryDict["항해박명(저녁)"])
        tw_ast=self.sun_info.LoadTimes( Suninfo.CategoryDict["천문박명(아침)"])+self.sun_info.LoadTimes( Suninfo.CategoryDict["천문박명(저녁)"])

        self.canvas.itemconfig(self.date_text, text="날짜: " + self.travel_date.strftime("%Y-%m-%d"))
        self.canvas.itemconfig(self.location_text, text="지역: " + self.LocationBox.get())
        self.canvas.itemconfig(self.longitude_text,
                               text="위치: 동경 {0}도{1}분 / 북위 {2}도{3}분".format(longitude[0], longitude[1], latitude[0],
                                                                           latitude[1]))

        self.canvas.itemconfig(self.civil_text,
                               text="시민박명(아침/저녁): 아침-{0}시{1}분 / 저녁- {2}시{3}분".format(tw_civil[0], tw_civil[1], tw_civil[2],
                                                                           tw_civil[3]))
        self.canvas.itemconfig(self.naut_text,
                               text="항해박명(아침/저녁): 아침-{0}시{1}분 / 저녁- {2}시{3}분".format(tw_naut[0], tw_naut[1],
                                                                                     tw_naut[2],
                                                                                     tw_naut[3]))
        self.canvas.itemconfig(self.ast_text,
                               text="천문박명(아침/저녁): 아침-{0}시{1}분 / 저녁- {2}시{3}분".format(tw_ast[0], tw_ast[1],
                                                                                     tw_ast[2],
                                                                                     tw_ast[3]))


    def SearchSunHeight(self):
        locdate = self.travel_date.strftime("%Y%m%d")

        self.sun_info = Suninfo(self.LocationBox.get(), locdate)
        longitude = self.sun_info.LoadLongitude()
        latitude = self.sun_info.LoadLatitude()
        tw_civil = self.sun_info.LoadTimes(Suninfo.CategoryDict["시민박명(아침)"]) + self.sun_info.LoadTimes(
            Suninfo.CategoryDict["시민박명(저녁)"])
        tw_naut = self.sun_info.LoadTimes(Suninfo.CategoryDict["항해박명(아침)"]) + self.sun_info.LoadTimes(
            Suninfo.CategoryDict["항해박명(저녁)"])
        tw_ast = self.sun_info.LoadTimes(Suninfo.CategoryDict["천문박명(아침)"]) + self.sun_info.LoadTimes(
            Suninfo.CategoryDict["천문박명(저녁)"])

        self.canvas.itemconfig(self.date_text, text="날짜: " + self.travel_date.strftime("%Y-%m-%d"))
        self.canvas.itemconfig(self.location_text, text="지역: " + self.LocationBox.get())
    def Closing(self):
        SearchGUI.is_open = False
        self.gui.destroy()
