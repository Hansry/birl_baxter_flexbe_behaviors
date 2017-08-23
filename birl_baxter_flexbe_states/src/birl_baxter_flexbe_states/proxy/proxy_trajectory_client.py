#!/usr/bin/env python

import rospy
import actionlib
from threading import Timer
import time
import sys

import ipdb


from flexbe_core.logger import Logger
from flexbe_core.proxy import ProxyActionClient

##############
import rospy
import rospkg
import copy
import struct

import actionlib


from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)
from trajectory_msgs.msg import (
    JointTrajectoryPoint,
)

from std_msgs.msg import (
    Header,
    Empty,
)

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

'''
Created on 08.22.2017

@author: Ben Lin
'''

import baxter_interface




class ProxyTrajectoryClient(object):
    """
    A proxy for easily using moveit.
    """
    _is_initialized = False

    _action_topic = 'robot/limb/right/follow_joint_trajectory'

    _client = None

    _limb = 'right'

    _rs = None

    _init_state = None

    _verbose =  None

    _iksvc = None

    _baxter_limb_interface = None

    _joint_name = None

    _gripper = None


    def __init__(self,verbose = False):
        if not ProxyTrajectoryClient._is_initialized:
            ProxyTrajectoryClient._is_initialized = True
            Logger.loginfo("Initializing proxy FollowJointTrajectory client...")

            ProxyTrajectoryClient._client = ProxyActionClient({ProxyTrajectoryClient._action_topic:FollowJointTrajectoryAction})


            ProxyTrajectoryClient._verbose = verbose


            # enable the IK Service
            ik_ns = "ExternalTools/" + ProxyTrajectoryClient._limb + "/PositionKinematicsNode/IKService"
            ProxyTrajectoryClient._iksvc = rospy.ServiceProxy(ik_ns, SolvePositionIK)
            rospy.wait_for_service(ik_ns, 5.0)

            # enable the Baxter
            ProxyTrajectoryClient._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
            ProxyTrajectoryClient._init_state = ProxyTrajectoryClient._rs.state().enabled
            print("Enabling robot... ")
            ProxyTrajectoryClient._rs.enable()

            #  enable baxter limb interface
            ProxyTrajectoryClient._baxter_limb_interface = baxter_interface.limb.Limb(ProxyTrajectoryClient._limb)

            #  Get the names from joints
            ProxyTrajectoryClient._joint_name = [joint for joint in ProxyTrajectoryClient._baxter_limb_interface.joint_names()]

            ProxyTrajectoryClient._gripper = baxter_interface.Gripper(ProxyTrajectoryClient._limb)

        self._goal = FollowJointTrajectoryGoal()
        self._result = None
        self._goal_time_tolerance = rospy.Time(0.1)
        self._goal.goal_time_tolerance = self._goal_time_tolerance



    def add_point(self, positions, time):
        point = JointTrajectoryPoint()
        point.positions = copy.deepcopy(positions)
        point.time_from_start = rospy.Duration(time)
        self._goal.trajectory.points.append(point)

    def start(self):
        self._goal.trajectory.header.stamp = rospy.Time.now()
        ProxyTrajectoryClient._client.send_goal(ProxyTrajectoryClient._action_topic,
                                                self._goal)
        self._goal = None

    def stop(self):
        ProxyTrajectoryClient._client.cancel(ProxyTrajectoryClient._action_topic)

    def wait(self, timeout=15.0):
        return ProxyTrajectoryClient._client.wait_for_result(timeout=rospy.Duration(timeout))

    
    def finished(self):
        if ProxyTrajectoryClient._client.has_result(ProxyTrajectoryClient._action_topic):
            self._result = ProxyTrajectoryClient._client.get_result(ProxyTrajectoryClient._action_topic)
            return True
        return False

    def add_pose_point(self, pose, time):
        angles = self.ik_request(pose)
        if not angles:
            return False
        else:
            self.add_point(angles, time)
            return True

    def clear(self):
        self._goal = FollowJointTrajectoryGoal()
        self._goal.goal_time_tolerance = self._goal_time_tolerance
        self._goal.trajectory.joint_names = [ProxyTrajectoryClient._limb + '_' + joint for joint in \
                                             ['s0', 's1', 'e0', 'e1', 'w0', 'w1', 'w2']]


    def ik_request(self, pose):
        hdr = Header(stamp=rospy.Time.now(), frame_id='base')
        ikreq = SolvePositionIKRequest()
        ikreq.pose_stamp.append(PoseStamped(header=hdr, pose=pose))
        try:
            resp = self._iksvc(ikreq)
        except (rospy.ServiceException, rospy.ROSException), e:
            rospy.logerr("Service call failed: %s" % (e,))
            return False
        # Check if result valid, and type of seed ultimately used to get solution
        # convert rospy's string representation of uint8[]'s to int's
        resp_seeds = struct.unpack('<%dB' % len(resp.result_type), resp.result_type)
        limb_joints = {}
        if (resp_seeds[0] != resp.RESULT_INVALID):
            seed_str = {
                ikreq.SEED_USER: 'User Provided Seed',
                ikreq.SEED_CURRENT: 'Current Joint Angles',
                ikreq.SEED_NS_MAP: 'Nullspace Setpoints',
            }.get(resp_seeds[0], 'None')
            if self._verbose:
                print("IK Solution SUCCESS - Valid Joint Solution Found from Seed Type: {0}".format(
                    (seed_str)))
            # Format solution into Limb API-compatible dictionary
            limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
            if self._verbose:
                print("IK Joint Solution:\n{0}".format(limb_joints))
                print("------------------")
        else:
            rospy.logerr("INVALID POSE - No Valid Joint Solution Found.")
            return False

        limb_names = [ProxyTrajectoryClient._limb + '_' + joint for joint in \
                                             ['s0', 's1', 'e0', 'e1', 'w0', 'w1', 'w2']]

        limb_angles = [limb_joints[joint] for joint in limb_names]

        return limb_angles


    def get_current_angles(self):
        try:
            current_angles = [ProxyTrajectoryClient._baxter_limb_interface.joint_angle(joint) for joint in ProxyTrajectoryClient._joint_name]
            return current_angles
        except:
            rospy.logerr("Cannot get the current angles")
            return False

    def gripper_open(self):
        ProxyTrajectoryClient._gripper.open()
        return 0


    def gripper_close(self):
        ProxyTrajectoryClient._gripper.close()
        return 0


