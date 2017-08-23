#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_place_behavior')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from birl_baxter_flexbe_states.get_pose_config import GetPoseConfig
from birl_baxter_flexbe_states.execute_trajectory_move_pose import ExecuteTrajectoryMovePose
from birl_baxter_flexbe_states.execute_gripper_move import ExecuteGripperMove
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 23 2017
@author: Ben
'''
class PlacebehaviorSM(Behavior):
	'''
	place a object below the gripper
	'''


	def __init__(self):
		super(PlacebehaviorSM, self).__init__()
		self.name = 'Place behavior'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:509 y:527, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:48 y:111
			OperatableStateMachine.add('get place pose',
										GetPoseConfig(pose_name="place_goal_pose", path="default"),
										transitions={'done': 'move to place pose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:627 y:428
			OperatableStateMachine.add('move to pose',
										ExecuteTrajectoryMovePose(duration=5.0),
										transitions={'reached': 'finished', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:240 y:137
			OperatableStateMachine.add('move to place pose',
										ExecuteTrajectoryMovePose(duration=5.0),
										transitions={'reached': 'gripper open', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:438 y:156
			OperatableStateMachine.add('gripper open',
										ExecuteGripperMove(gripper_move=False),
										transitions={'reached': 'get place hover pose', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off})

			# x:600 y:230
			OperatableStateMachine.add('get place hover pose',
										GetPoseConfig(pose_name="place_hover_goal_pose", path="default"),
										transitions={'done': 'move to pose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
