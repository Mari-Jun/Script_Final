import urllib.request
import json
import base64
from TKHelper import *

show_icon = False

apikey = "733f3162f8e13267b03559210f37cc68"

api_cur = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
api_cur_geo = "http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={key}"
api_day = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}8&exclude=hourly&appid={key}"
icon_url = "http://openweathermap.org/img/wn/{icon}@2x.png"

k2c = lambda k: k - 273.15

json_data = None
json_day_data = None
icon_data = {}

def LoadIconData():
    if not show_icon:
        return
    icons = ["01d", "02d", "03d", "04d", "09d", "10d", "11d", "13d", "50d",\
             "01n", "02n", "03n", "04n", "09n", "10n", "11n", "13n", "50n"]
    for icon in icons:
        url = icon_url.format(icon=icon)
        icon_url_data = urllib.request.urlopen(url)
        icon_data[icon] = PhotoImage(data=base64.encodebytes(icon_url_data.read()))

def LoadCurrentWeather(city):
    url = api_cur.format(city=city, key=apikey)
    url_data = urllib.request.urlopen(url)
    weather_data = url_data.read()
    global json_data
    json_data = json.loads(weather_data)

def LoadCurrentWeather(lat, lon):
    url = api_cur_geo.format(lat=lat, lon=lon, key=apikey)
    url_data = urllib.request.urlopen(url)
    weather_data = url_data.read()
    global json_data
    json_data = json.loads(weather_data)

def ShowCurrentWeather():
    global json_data
    data = [json_data["weather"][0]["description"], round(k2c(json_data["main"]["temp"])), json_data["clouds"]["all"],\
            icon_data[json_data["weather"][0]["icon"]] if show_icon else None]
    return data

F_WIDTH, F_HEIGHT = 900, 500
CW_WIDTH, CW_HEIGHT = 900, 200
WW_WIDTH = 150

class ForecastGUI:
    is_open = False
    def __init__(self, MainGui):
        if ForecastGUI.is_open:
            return
        self.main_gui = MainGui
        self.main_gui.forecast = self
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("Forecast")
        self.gui.geometry("{width}x{height}".format(width=F_WIDTH, height=F_HEIGHT))
        self.gui.resizable(width=False, height=False)
        self.canvas = Canvas(self.gui, height=F_HEIGHT, width=F_WIDTH, background="sky blue")
        self.canvas.pack()

        self.cur_data = {}
        self.week_data = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}

        self.SetCurWeatherInfo()
        self.SetWeekWeatherInfo()

        self.gui.protocol("WM_DELETE_WINDOW", self.Closing)

        ForecastGUI.is_open = True

        self.gui.mainloop()

    def SetCurWeatherInfo(self):
        CreateAlphaRectangle(self.gui, self.canvas, 5, 10, CW_WIDTH - 5, CW_HEIGHT - 10,\
                             color="white", alpha=0.7)
        self.cur_data["date"] = self.canvas.create_text((CW_WIDTH // 2, 35), font=font_dic["Forte"], anchor=CENTER)
        self.cur_data["temp"] = self.canvas.create_text((CW_WIDTH // 2, 85), font=font_dic["Forte20"], anchor=CENTER)
        self.cur_data["wind"] = self.canvas.create_text((CW_WIDTH // 2, 125), font=font_dic["Forte20"], anchor=CENTER)
        self.cur_data["etc"] = self.canvas.create_text((CW_WIDTH // 2, 165), font=font_dic["Forte20"], anchor=CENTER)

        self.UpdateCurWeatherInfo()

    def UpdateCurWeatherInfoDirect(self):
        self.canvas.itemconfig(self.cur_data["date"], text="{0} - {1}".format( \
            cg_unix_mdh(json_data["dt"]), cg_unix_d(json_data["dt"])))
        self.canvas.itemconfig(self.cur_data["temp"], \
                               text="현재 온도 : {temp:.1f}ºC, 체감 온도 : {feel:.1f}ºC, 습도 : {humi}%".format( \
                                   temp=k2c(json_data["main"]["temp"]), feel=k2c(json_data["main"]["feels_like"]), \
                                   humi=json_data["main"]["humidity"]))
        self.canvas.itemconfig(self.cur_data["wind"], text="풍속 : {speed}meter/sec, 방향 : {deg}º".format( \
            speed=json_data["wind"]["speed"], deg=json_data["wind"]["deg"]))
        self.canvas.itemconfig(self.cur_data["etc"], text="강우량 : {rain}mm/h, 강설량 : {snow}mm/h".format( \
            rain=json_data["rain"]["1h"] if "rain" in json_data else 0, \
            snow=json_data["snow"]["1h"] if "snow" in json_data else 0))

    def UpdateCurWeatherInfo(self):
        self.UpdateCurWeatherInfoDirect()
        self.gui.after(5000, self.UpdateCurWeatherInfo)

    def SetWeekWeatherInfo(self):
        self.SetDailyWeatherInfo(WW_WIDTH * 0 + WW_WIDTH // 2, CW_HEIGHT + 10, 1)
        self.SetDailyWeatherInfo(WW_WIDTH * 1 + WW_WIDTH // 2, CW_HEIGHT + 10, 2)
        self.SetDailyWeatherInfo(WW_WIDTH * 2 + WW_WIDTH // 2, CW_HEIGHT + 10, 3)
        self.SetDailyWeatherInfo(WW_WIDTH * 3 + WW_WIDTH // 2, CW_HEIGHT + 10, 4)
        self.SetDailyWeatherInfo(WW_WIDTH * 4 + WW_WIDTH // 2, CW_HEIGHT + 10, 5)
        self.SetDailyWeatherInfo(WW_WIDTH * 5 + WW_WIDTH // 2, CW_HEIGHT + 10, 6)

        self.UpdateWeekWeatherInfo()

    def SetDailyWeatherInfo(self, x, y, day):
        CreateAlphaRectangle(self.gui, self.canvas, x - WW_WIDTH // 2 + 5, CW_HEIGHT + 10,\
                             x + WW_WIDTH // 2 - 5, F_HEIGHT - 10, color="white", alpha=0.7)
        self.week_data[day]["day"] = self.canvas.create_text((x, y + 25), font=font_dic["Cooper"], anchor=CENTER)
        self.week_data[day]["date"] = self.canvas.create_text((x, y + 65), font=font_dic["Cooper"], anchor=CENTER)
        self.week_data[day]["icon"] = self.canvas.create_image((x, y + 115), image=None, anchor=CENTER)
        self.week_data[day]["temp_min"] = self.canvas.create_text((x, y + 185), font=font_dic["Cooper"],\
                                                                  anchor=CENTER, fill="royal blue")
        self.week_data[day]["temp_max"] = self.canvas.create_text((x, y + 215), font=font_dic["Cooper"],\
                                                                  anchor=CENTER, fill="orange red")
        self.week_data[day]["pop"] = self.canvas.create_text((x, y + 245), font=font_dic["Cooper"],\
                                                             anchor=CENTER, fill="deep sky blue")

    def LoadJsonData(self):
        global json_data, json_day_data
        url = api_day.format(lat=json_data["coord"]["lat"], lon=json_data["coord"]["lon"], key=apikey)
        url_data = urllib.request.urlopen(url)
        day_data = url_data.read()
        json_day_data = json.loads(day_data)

    def UpdateWeekWeatherInfoDirect(self):
        self.LoadJsonData()
        self.UpdateDailyWeatherInfo(day=1)
        self.UpdateDailyWeatherInfo(day=2)
        self.UpdateDailyWeatherInfo(day=3)
        self.UpdateDailyWeatherInfo(day=4)
        self.UpdateDailyWeatherInfo(day=5)
        self.UpdateDailyWeatherInfo(day=6)

    def UpdateWeekWeatherInfo(self):
        self.UpdateWeekWeatherInfoDirect()
        self.gui.after(60000, self.UpdateWeekWeatherInfo)

    def UpdateDailyWeatherInfo(self, day):
        self.canvas.itemconfig(self.week_data[day]["day"], text=cg_unix_d(json_day_data["daily"][day]["dt"]))
        self.canvas.itemconfig(self.week_data[day]["date"], text=cg_unix_md(json_day_data["daily"][day]["dt"]))
        self.canvas.itemconfig(self.week_data[day]["temp_min"], text="min : {min}ºC".format(\
            min=round(k2c(json_day_data["daily"][day]["temp"]["min"]))))
        self.canvas.itemconfig(self.week_data[day]["temp_max"], text="max : {max}ºC".format( \
            max=round(k2c(json_day_data["daily"][day]["temp"]["max"]))))
        self.canvas.itemconfig(self.week_data[day]["pop"], text="pop : {pop}%".format(\
            pop=int(json_day_data["daily"][day]["pop"] * 100)))
        self.canvas.itemconfig(self.week_data[day]["icon"],\
            image=icon_data[json_day_data["daily"][day]["weather"][0]["icon"]] if show_icon else None)

    def Closing(self):
        ForecastGUI.is_open = False
        self.gui.destroy()
