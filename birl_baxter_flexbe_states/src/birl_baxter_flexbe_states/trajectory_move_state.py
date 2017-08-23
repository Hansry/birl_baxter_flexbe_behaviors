#!/usr/bin/env python

import rospy
import ipdb


from flexbe_core import EventState, Logger
from birl_flexbe_states.proxy import ProxyTrajectoryClient


"""
Created on 8/22/2017

@author: Ben Lin
"""

class TrajectoryMoveState(EventState):
	"""
	Uses Joint trajectory

	># joint_positions  float[][]	Trajectory to be executed, given as list of time steps where each step contains a list of target joint values.
	># time 			float[]		Relative time in seconds from starting the execution when the corresponding time step should be reached.

	<= reached 							Requested joint configuration has been reached successfully.
	<= failed 							Failed to reach requested joint configuration.

	"""
	
	def __init__(self):
		"""Constructor"""
		super(TrajectoryMoveState, self).__init__(outcomes=['reached', 'failed'],
												  input_keys=['joint_positions', 'time'])

		self._client = ProxyTrajectoryClient()

		self._failed = False


	def execute(self, userdata):
		"""Execute this state"""
		if self._failed:
			return 'failed'

		if self._client.finished():
			return 'reached'

	
	
	def on_enter(self, userdata):
		self._failed = False

		self._duration = 4.0

		# create the motion goal
		self._client.clear()
		self._client.add_point(self._client.get_current_angles(), 0.0)

		for i in range(len(userdata.joint_positions)):
			ordered_position = [userdata.joint_positions[i][joint] for joint in self._client._joint_name]
			time_from_start = userdata.time[i]
			self._client.add_point(ordered_position, time_from_start)


		# execute the motion
		try:
			self._client.start()
		except Exception as e:
			Logger.logwarn('Was unable to execute trajectory request:\n%s' % str(e))
			self._failed = True
