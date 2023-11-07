import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class RobotNode(Node):
    def __init__(self, robot):
        super().__init__('robot_node')
        self._robot = robot
        self._initialize_subscribers()
        self._initialize_publishers()

    def _initialize_subscribers(self):
        self._vel_subscriber = self.create_subscription(Twist, 'cmd_vel',
                               self._vel_callback, 10)

    def _initialize_publishers(self):
        self._scan_publisher = self.create_publisher(LaserScan, 'scan', 10)
        timer_period = 0.5
        self.create_timer(timer_period, self._scan_callback)

    def _vel_callback(self, msg):
        robot = self._robot
        velocity = msg.linear.x
        robot.set_velocity(velocity)

        angular_velocity = msg.angular.z
        robot.set_angular_velocity(angular_velocity)

    def _scan_callback(self):
        robot = self._robot
        msg = LaserScan()
        msg.ranges = robot.get_sensor_reading()
        self._scan_publisher.publish(msg)