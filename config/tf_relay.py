#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy

class TFRelay(Node):
    def __init__(self):
        super().__init__('tf_relay')

        # Regular TF QoS
        tf_qos = QoSProfile(depth=100)

        # Static TF QoS - MUST be TRANSIENT_LOCAL
        static_qos = QoSProfile(
            depth=100,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            reliability=ReliabilityPolicy.RELIABLE
        )

        # Regular TF relay
        self.sub_tf = self.create_subscription(
            TFMessage,
            '/cpr_a300_0001/tf',
            self.tf_callback,
            tf_qos
        )
        self.pub_tf = self.create_publisher(
            TFMessage,
            '/tf',
            tf_qos
        )

        # Static TF relay with correct QoS
        self.sub_tf_static = self.create_subscription(
            TFMessage,
            '/cpr_a300_0001/tf_static',
            self.tf_static_callback,
            static_qos
        )
        self.pub_tf_static = self.create_publisher(
            TFMessage,
            '/tf_static',
            static_qos
        )

        self.get_logger().info('TF Relay running!')

    def tf_callback(self, msg):
        self.pub_tf.publish(msg)

    def tf_static_callback(self, msg):
        self.get_logger().info(f'Relaying static TF: {[t.child_frame_id for t in msg.transforms]}')
        self.pub_tf_static.publish(msg)

def main():
    rclpy.init()
    node = TFRelay()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
