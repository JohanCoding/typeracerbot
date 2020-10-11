from PIL import Image, ImageTk, ImageGrab, ImageEnhance
import PIL
import pyscreenshot as ImageGrab
import re
import tkinter as tk
import time
from pynput.keyboard import Key, Controller
from pytesseract import image_to_string
keyboard = Controller()

root = tk.Tk()
root.resizable(0, 0)
def tr():
    x1 = y1 = x2 = y2 = 0
    roi_image = None

    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')

    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete('roi-image') # remove old overlay image
        roi_image = image.crop((x1, y1, x2, y2)) # get the image of selected region
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
        # make sure the select rectangle is on top of the overlay image
        canvas.lift('roi')

    root.withdraw()  # hide the root window
    image = ImageGrab.grab()  # grab the fullscreen as select region background
    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken the capture image
    # create a fullscreen window to perform the select region action
    win = tk.Toplevel()
    win.attributes('-fullscreen', 1)
    win.attributes('-topmost', 1)
    canvas = tk.Canvas(win, highlightthickness=0)
    canvas.pack(fill='both', expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')
    # bind the mouse events for selecting region
    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<B1-Motion>', on_mouse_move)
    win.bind('<ButtonRelease-1>', lambda e: win.destroy())
    # use Esc key to abort the capture
    win.bind('<Escape>', lambda e: win.destroy())
    # make the capture window modal
    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify()  # restore root window
    im=ImageGrab.grab(bbox=(x1,y1,x2,y2))
    im.save('tr.png')
    image = Image.open('tr.png', mode='r')
    typeracertext = image_to_string(image)
    styperacer = typeracertext[:-1]
    filter = styperacer.replace('|', 'I')
    filter = filter.replace('Lf', 'If')
    filter = filter.replace('Guest', '')
    filter = filter.replace('>', '')
    filter = filter.replace('>', '')
    filter = filter.replace('\\', '')
    filter = filter.replace('change display format', '')
    bignew = filter.replace(' ', ' ').split()
    print(bignew)
    time.sleep(1.2)
    for word in bignew:
        keyboard.type(word)
        keyboard.press(Key.space)
        time.sleep(0.1)
    root.destroy()

tr()

root.mainloop()
