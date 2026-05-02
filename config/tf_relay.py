#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage

class TFRelay(Node):
    def __init__(self):
        super().__init__('tf_relay')

        # Relay /cpr_a300_0001/tf -> /tf
        self.sub_tf = self.create_subscription(
            TFMessage,
            '/cpr_a300_0001/tf',
            self.tf_callback,
            10
        )
        self.pub_tf = self.create_publisher(
            TFMessage,
            '/tf',
            10
        )

        # Relay /cpr_a300_0001/tf_static -> /tf_static
        self.sub_tf_static = self.create_subscription(
            TFMessage,
            '/cpr_a300_0001/tf_static',
            self.tf_static_callback,
            10
        )
        self.pub_tf_static = self.create_publisher(
            TFMessage,
            '/tf_static',
            10
        )

        self.get_logger().info('TF Relay running!')

    def tf_callback(self, msg):
        self.pub_tf.publish(msg)

    def tf_static_callback(self, msg):
        self.pub_tf_static.publish(msg)

def main():
    rclpy.init()
    node = TFRelay()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
