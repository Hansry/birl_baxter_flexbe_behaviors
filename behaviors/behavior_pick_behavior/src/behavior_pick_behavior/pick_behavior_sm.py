#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_pick_behavior')
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
class PickbehaviorSM(Behavior):
	'''
	pick a object below the gripper
	'''


	def __init__(self):
		super(PickbehaviorSM, self).__init__()
		self.name = 'Pick behavior'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:580 y:651, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:158 y:54
			OperatableStateMachine.add('gripper_open',
										ExecuteGripperMove(gripper_move=False),
										transitions={'reached': 'get pick pose', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off})

			# x:536 y:156
			OperatableStateMachine.add('move to pose',
										ExecuteTrajectoryMovePose(duration=5.0),
										transitions={'reached': 'gripper close', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:695 y:248
			OperatableStateMachine.add('gripper close',
										ExecuteGripperMove(gripper_move=True),
										transitions={'reached': 'get hover pick pose', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off})

			# x:639 y:412
			OperatableStateMachine.add('get hover pick pose',
										GetPoseConfig(pose_name="pick_hover_goal_pose", path="default"),
										transitions={'done': 'move to hover pose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:384 y:495
			OperatableStateMachine.add('move to hover pose',
										ExecuteTrajectoryMovePose(duration=5.0),
										transitions={'reached': 'finished', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:344 y:136
			OperatableStateMachine.add('get pick pose',
										GetPoseConfig(pose_name="pick_goal_pose", path="default"),
										transitions={'done': 'move to pose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
