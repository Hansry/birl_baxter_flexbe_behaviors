#!/usr/bin/env python

import rospy
import rospkg
import sys
from flexbe_core import EventState, Logger
from rospy.exceptions import ROSInterruptException

'''
Created on 8.22.2017

@author: Ben Lin
'''

class GetHardcodedConfig(EventState):
	'''
	Evaluates a condition function in order to return one of the specified outcomes.
	This state can be used if the further control flow of the behavior depends on an advanced condition.


	-- path         string   path to config file, optional

	#> config_group_data   	dict      Get the specific config from file

	'''


	def __init__(self ,path="default"):
		'''
		Constructor
		'''
		super(GetHardcodedConfig, self).__init__(outcomes=['done','failed'],
											output_keys=['config_group_data'])
		self.failed = None
		self.start_angles = None
		self.config_group_data = None



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
		elif self.config_group_data is None:
			return 'failed'
		else:
			userdata.config_group_data = self.config_group_data
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
				self.config_group_data = hardcoded_config.user_data
			except:
				rospy.logerr('cannot import hardcoded config.py, it might be the syntax error in hardcoded config.py')
				rospy.loginfo('Please check the config file')
				self.failed = True
		except ROSInterruptException:
			rospy.logwarn('cannot find "birl_sim_examples" ROS package')
			self.failed = True
