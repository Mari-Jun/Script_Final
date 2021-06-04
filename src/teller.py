#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
from SunInfo import *
import noti




class TelegramBot:
    def __init__(self):

        today = date.today()
        self.travel_date = today



        bot = telepot.Bot(noti.TOKEN)
        pprint(bot.getMe())

        bot.message_loop(self.handle)



        while 1:
            time.sleep(10)
    def makeSuninfo(self,loc_param,time):
        self.suninfo = Suninfo(loc_param, time)
        longitude = self.suninfo.LoadLongitude()
        latitude = self.suninfo.LoadLatitude()
        tw_civil = self.suninfo.LoadTimes(Suninfo.CategoryDict["시민박명(아침)"]) + self.suninfo.LoadTimes(
            Suninfo.CategoryDict["시민박명(저녁)"])
        tw_naut = self.suninfo.LoadTimes(Suninfo.CategoryDict["항해박명(아침)"]) + self.suninfo.LoadTimes(
            Suninfo.CategoryDict["항해박명(저녁)"])
        tw_ast = self.suninfo.LoadTimes(Suninfo.CategoryDict["천문박명(아침)"]) + self.suninfo.LoadTimes(
            Suninfo.CategoryDict["천문박명(저녁)"])

        time1 = self.suninfo.LoadTimes(Suninfo.CategoryDict["일출"])
        time2 = self.suninfo.LoadTimes(Suninfo.CategoryDict["일중"])
        time3 = self.suninfo.LoadTimes(Suninfo.CategoryDict["일몰"])

        msg = ''' 

                        날짜 : {0} , 지역 : {1}
                        위치: 동경 {2}도{3}분 / 북위 {4}도{5}분

                        박명시간
                        시민박명(아침/저녁) :  아침-{6}시{7}분  /  저녁- {8}시{9}분
                        항해박명(아침/저녁) : 아침-{10}시{11}분  /  저녁- {12}시{13}분
                        천문박명(아침/저녁) : 아침-{14}시{15}분  /  저녁- {16}시{17}분

                        해뜨는 시각(일출) : {18}시 {19}분
                        한낮의 시각(남중) : {20}시 {21}분
                        해지는 시각(일몰) : {22}시 {23}분

                    '''.format(time[:4]+"/"+time[4:6]+"/"+time[6:], loc_param, longitude[0], longitude[1],
                               latitude[0], latitude[1], tw_civil[0], tw_civil[1], tw_civil[2], tw_civil[3],
                               tw_naut[0], tw_naut[1], tw_naut[2], tw_naut[3], tw_ast[0], tw_ast[1], tw_ast[2],
                               tw_ast[3],
                               time1[0], time1[1], time2[0], time2[1], time3[0], time3[1])
        return msg
    def replyTodayData(self,date_param, user, loc_param='서울'):


        msg=self.makeSuninfo(loc_param,date_param)
        if msg:
            noti.sendMessage( user, msg )
        else:
            noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

    def replyDayPlaceData(self, user,loc_param ,date_param ):

            msg=self.makeSuninfo(loc_param,date_param)
            if msg:
                noti.sendMessage(user, msg)
            else:
                noti.sendMessage(user, '%s 기간에 해당하는 데이터가 없습니다.' % date_param)


    def handle(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('지역은') and len(args)>1:
            print('try to 지역', args[1])
            self.replyTodayData( self.travel_date.strftime("%Y%m%d"), chat_id, args[1] )
        elif text.startswith('여기이때')  and len(args)>2:
            print('try to 저장', args[1])
            self.replyDayPlaceData( chat_id, args[1],args[2])

        else:
            noti.sendMessage(chat_id, '모르는 명령어입니다.\n지역은 [지역이름], 여기이때 [지역이름] [날짜] 중 하나의 명령을 입력하세요.')


TelegramBot()
