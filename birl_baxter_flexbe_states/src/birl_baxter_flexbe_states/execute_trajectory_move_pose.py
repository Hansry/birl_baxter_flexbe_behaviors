#!/usr/bin/env python

import rospy
import ipdb


from flexbe_core import EventState, Logger
from birl_baxter_flexbe_states.proxy import ProxyTrajectoryClient

from geometry_msgs.msg import (
    Pose,
    Point,
    Quaternion,
)

"""
Created on 8/22/2017

@author: Ben Lin
"""

class ExecuteTrajectoryMovePose(EventState):
	"""


	-- duration     	float      	Duration of Action move to start pose.

	># pose_config        Pose()      Destination of Pose


	<= reached 							Requested joint configuration has been reached successfully.
	<= failed 							Failed to reach requested joint configuration.

	"""
	
	def __init__(self, duration):
		"""Constructor"""
		super(ExecuteTrajectoryMovePose, self).__init__(outcomes=['reached', 'failed'],
															  input_keys=['pose_config'])

		self._client = ProxyTrajectoryClient()

		self._failed = False

		self._duration = duration



	def execute(self, userdata):
		"""Execute this state"""
		if self._failed:
			return 'failed'

		if self._client.finished():
			return 'reached'

	
	
	def on_enter(self, userdata):
		self._failed = False


		# create the motion goal
		self._client.clear()
		self._client.add_point(self._client.get_current_angles(), 0.0)


		self.pose_config = userdata.pose_config
		self._client.add_pose_point(self.pose_config, self._duration)


		# execute the motion
		try:
			self._client.start()
		except Exception as e:
			Logger.logwarn('Was unable to execute trajectory request:\n%s' % str(e))
			self._failed = True
