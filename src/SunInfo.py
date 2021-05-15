import xml.etree.ElementTree as ET
import urllib.request
from xml.dom.minidom import parse,parseString

Sun_infoDoc=None

#인증키
encoding_key="yc4yEDg1e6WWu78efmKyu3cUfYRodEuVtAKv%2FpABsgm0CvRvkx9RHCMAPXsx9v7mU6Fg7XMvq3zTBq%2BvB6ePhQ%3D%3D"
decoding_key='yc4yEDg1e6WWu78efmKyu3cUfYRodEuVtAKv/pABsgm0CvRvkx9RHCMAPXsx9v7mU6Fg7XMvq3zTBq+vB6ePhQ=='

#지역기준 검색
server="http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo?serviceKey="








def InitData(location,locdata):
    global Sun_infoDoc
    # 지역
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
        Sun_infoDoc=parseString(a)

    else:
        print("Error Code:"+rescode)


def checkDocument():
    global Sun_infoDoc
    if Sun_infoDoc == None:
        print("Error : Document is empty")
        return False
    return True

#정보 마다로 수정해야함
def SearchSunData(category):
    global Sun_infoDoc
    if not checkDocument():
        return None

    try:
        tree = ET.fromstring(str(Sun_infoDoc.toxml()))
    except Exception:
        print("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None

    SunElements = tree.iter("item")
    for item in SunElements:
        strTitle = item.find(category)

    return strTitle.text

InitData("서울","20210515")
'''
나중에 태양고도용
def SearchSunData(a,b):
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