#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_go_to_start_pose')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from birl_baxter_flexbe_states.get_start_pose import GetStartPose
from birl_baxter_flexbe_states.execute_trajectory_move_start_pose import ExecuteTrajectoryMoveStartPose
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Aug 23 2017
@author: Ben Lin
'''
class GotoStartPoseSM(Behavior):
	'''
	Move the arm to start pose
	'''


	def __init__(self):
		super(GotoStartPoseSM, self).__init__()
		self.name = 'Go to Start Pose'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:509 y:406, x:195 y:368
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:70 y:99
			OperatableStateMachine.add('get start pose',
										GetStartPose(path="default"),
										transitions={'done': 'Move to start', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'start_angles': 'start_angles'})

			# x:485 y:159
			OperatableStateMachine.add('Move to start',
										ExecuteTrajectoryMoveStartPose(duration=6.0),
										transitions={'reached': 'finished', 'failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'start_angles': 'start_angles'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
