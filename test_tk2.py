from tkinter.constants import NW
from PIL import Image, ImageTk, ExifTags, ImageOps
import tkinter
import threading
import time
import os
#from getkey import getkey
import keyboard

terminate = False
def show_image(filenames):
    root = tkinter.Tk()
    root.title("Slide Show")

    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    root.attributes('-fullscreen', True)

    root.geometry("1920x1080")
    root.config(bg="black")

    def rotate_image(image):
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break

        exif = image._getexif()
        image = ImageOps.exif_transpose(image)
        #if exif[orientation] == 3:
        #    image=image.rotate(180, expand=True)
        #elif exif[orientation] == 6:
        #    image=image.rotate(270, expand=True)
        #elif exif[orientation] == 8:
        #    image=image.rotate(90, expand=True)
        return image

    file_index = 1
    img1 = Image.open(filenames[file_index])
    img1 = rotate_image(img1)
    img1.thumbnail(size, Image.ANTIALIAS)

    tkimg = ImageTk.PhotoImage(img1)
    #tkinter.Label(root, image=tkimg)
    canvas = tkinter.Canvas(root, width = 1920, height = 1080)
    canvas.pack()

    image_on_canvas = canvas.create_image(int((1920-tkimg.width())/2), 0, anchor="nw", image=tkimg)

    while not terminate:
        root.update()
        if keyboard.is_pressed(' '):  # if key 'q' is pressed
            file_index += 1
            if file_index >= len(filenames):
                file_index = 0
            img1 = Image.open(filenames[file_index])
            img1 = rotate_image(img1)
            img1.thumbnail(size, Image.ANTIALIAS)
            tkimg = ImageTk.PhotoImage(img1)
            canvas.itemconfig(image_on_canvas, image=tkimg)
            canvas.moveto(image_on_canvas, int((1920-tkimg.width())/2), 0)

    root.quit()

filename = r"E:\Diabilder\5b-1971\692A9421.JPG"
filename2 = r"E:\Diabilder\5b-1971\692A9449.JPG"
size = (1920,1080)
filenames = []

os.chdir(r'E:\Diabilder\5b-1971')

jpgs = []
for filename in os.listdir('.'):
    if '.jpg' in filename.lower():
        jpgs.append('E:\\Diabilder\\5b-1971\\' + filename)

#root.mainloop()
x = threading.Thread(target=show_image, args=(jpgs,))
x.start()
run = True
while(run):
    #p=getkey()
    #p = p.strip()
    if keyboard.is_pressed('esc'):  # if key 'q' is pressed
        terminate = True
        print("q pressed")
        run = False
    time.sleep(0.1)

