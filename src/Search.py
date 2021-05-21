from TKHelper import *
import tkinter.messagebox
from Calendar import *
import datetime
from SunInfo import *
B_Size = 35
class SearchGUI:
    is_open=False
    def __init__(self,MainGui):
        if SearchGUI.is_open:
            return
        SearchGUI.is_open = True
        self.main_gui = MainGui
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("검색")
        self.gui.geometry("900x400")
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
        LoadImageDir(dir,900,400)
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

    #날짜를 선택하면 나오게 함
    def InitInputLabel(self):

        self.canvas.create_text(520,65,font=self.TempFont,text="날짜", anchor=W)
        self.text=StringVar()
        self.text.set("00-00-00")

        self.RenderDate=Label(self.gui,textvariable=self.text,font=self.TempFont,bg='white')
        self.RenderDate.pack()
        self.RenderDate.place(x=580, y=42)
        self.SetMainButton("asset/calendar.png",740, 40 , self.CreateCalendar)

    #극한의 노가다로 콤보박스만듬
    def InitSearchListBox(self):

        labelTop=Label(self.gui,text="검색")
        labelTop.pack()
        labelTop.place(x=10,y=20)


        self.SearchListBox = ttk.Combobox(self.gui,width=15,font=self.TempFont)
        self.SearchListBox['values']=('정보선택','일출시간','일몰시간','박명시간','태양고도')
        self.SearchListBox.pack()
        self.SearchListBox.place(x=10, y=42)
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
        self.LocationBox.place(x=300, y=42)
        self.LocationBox.current(0)




    #검색 버튼
    def InitSearchButton(self):

        SearchButton = Button(self.gui, font=self.TempFont, text="검색", command=self.SearchButtonAction)
        SearchButton.pack()
        SearchButton.place(x=10, y=110)
    #스크롤 박스고른걸로 작동
    def SearchButtonAction(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)  # ?댁쟾 異쒕젰 ?띿뒪??紐⑤몢 ??젣
        iSearchIndex = self.SearchListBox.current()  # 由ъ뒪?몃컯???몃뜳??媛?몄삤湲?
        if iSearchIndex == 0:  # ?꾩꽌愿
            pass#self.SearchLibrary()
        elif iSearchIndex == 1:  # 紐⑤쾾?뚯떇
            self.SearchLibrary()
        elif iSearchIndex == 2:  # 留덉폆
            pass  # SearchMarket()
        elif iSearchIndex == 3:
            pass  # SearchCultural()

        self.RenderText.configure(state='disabled')
    #검색정보 나오게한다
    def InitRenderText(self):
        RenderTextScrollbar = Scrollbar(self.gui)
        RenderTextScrollbar.pack()
        RenderTextScrollbar.place(x=375, y=200)

        self.RenderText = Text(self.gui, width=100, height=10,relief="solid",borderwidth=5,
                         yscrollcommand=RenderTextScrollbar.set)
        self.RenderText.pack()
        self.RenderText.place(x=10, y=215)
        RenderTextScrollbar.config(command=self.RenderText.yview)
        RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

        self.RenderText.configure(state='disabled')

    #일단 간단하게 만들어놨다 걱정 ㄴㄴ
    def SearchLibrary(self):
        locdate=self.travel_date.strftime("%Y%m%d")
        curr=self.SearchListBox.current()
        category=""
        if curr==1:
            category=Suninfo.CategoryDict["일출"]
        elif curr==2:
            category = Suninfo.CategoryDict["일몰"]
        self.sun_info=Suninfo(self.LocationBox.get(),locdate)
        self.DataList.append(self.sun_info.SearchSunData(category))
        for x in self.DataList:
            self.RenderText.insert(INSERT,x)
    def Closing(self):
        SearchGUI.is_open = False
        self.gui.destroy()