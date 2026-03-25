# auto_rectangle.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
from std_msgs.msg import Bool
import numpy as np
class RectangularDrive(Node):
    def __init__(self):
        super().__init__('rectangular_drive')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.done_pub = self.create_publisher(Bool, '/experiment_done', 10)
        self.timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(self.timer_period, self.drive)
        self.phase = 0
        self.step_count = 0
        self.phase_steps = [65, 31, 65, 31]  # steps for forward/turns
        self.speed_linear = 1.2   # fast forward speed
        self.speed_angular = 2.0  # turning speed

        # ✅ NEW: turn counter
        self.turn_count = 0
        self.max_turns = 4

        # Wait 5 seconds before moving
        self.get_logger().info("Waiting 5 seconds before starting...")
        time.sleep(5)
        self.get_logger().info("Starting rectangular movement!")

    def drive(self):
        msg = Twist()

        if self.phase % 2 == 0:
            # Forward motion
            msg.linear.x = self.speed_linear
            msg.angular.z = 0.0
        else:
            # Turn while moving (no stop, same trajectory)
            msg.linear.x = self.speed_linear
            msg.angular.z = self.speed_angular*0.5
        self.publisher.publish(msg)
        self.step_count += 1

        # Check if phase finished
        if self.step_count >= self.phase_steps[self.phase]:
            self.step_count = 0

            # ✅ If this phase was a TURN → count it
            if self.phase % 2 == 1:
                self.turn_count += 1
                self.get_logger().info(f"Turn {self.turn_count} completed")

                # ✅ Stop after 4 turns
                if self.turn_count >= self.max_turns:
                    self.get_logger().info("Rectangle completed. Stopping robot.")
                    
                    self.get_logger().info("Rectangle finished") 
                    msg = Bool()
                    msg.data = True
                    self.done_pub.publish(msg)

                    stop_msg = Twist()
                    for _ in range(5):  # ensure full stop
                        self.publisher.publish(stop_msg)

                    self.timer.cancel()
                    return

            # Move to next phase
            self.phase += 1

            # Loop phases (safe, won't matter because we stop before reaching here again)
            if self.phase >= len(self.phase_steps):
                self.phase = 0


def main(args=None):
    rclpy.init(args=args)
    node = RectangularDrive()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()