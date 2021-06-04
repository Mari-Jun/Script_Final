 #-*- coding: utf-8 -*-
import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from TKHelper import*
from SunInfo import *
#global value
host = "smtp.gmail.com" # Gmail STMP 서버 주소.
port = "587"
senderAddr = "undugy98@gmail.com"     # 보내는 사람 email 주소.

class SendMail:
    is_open = False

    def __init__(self, MainGui):
        if SendMail.is_open:
            return
        SendMail.is_open = True
        self.main_gui = MainGui
        self.gui =Toplevel(self.main_gui.gui)
        self.gui.title("메일발송")
        self.gui.geometry("300x200")
        self.gui.configure(background="peach puff")
        self.id_input = Entry(self.gui, width=30)
        self.id_input.pack()

        self.location = self.main_gui.cur_location
        self.travel_date = self.main_gui.travel_date

        self.button = Button(self.gui, text="보내기", background="white",command=self.Send)
        self.button.pack()

        self.gui.protocol("WM_DELETE_WINDOW", self.Closing)

        self.gui.mainloop()
    def Send(self):
        recipientAddr = self.id_input.get()  # 받는 사람 email 주소.
        if recipientAddr=="":
            return
        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "해가 뜰때까지에서 보내드립니다"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr
        self.suninfo=Suninfo(self.location,self.travel_date.strftime("%Y%m%d"))
        longitude=self.suninfo.LoadLongitude()
        latitude=self.suninfo.LoadLatitude()
        tw_civil = self.suninfo.LoadTimes(Suninfo.CategoryDict["시민박명(아침)"]) + self.suninfo.LoadTimes(
            Suninfo.CategoryDict["시민박명(저녁)"])
        tw_naut = self.suninfo.LoadTimes(Suninfo.CategoryDict["항해박명(아침)"]) + self.suninfo.LoadTimes(
            Suninfo.CategoryDict["항해박명(저녁)"])
        tw_ast = self.suninfo.LoadTimes(Suninfo.CategoryDict["천문박명(아침)"]) + self.suninfo.LoadTimes(
            Suninfo.CategoryDict["천문박명(저녁)"])

        time1 = self.suninfo.LoadTimes(Suninfo.CategoryDict["일출"])
        time2 = self.suninfo.LoadTimes(Suninfo.CategoryDict["일중"])
        time3 = self.suninfo.LoadTimes(Suninfo.CategoryDict["일몰"])

        msgtext='''
                날짜 : {0} , 지역 : {1}
                위치: 동경 {2}도{3}분 / 북위 {4}도{5}분
                
                박명시간
                시민박명(아침/저녁) :  아침-{6}시{7}분  /  저녁- {8}시{9}분
                항해박명(아침/저녁) : 아침-{10}시{11}분  /  저녁- {12}시{13}분
                천문박명(아침/저녁) : 아침-{14}시{15}분  /  저녁- {16}시{17}분
                
                해뜨는 시각(일출) : {18}시 {19}분
                한낮의 시각(남중) : {20}시 {21}분
                해지는 시각(일몰) : {22}시 {23}분
            '''.format(self.travel_date.strftime("%Y-%m-%d"),self.location,longitude[0],longitude[1],
                       latitude[0],latitude[1],tw_civil[0],tw_civil[1],tw_civil[2],tw_civil[3],
                                       tw_naut[0],tw_naut[1],tw_naut[2],tw_naut[3],tw_ast[0],tw_ast[1],tw_ast[2],tw_ast[3],
                       time1[0],time1[1],time2[0],time2[1],time3[0],time3[1])
        msgPart = MIMEText(msgtext, 'plain')


        msg.attach(msgPart)


        # 메일을 발송한다.
        s = smtplib.SMTP(host,port)
        #s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("undugy98@gmail.com","undugy98")
        s.sendmail(senderAddr , [recipientAddr], msg.as_string())
        s.close()

    def Closing(self):
        SendMail.is_open = False
        self.gui.destroy()