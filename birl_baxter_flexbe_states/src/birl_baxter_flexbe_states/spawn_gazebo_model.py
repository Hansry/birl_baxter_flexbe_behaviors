#!/usr/bin/env python

import rospy
import rospkg
from flexbe_core import EventState, Logger


from flexbe_core.proxy.proxy_service_caller import ProxyServiceCaller

import ipdb

from gazebo_msgs.srv import (
    SpawnModel,
	SpawnModelRequest
)

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
'''
Created on 08/22/2017

@author: Ben Lin
'''
class SpawnGazeboModel(EventState):
	'''
	Call a service given a name.

	-- model_name 	string 		Name of the calling service

	<= done 					Affordance data is available.
	<= failed 					Failed to get affordance information.

	'''

	# BOX_MALE = 'box_male'
	# BOX_FEMALE = 'box_female'


	def __init__(self, model_name):
		'''Constructor'''
		super(SpawnGazeboModel, self).__init__(outcomes = ['done', 'failed'],
											 input = ['gazebo_model_pose'])

		# ipdb.set_trace()
		# self._srv_result = None
		# self._service_name = '/gazebo/spawn_urdf_model'
        #
        #
		# self._failed = False
		# self._done = False
        #
		# self._srv = ProxyServiceCaller({self._service_name:SpawnModel})
        #
		# self._model_reference_frame = 'base'
		# self._gazebo_model_pose = None
		# self._model_name = model_name
        #
		# self._gazebo_model_pose = Pose(Point(x=0.6,
		# 								   y=-0.4,
		# 								   z=-0.12),
		# 							 Quaternion(x=0.0,
		# 										y=1.0,
		# 										z=0.0,
		# 										w=6.123233995736766e-17))


	def execute(self, userdata):
		print 'hello'

		# if self._failed or self._srv_result is None:
		# 	return 'failed'
		# if self._done:
		# 	return 'done'
        #
		#
		# self._done = True
		# return 'done'


	def on_enter(self, userdata):
		print 'hello'
		# self._gazebo_model_pose = userdata.gazebo_model_pose
        #
		# if self._gazebo_model_pose is not None:
        #
        #
		# 	if self.model_name == "box_male":
		# 		# Get male box Path
		# 		model_path = rospkg.RosPack().get_path('birl_baxter_description') + "/urdf/box/"
		# 		# Load male box SDF
		# 		self._model_xml = ''
		# 		with open(model_path + "box_male/robots/box_male.URDF", "r") as box_male_file:
		# 			self._model_xml = box_male_file.read().replace('\n', '')
		# 		try:
		# 			self._srv_result = self._srv.call(self._service_name,
		# 											  SpawnModelRequest(self._model_name, self._model_xml, "/",
		# 								 								self._model_pose, self._model_reference_frame))
        #
		# 			rospy.loginfo('loading male box succesfully')
		# 		except Exception, e:
		# 			rospy.logerr("Spawn URDF service call failed: {0}".format(e))
		# 			self._failed = True
        #
		# 	if self.model_name == "box_female":
		# 		# get path
		# 		model_path = rospkg.RosPack().get_path('birl_baxter_description') + "/urdf/box/"
		# 		# Load female box  URDF
		# 		box_female_xml = ''
		# 		with open(model_path + "box_female/robots/box_female.URDF", "r") as box_female_file:
		# 			box_female_xml = box_female_file.read().replace('\n', '')
		# 		rospy.wait_for_service('/gazebo/spawn_urdf_model')
		# 		try:
		# 			self._srv_result = self._srv.call(self._service_name,
		# 											  SpawnModelRequest(self._model_name, self._model_xml, "/",
		# 																self._model_pose, self._model_reference_frame))
		# 		except Exception, e:
		# 			rospy.logerr("Spawn URDF service call failed: {0}".format(e))
		# 			self._failed = True
        #
		# 	else:
		# 		rospy.logerr('model_name is incorrect, please choose another one')
		# 		self._failed = True
        #
		# else:
		# 	rospy.logerr('userdata.gazebo_model_pose is missing')
		# 	self._failed = True
        #
		# try:
		# 	self._srv_result = self._srv.call(self._service_name, Add_Gazebo_ModelRequest(self._model_name,
		# 																				   self._pose,
		# 																	    		   self._model_reference_frame))
		#
		# except Exception as e:
		# 	Logger.logwarn('Failed to send service call:\n%s' % str(e))
		# 	self._failed = True