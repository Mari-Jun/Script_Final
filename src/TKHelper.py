from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

image_list = []

def CreateAlphaRectangle(gui, canvas, x1, y1, x2, y2, **kwargs):
    if "alpha" in kwargs:
        alpha = int(kwargs.pop("alpha") * 255)
        color = kwargs.pop("color")
        color = gui.winfo_rgb(color) + (alpha,)
        image = Image.new("RGBA", (x2-x1, y2-y1), color)
        image_list.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=image_list[-1], anchor="nw")
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
