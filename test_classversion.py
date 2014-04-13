#!/usr/bin/env python
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

class GUI(object):
    """GUI for Auto-Parking """
    def __init__(self):

        cwidth = 1300
        cheight= 1000
        self.count = 0
        self.root = Tk()
        self.c = Canvas(self.root, width=cwidth, height=cheight)

        self.canvasWidth = cwidth
        self.canvasHeight = cheight
        # create instance of Car class 
        

        # subscriber 
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.callBackY)
        rospy.init_node('subscriber')


    def drawStaticPart(self):
        x0 = 0
        y0 = 0
        x1 = 200
        y1 = 200
        parkinglotx = self.canvasWidth/2
        parkingloty = 450
        titlex = self.canvasWidth/2
        titley = 50
        photo1x = 0
        photo1y = 0 
        photo2x = 500
        photo2y = 0
       
        self.c.create_rectangle(0,0, self.canvasWidth, self.canvasHeight, fill="black")

        # title text 
        tk_rgb = "#%02x%02x%02x" % (0, 205, 205)
        self.c.create_text(titlex,titley, font=("Rouge",40), fill = tk_rgb,
         text="Auto-Parking for Social Robots")
        self.c.pack()  
        
        # parking lot
        self.drawBackground(PARKINGLOT, parkinglotx, parkingloty)
        # self.c.pack()

    def redrawAll(self):
        # self.c.delete(ALL)

        # self.c.delete(B1)
        # self.c.delete(R1)
        if self.count != 0:
            for car in carList:
                self.c.delete(self.car)

        self.drawPicture(CAR_YELLOW, "Y", self.linear_x, self.linear_y, self.angular_z)
        self.drawPicture(CAR_BLUE, "B", self.angular_z, self.linear_x, self.linear_y)
        # self.drawPicture(CAR_RED, "R", self.angular_z, self.linear_y, self.linear_y)
        self.count += 1
    
    def timerFired(self):
        self.redrawAll()
        delay = 1000 # milliseconds
        self.c.after(delay, self.timerFired) # pause, then call timerFired again

    def callBackY(self, data):
        # refresh the pos values    
        self.linear_x = SCALE * data.pose.pose.position.x + self.canvasWidth/2
        self.linear_y = -SCALE * data.pose.pose.position.y + self.canvasHeight/2
        self.angular_z = SCALE * data.pose.pose.orientation.z
        self.angular_w = SCALE * data.pose.pose.orientation.w
    
    def run(self):
        self.drawStaticPart()
        self.timerFired()
        self.root.mainloop()


    def drawBackground(self, image, linear_x, linear_y, angular_z = 0):
        img = Image.open(image)
        rotatedImage = img.rotate(angular_z)
        self.background = ImageTk.PhotoImage(rotatedImage)
        self.background1 = self.c.create_image(linear_x, linear_y, image=self.background)
        self.c.pack()

class Car(object):
    def __init__(self, carPath):



         ##### util #####
    def drawPicture(self, carImage, carIdx, linear_x, linear_y, angular_z = 0):
        img = Image.open(carImage)
        rotatedImage = img.rotate(angular_z)
        self.carIdx = ImageTk.PhotoImage(rotatedImage)
        carIdx1  = carIdx + "1"
        self.carIdx1 = self.c.create_image(linear_x, linear_y, image=self.carIdx)
        self.c.pack()



def main():      
    test = GUI()
    test.run()

if __name__ == '__main__':
    main() 