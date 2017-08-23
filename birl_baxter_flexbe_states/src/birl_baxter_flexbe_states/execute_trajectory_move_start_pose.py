#!/usr/bin/env python

import rospy
import ipdb


from flexbe_core import EventState, Logger
from birl_baxter_flexbe_states.proxy import ProxyTrajectoryClient


"""
Created on 8/22/2017

@author: Ben Lin
"""

class ExecuteTrajectoryMoveStartPose(EventState):
	"""


	-- duration     	float      	Duration of Action move to start pose.

	># start_angles     dict	Trajectory to be executed, given as list of time steps where each step contains a list of target joint values.


	<= reached 							Requested joint configuration has been reached successfully.
	<= failed 							Failed to reach requested joint configuration.

	"""
	
	def __init__(self, duration):
		"""Constructor"""
		super(ExecuteTrajectoryMoveStartPose, self).__init__(outcomes=['reached', 'failed'],
															  input_keys=['start_angles'])

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


		start_ordered_angles = [userdata.start_angles[joint] for joint in self._client._joint_name]
		self._client.add_point(start_ordered_angles, self._duration)


		# execute the motion
		try:
			self._client.start()
		except Exception as e:
			Logger.logwarn('Was unable to execute trajectory request:\n%s' % str(e))
			self._failed = True
