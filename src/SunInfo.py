import xml.etree.ElementTree as ET
import urllib.request
from xml.dom.minidom import parse,parseString
import re


# 출몰정보 인증키
encoding_key="yc4yEDg1e6WWu78efmKyu3cUfYRodEuVtAKv%2FpABsgm0CvRvkx9RHCMAPXsx9v7mU6Fg7XMvq3zTBq%2BvB6ePhQ%3D%3D"
decoding_key='yc4yEDg1e6WWu78efmKyu3cUfYRodEuVtAKv/pABsgm0CvRvkx9RHCMAPXsx9v7mU6Fg7XMvq3zTBq+vB6ePhQ=='

#출몰정보 지역기준 검색
server="http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo?serviceKey="

#태양고도 인증키
encoding_key1="yc4yEDg1e6WWu78efmKyu3cUfYRodEuVtAKv%2FpABsgm0CvRvkx9RHCMAPXsx9v7mU6Fg7XMvq3zTBq%2BvB6ePhQ%3D%3D"
decoding_key1="yc4yEDg1e6WWu78efmKyu3cUfYRodEuVtAKv/pABsgm0CvRvkx9RHCMAPXsx9v7mU6Fg7XMvq3zTBq+vB6ePhQ=="

#태양고도 지역기준 검색
location_server="http://apis.data.go.kr/B090041/openapi/service/SrAltudeInfoService/getAreaSrAltudeInfo?serviceKey="


class Suninfo:
    CategoryDict = {"날짜": "locdata", "지역": "location", "경도": "longitude",
                    "경도(10진수)": "longitudeNum", "위도": "latitude", "위도(10진수)": "latitudeNum",
                    "일출": "sunrise", "일중": "suntransit", "일몰": "sunset", "월출": "moonrise",
                    "월중": "moontransit", "월몰": "moonset", "시민박명(아침)": "civilm", "시민박명(저녁)": "civile",
                    "항해박명(아침)": "nautm", "항해박명(저녁)": "naute", "천문박명(아침)": "astm", "천문박명(저녁)": "aste"
                    }
    def __init__(self,location="서울",locdata="20210515"):
        self.InitSunData(location,locdata)
        self.InitSunHeightData(location,locdata)
    def InitSunData(self,location,locdata):

        my_location = urllib.parse.quote(location)
        location = "&location=" + my_location

        # 날짜
        locdate = "&locdate=" + locdata

        url=server+encoding_key+locdate+location
        request=urllib.request.Request(url)

        response=urllib.request.urlopen(request)
        rescode=response.getcode()

        if(rescode==200):
            response_body=response.read()
            a=response_body.decode("utf-8")
            self.SunInfoDoc=parseString(a)

        else:
            print("Error Code:"+rescode)

    def InitSunHeightData(self,location,locdata):

        my_location = urllib.parse.quote(location)
        location = "&location=" + my_location

        # 날짜
        locdate = "&locdate=" + locdata

        url=location_server+encoding_key1+location+locdate
        request=urllib.request.Request(url)

        response=urllib.request.urlopen(request)
        rescode=response.getcode()

        if(rescode==200):
            response_body=response.read()
            a=response_body.decode("utf-8")
            self.SunHeightDoc=parseString(a)

        else:
            print("Error Code:"+rescode)
    def checkDocument(self,doc):

        if doc == None :
            print("Error : Document is empty")
            return False

        return True

    #정보 마다로 수정해야함
    def SearchSunData(self,category,is_SunHeight=False):

        if is_SunHeight:
            if not self.checkDocument(self.SunHeightDoc):
                return None

            try:
                tree = ET.fromstring(str(self.SunHeightDoc.toxml()))
            except Exception:
                print("Element Tree parsing Error : maybe the xml document is not corrected.")
                return None


        else:
            if not self.checkDocument(self.SunInfoDoc):
                return None

            try:
                tree = ET.fromstring(str(self.SunInfoDoc.toxml()))
            except Exception:
                print("Element Tree parsing Error : maybe the xml document is not corrected.")
                return None
        strTitle=None
        SunElements = tree.iter("item")
        for item in SunElements:
            strTitle = item.find(category)
        if strTitle==None:
            return ""
        return strTitle.text


    #얘는 예외처리 따로 안할꺼임 시간부를때만 사용좀
    def LoadTimes(self,category,is_SunHeight=False):
        Times=self.SearchSunData(category,is_SunHeight)

        if not Times.replace(' ',"")=='':

            return(int(Times[:2]),int(Times[2:4]))
        else:
            return(0,0)

    def LoadLatitude(self,is_SunHeight=False):
        latitude=self.SearchSunData(self.CategoryDict["위도"],is_SunHeight)
        if not latitude.replace(' ',"")=='':

            return(int(latitude[:2]),int(latitude[2:]))
        else:
            return(0,0)



    def LoadLongitude(self,is_SunHeight=False):
        latitude=self.SearchSunData(self.CategoryDict["경도"],is_SunHeight)
        #도,분으로 나눠서 반환
        if not latitude.replace(' ',"")=='':

            return(int(latitude[:3]),int(latitude[3:]))
        else:
            return(0,0)



    def LoadLatitudeNUM(self,is_SunHeight=False):
        latitude=self.SearchSunData(self.CategoryDict["위도(10진수)"],is_SunHeight)
        return eval(latitude)


    def LoadLongitudeNUM(self,is_SunHeight=False):
        latitude=self.SearchSunData(self.CategoryDict["경도(10진수)"],is_SunHeight)
        return eval(latitude)




    def LoadAltitude(self,time):
        altitude=self.SearchSunData("altitude_"+time,is_SunHeight=True)
        if altitude=="":
            return 0
        if altitude[0]=="-":
            return 0

        else:
            a=re.findall("\d+",altitude)
            return eval(a[0])

