#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Header
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import sys
import termios
import tty

# 速度（非常稳，不翻车）
BASE_SPEED = 10.0

class M20Teleop(Node):
    def __init__(self):
        super().__init__('m20_teleop')
        # 轮子控制发布者
        self.wheel_pub = self.create_publisher(
            Float64MultiArray,
            "/wheel_velocity_controller/commands",
            10
        )
        # 腿部关节轨迹发布者
        self.joint_traj_pub = self.create_publisher(
            JointTrajectory,
            "/joint_trajectory_controller/joint_trajectory",
            10
        )
        self.get_logger().info("""
--- 轮子+腿部混合控制 ---
W : 前进（轮子）
S : 后退（轮子）
A : 左走（腿部）
D : 右走（腿部）
空格 : 停止（轮子）
X : 趴下（腿部）
Z : 站立（腿部）
-------------------------------
""")

    def stop(self):
        msg = Float64MultiArray()
        msg.data = [0.0, 0.0, 0.0, 0.0]
        self.wheel_pub.publish(msg)

    def move_left(self):
        """发布左走的关节轨迹指令"""
        msg = JointTrajectory()
        msg.header = Header(frame_id='base_link')
        msg.joint_names = [
            'fl_hipx_joint','fl_hipy_joint','fl_knee_joint',
            'fr_hipx_joint','fr_hipy_joint','fr_knee_joint',
            'hl_hipx_joint','hl_hipy_joint','hl_knee_joint',
            'hr_hipx_joint','hr_hipy_joint','hr_knee_joint'
        ]
        # 第1个点：抬起左前+右后并向左摆
        point1 = JointTrajectoryPoint()
        point1.positions = [0.8, -1.2, 1.6, 0.0, -0.8, 1.3, 0.0, 0.8, -1.3, 0.8, 1.2, -1.6]
        point1.time_from_start = Duration(sec=0, nanosec=100000000)
        
        # 第2个点：左前+右后向左落地
        point2 = JointTrajectoryPoint()
        point2.positions = [0.0, -0.8, 1.3, 0.0, -0.8, 1.3, 0.0, 0.8, -1.3, 0.0, 0.8, -1.3]
        point2.time_from_start = Duration(sec=0, nanosec=200000000)
        
        # 第3个点：抬起右前+左后并向左摆
        point3 = JointTrajectoryPoint()
        point3.positions = [0.0, -0.8, 1.3, 0.8, -1.2, 1.6, 0.8, 1.2, -1.6, 0.0, 0.8, -1.3]
        point3.time_from_start = Duration(sec=0, nanosec=300000000)
        
        # 第4个点：右前+左后向左落地（完成一步）
        point4 = JointTrajectoryPoint()
        point4.positions = [0.0, -0.8, 1.3, 0.0, -0.8, 1.3, 0.0, 0.8, -1.3, 0.0, 0.8, -1.3]
        point4.time_from_start = Duration(sec=0, nanosec=400000000)
        
        msg.points = [point1, point2, point3, point4]
        self.joint_traj_pub.publish(msg)
        self.get_logger().info("左走一步")

    def move_right(self):
        """发布右走的关节轨迹指令"""
        msg = JointTrajectory()
        msg.header = Header(frame_id='base_link')
        msg.joint_names = [
            'fl_hipx_joint','fl_hipy_joint','fl_knee_joint',
            'fr_hipx_joint','fr_hipy_joint','fr_knee_joint',
            'hl_hipx_joint','hl_hipy_joint','hl_knee_joint',
            'hr_hipx_joint','hr_hipy_joint','hr_knee_joint'
        ]
        # 第1个点：右前+左后，向右
        point1 = JointTrajectoryPoint()
        point1.positions = [0.0, -0.8, 1.3, -0.8, -1.2, 1.6, -0.8, 1.2, -1.6, 0.0, 0.8, -1.3]
        point1.time_from_start = Duration(sec=0, nanosec=100000000)
        
        # 第2个点：落地
        point2 = JointTrajectoryPoint()
        point2.positions = [0.0, -0.8, 1.3,  0.0, -0.8, 1.3,  0.0, 0.8,-1.3,  0.0, 0.8,-1.3]
        point2.time_from_start = Duration(sec=0, nanosec=200000000)
        
        
        # 第3个点：抬起左前+右后并向右边摆
        point3 = JointTrajectoryPoint()
        point3.positions = [-0.8, -1.2, 1.6, 0.0, -0.8, 1.3, 0.0, 0.8, -1.3, -0.8, 1.2, -1.6]
        point3.time_from_start = Duration(sec=0, nanosec=300000000)
        
        # 第4个点：右前+左后向左落地（完成一步）
        point4 = JointTrajectoryPoint()
        point4.positions = [0.0, -0.8, 1.3,  0.0, -0.8, 1.3,  0.0, 0.8,-1.3,  0.0, 0.8,-1.3]
        point4.time_from_start = Duration(sec=0, nanosec=400000000)
        
        msg.points = [point1, point2, point3, point4]
        self.joint_traj_pub.publish(msg)
        self.get_logger().info("右走一步")

    def move_down(self):
        """发布趴下的关节轨迹指令"""
        msg = JointTrajectory()
        msg.header = Header(frame_id='base_link')
        msg.joint_names = [
            'fl_hipx_joint','fl_hipy_joint','fl_knee_joint',
            'fr_hipx_joint','fr_hipy_joint','fr_knee_joint',
            'hl_hipx_joint','hl_hipy_joint','hl_knee_joint',
            'hr_hipx_joint','hr_hipy_joint','hr_knee_joint'
        ]
        # 趴下位置点（0.5秒完成动作）
        point = JointTrajectoryPoint()
        point.positions = [-0.438, -1.16, 2.76, 0.438, -1.16, 2.76, -0.438, 1.16, -2.76, 0.438, 1.16, -2.76]
        point.time_from_start = Duration(sec=0, nanosec=500000000)
        msg.points = [point]
        self.joint_traj_pub.publish(msg)
        self.get_logger().info("执行趴下动作")

    def rl(self):
        """发布站立的关节轨迹指令"""
        msg = JointTrajectory()
        msg.header = Header(frame_id='base_link')
        msg.joint_names = [
            'fl_hipx_joint','fl_hipy_joint','fl_knee_joint',
            'fr_hipx_joint','fr_hipy_joint','fr_knee_joint',
            'hl_hipx_joint','hl_hipy_joint','hl_knee_joint',
            'hr_hipx_joint','hr_hipy_joint','hr_knee_joint'
        ]
        # 站立位置点（0.5秒完成动作）
        point = JointTrajectoryPoint()
        #point.positions = [0.0, -0.62, 1.0,  0.0, -0.62, 1.0,  0.0, 0.62,-1.0,  0.0, 0.62,-1.0]
        point.positions = [0.0, -0.8, 1.3,  0.0, -0.8, 1.3,  0.0, 0.8,-1.3,  0.0, 0.8,-1.3]
        point.time_from_start = Duration(sec=0, nanosec=500000000)
        msg.points = [point]
        self.joint_traj_pub.publish(msg)
        self.get_logger().info("执行站立动作")

    def stand_up(self):
        """发布站立的关节轨迹指令"""
        msg = JointTrajectory()
        msg.header = Header(frame_id='base_link')
        msg.joint_names = [
            'fl_hipx_joint','fl_hipy_joint','fl_knee_joint',
            'fr_hipx_joint','fr_hipy_joint','fr_knee_joint',
            'hl_hipx_joint','hl_hipy_joint','hl_knee_joint',
            'hr_hipx_joint','hr_hipy_joint','hr_knee_joint'
        ]
        # 站立位置点（0.5秒完成动作）
        point = JointTrajectoryPoint()
        point.positions = [0.0, -0.688, 1.48,  0.0, -0.688, 1.48,  0.0, 0.688,-1.48,  0.0, 0.688,-1.48]
        point.time_from_start = Duration(sec=0, nanosec=500000000)
        msg.points = [point]
        self.joint_traj_pub.publish(msg)
        self.get_logger().info("执行站立动作")

def main(args=None):
    rclpy.init(args=args)
    tele = M20Teleop()
    tele.stop()

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)

    try:
        while True:
            key = sys.stdin.read(1)

            # 前进
            if key == 'w':
                msg = Float64MultiArray()
                msg.data = [BASE_SPEED, BASE_SPEED, BASE_SPEED, BASE_SPEED]
                tele.wheel_pub.publish(msg)

            # 后退
            elif key == 's':
                msg = Float64MultiArray()
                msg.data = [-BASE_SPEED, -BASE_SPEED, -BASE_SPEED, -BASE_SPEED]
                tele.wheel_pub.publish(msg)

            # 左走（腿部）
            elif key == 'a':
                tele.move_left()

            # 右走（腿部）
            elif key == 'd':
                tele.move_right()

            # 停止
            elif key == ' ':
                tele.stop()

            # 趴下
            elif key == 'x':
                tele.move_down()

            # 站立
            elif key == 'z':
                tele.stand_up()

            # 运动
            elif key == 'c':
                tele.rl()
            # 退出
            elif key == '\x03':
                break

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        tele.stop()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
