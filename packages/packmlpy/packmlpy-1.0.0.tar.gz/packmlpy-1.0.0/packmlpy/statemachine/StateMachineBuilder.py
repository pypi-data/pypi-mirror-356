from typing import Self
from packmlpy.statemachine.PackMlStateMachine import PackMlStateMachine
from packmlpy.statemachine.PackMlStateMachine import StateNames

class StateMachineBuilder:
	"""
	Builder class that is in charge of constructing a properly set up PackMlStateMachine
	"""
	

	def __init__(self):
		self.stateMachine = PackMlStateMachine(StateNames.Idle)

	
	def with_initial_state(self, initialState: str) -> Self :  
		""" 
		* Constructs a state machine with a special initial state
		* 
		* initialState The state that is to be the initial state of the state machine
		* return: This StateMachineBuilder instance to use for further construction operations
		"""
		self.stateMachine.set_state(initialState)
		return self
	

	
	"""
	 * Adds an IStateAction to a certain State. The IStateAction will be executed in that given State.
	 * 
	 * @param action An instance of IStateAction that is executed in StartingState
	 * @param stateName Name of the State that the action will be executed in.
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action(self, action, stateName: StateNames) -> Self :
		self.stateMachine.append_action(action, stateName)
		
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in StartingState. Alias for withAction(action, 'Starting').
	 * 
	 * @param action An instance of IStateAction that is executed in StartingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_starting(self, action) -> Self :
		self.with_action(action, StateNames.Starting)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in ExecuteState. Alias for withAction(action, StateNamess.Execute).
	 * 
	 * @param action An instance of IStateAction that is executed in ExecuteState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_execute(self, action) -> Self :
		self.with_action(action, StateNames.Execute)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in CompletingState. Alias for withAction(action, StateNames.Completing).
	 * 
	 * @param action An instance of IStateAction that is executed in CompletingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_completing(self, action) -> Self :
		self.with_action(action, StateNames.Completing)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in SuspendingState. Alias for withAction(action, StateNames.Suspending).
	 * 
	 * @param action An instance of IStateAction that is executed in SuspendingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_suspending(self, action) -> Self :
		self.with_action(action, StateNames.Suspending)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in UnsuspendingState. Alias for withAction(action, StateNames.Unsuspending).
	 * 
	 * @param action An instance of IStateAction that is executed in UnsuspendingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_unsuspending(self, action) -> Self :
		self.with_action(action, StateNames.Unsuspending)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in HoldingState. Alias for withAction(action, StateNames.Holding).
	 * 
	 * @param action An instance of IStateAction that is executed in HoldingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_holding(self, action) -> Self :
		self.with_action(action, StateNames.Holding)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in UnholdingState. Alias for withAction(action, StateNames.Unholding).
	 * 
	 * @param action An instance of IStateAction that is executed in UnholdingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_unholding(self, action) -> Self :
		self.with_action(action, StateNames.Unholding)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in ResettingState. Alias for withAction(action, StateNames.Resetting).
	 * 
	 * @param action An instance of IStateAction that is executed in ResettingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_resetting(self, action) -> Self :
		self.with_action(action, StateNames.Resetting)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in StoppingState. Alias for withAction(action, StateNames.Stopping).
	 * 
	 * @param action An instance of IStateAction that is executed in StoppingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_stopping(self, action) -> Self :
		self.with_action(action, StateNames.Stopping)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in AbortingState. Alias for withAction(action, StateNames.Aborting).
	 * 
	 * @param action An instance of IStateAction that is executed in AbortingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_aborting(self, action) -> Self :
		self.with_action(action, StateNames.Aborting)
		return self
	

	"""
	 * Adds an IStateAction that is to be executed in ClearingState. Alias for withAction(action, StateNames.Clearing).
	 * 
	 * @param action An instance of IStateAction that is executed in ClearingState
	 * @return This StateMachineBuilder instance to use for further construction operations
	"""
	def with_action_in_clearing(self, action) -> Self :
		self.with_action(action, StateNames.Clearing)
		return self
	

	"""
	 * Finishes building the PackMlStateMachine and returns a fresh instance with the given attributes
	 * 
	 * @return Fresh instance of PackMlStateMachine
	"""
	def build(self) :
		return self.stateMachine
	
