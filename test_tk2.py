from tkinter.constants import NW
from PIL import Image, ImageTk
import tkinter
import threading
import time
#from getkey import getkey
import keyboard

terminate = False

def show_image(filename):
    root = tkinter.Tk()
    root.title("Slide Show")

    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    root.attributes('-fullscreen', True)

    root.geometry("1920x1080")
    root.config(bg="black")

    img1 = Image.open(filename)
    img1.thumbnail(size, Image.ANTIALIAS)

    tkimg = ImageTk.PhotoImage(img1)
    #tkinter.Label(root, image=tkimg)
    canvas = tkinter.Canvas(root, width = img1.width, height = img1.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=NW, image=tkimg)
    while not terminate:
        root.update()
    root.quit()

filename = r"E:\Diabilder\5b-1971\692A9421.JPG"

size = (1920*0.8,1080*0.8)

#root.mainloop()
x = threading.Thread(target=show_image, args=(filename,))
x.start()
while(1):
    #p=getkey()
    #p = p.strip()
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        terminate = True
        print("q pressed")
    time.sleep(0.1)
