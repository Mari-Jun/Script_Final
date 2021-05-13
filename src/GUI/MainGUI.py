from tkinter import *
from PIL import Image, ImageTk

B_Size = 80
B_POS_X, B_POS_Y = 1100, 100

class MainGUI:
    def __init__(self):
        self.gui = Tk()
        self.gui.title("해가 뜰 때까지")
        self.gui.geometry("1280x720")
        self.gui.resizable(width=False, height=False)

        self.LoadBackGround()
        self.LoadButtons()

        self.gui.mainloop()

    def LoadBackGround(self):
        self.bgImg = PhotoImage(file="asset/bg_sunset.png")
        self.bg_label = Label(self.gui, image=self.bgImg)
        self.bg_label.place(x=-2, y=-2)

        pass

    def LoadButtons(self):
        self.b_image_list = []
        self.SetMainButton("asset/magnifier.png", B_POS_X, B_POS_Y)
        self.SetMainButton("asset/map.png", B_POS_X, B_POS_Y + B_Size)
        self.SetMainButton("asset/calendar.png", B_POS_X, B_POS_Y + B_Size * 2)
        self.SetMainButton("asset/sunset.png", B_POS_X, B_POS_Y + B_Size * 3)
        self.SetMainButton("asset/detail.png", B_POS_X, B_POS_Y + B_Size * 4)
        self.SetMainButton("asset/gmail.png", B_POS_X, B_POS_Y + B_Size * 5)
        self.SetMainButton("asset/telegram.png", B_POS_X, B_POS_Y + B_Size * 6)


    def SetMainButton(self, dir, x_pos, y_pos):
        img = Image.open(dir)
        img = img.resize((B_Size, B_Size), Image.ANTIALIAS)
        b_image = ImageTk.PhotoImage(img)
        self.b_image_list.append(b_image)
        Button(self.gui, image=b_image, width=B_Size, height=B_Size).place(x=x_pos, y=y_pos)
