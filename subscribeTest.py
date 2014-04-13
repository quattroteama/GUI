#!/usr/bin/env python
import rospy
from cv_bridge import CvBridge, CvBridgeError
import actionlib
import threading
from Tkinter import *
# import mtTkinter as Tkinter
import ImageTk
import Image
import numpy as np
import os
import tkMessageBox
import time
import roslib
import tf
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
from std_msgs.msg import Float32
from std_msgs.msg import String

SCALE = 5
def callBack(data):
    # refresh the pos values 
    linear_x = SCALE * data.pose.pose.position.x + 50
    linear_y = SCALE * data.pose.pose.position.y + 50
    angular_z = SCALE * data.pose.pose.orientation.z
    angular_w = SCALE * data.pose.pose.orientation.w
    print [linear_x, linear_y, angular_z]

def subscriber():
    # subscriber ROS
    pub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callBack)
    rospy.init_node('subscribeToPose')
    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass

