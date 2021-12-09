import os
import sys
import time
import traceback

import keyboard
#from getkey import getkey
from PIL import Image

WINDOWS = True

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
    print("    s - VISA ALLA SLUMPADE")
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
                jpgs.append(filename)

        if randomize:
            command = command.replace('<RANDOMIZE>', '-zD 2.0')
            command = command.replace('--sort dirname ', '')
        else:
            command = command.replace('<RANDOMIZE>', '')
        print("Running command: " + command)
        time.sleep(2)
        os.system(command)

