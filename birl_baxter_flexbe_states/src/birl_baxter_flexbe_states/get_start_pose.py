#!/usr/bin/env python

import rospy
import rospkg
import sys
import os
from flexbe_core import EventState, Logger
from rospy.exceptions import ROSInterruptException

import ipdb


'''
Created on 8.22.2017

@author: Ben Lin
'''

class GetStartPose(EventState):
	'''
	Get the right_start_joint_angles config from hardcoded_config

	-- path 	string[] path to the hard_coded.

	># input_value	object		Input to the condition function.
	#> start_angles  dict        the pose of angles of joints in baxter starting

	'''


	def __init__(self, path="default"):
		'''
		Constructor
		'''
		super(GetStartPose, self).__init__(outcomes=['done','failed'],
											output_keys=['start_angles'])
		self.failed = None
		self.start_angles = None
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
		elif self.start_angles is None:
			return 'failed'
		else:
			userdata.start_angles = self.start_angles
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
				self.start_angles = hardcoded_config.user_data['right_start_joint_angles']
			except:
				rospy.logerr('cannot import hardcoded config.py, it might be the syntax error in hardcoded config.py')
				rospy.loginfo('Please check the config file')
				self.failed = True
		except ROSInterruptException:
			rospy.logwarn('cannot find "birl_sim_examples" ROS package')
			self.failed = True
