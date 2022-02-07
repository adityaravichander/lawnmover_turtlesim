# ADITYA RAVICHANDER, ASU ID: 1222470717, aravic22@asu.edu

# SES 598 - HW1 - PROBLEM 2 - LAWNMOVER

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from std_srvs.srv import Empty
import math

class Turtlebot():
    def __init__(self):
        
        rospy.init_node('turtlebot_controller', anonymous= True)
        
        self.velocity_publisher = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        self.Pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x,2)
        self.pose.y = round(self.pose.y,2)
    
    def euclidean_distance(self, goal_pose):
        # Euclidean distance between current pose and the goal pose
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
    
    def steering_angle(self, goal_pose):
        # calculate the steering angle
        return atan2(goal_pose.y -self.pose.y, goal_pose.x-self.pose.x)
        
    def angular_vel(self, goal_pose, constant = 12):
        # calculate the angular velocity
        return constant * (self.steering_angle(goal_pose)-self.pose.theta) # Proportional controller for angular velocity with gain as 12
    
    def move2goal(self):

        # target initial position 
        i_pose= Pose()
        i_pose.x = float(input("Initial coordinate x: "))
        i_pose.y = float(input("Initial coordinate y: "))

        # tolerance limit
        tol = input("Tolerance limit : ")

        # msg type
        vel_msg = Twist()

        # Loop to reach initial position
        while(self.euclidean_distance(i_pose)>=tol):
                vel_msg.linear.x = 1
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(i_pose) # Proportional controller

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.linear.y=0
        vel_msg.angular.z =0
        self.velocity_publisher.publish(vel_msg)

        # current position
        goal_pose= Pose()

        # input of a,b from user
        a = float(input(" Value of a: "))
        b = float(input(" Value of b: "))

        ix = i_pose.x
        iy = i_pose.y

        # defining waypoints
        wayp_x = [ix + a, ix + a, ix, ix, ix + a, iy]
        wayp_y = [iy, iy+b, iy+b, iy + 2*b, iy+2*b, iy]

        # loop to reach every waypoint
        for i in range(0,6):
            goal_pose.x = wayp_x[i]
            goal_pose.y = wayp_y[i]
            while(self.euclidean_distance(goal_pose) >= tol):
                vel_msg.linear.x = 1
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
                vel_msg.angular.x =0
                vel_msg.angular.y =0
                vel_msg.angular.z =self.angular_vel(goal_pose) # Proportional controller
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()
        
        # Stopping our robot after the movement is over.
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.angular.z=0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x =  Turtlebot()
        x.move2goal()
    
    except rospy.ROSInterruptException:
        pass
