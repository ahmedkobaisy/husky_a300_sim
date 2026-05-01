#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from geometry_msgs.msg import Twist, TwistStamped

class TwistConverter(Node):
    def __init__(self):
        super().__init__('twist_converter')
        
        # Subscribe to regular cmd_vel (Twist)
        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.callback,
            10
        )
        
        # Publish TwistStamped with best_effort QoS
        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT
        )
        self.pub = self.create_publisher(
            TwistStamped,
            '/cpr_a300_0001/platform/cmd_vel',
            qos
        )
        self.get_logger().info('Twist Converter running!')

    def callback(self, msg):
        stamped = TwistStamped()
        stamped.header.stamp = self.get_clock().now().to_msg()
        stamped.header.frame_id = 'base_link'
        stamped.twist = msg
        self.pub.publish(stamped)

def main():
    rclpy.init()
    node = TwistConverter()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
