#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger


from flexbe_core.proxy.proxy_service_caller import ProxyServiceCaller

import rospy
import copy

from arm_move.srv_client import *

import smach
import smach_ros

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

from std_msgs.msg import String

'''
Created on 08/22/2017

@author: Ben Lin
'''
class CallBirlService(EventState):
	'''
	Call a service given a name.

	-- service_name 	string 		Name of the calling service

	<= done 					Affordance data is available.
	<= failed 					Failed to get affordance information.

	'''

	def __init__(self, service_name):
		'''Constructor'''
		super(CallBirlService, self).__init__(outcomes = ['done', 'failed'])



		self._srv_result = None
		self._service_name = service_name
		self._hand_side = None

		self._failed = False
		self._done = False

		self._srv = ProxyServiceCaller({self._service_name:Add_Gazebo_Model})

		self._model_reference_frame = None
		self._pose = None
		self._model_name = None


	def execute(self, userdata):

		if self._failed or self._srv_result is None:
			return 'failed'
		if self._done:
			return 'done'

		
		self._done = True
		return 'done'


	def on_enter(self, userdata):

		self._failed = False
		self._done = False
		self._srv_result = None

		self._pose = Pose()
		self._pose.position.x = 0.6
		self._pose.position.y = 0
		self._pose.position.z = -0.115

		self._pose.orientation.x = 0
		self._pose.orientation.y = 0
		self._pose.orientation.z = 0
		self._pose.orientation.w = 1

		self._model_reference_frame = String()
		self._model_reference_frame.data = "base"
		self._model_name = String()
		self._model_name.data = "box_female"

		try:
			self._srv_result = self._srv.call(self._service_name, Add_Gazebo_ModelRequest(self._model_name,
																						   self._pose,
																			    		   self._model_reference_frame))
		
		except Exception as e:
			Logger.logwarn('Failed to send service call:\n%s' % str(e))
			self._failed = True