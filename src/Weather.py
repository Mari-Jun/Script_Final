import urllib.request
import json
import base64
import datetime
from TKHelper import *

apikey = "733f3162f8e13267b03559210f37cc68"

api_cur = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
icon_url = "http://openweathermap.org/img/wn/{icon}@2x.png"

k2c = lambda k: k - 273.15

json_data = None

def LoadCurrentWeather(city):
    url = api_cur.format(city=city, key=apikey)
    url_data = urllib.request.urlopen(url)
    weather_data = url_data.read()

    global json_data
    json_data = json.loads(weather_data)

def ShowCurrentWeather():
    global json_data
    print(json_data)
    url = icon_url.format(icon=json_data["weather"][0]["icon"])
    icon_url_data = urllib.request.urlopen(url)
    icon_data = icon_url_data.read()
    data = [json_data["weather"][0]["description"], round(k2c(json_data["main"]["temp"])), json_data["clouds"]["all"],\
            base64.encodebytes(icon_data)]
    return data

class ForecastGUI:
    def __init__(self, MainGui):
        self.main_gui = MainGui
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("Forecast")



# print("+ 도시 =", json_data["name"])

# print("| 최저 기온 =", k2c(json_data["main"]["temp_min"]))
# print("| 최고 기온 =", k2c(json_data["main"]["temp_max"]))
# print("| 습도 =", json_data["main"]["humidity"])
# print("| 기압 =", json_data["main"]["pressure"])
# print("| 풍향 =", json_data["wind"]["deg"])
# print("| 풍속 =", json_data["wind"]["speed"])

# api_day = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}8&exclude=hourly&appid={key}"
#
# url = api_day.format(lat=json_data["coord"]["lat"], lon=json_data["coord"]["lon"], key=apikey)
# url_data = urllib.request.urlopen(url)
# day_data = url_data.read()
# json_data = json.loads(day_data)
#
# cg_unix = lambda ts: (datetime.datetime.fromtimestamp(ts) - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
#
# unix_ts = 1621047600
# dt = cg_unix(unix_ts)
# print(dt)
#
# print(cg_unix(json_data["current"]["dt"]))
# print(cg_unix(json_data["daily"][0]["dt"]))
# print(cg_unix(json_data["daily"][1]["dt"]))
# print(cg_unix(json_data["daily"][2]["dt"]))
# print(cg_unix(json_data["daily"][3]["dt"]))
# print(cg_unix(json_data["daily"][4]["dt"]))
#
# print(json_data)