from TKHelper import *
from tkcalendar import Calendar
import MainGUI

import datetime

class CalendarGUI:
    is_open = False
    #새로 생성되는 클래스의 인자에 MainGUI을 넣어서 MainGUI 객체를 가져오게 함 그렇게 되면 MainGUI에 있는 변수들을 수정 가능

    def __init__(self, MainGui, selectCommand=None):

        if CalendarGUI.is_open:
            return
        CalendarGUI.is_open = True
        self.main_gui = MainGui
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("Calendar")
        now = datetime.datetime.now()
        self.cal = Calendar(self.gui, selectmode='day', year=now.year, month=now.month, day=now.day)
        self.cal.pack(pady=10)

        Button(self.gui, text="날짜 선택", command=lambda cmd=selectCommand: self.SetTravelDate(cmd)).pack()

        self.gui.protocol("WM_DELETE_WINDOW", self.Closing)

        self.gui.mainloop()

    def PrintHello(self):
        print("Hello")

    #현재는 시간이 20, 30으로 고정되어 있는데 이 부분은 xml 데이터 파일의 정보를 가져와서 설정해 주어야함.
    def SetTravelDate(self, command=None):
        date = self.cal.selection_get()
        #여기서 xml 데이터 가져온다.
        self.main_gui.travel_date = datetime.datetime(date.year, date.month, date.day, 20, 30)

        if command is not None:
            command()

        print(self.main_gui.travel_date)


    def Closing(self):
        CalendarGUI.is_open = False
        self.gui.destroy()
