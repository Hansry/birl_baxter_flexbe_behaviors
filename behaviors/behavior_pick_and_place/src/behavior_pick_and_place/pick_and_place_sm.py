#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_pick_and_place')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_add_gazebo_model.add_gazebo_model_sm import AddGazeboModelSM
from behavior_go_to_hover_pick_pose.go_to_hover_pick_pose_sm import GotoHoverPickPoseSM
from behavior_go_to_start_pose.go_to_start_pose_sm import GotoStartPoseSM
from behavior_pick_behavior.pick_behavior_sm import PickbehaviorSM
from behavior_go_to_hover_place.go_to_hover_place_sm import gotohoverplaceSM
from behavior_place_behavior.place_behavior_sm import PlacebehaviorSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 23 2017
@author: Ben
'''
class pickandplaceSM(Behavior):
	'''
	Baxter robot executing pick and place behavior
	'''


	def __init__(self):
		super(pickandplaceSM, self).__init__()
		self.name = 'pick and place'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(AddGazeboModelSM, 'Add Gazebo Model')
		self.add_behavior(GotoHoverPickPoseSM, 'Go to Hover Pick Pose')
		self.add_behavior(GotoStartPoseSM, 'Go to Start Pose')
		self.add_behavior(PickbehaviorSM, 'Pick behavior')
		self.add_behavior(gotohoverplaceSM, 'go to hover place')
		self.add_behavior(PlacebehaviorSM, 'Place behavior')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:260 y:629, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Add Gazebo Model',
										self.use_behavior(AddGazeboModelSM, 'Add Gazebo Model'),
										transitions={'finished': 'Go to Start Pose', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:417 y:177
			OperatableStateMachine.add('Go to Hover Pick Pose',
										self.use_behavior(GotoHoverPickPoseSM, 'Go to Hover Pick Pose'),
										transitions={'finished': 'Pick behavior', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:240 y:101
			OperatableStateMachine.add('Go to Start Pose',
										self.use_behavior(GotoStartPoseSM, 'Go to Start Pose'),
										transitions={'finished': 'Go to Hover Pick Pose', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:578 y:251
			OperatableStateMachine.add('Pick behavior',
										self.use_behavior(PickbehaviorSM, 'Pick behavior'),
										transitions={'finished': 'go to hover place', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:629 y:411
			OperatableStateMachine.add('go to hover place',
										self.use_behavior(gotohoverplaceSM, 'go to hover place'),
										transitions={'finished': 'Place behavior', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:483 y:610
			OperatableStateMachine.add('Place behavior',
										self.use_behavior(PlacebehaviorSM, 'Place behavior'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
