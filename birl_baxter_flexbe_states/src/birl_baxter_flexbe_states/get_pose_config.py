#!/usr/bin/env python

import rospy
import rospkg
import sys
import copy
from flexbe_core import EventState, Logger
from rospy.exceptions import ROSInterruptException
from geometry_msgs.msg import (
    Pose,
    Point,
    Quaternion,
)
import ipdb


'''
Created on 8.22.2017

@author: Ben Lin
'''

class GetPoseConfig(EventState):
	'''
	Evaluates a condition function in order to return one of the specified outcomes.
	This state can be used if the further control flow of the behavior depends on an advanced condition.

	-- pose_name    string   name of pose config
	-- path         string   path to config file, optional

	#> pose_config       	Pose()      Get the specific config from file

	'''


	def __init__(self, pose_name ,path="default"):
		'''
		Constructor
		'''
		super(GetPoseConfig, self).__init__(outcomes=['done','failed'],
											output_keys=['pose_config'])
		self.failed = None
		self.start_angles = None
		self.pose_config = None
		self.pose_name = pose_name



		self.hardcoded_config_path = None

		if path is not "default":
			self.hardcoded_config_path = path
			sys.path.append(self.hardcoded_config_path)

		
		
	def execute(self, userdata):
		'''
		Execute this state
		'''
		
		if self.failed == True:
			return 'failed'
		elif self.pose_config is None:
			return 'failed'
		else:
			userdata.pose_config = self.pose_config
			return 'done'


	def on_enter(self, userdata):
		try:

			if self.hardcoded_config_path is None:
				rospack = rospkg.RosPack()
				self.packge_path = rospack.get_path('birl_sim_examples')
				self.hardcoded_config_path = self.packge_path + '/config'
				sys.path.append(self.hardcoded_config_path)
			try:
				import hardcoded_config
				#ipdb.set_trace()
				self.pose_config = hardcoded_config.user_data[self.pose_name]

			except:
				rospy.logerr('cannot import hardcoded config.py, it might be the syntax error in hardcoded config.py')
				rospy.loginfo('Please check the config file')
				self.failed = True
		except Exception:
			rospy.logwarn('cannot find "birl_sim_examples" ROS package')
			self.failed = True
