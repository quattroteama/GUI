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

class Draw(object):
    """docstring for Draw"""
    def __init__(self):

        cwidth = 1200
        cheight= 785
        self.count = 0

        self.root = Tk()
        self.c = Canvas(self.root, width=cwidth, height=cheight)

        self.canvasWidth = cwidth
        self.canvasHeight = cheight
        self.parkinglotx = self.canvasWidth/2
        self.parkingloty = self.canvasHeight/2
        # self.drawBackground(PARKINGLOT, self.parkinglotx, self.parkingloty)
    
        # subscriber 
        rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.callBackY)
        rospy.init_node('subscriber_Y')

        # rospy.Subscriber('carB_amcl_pose', PoseWithCovarianceStamped, self.callBackB)
        # rospy.init_node('subscriber_B')

    def redrawAll(self):
        self.c.delete(ALL)
        # parking lot
        self.drawBackground(PARKINGLOT, self.parkinglotx, self.parkingloty)
        self.c.pack()
        r1 = 8
        r2 = 12
        r3 = 15
        coordinatesY = "%.0fcm, %.0fcm" %(self.linear_xy, self.linear_yy)
        coordinatesB = "%.0fcm, %.0fcm" %(self.parkinglotx + 200, self.parkingloty + 200)
        coordinatesR = "%.0fcm, %.0fcm" %(self.parkinglotx + 200, self.parkingloty + 230)

        self.c.create_text(20, self.canvasHeight/3, anchor = "nw", font = "Ariel, 15", text = "Yellow Car: " + str(coordinatesY))
        self.c.create_text(20, self.canvasHeight/3 + 40, anchor = "nw", font = "Ariel, 15", text = "Blue Car: "+ str(coordinatesB))
        self.c.create_text(20, self.canvasHeight/3 + 80, anchor = "nw", font = "Ariel, 15", text = "Red Car: "+ str(coordinatesR))

        self.c.create_rectangle(self.linear_xy-r1, self.linear_yy-r1, self.linear_xy+r1, self.linear_yy+r1,
                                fill = "yellow", outline = "yellow")

        self.c.create_rectangle(self.parkinglotx + 200-r2, (self.parkingloty + 200)-r2, 
            (self.parkinglotx + 200)+r2, self.parkingloty+200+r2, fill = "blue", outline = "blue")
        
        self.c.create_rectangle(self.parkinglotx + 200-r3, (self.parkingloty + 230)-r3, 
            (self.parkinglotx + 200)+r3, self.parkingloty+230+r3,
                                fill = "red", outline = "red")
        # self.c.create_rectangle((self.linear_yy + 100)-r2, (self.linear_xy - 100)-r2, (self.linear_yy + 100)+r2, self.linear_xy-100+r2,
                                # fill = "blue", outline = "blue")
        # self.c.create_rectangle((self.angular_zy +self.canvasWidth/2) -r3, (self.linear_yy + 20)-r3, 
            # (self.angular_zy + self.canvasWidth/2)+r3, (self.linear_yy+20)+r3,
                                # fill = "red", outline = "red")
    
    def timerFired(self):
        self.redrawAll()
        delay = 1 # milliseconds
        self.c.after(delay, self.timerFired) # pause, then call timerFired again

    def callBackY(self, data):
        # refresh the pos values    
        self.linear_xy = SCALE * data.pose.pose.position.x + self.canvasWidth/2
        self.linear_yy = -SCALE * data.pose.pose.position.y + self.canvasHeight/2
        self.angular_zy = SCALE * data.pose.pose.orientation.z
    
    # def callBackB(self, data):
    #     self.linear_xb = SCALE * data.pose.pose.position.x + self.canvasWidth/2
    #     self.linear_yb = -SCALE * data.pose.pose.position.y + self.canvasHeight/2
    #     self.angular_zb = SCALE * data.pose.pose.orientation.z
    
    def run(self):
        self.timerFired()
        self.root.mainloop()

    ##### util #####
    def drawPicture(self, carImage, carIdx, linear_x, linear_y, angular_z = 0):
        img = Image.open(carImage)
        rotatedImage = img.rotate(angular_z)
        self.carIdx = ImageTk.PhotoImage(rotatedImage)
        carIdx1  = carIdx + "1"
        self.carIdx1 = self.c.create_image(linear_x, linear_y, image=self.carIdx)
        self.c.pack()

    def drawBackground(self, image, linear_x, linear_y, angular_z = 0):
        img = Image.open(image)
        self.background = ImageTk.PhotoImage(img)
        self.background1 = self.c.create_image(linear_x, linear_y, image=self.background)
        self.c.pack()

def main():      
    test = Draw()
    test.run()

if __name__ == '__main__':
    main() 