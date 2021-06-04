from cefpython3 import cefpython as cef
from tkinter import *
import platform
import os
import sys
import threading
from bs4 import BeautifulSoup

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

MAP_HTMP_PATH =  "file:///" + os.getcwd() + "/map.html"
MAP_HTMP_PATH = MAP_HTMP_PATH.replace("\\", "/")
MAP_HTMP_PATH = "https://marijunscript.neocities.org"

GUI_WIDTH, GUI_HEIGHT = 600, 700



class Visitor(object):
    def __init__(self, MainGui):
        self.main_gui = MainGui

    def Visit(self, value):
        html = BeautifulSoup(value, "html.parser")
        addr = html.find("span", {"id":"centerAddr"})
        latlng = html.find("span", {"id":"latlng"})

        if len(addr.text):
            self.main_gui.UpdateLocation(addr=addr.text)
        if len(latlng.text):
            latlng = eval(latlng.text)
            self.main_gui.UpdateLocation(lat=str(latlng[0]), lon=str(latlng[1]))


browser = None

def embed_broser(frame):
    global browser
    window_info = cef.WindowInfo(frame.winfo_id())
    rect = [0, 0, GUI_WIDTH, GUI_HEIGHT]
    window_info.SetAsChild(frame.winfo_id(), rect)
    settings = {}
    settings["multi_threaded_message_loop"] = False
    cef.Initialize(settings=settings)
    browser = cef.CreateBrowserSync(window_info, url=MAP_HTMP_PATH)
    cef.MessageLoop()


class MapGUI:
    is_open = False
    def __init__(self, MainGui):
        if MapGUI.is_open:
            return
        self.main_gui = MainGui
        self.gui = Toplevel(self.main_gui.gui)
        self.gui.title("Map")
        self.gui.geometry("{width}x{height}".format(width=GUI_WIDTH, height=GUI_HEIGHT))
        self.gui.resizable(width=False, height=False)
        self.gui.protocol("WM_DELETE_WINDOW", self.Closing)

        self.frame = Frame(self.gui, width=GUI_WIDTH, height=GUI_HEIGHT)
        self.frame.grid(row=1, column=0, sticky=(N + S + E + W))
        Grid.rowconfigure(self.gui, 1, weight=1)
        Grid.columnconfigure(self.gui, 0, weight=1)

        self.UpdateInfo()

        self.thread = threading.Thread(target=embed_broser, args=(self.frame,))
        self.thread.daemon = True
        self.thread.start()

    def UpdateInfo(self):
        global browser
        if browser is not None:
            self.myvisitor = Visitor(self.main_gui)
            mainFrame = browser.GetMainFrame()
            mainFrame.GetSource(self.myvisitor)

        self.gui.after(1000, self.UpdateInfo)

    def Closing(self):
        global browser
        MapGUI.is_open = False
        browser = None
        cef.QuitMessageLoop()
        self.gui.destroy()


class BrowserFrame(Frame):

    def __init__(self, mainframe, MainGUI):
        self.browser = None
        Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.main_gui = MainGUI
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """

    def on_configure(self, _):
        self.embed_browser()