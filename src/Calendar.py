from TKHelper import *
from tkcalendar import Calendar
import MainGUI

import datetime

class CalendarGUI:
    #새로 생성되는 클래스의 인자에 MainGUI을 넣어서 MainGUI 객체를 가져오게 함 그렇게 되면 MainGUI에 있는 변수들을 수정 가능
    def __init__(self, MainGui):
        self.main_gui = MainGui
        self.cal_gui = Toplevel(self.main_gui.gui)
        self.cal_gui.title("Calendar")
        now = datetime.datetime.now()
        self.cal = Calendar(self.cal_gui, selectmode='day', year=now.year, month=now.month, day=now.day)
        self.cal.pack(pady=10)

        Button(self.cal_gui, text="날짜 선택", command=self.SetTravelDate).pack()

    #현재는 시간이 20, 30으로 고정되어 있는데 이 부분은 xml 데이터 파일의 정보를 가져와서 설정해 주어야함.
    def SetTravelDate(self):
        date = self.cal.selection_get()
        self.main_gui.travel_date = datetime.datetime(date.year, date.month, date.day, 20, 30)
        self.main_gui.text.set(self.main_gui.travel_date.strftime("%Y-%m-%d"))
        print(self.main_gui.travel_date)

