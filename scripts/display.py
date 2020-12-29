#!/usr/bin/env python2
# license removed for brevity
import time

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from visualization_msgs.msg import Marker

from pythonAPI.mycobot import MyCobot


def talker():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    pub_marker = rospy.Publisher('visualization_marker', Marker, queue_size=10)
    rospy.init_node('display', anonymous=True)
    rate = rospy.Rate(30) # 30hz

    # pub joint state
    joint_state_send = JointState()
    joint_state_send.header = Header()

    joint_state_send.name = [
                            'joint2_to_joint1', 
                            'joint3_to_joint2', 
                            'joint4_to_joint3', 
                            'joint5_to_joint4', 
                            'joint6_to_joint5', 
                            'joint6output_to_joint6'
                            ]
    joint_state_send.velocity = [0]
    joint_state_send.effort = []

    marker_ = Marker()
    marker_.header.frame_id = '/joint1'
    marker_.ns = 'my_namespace'

    while not rospy.is_shutdown():
        joint_state_send.header.stamp = rospy.Time.now()

        angles = mycobot.get_angles_of_radian()
        data_list = []
        for index, value in enumerate(angles):
            if index != 2:
                value *= -1
            data_list.append(value)

        joint_state_send.position = data_list

        pub.publish(joint_state_send)

        coords = mycobot.get_coords()
        rospy.loginfo('{}'.format(coords))

        #marker 
        marker_.header.stamp = rospy.Time.now()
        marker_.type = marker_.SPHERE
        marker_.action = marker_.ADD
        marker_.scale.x = 0.04
        marker_.scale.y = 0.04
        marker_.scale.z = 0.04

        #marker position initial 
        # print(coords)
        if not coords:
            coords = [0,0,0,0,0,0]
            rospy.loginfo('error [101]: can not get coord values')
	
        marker_.pose.position.x =  coords[1] / 1000 * -1
        marker_.pose.position.y =  coords[0] / 1000 
        marker_.pose.position.z =  coords[2] / 1000

        marker_.color.a = 1.0
        marker_.color.g = 1.0
        pub_marker.publish(marker_)

        rate.sleep()

if __name__ == '__main__':
    mycobot = MyCobot()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

