import xml.etree.ElementTree as ET
import urllib.request
from xml.dom.minidom import parse,parseString



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


    def checkDocument(self):

        if self.SunInfoDoc == None:
            print("Error : Document is empty")
            return False
        return True

    #정보 마다로 수정해야함
    def SearchSunData(self,category):

        if not self.checkDocument():
            return None

        try:
            tree = ET.fromstring(str(self.SunInfoDoc.toxml()))
        except Exception:
            print("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None

        SunElements = tree.iter("item")
        for item in SunElements:
            strTitle = item.find(category)

        return strTitle.text

    #얘는 예외처리 따로 안할꺼임 시간부를때만 사용좀
    def LoadTimes(self,category):
        Times=self.SearchSunData(category)
        return(int(Times[:2]),int(Times[2:]))

    def InitSunHeightData(self,location,locdata):

        my_location = urllib.parse.quote(location)
        location = "&location=" + my_location

        # 날짜
        locdate = "&locdate=" + locdata

        url=location_server+encoding_key+location+locdate
        request=urllib.request.Request(url)

        response=urllib.request.urlopen(request)
        rescode=response.getcode()

        if(rescode==200):
            response_body=response.read()
            a=response_body.decode("utf-8")
            self.SunHeightDoc=parseString(a)

        else:
            print("Error Code:"+rescode)
    '''
    def SearchSunHeightData(self,a,b):
        global SuninfoDoc
        if not checkDocument():
            return None
    
        try:
            tree = ET.fromstring(str(SuninfoDoc.toxml()))
        except Exception:
            print("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None
    
        SunElements = tree.iter(a)
        for item in SunElements:
            strTitle = item.find(b)
    
        return strTitle
    '''