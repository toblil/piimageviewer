import os
import sys
import time
import traceback
from PIL import Image, ImageTk, ExifTags, ImageOps
from PIL import ImageDraw
import tkinter
import threading
import json

import keyboard
from PIL import Image

WINDOWS = True

if not WINDOWS:
    from getkey import getkey
else:
    import msvcrt

if WINDOWS:
    DIR_BASE = r'N:\Negativbilder\Test_Image_Viewer'
    IMAGE_VIEWER_EXEC = "feh"
    clear = lambda: os.system('cls')
else:
    DIR_BASE = '/home/pi/Pictures'
    IMAGE_VIEWER_EXEC = "feh"
    clear = lambda: os.system('clear')

LOG_FILE = DIR_BASE + "/../viewlog.txt"
ROTATION_LOG_FILE = DIR_BASE + "/../rotationlog.json"
STAR_LOG_FILE = DIR_BASE + "/../stars.txt"

if WINDOWS:
    LOG_FILE = LOG_FILE.replace('/', '\\')
    ROTATION_LOG_FILE = ROTATION_LOG_FILE.replace('/', '\\')
    STAR_LOG_FILE = STAR_LOG_FILE.replace('/', '\\')

def my_getkey():
    p = keyboard.read_key().strip()
    # print(p)
    if 'ift' in p: #ift for both shift and skift
        p = keyboard.read_key().strip() #Read once more the get *
    if 'esc' in p:
        p = chr(27)
    return p

def read_rotation_data():
    data = {}
    if os.path.exists(ROTATION_LOG_FILE):
        with open(ROTATION_LOG_FILE) as f:
            data = json.load(f)
    return data

def log(filename):
    open(LOG_FILE,'at').write('%s|%f|%s\n' % (time.ctime(), time.time(), filename))

def is_starred(filename):
    already_starred = False
    line_index = -1
    if os.path.exists(STAR_LOG_FILE):
        for line in open(STAR_LOG_FILE):
            line_index += 1
            if filename in line:
                already_starred = True
                break
    return already_starred, line_index

def log_star(filename):
    starred, line_index = is_starred(filename)
    if not starred:
        open(STAR_LOG_FILE,'at').write('%s|%f|%s\n' % (time.ctime(), time.time(), filename))
    else:
        lines = open(STAR_LOG_FILE, 'rt').readlines()
        lines.pop(line_index)
        open(STAR_LOG_FILE,'wt').writelines(lines)

def log_rotation(jsondict, filename, rotation_data):
    save = False
    if not filename in jsondict:
        jsondict[filename] = rotation_data
        save = True
    else:
        if jsondict[filename] != rotation_data:
            jsondict[filename] = rotation_data
            save = True
    if save:
        with open(ROTATION_LOG_FILE, 'wt') as f:
            json.dump(jsondict, f)

#Returns exif rotation if found otherwise None
def get_rotation(jsondict, filename):
    if filename in jsondict:
        return jsondict[filename]
    return None

display_next_image_state = False
display_previous_image_state = False
rotate_image_state = False
terminate_image_show = False
star_image = False
rotation_data = read_rotation_data()

def onkeypress(event):
    global display_next_image_state
    global display_previous_image_state
    global rotate_image_state
    global star_image
    #print(event)
    if event.name == 'space':
        display_next_image_state = True
    if event.name == 'r':
        rotate_image_state = True
    if 'sterpil' in event.name or 'left' in event.name:
        display_previous_image_state = True
    if 'gerpil' in event.name or 'right' in event.name:
        display_next_image_state = True
    if 'p' == event.name:
        star_image = True

def get_jpgs(dirname):
    jpgs = []

    if 'favorites' in dirname:
        for line in open(STAR_LOG_FILE):
            filename = line.split('|')[-1].strip()
            if os.path.exists(filename):
                jpgs.append(filename)
            else:
                print("VARNING. FAVORIT SAKNAS: " + filename)
    else:
        if '.' == dirname:
            for current_dir_path, sub_folders, files in os.walk(dirname):
                for item in files:
                    if item.endswith(".jpg") :
                        fileNamePath = str(os.path.join(current_dir_path, item))
                        to_add = os.getcwd() + "\\" + fileNamePath
                        to_add = os.path.abspath(to_add)
                        jpgs.append(to_add)
        else:
            for filename in os.listdir(dirname):
                if '.jpg' in filename.lower():
                    jpgs.append(os.getcwd() + "\\" + replace_with + "\\" + filename)
    return jpgs

keyboard.on_press(onkeypress)

def show_image(filenames):
    global terminate_image_show
    global display_next_image_state
    global display_previous_image_state
    global rotate_image_state
    global rotation_data
    global star_image

    terminate_image_show = False
    root = tkinter.Tk()
    size = (root.winfo_screenwidth(), root.winfo_screenheight())
    size_str = "%dx%d" % (size[0], size[1])
    root.title("Slide Show")

    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    root.attributes('-fullscreen', True)

    root.geometry(size_str)
    root.config(bg="black")

    def get_next_exif_rotation(exif_rotation):
        if exif_rotation < 6:
            exif_rotation += 3
        elif exif_rotation == 6:
            exif_rotation = 8
        else:
            exif_rotation = 0
        return exif_rotation

    def get_exif_image_rotation(image):
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            if orientation in exif:
                if exif[orientation] is not None:
                    return exif[orientation]
        return 0

    def rotate_image(image, exif_rotation):
        if exif_rotation == 3:
            image=image.rotate(180, expand=True)
        elif exif_rotation == 6:
            image=image.rotate(270, expand=True)
        elif exif_rotation == 8:
            image=image.rotate(90, expand=True)
        else:
            pass #Do nothing. Don't rotate image.
        return image

    file_index = 0
    filename = filenames[file_index]
    filename = filename.replace('\\','/')
    print(filename)
    img1 = Image.open(filename)
    overridden_rotation = get_rotation(rotation_data, filenames[file_index])
    if overridden_rotation is not None:
        exif_rotation = overridden_rotation
    else:
        exif_rotation = get_exif_image_rotation(img1)
    original_exif_rotation = exif_rotation
    img1 = rotate_image(img1, exif_rotation)
    img1.thumbnail(size, Image.ANTIALIAS)
    #img1 = img1.resize(size)
    draw = ImageDraw.Draw(img1)
    draw.rectangle((0, 0, size[0], 10), fill='black')
    title_text = "%d av %d - %s (%dpx, %dpx) (Rotation: %d)" % (file_index+1, len(filenames), filename, size[0], size[1], exif_rotation)
    starred, line_index = is_starred(filenames[file_index])
    if starred:
        title_text = "+ " + title_text
    draw.text((0,0), title_text)

    tkimg = ImageTk.PhotoImage(img1)
    #tkinter.Label(root, image=tkimg)
    canvas = tkinter.Canvas(root, width = size[0], height = size[1])
    canvas.pack()

    image_on_canvas = canvas.create_image(int((size[0]-tkimg.width())/2), 0, anchor="nw", image=tkimg)
    log(filenames[file_index])

    while not terminate_image_show:
        root.update()
        if display_next_image_state or rotate_image_state or display_previous_image_state or star_image:
            if star_image:
                log_star(filenames[file_index])
            elif display_next_image_state or display_previous_image_state:
                if display_previous_image_state:
                    file_index -= 1
                else:
                    file_index += 1

                if file_index >= len(filenames):
                    file_index = 0
                if file_index < 0:
                    file_index = len(filenames) - 1

                filename = filenames[file_index]
                filename = filename.replace('\\','/')
                img1 = Image.open(filename)
                overridden_rotation = get_rotation(rotation_data, filenames[file_index])
                if overridden_rotation is not None:
                    exif_rotation = overridden_rotation
                else:
                    exif_rotation = get_exif_image_rotation(img1)
                original_exif_rotation = exif_rotation
            elif rotate_image_state:
                exif_rotation = get_next_exif_rotation(exif_rotation)
                img1 = Image.open(filename)
            else:
                pass # Do nothing. Why are we here?
            img1 = rotate_image(img1, exif_rotation)
            img1.thumbnail(size, Image.ANTIALIAS)
            draw = ImageDraw.Draw(img1)
            draw.rectangle((0, 0, size[0], 10), fill='black')
            title_text = "%d av %d - %s (%dpx, %dpx) (Rotation: %d)" % (file_index+1, len(filenames), filename, size[0], size[1], exif_rotation)
            starred, line_index = is_starred(filenames[file_index])
            if starred:
                title_text = "+ " + title_text
            draw.text((0,0), title_text)
            tkimg = ImageTk.PhotoImage(img1)
            canvas.itemconfig(image_on_canvas, image=tkimg)
            xPos = int((size[0]-tkimg.width())/2)
            yPos = 0
            canvas.tk.call(canvas._w, 'moveto',image_on_canvas,xPos,yPos) # Replaces: canvas.moveto(image_on_canvas, xPos, yPos)
            log(filenames[file_index])
            if original_exif_rotation != exif_rotation:
                log_rotation(rotation_data, filenames[file_index], exif_rotation)
            display_next_image_state = False
            display_previous_image_state = False
            rotate_image_state = False
            star_image = False
        if keyboard.is_pressed('esc'):
            terminate_image_show = True
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
    print("    P - VISA FAVORITER")
    print("    Q - AVSLUTA")
    #p = sys.stdin.readline()
    p=my_getkey()
    p=p.strip()

    feh_command = "<FEH> -r -F <RANDOMIZE> --sort dirname --draw-filename --auto-rotate <DIRECTORY>"
    feh_command = feh_command.replace('<FEH>', IMAGE_VIEWER_EXEC)
    error = False
    randomize = False
    contains_dirs = False
    esc_pressed = False
    show_favs = False
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
            elif(p=="p"):
                replace_with = "favorites"
            elif(ord(p)==27): #ESC
                esc_pressed = True
                if len(os.getcwd()) > len(DIR_BASE):
                    os.chdir('..')
            elif((ord(p))>=0x30 and (ord(p)) <= 0x39):
                try:
                    replace_with = keytodirname[p]
                    #print("Key: " + replace_with)
                    os.chdir(replace_with)
                    #print("Testing dir: " + os.getcwd())
                    contains_dirs = False
                    for dirname in os.listdir('.'):
                        filename_to_test = os.getcwd() + '/' + dirname
                        #print("Testing filename: " + filename_to_test)
                        if os.path.isdir(filename_to_test):
                            contains_dirs = True
                            #print("IS DIR")
                        else:
                            #print("IS NOT DIR")
                            pass
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
            print(p)
            print(traceback.format_exc())
            time.sleep(0.5)
            error = True

    if not error and not contains_dirs and not esc_pressed:
        command = feh_command.replace('<DIRECTORY>', '"' + replace_with + '"')
        jpgs = get_jpgs(replace_with)

        if len(jpgs) > 0:
            show_image(jpgs)

        esc_pressed = True
