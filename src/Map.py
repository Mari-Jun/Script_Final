from cefpython3 import cefpython as cef
from tkinter import *
import platform
import os

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

MAP_HTMP_PATH =  "file:///" + os.getcwd() + "/map.html"
MAP_HTMP_PATH = MAP_HTMP_PATH.replace("\\", "/")

GUI_WIDTH, GUI_HEIGHT = 600, 700

class Visitor(object):
    def Visit(self, value):
        #print("This is the HTML source:")
        #print(value)
        pass

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

        self.browser = BrowserFrame(self.gui)
        self.browser.grid(row=1, column=0, sticky=(N + S + E + W))
        Grid.rowconfigure(self.gui, 1, weight=1)
        Grid.columnconfigure(self.gui, 0, weight=1)

        cef.Initialize()
        self.browser.mainloop()
        cef.Shutdown()

        self.gui.mainloop()


class BrowserFrame(Frame):

    def __init__(self, mainframe):
        self.browser = None
        Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """

        self.UpdateInfo()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.winfo_id(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=MAP_HTMP_PATH)
        self.message_loop_work()

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def UpdateInfo(self):
        if self.browser is not None:

            self.myvisitor = Visitor()
            mainFrame = self.browser.GetMainFrame()
            mainFrame.GetSource(self.myvisitor)

        self.after(1000, self.UpdateInfo)


    def on_configure(self, _):
        self.embed_browser()