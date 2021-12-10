import os
import sys
import time
import traceback
from PIL import Image, ImageTk, ExifTags, ImageOps
import tkinter
import threading

import keyboard
#from getkey import getkey
from PIL import Image

WINDOWS = True
size = (1920,1080)

if WINDOWS:
    DIR_BASE = 'e:/negativbilder'
    IMAGE_VIEWER_EXEC = "feh"
    clear = lambda: os.system('cls')
else:
    DIR_BASE = '/home/pi/Pictures'
    IMAGE_VIEWER_EXEC = "feh"
    clear = lambda: os.system('clear')

def getkey():
    return keyboard.read_key().strip()


terminate = False
def show_image(filenames):
    global terminate
    terminate = False
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
        if keyboard.is_pressed('esc'):
            terminate = True

    root.destroy()


contains_dirs = False
os.chdir(DIR_BASE)
while(1):
    clear()
    print(" KATALOG: " + os.getcwd())
    keytodirname = {}
    count = 0
    row_count = 0
    print("")
    line = ""
    dirs = os.listdir('.')
    dirs.sort()
    for dirname in dirs:
        count += 1
        keytodirname[str(count)] = dirname
        d = "    %d - %s" % (count, dirname)
        line += d
        if row_count < 0:
            row_count += 1
        else:
            print(line)
            row_count = 0
            line = ""
    if len(line) > 0:
        print(line)
    print('')
    if len(os.getcwd()) > len(DIR_BASE):
        print("    ESC - TILLBAKA")
    print("    0 - VISA ALLA")
    print("    Q - AVSLUTA")
    print("")
    #print("    SKRIV SIFFRA OCH ENTER: ")
    #p = sys.stdin.readline()
    p=getkey()
    p = p.strip()

    feh_command = "<FEH> -r -F <RANDOMIZE> --sort dirname --draw-filename --auto-rotate <DIRECTORY>"
    feh_command = feh_command.replace('<FEH>', IMAGE_VIEWER_EXEC)
    error = False
    randomize = False
    contains_dirs = False
    esc_pressed = False
    if(p=="*" or p=="'"):
        sys.exit(0)
    if(p=="Q"):
        os.system('sudo shutdown now')
    else:
        try:
            if(p=="0"):
                replace_with = "."
            elif(p=="s"):
                replace_with = "."
                randomize = True
            elif(ord(p)==27): #ESC
                esc_pressed = True
                if len(os.getcwd()) > len(DIR_BASE):
                    os.chdir('..')
            elif((ord(p))>=0x30 and (ord(p)) <= 0x39):
                try:
                    replace_with = keytodirname[p]
                    os.chdir(replace_with)
                    #print("Testing dir: " + os.getcwd())
                    contains_dirs = False
                    for dirname in os.listdir('.'):
                        filename_to_test = os.getcwd() + '/' + dirname
                        #print("Testing filename: " + filename_to_test)
                        if os.path.isdir(filename_to_test):
                            contains_dirs = True
                    if not contains_dirs:
                        os.chdir('..')
                except:
                    print("FEL...")
                    print(traceback.format_exc())
                    time.sleep(0.5)
                    error = True
            else:
                print("FEL...")
                print(traceback.format_exc())
                time.sleep(0.5)
                error = True
        except:
            print("FEL...")
            print(traceback.format_exc())
            time.sleep(0.5)
            error = True

    if not error and not contains_dirs and not esc_pressed:
        command = feh_command.replace('<DIRECTORY>', '"' + replace_with + '"')
        jpgs = []
        for filename in os.listdir(replace_with):
            if '.jpg' in filename.lower():
                jpgs.append(replace_with + "\\" + filename)

        show_image(jpgs)
        esc_pressed = True
