import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

from tf2_ros import TransformBroadcaster
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
import math

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

class TFNode(Node):
    def __init__(self, robot, sensor):
        super().__init__('static_tf2_broadcaster_node')
        self._robot = robot
        self._sensor = sensor
        self._initialize_broadcaster()
        self._make_transform()

    def _initialize_broadcaster(self):
        self._broadcaster = StaticTransformBroadcaster(self)

    def _make_transform(self):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'base_laser'

        robot_pose = self._robot.get_pose()
        sensor_pose = self._sensor.get_pose()

        t.transform.translation.x = float(sensor_pose.x - robot_pose.x)
        t.transform.translation.y = float(sensor_pose.y - robot_pose.y)
        t.transform.translation.z = 0.0

        quat = self._quaternion_from_euler(0, 0, sensor_pose.theta - robot_pose.theta)
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        self._broadcaster.sendTransform(t)

    def _quaternion_from_euler(self, ai, aj, ak):
        ai /= 2.0
        aj /= 2.0
        ak /= 2.0
        ci = math.cos(ai)
        si = math.sin(ai)
        cj = math.cos(aj)
        sj = math.sin(aj)
        ck = math.cos(ak)
        sk = math.sin(ak)
        cc = ci*ck
        cs = ci*sk
        sc = si*ck
        ss = si*sk
        
        q = [0, 0, 0, 0]
        q[0] = cj*sc - sj*cs
        q[1] = cj*ss + sj*cc
        q[2] = cj*cs - sj*sc
        q[3] = cj*cc + sj*ss
        
        return q


class OdometryNode(Node):
    def __init__(self, robot):
        super().__init__('odometry_publisher_node')
        self._robot = robot
        self._initialize_publishers()

    def _initialize_publishers(self):
        self._broadcaster = TransformBroadcaster(self)
        self._odom_publisher = self.create_publisher(Odometry, 'odom', 10)
        timer_period = 0.5
        self.create_timer(timer_period, self._odom_callback)

    def _odom_callback(self):
        self._publish_transform()
        self._publish_odom()

    def _publish_transform(self):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'

        robot_pose = self._robot.get_pose()

        t.transform.translation.x = float(robot_pose.x)
        t.transform.translation.y = float(robot_pose.y)
        t.transform.translation.z = 0.0

        quat = self._quaternion_from_euler(0, 0, robot_pose.theta)
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        self._broadcaster.sendTransform(t)

    def _publish_odom(self):
        o = Odometry()
        
        o.header.stamp = self.get_clock().now().to_msg()
        o.header.frame_id = 'odom'

        robot_pose = self._robot.get_pose()
        robot_v = self._robot.get_velocity()
        robot_w = self._robot.get_angular_velocity()

        o.pose.pose.position.x = float(robot_pose.x)
        o.pose.pose.position.y = float(robot_pose.y)
        o.pose.pose.position.z = 0.0

        quat = self._quaternion_from_euler(0, 0, robot_pose.theta)
        o.pose.pose.orientation.x = quat[0]
        o.pose.pose.orientation.y = quat[1]
        o.pose.pose.orientation.z = quat[2]
        o.pose.pose.orientation.w = quat[3]

        o.child_frame_id = 'base_link'
        o.twist.twist.linear.x = float(robot_v)
        o.twist.twist.linear.y = 0.0
        o.twist.twist.angular.z = float(robot_w)

        self._odom_publisher.publish(o)

    def _quaternion_from_euler(self, ai, aj, ak):
        ai /= 2.0
        aj /= 2.0
        ak /= 2.0
        ci = math.cos(ai)
        si = math.sin(ai)
        cj = math.cos(aj)
        sj = math.sin(aj)
        ck = math.cos(ak)
        sk = math.sin(ak)
        cc = ci*ck
        cs = ci*sk
        sc = si*ck
        ss = si*sk
        
        q = [0, 0, 0, 0]
        q[0] = cj*sc - sj*cs
        q[1] = cj*ss + sj*cc
        q[2] = cj*cs - sj*sc
        q[3] = cj*cc + sj*ss
        
        return q