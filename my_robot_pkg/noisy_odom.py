#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import random
import math
import tf_transformations


class NoisyOdom(Node):

    def __init__(self):
        super().__init__('noisy_odom')

        # Drift variables
        self.drift_x = 0.0
        self.drift_y = 0.0
        self.drift_theta = 0.0

        # ADD THIS (bias direction)
        self.bias_x = random.uniform(0.0002, 0.0005)
        self.bias_y = random.uniform(0.0002, 0.0005)
        self.bias_theta = random.uniform(0.00008, 0.0002)
        # Store latest message only
        self.latest_msg = None

        # Subscriber (lightweight now)
        self.sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Publisher
        self.pub = self.create_publisher(
            Odometry,
            '/noisy_odom',
            10
        )

        # Timer → process at 20 Hz (0.05 sec)
        self.timer = self.create_timer(0.05, self.process_odom)

        self.get_logger().info("Noisy odom node started (optimized)")

    # ================= STORE ONLY =================
    def odom_callback(self, msg):
        self.latest_msg = msg

    # ================= PROCESS AT FIXED RATE =================
    def process_odom(self):
        if self.latest_msg is None:
            return

        msg = self.latest_msg

        noisy_msg = Odometry()

        # Copy header
        noisy_msg.header = msg.header
        noisy_msg.child_frame_id = msg.child_frame_id

        # ================= DRIFT =================
        # biased drift (ALWAYS grows)
        self.drift_x += self.bias_x + random.gauss(0, 0.0003)
        self.drift_y += self.bias_y + random.gauss(0, 0.0003)
        self.drift_theta += self.bias_theta + random.gauss(0, 0.00015)
        # ================= ORIGINAL POSITION =================
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # ================= ROTATION DRIFT =================
        x_rot = x * math.cos(self.drift_theta) - y * math.sin(self.drift_theta)
        y_rot = x * math.sin(self.drift_theta) + y * math.cos(self.drift_theta)

        # ================= FINAL POSITION =================
        noisy_msg.pose.pose.position.x = x_rot + self.drift_x + random.gauss(0, 0.04) + random.gauss(0, 0.1)
        noisy_msg.pose.pose.position.y = y_rot + self.drift_y + random.gauss(0, 0.04) + random.gauss(0, 0.1)
        noisy_msg.pose.pose.position.z = msg.pose.pose.position.z

        # ================= ORIENTATION =================

        q = msg.pose.pose.orientation

        # Convert to yaw
        _, _, yaw = tf_transformations.euler_from_quaternion([
            q.x, q.y, q.z, q.w
        ])

        # Add noise
        yaw += random.gauss(0, 0.008)        
        # Convert back
        qx, qy, qz, qw = tf_transformations.quaternion_from_euler(0, 0, yaw)

        noisy_msg.pose.pose.orientation.x = qx
        noisy_msg.pose.pose.orientation.y = qy
        noisy_msg.pose.pose.orientation.z = qz
        noisy_msg.pose.pose.orientation.w = qw

        # Normalize quaternion (VERY IMPORTANT)
        norm = math.sqrt(qx*qx + qy*qy + qz*qz + qw*qw)
        qx /= norm
        qy /= norm
        qz /= norm
        qw /= norm
        # ================= VELOCITY =================
        noisy_msg.twist.twist.linear.x = msg.twist.twist.linear.x + random.gauss(0, 0.05)
        noisy_msg.twist.twist.angular.z = msg.twist.twist.angular.z + random.gauss(0, 0.025)
        # ================= COPY COVARIANCE =================
        noisy_msg.pose.covariance = [
            0.5, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.5, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.05
        ]

        noisy_msg.twist.covariance = [
            0.01, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.01, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.1, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.1, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.1, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.05
        ]

        # Publish
        self.pub.publish(noisy_msg)


def main(args=None):
    rclpy.init(args=args)
    node = NoisyOdom()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()