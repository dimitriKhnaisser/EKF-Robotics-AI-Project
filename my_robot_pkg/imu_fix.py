#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class ImuFix(Node):

    def __init__(self):
        super().__init__('imu_fix_node')

        self.sub = self.create_subscription(
            Imu,
            '/imu/data',          # original IMU
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            Imu,
            '/imu/data_fixed',    # fixed IMU (we will use this in EKF)
            10
        )

        self.get_logger().info("IMU Fix Node Started")

    def callback(self, msg):

        # ✅ FIX ORIENTATION COVARIANCE (CRITICAL)
        msg.orientation_covariance = [
            0.01, 0.0, 0.0,
            0.0, 0.01, 0.0,
            0.0, 0.0, 0.02
        ]

        # ✅ (optional but good)
        msg.angular_velocity_covariance = [
            0.01, 0.0, 0.0,
            0.0, 0.01, 0.0,
            0.0, 0.0, 0.02
        ]
        msg.linear_acceleration.x = 0.0
        msg.linear_acceleration.y = 0.0
        msg.linear_acceleration.z = 0.0

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImuFix()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()