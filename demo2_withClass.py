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

PARKINGLOT = './images/background.jpg'
SCALE = 100

class GUI(object):
    """docstring for GUI"""
    def __init__(self):
        print "here"
        cwidth = 1000
        cheight= 750
        self.count = 0
        r1 = 13
        r2 = 16
        r3 = 10

        self.root = Tk()
        self.c = Canvas(self.root, width=cwidth, height=cheight)

        self.canvasWidth = cwidth
        self.canvasHeight = cheight
        self.parkinglotx = self.canvasWidth/2
        self.parkingloty = self.canvasHeight/2

        # create instances of cars 
    	self.car1 = Car(self.c, r1, "blue", self.parkinglotx, self.parkingloty)
    	self.car2 = Car(self.c, r2, "green", self.parkinglotx, self.parkingloty)
    	self.car3 = Car(self.c, r3, "Orange", self.parkinglotx, self.parkingloty)
        # subscriber

        rospy.init_node('subscriber')
        rospy.Subscriber('car1/amcl_pose', PoseWithCovarianceStamped, self.car1.callBack)
        rospy.Subscriber('car2/amcl_pose', PoseWithCovarianceStamped, self.car2.callBack)
        rospy.Subscriber('car3/amcl_pose', PoseWithCovarianceStamped, self.car3.callBack)


    def redrawAll(self):
        self.c.delete(ALL)
        # parking lot
        self.drawBackground(PARKINGLOT, self.parkinglotx, self.parkingloty)
        self.c.pack()

        x1, y1, z1 = self.car1.linear_x, self.car1.linear_y, self.car1.angular_z
        x2, y2, z2 = self.car2.linear_x, self.car2.linear_y, self.car2.angular_z
        x3, y3, z3 = self.car3.linear_x, self.car3.linear_y, self.car3.angular_z

		            
        coordinatesY = "%.0fcm, %.0fcm" %(x1, y1)
        coordinatesB = "%.0fcm, %.0fcm" %(x2 + 200, y2 + 200)
        coordinatesR = "%.0fcm, %.0fcm" %(x3 + 200, y3 + 230)

        self.c.create_text(20, self.canvasHeight/3, anchor = "nw", font = "Ariel, 15", text = "Yellow Car: " + str(coordinatesY))
        self.c.create_text(20, self.canvasHeight/3 + 40, anchor = "nw", font = "Ariel, 15", text = "Blue Car: "+ str(coordinatesB))
        self.c.create_text(20, self.canvasHeight/3 + 80, anchor = "nw", font = "Ariel, 15", text = "Red Car: "+ str(coordinatesR))
    
    	self.car1.drawCar()
    	self.car2.drawCar()
    	self.car3.drawCar()

    def timerFired(self):
        self.redrawAll()
        delay = 1 # milliseconds
        self.c.after(delay, self.timerFired) # pause, then call timerFired again


    def run(self):
        self.timerFired()
        self.root.mainloop()

    ##### util #####
    def drawBackground(self, image, linear_x, linear_y, angular_z = 0):
        img = Image.open(image)
        self.background = ImageTk.PhotoImage(img)
        self.background1 = self.c.create_image(linear_x, linear_y, image=self.background)
        self.c.pack()

class Car(object):
    def __init__(self, c, r, color, parkinglotx, parkingloty):
        self.linear_x = parkinglotx + 200
        self.linear_y = parkingloty + 230
        self.angular_z = 0
        self.c = c
        self.r = r
        self.color = color

    def drawCar(self):
        r = self.r
        scale_x = float(435)/625
        scale_y = float(350)/522  
        scale_cmToPixel = 75
        offset_y = 45

        x = 280 + self.linear_x * scale_x
        y = 580 - (self.linear_y - offset_y) * scale_y

        color = self.color
	self.c.create_rectangle(x-r, y-r, x+r, y+r, fill = color, outline = color)
	
##    def returnCoord(self):
##        
##        return self.linear_x, self.linear_y, self.angular_z

    def callBack(self, data):
	meterToCm = 100
        # refresh the pos values    
        if data.pose.pose.position != None: 
            self.linear_x = 100*data.pose.pose.position.x 
            self.linear_y = 100*data.pose.pose.position.y
            self.angular_z = 100*data.pose.pose.orientation.z
        else: 
            self.linear_x = 625 
            self.linear_y = 605
            self.angular_z = 0
 


def main():      
    test = GUI()
    test.run()

if __name__ == '__main__':
    main() 
