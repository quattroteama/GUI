from Tkinter import *

import ImageTk
import Image

PHOTO1 = './images/photo_1_.png'
PHOTO2 = './images/photo_2_.png'

class DrawPicture(Frame):
    def __init__(self):
        Frame.__init__(self)   
        root = Tk()
        cwidth = 1300
        cheight= 700
        self.c = Canvas(root, width=cwidth, height=cheight)
        self.c.pack()
        
        self.c.mainloop()

    def drawMultiple(self):

        self.draw(PHOTO1)
        self.draw(PHOTO2)
    
    def draw(self, path):

        self.parent.title("High Tatras")        
        self.pack(fill=BOTH, expand=1)

        self.img = Image.open(path)
        self.photo1 = ImageTk.PhotoImage(self.img)

        self.background1 = self.canvas.create_image(x1, y1, anchor=NW, image=self.photo1)
        self.canvas.pack(fill=BOTH, expand=2)


photo = DrawPicture()
photo.drawMultiple()