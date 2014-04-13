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
        self.canvasWidth = 1248
        self.canvasHeight = 1248
        self.canvas = Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
  
        # subscribe to topic amcl_pose
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.callBackY)
        rospy.init_node('subscriber')

        # self.drawMultiple()
        self.timerFired()

    def drawMultiple(self):
        margin = 50
        titlex = self.canvasWidth/2
        titley = 50
        x1 = 0
        y1 = 0 
        x2 = 700
        y2 = 0
        x3 = 200
        y3 = titley + margin + margin


        self.parent.title("High Tatras")        
        self.pack(fill=BOTH, expand=1)
         # background black
        self.canvas.create_rectangle(0,0, self.canvasWidth, self.canvasHeight, fill="black")

        # # parking lot
        # self.img3 = Image.open(PARKINGLOT)
        # self.photo3 = ImageTk.PhotoImage(self.img3)

        # self.background3 = self.canvas.create_image(x3, y3, anchor=NW, image=self.photo3)
        # self.canvas.pack(fill=BOTH, expand=2)
        # # two pictures  
        # self.img1 = Image.open(PHOTO1)
        # self.photo1 = ImageTk.PhotoImage(self.img1)

        # self.background1 = self.canvas.create_image(x1, y1, anchor=NW, image=self.photo1)
        # self.canvas.pack(fill=BOTH, expand=2)

        # self.img2 = Image.open(PHOTO2)
        # self.photo2 = ImageTk.PhotoImage(self.img2)

        # self.background2 = self.canvas.create_image(x2, y2, anchor=NW, image=self.photo2)
        # self.canvas.pack(fill=BOTH, expand=2)
        # self.background2.image = self.photo2 # keep a reference!
        
        # title text 
        tk_rgb = "#%02x%02x%02x" % (255, 255, 255)
        self.canvas.create_text(titlex,titley, font=("URW Gothic L Semi-Bold Oblique",40), fill = tk_rgb, 
           						text="Auto-Park")
        self.canvas.create_text(titlex,titley + margin, font=("URW Gothic L Semi-Bold Oblique",40), fill = tk_rgb, 
           						text="for Social Robots")
        self.canvas.pack()  

    def drawMovingCar(self, carImage, linear_x, linear_y, angular_z = 0):
        car = Image.open(carImage)
        rotatedImage = car.rotate(angular_z)
        tkimage = ImageTk.PhotoImage(rotatedImage)
        image = self.canvas.create_image(linear_x, linear_y, image=tkimage)
        
        self.image = image # keep a reference!
        
        self.canvas.pack()
        # self.canvas.pack(fill=BOTH, expand=0)

    def redrawAll(self):
        self.canvas.delete(ALL)
        # self.drawMultiple()

        # self.parent.title("High Tatras")        
        self.pack(fill=BOTH, expand=1)
        self.canvas.create_rectangle(0,0, self.canvasWidth, self.canvasHeight, fill="black")

        # rotate the cars and show
        self.drawMovingCar(CAR_YELLOW, self.linear_xy, self.linear_yy, self.angular_zy)
        # print "hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        # self.drawMovingCar(CAR_BLUE, self.c.d.angular_zb, self.c.d.linear_xb, self.c.d.linear_yb)
        # self.drawMovingCar(CAR_RED, self.c.d.angular_zr, self.c.d.linear_xr, self.c.d.linear_yr)
    
    def timerFired(self):
        self.redrawAll()
        delay = 1 # milliseconds
        self.canvas.after(delay, self.timerFired) # pause, then call timerFired again
	
    def callBackY(self, data):
        # refresh the pos values
        self.linear_xy = SCALE * data.pose.pose.position.x + self.canvasWidth/2
        self.linear_yy = -SCALE * data.pose.pose.position.y + self.canvasHeight/2
        self.angular_zy = SCALE * data.pose.pose.orientation.z
        self.angular_wy = SCALE * data.pose.pose.orientation.w

def main():  
    root = Tk()
    GUI = Draw(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 