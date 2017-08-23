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

class ExecuteGripperMove(EventState):
	"""


	-- gripper_move       Bool      	True for gripper close, False for gripper open



	<= reached 							Requested joint configuration has been reached successfully.
	<= failed 							Failed to reach requested joint configuration.

	"""
	
	def __init__(self, gripper_move):
		"""Constructor"""
		super(ExecuteGripperMove, self).__init__(outcomes=['reached', 'failed'])

		self._client = ProxyTrajectoryClient()

		self._failed = False

		self._gripper_move = gripper_move




	def execute(self, userdata):
		"""Execute this state"""
		if self._failed:
			return 'failed'

		else:
			return 'reached'

	
	
	def on_enter(self, userdata):
		self._failed = False

		# gripper move
		if self._gripper_move is True:
			self._client.gripper_close()
		elif self._gripper_move is False:
			self._client.gripper_open()
		else:
			rospy.logerr('param gripper move is not define')
			self._failed = True

