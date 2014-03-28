import rospy
from Tkinter import *
import ImageTk
import Image
import numpy as np
import os
import tkMessageBox

from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
from std_msgs.msg import Float32

CAR_YELLOW = './images/car_yellow_100.png'
CAR_BLUE = './images/car_blue_120.png'
CAR_RED = './images/car_red_90.png'
PHOTO1 = './images/photo_1_.png'
PHOTO2 = './images/photo_2_.png'
PARKINGLOT = './images/parking_lot.gif'
SCALE = 100

class Draw(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent     
        self.canvasWidth = 1000
        self.canvasHeight = 500
        self.canvas = Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
  
        # subscribe to topic amcl_pose
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.callBackY)
        rospy.init_node('subscriber')

        self.drawMultiple()

    def drawMultiple(self):
    # def draw(self, path, x, y):
        x1 = 0
        y1 = 0 
        x2 = 700
        y2 = 0
        titlex = self.canvasWidth/2
        titley = 50
        self.parent.title("High Tatras")        
        self.pack(fill=BOTH, expand=1)
         # # background black
        self.canvas.create_rectangle(0,0, self.canvasWidth, self.canvasHeight, fill="black")
      
        self.img = Image.open(PHOTO1)
        self.photo1 = ImageTk.PhotoImage(self.img)

        self.background1 = self.canvas.create_image(x1, y1, anchor=NW, image=self.photo1)
        self.canvas.pack(fill=BOTH, expand=2)

        self.img = Image.open(PHOTO2)
        self.photo2 = ImageTk.PhotoImage(self.img)

        self.background2 = self.canvas.create_image(x2, y2, anchor=NW, image=self.photo2)
        self.canvas.pack(fill=BOTH, expand=2)
        # self.background2.image = self.photo2 # keep a reference!
        
        # title text 
        tk_rgb = "#%02x%02x%02x" % (255, 255, 255)
        self.canvas.create_text(titlex,titley, font=("URW Gothic L Semi-Bold Oblique",40), fill = tk_rgb, 
           						text="Auto-Park")
        self.canvas.create_text(titlex,titley + 50, font=("URW Gothic L Semi-Bold Oblique",40), fill = tk_rgb, 
           						text="for Social Robots")
        self.canvas.pack()  

    def callBackY(self):
        # refresh the pos values
        self.linear_xy = SCALE * self.pose.pose.position.x + self.canvasWidth/2
        self.linear_yy = -SCALE * self.pose.pose.position.y + self.canvasHeight/2
        self.angular_zy = SCALE * self.pose.pose.orientation.z
        self.angular_wy = SCALE * self.pose.pose.orientation.w

def main():  
    root = Tk()
    ex = Draw(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 