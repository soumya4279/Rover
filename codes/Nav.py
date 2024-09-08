#!/usr/bin/env python3

import rospy2
from std_msgs.msg import String
from gpiozero import Motor

# Initialize the motors
right_motor = Motor(forward=17, backward=18)
left_motor = Motor(forward=22, backward=23)


def move_forward():
    right_motor.forward()
    left_motor.forward()


def move_backward():
    right_motor.backward()
    left_motor.backward()


def stop_motors():
    right_motor.stop()
    left_motor.stop()


def command_callback(msg):
    command = msg.data
    if command == "forward":
        move_forward()
    elif command == "backward":
        move_backward()
    elif command == "stop":
        stop_motors()


def main():
    rospy2.init_node('motor_control_node', anonymous=True)
    rospy2.Subscriber('/cmd_vel', String, command_callback)
    rospy2.spin()


if _name_ == '_main_':
    main()
