

import random
import tkinter as tk
from  TKHelper import *

###############################################################################################
#바 차트
class BarChart:

    def __init__(self,width,height,data,gui,y_stretch=15,y_gap=20,x_stretch=10,
                 x_width=20,x_gap=20):
        self.data =data
        self.width = width
        self.height = height
        self.y_stretch = y_stretch
        self.y_gap = y_gap
        self.x_stretch = x_stretch
        self.x_width = x_width
        self.x_gap = x_gap
        self.canvas=gui.canvas
        self.barlist=[]
        self.dotextlist=[]
        self.sitextlist = []
    def DrawBar(self):
     for x, y in enumerate(self.data):
        # calculate reactangle coordinates
        x0 = x * self.x_stretch + x * self.x_width + self.x_gap
        y0 = self.height - (y * self.y_stretch + self.y_gap)
        x1 = x * self.x_stretch + x * self.x_width + self.x_width + self.x_gap
        y1 = self.height - self.y_gap
        # Here we draw the bar
        self.barlist.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill="steelblue"))
        self.dotextlist.append(self.canvas.create_text(x0, y0, anchor=tk.SW, text=str(y)+"도",font=font_dic["CooperSmall"]))
        self.sitextlist.append(self.canvas.create_text(x0 , self.height, anchor=tk.SW, text=str(x+9) + "시",font=font_dic["CooperSmall"]))
    def resetbar(self):
        for x in self.barlist:
            self.canvas.delete(x)
        for x in self.dotextlist:
            self.canvas.delete(x)
        for x in self.sitextlist:
            self.canvas.delete(x)
        pass


