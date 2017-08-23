#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_add_gazebo_model')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from birl_baxter_flexbe_states.get_pose_config import GetPoseConfig
from birl_baxter_flexbe_states.add_gazebo_model import AddGazeboModel
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 23 2017
@author: Ben
'''
class AddGazeboModelSM(Behavior):
	'''
	add male box
	'''


	def __init__(self):
		super(AddGazeboModelSM, self).__init__()
		self.name = 'Add Gazebo Model'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:435 y:361, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:63 y:150
			OperatableStateMachine.add('get_pose',
										GetPoseConfig(pose_name="gazebo_model_pose", path="default"),
										transitions={'done': 'add gazebo model', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'gazebo_model_pose'})

			# x:377 y:196
			OperatableStateMachine.add('add gazebo model',
										AddGazeboModel(model_name="box_male"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.High, 'failed': Autonomy.Off},
										remapping={'gazebo_model_pose': 'gazebo_model_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
