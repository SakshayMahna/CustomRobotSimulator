import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

from tf2_ros import TransformBroadcaster
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
import math

LINEAR_SCALE = 150.0
ANGULAR_SCALE = 1.0

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
        self._scan_publisher = self.create_publisher(LaserScan, 'scan', 20)
        timer_period = 0.5
        self.create_timer(timer_period, self._scan_callback)

    def _vel_callback(self, msg):
        robot = self._robot
        velocity = msg.linear.x * LINEAR_SCALE
        robot.set_velocity(velocity)

        angular_velocity = msg.angular.z * ANGULAR_SCALE
        robot.set_angular_velocity(angular_velocity)

    def _scan_callback(self):
        robot = self._robot
        msg = LaserScan()
        
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_laser'

        laser_values = robot.get_sensor_reading()
        offset_values = robot.get_sensor_offsets()
        scaled_values = [l / LINEAR_SCALE for l in laser_values]

        msg.angle_min = offset_values[0]
        msg.angle_max = offset_values[-1]
        msg.angle_increment = (offset_values[-1] - offset_values[0]) / (len(offset_values) - 1)
        msg.time_increment = 0.01
        msg.scan_time = 0.5
        msg.range_min = 0.0
        msg.range_max = 20.0
        msg.ranges = scaled_values
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
        robot_pose = self._robot.get_pose()
        sensor_pose = self._sensor.get_pose()

        dx = (sensor_pose.x - robot_pose.x) / LINEAR_SCALE
        dy = (sensor_pose.y - robot_pose.y) / LINEAR_SCALE
        dtheta = (sensor_pose.theta - robot_pose.theta) / ANGULAR_SCALE

        header = self.get_clock().now().to_msg()

        t1 = TransformStamped()

        t1.header.stamp = header
        t1.header.frame_id = 'base_link'
        t1.child_frame_id = 'base_laser'

        t1.transform.translation.x = dx
        t1.transform.translation.y = dy
        t1.transform.translation.z = 0.0

        quat = self._quaternion_from_euler(0, 0, dtheta)
        t1.transform.rotation.x = quat[0]
        t1.transform.rotation.y = quat[1]
        t1.transform.rotation.z = quat[2]
        t1.transform.rotation.w = quat[3]

        t2 = TransformStamped()

        t2.header.stamp = header
        t2.header.frame_id = 'base_footprint'
        t2.child_frame_id = 'base_link'

        t2.transform.translation.x = 0.0
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.0

        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0

        self._broadcaster.sendTransform([t1, t2])

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
        header = self.get_clock().now().to_msg()
        self._publish_transform(header)
        self._publish_odom(header)

    def _publish_transform(self, header):
        robot_pose = self._robot.get_pose()
        
        t = TransformStamped()

        t.header.stamp = header
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'

        t.transform.translation.x = robot_pose.x / LINEAR_SCALE
        t.transform.translation.y = robot_pose.y / LINEAR_SCALE
        t.transform.translation.z = 0.0

        quat = self._quaternion_from_euler(0, 0, robot_pose.theta / ANGULAR_SCALE)
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        self._broadcaster.sendTransform(t)

    def _publish_odom(self, header):
        o = Odometry()
        
        o.header.stamp = header
        o.header.frame_id = 'odom'

        robot_pose = self._robot.get_pose()
        robot_v = self._robot.get_velocity()
        robot_w = self._robot.get_angular_velocity()

        o.pose.pose.position.x = robot_pose.x / LINEAR_SCALE
        o.pose.pose.position.y = robot_pose.y / LINEAR_SCALE
        o.pose.pose.position.z = 0.0

        quat = self._quaternion_from_euler(0, 0, robot_pose.theta / ANGULAR_SCALE)
        o.pose.pose.orientation.x = quat[0]
        o.pose.pose.orientation.y = quat[1]
        o.pose.pose.orientation.z = quat[2]
        o.pose.pose.orientation.w = quat[3]

        o.child_frame_id = 'base_link'
        o.twist.twist.linear.x = robot_v / LINEAR_SCALE
        o.twist.twist.linear.y = 0.0
        o.twist.twist.angular.z = robot_w / ANGULAR_SCALE

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