from tkinter import *
from PIL import Image, ImageTk
root = Tk()
root.title("Slide Show")
root.geometry("1000x600")
root.config(bg="blue4")
root.resizable(0, 0)
def start():                                                     
    global i, show
    if i >= (len(images)-1):
        i = 0
        slide_image.config(image = images[i])
    else:
        i = i + 1
        slide_image.configure(image = images[i])
    show = slide_image.after(2000 , start)
def stop():
    global show
    slide_image.after_cancel(show)
    
def resume():
    start()
            
# create thumbanials of all images  
img1 = Image.open('slide1.png')
img1.thumbnail((600, 650))      # 650 --> 550
img2 = Image.open('slide2.png')
img2.thumbnail((600, 650))
img3 = Image.open('slide3.png')
img3.thumbnail((600, 650))
img4 = Image.open('slide4.png')
img4.thumbnail((600, 650))
# open images to use with labels
image1 = ImageTk.PhotoImage(img1)
image2 = ImageTk.PhotoImage(img2)
image3 = ImageTk.PhotoImage(img3)
image4 = ImageTk.PhotoImage(img4)
# create list of images
images = [image1, image2, image3, image4]
# configure the image to the Label 
i = 0
slide_image = Label(root , image=images[i])
slide_image.pack(pady=50)
# create buttons
btn1 = Button(root, text="Start", bg='black', fg='gold', width=6, font=('ariel 20 bold'), relief=GROOVE, command=start)
btn1.pack(side=LEFT, padx=60, pady=50)
btn2 = Button(root, text="Pause/Stop", bg='black', fg='gold', width=10, font=('ariel 20 bold'), relief=GROOVE, command=stop)
btn2.pack(side=LEFT, padx=60, pady=50)
btn3 = Button(root, text="Resume", bg='black', fg='gold', width=8, font=('ariel 20 bold'), relief=GROOVE, command=resume)
btn3.pack(side=LEFT, padx=60, pady=50)
btn4 = Button(root, text="Exit", bg='black', fg='gold', width=6, font=('ariel 20 bold'), relief=GROOVE, command=root.destroy)
btn4.pack(side=LEFT, padx=30, pady=50)
root.mainloop()
