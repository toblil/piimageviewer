from tkinter.constants import NW
from PIL import Image, ImageTk
import tkinter
filename = r"E:\Diabilder\5b-1971\692A9421.JPG"

size = (1920*0.5,1080*0.5)

root = tkinter.Tk()
root.title("Slide Show")
#root.geometry("1920x900")
root.config(bg="black")
img1 = Image.open(filename)
img1.thumbnail(size, Image.ANTIALIAS)

tkimg = ImageTk.PhotoImage(img1)
#tkinter.Label(root, image=tkimg)
# canvas = tkinter.Canvas(root, width = 1800, height = 900)
# canvas.pack()
# canvas.create_image(0, 0, anchor=NW, image=tkimg) 
root.mainloop()
