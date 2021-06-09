from distutils.core import setup

setup(name="Until Sunrise",
      version="1.0",
      py_modules=["BarChart", "Calendar", "Details", "Gmail", "main", "MainGUI",
                  "Map", "noti", "Search", "SunInfo", "teller", "TKHelper", "Weather"],
      data_files=[('', ["지역위치.txt", "latlon.pyd"]),
                  ('asset', ["asset/bg_sunrise.png", "asset/bg_sunset.png", "asset/calendar.png",
                             "asset/detail.png", "asset/forecast.png", "asset/gmail.png", "asset/magnifier.png",
                             "asset/map.png", "asset/Search.jpg", "asset/sun.png", "asset/sunrise.png",
                             "asset/sunset.png", "asset/telegram.png", "asset/저작권"])]
      )
