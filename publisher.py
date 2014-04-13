import rospy
import math

from std_msgs.msg import * 

from geometry_msgs.msg import PoseWithCovarianceStamped

class CarPosePublisher:

    def __init__(self):
        self.pub = rospy.Publisher("/carB_amcl_pose", PoseWithCovarianceStamped)

        while not rospy.is_shutdown():
            # Run this loop at about 10Hz
            rospy.sleep(0.1)
            counter += 1 
            t =  PoseWithCovarianceStamped()

            t.header.stamp = rospy.Time.now()

            t.pose.position.x = counter
            t.pose.position.y = counter
            t.pose.position.z = 0

            t.pose.orientation.x = 0.0
            t.pose.orientation.y = 0.0
            t.pose.orientation.z = counter
           
            car_pose = (t.pose.position.x, t.pose.position.y, 
                        t.pose.position.z, t.pose.orientation.x, 
                        t.pose.orientation.y, t.pose.orientation.z)
            self.pub.publish(car_pose)

if __name__ == '__main__':
    rospy.init_node('carB_amcl_pose_publisher')
    tfb = CarPosePublisher()
    rospy.spin()
