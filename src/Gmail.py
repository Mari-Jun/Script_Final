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
        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "해가 뜰때까지에서 보내드립니다"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr
        self.suninfo=Suninfo(self.location,self.travel_date.strftime("%Y%m%d"))
        msgtext='''#
                #efmwekfmwekfm'  WEL;KFMW
                #EFKWOEFMGWRGMWRLDFWㄺ흐제갷
                #ㄷ개랒ㄷ랍ㅈ[ㄷ래ㅔㅏㅂㅈ[ㄷㄹ
                #라라라대자ㅡㄷ[히ㅐㅡ직ㄷ흐
            #ㅈ ㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄷ ㅇㅇ ㄷㅇㅂㅈㄷㄱ
            '''
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