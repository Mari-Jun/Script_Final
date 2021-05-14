from tkinter import *
from tkcalendar import Calendar
import MainGUI
import datetime

class Cal:
    def __init__(self, MainGui):
        self.main_gui = MainGui
        self.cal_gui = Toplevel(self.main_gui.gui)
        now = datetime.datetime.now()
        self.cal = Calendar(self.cal_gui, selectmode='day', year=now.year, month=now.month, day=now.day)
        self.cal.pack(pady = 20)

        Button(self.cal_gui, text="날짜 선택", command=self.SetTravelDate).pack()

    def SetTravelDate(self):
        date = self.cal.selection_get()
        self.main_gui.travel_date = datetime.datetime(date.year, date.month, date.day, 20, 30)
        print(self.main_gui.travel_date)
