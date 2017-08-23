#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_go_to_hover_pick_pose')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from birl_baxter_flexbe_states.get_pose_config import GetPoseConfig
from birl_baxter_flexbe_states.execute_trajectory_move_pose import ExecuteTrajectoryMovePose
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 23 2017
@author: Ben
'''
class GotoHoverPickPoseSM(Behavior):
	'''
	move arm to hover pose of picking
	'''


	def __init__(self):
		super(GotoHoverPickPoseSM, self).__init__()
		self.name = 'Go to Hover Pick Pose'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:392 y:389, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:48 y:111
			OperatableStateMachine.add('get pick hover pose',
										GetPoseConfig(pose_name="pick_hover_goal_pose", path="default"),
										transitions={'done': 'move to pose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})

			# x:162 y:275
			OperatableStateMachine.add('move to pose',
										ExecuteTrajectoryMovePose(duration=6.0),
										transitions={'reached': 'finished', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose_config': 'pose_config'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
