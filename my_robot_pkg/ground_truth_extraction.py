#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import pandas as pd
from std_msgs.msg import Bool
import os


class OdomSaver(Node):

    def __init__(self):
        super().__init__('odom_saver')

        # Store data in memory
        self.data = []

        # Store latest odom message
        self.latest_msg = None

        # Subscribe to odom
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Timer: save data every 1 second
        self.timer = self.create_timer(0.5, self.timer_callback)

        # Subscribe to experiment done signal
        self.done_sub = self.create_subscription(
            Bool,
            '/experiment_done',
            self.done_callback,
            10
        )

    def odom_callback(self, msg):
        # Just store latest message (no heavy work here)
        self.latest_msg = msg

    def timer_callback(self):
        # Called every 1 second
        if self.latest_msg is None:
            return

        msg = self.latest_msg

        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z

        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        self.data.append([t, x, y, z, qx, qy, qz, qw])

    def save_to_csv(self):
        if len(self.data) == 0:
            self.get_logger().warn("No data to save")
            return

        df = pd.DataFrame(self.data, columns=[
            'time',
            'x', 'y', 'z',
            'qx', 'qy', 'qz', 'qw'
        ])

        path = os.path.expanduser('~/ros2_ws/src/my_robot_pkg/data/ground_truth.csv')
        df.to_csv(path, index=False)

        self.get_logger().info(f'Saved ground_truth.csv at: {path}')

    def done_callback(self, msg):
        if msg.data:
            self.get_logger().info("Experiment finished — saving CSV")
            self.save_to_csv()
            rclpy.shutdown()

    def destroy_node(self):
        self.get_logger().info("Shutting down node")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = OdomSaver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()