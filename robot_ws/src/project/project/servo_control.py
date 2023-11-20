import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from arduino.getchar import Getchar

class Servo_Control(Node):

    def __init__(self):
        super().__init__('servo_control')
        self.pub_pt = self.create_publisher(String, 'pt_msg', 10)
        self.pt_msg = String()
        
    def up(self):
        msg = String()
        msg.data = 'up'
        self.pub_pt.publish(msg)
        
    def down(self):
        msg = String()
        msg.data = 'down'
        self.pub_pt.publish(msg)
    
