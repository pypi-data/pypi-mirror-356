from transitions.extensions.asyncio import AsyncMachine
from typing import Dict
from packmlpy.statemachine.definitions import StateNames, ActingStateNames, transitions


class PackMlStateMachine(AsyncMachine):

	def __init__(self, initial_state: StateNames):
		AsyncMachine.__init__(self, states=(StateNames), transitions=transitions, initial=initial_state, auto_transitions=False)
		self.state_change_observers: Dict[StateNames, int] = {} # dict to store state change observers per state (needed to remove them as the transitions library just stores them in a plain array)
		# fill state_change_oberservers with zeros
		self.state_change_observers = {state: 0 for state in StateNames}
		self._setup_all_self_completes()

	async def run_self_complete(self, transition_name):
		await self.trigger(transition_name)

	def _setup_all_self_completes(self):
		'''
		Setup all the self completes defined in PackML. Unfortunately this needs to be done explicitly to have static references to the lambda parameters. 
		It cannot be done using a loop over all ActingStateNames.
		'''
		state = self.get_state("Starting")
		starting_self_complete = lambda: self.run_self_complete('_starting_sc')
		state.on_enter.append(starting_self_complete)

		state = self.get_state("Execute")
		execute_self_complete = lambda: self.run_self_complete('_execute_sc')
		state.on_enter.append(execute_self_complete)

		state = self.get_state("Completing")
		completing_self_complete = lambda: self.run_self_complete('_completing_sc')
		state.on_enter.append(completing_self_complete)

		state = self.get_state("Holding")
		holding_self_complete = lambda: self.run_self_complete('_holding_sc')
		state.on_enter.append(holding_self_complete)

		state = self.get_state("Unholding")
		unholding_self_complete = lambda: self.run_self_complete('_unholding_sc')
		state.on_enter.append(unholding_self_complete)

		state = self.get_state("Suspending")
		suspending_self_complete = lambda: self.run_self_complete('_suspending_sc')
		state.on_enter.append(suspending_self_complete)

		state = self.get_state("Unsuspending")
		unsuspending_self_complete = lambda: self.run_self_complete('_unsuspending_sc')
		state.on_enter.append(unsuspending_self_complete)

		state = self.get_state("Stopping")
		stopping_self_complete = lambda: self.run_self_complete('_stopping_sc')
		state.on_enter.append(stopping_self_complete)

		state = self.get_state("Aborting")
		aborting_self_complete = lambda: self.run_self_complete('_aborting_sc')
		state.on_enter.append(aborting_self_complete)

		state = self.get_state("Clearing")
		clearing_self_complete = lambda: self.run_self_complete('_clearing_sc')
		state.on_enter.append(clearing_self_complete)

		state = self.get_state("Resetting")
		resetting_self_complete = lambda: self.run_self_complete('_resetting_sc')
		state.on_enter.append(resetting_self_complete)


	def add_state_change_observer(self, observer) :
		"""
		Adds a new StateChangeObserver instance to the list of observers.
		observer: The new observer to add.
		"""
		for state_name in StateNames:
			# Get the state object and add the observer as the first on_enter callback
			state = self.get_state(state_name)
			state.on_enter.insert(0, observer)
			
			# Get current count of observers (typically 0 before adding one, but there could be multiple observers) and increment it
			observers_in_state_count = self.state_change_observers[state_name]
			new_count = observers_in_state_count + 1
			self.state_change_observers[state_name] = new_count
	

	def remove_all_state_change_observers(self):
		"""
		Removes all StateChangeObservers.
		"""
		for state_name in StateNames:
			self.remove_state_change_observers(state_name)


	def remove_state_change_observers(self, state_name:StateNames):
		"""
		Removes all StateChangeObservers from a given state.
		"""
		self.test_state_name(state_name)
		# Get the number of observers for the state
		observer_count = self.state_change_observers.get(state_name)

		# get the state for the given state name
		state = self.get_state(state_name)
		state.on_enter = state.on_enter[observer_count:]


	def append_action(self, action, state_name: StateNames):
		'''
		Append an action to be executed at the end of the 'on_enter_<state>' array to ensure that the state observers are always called first
		'''
		self.test_state_name(state_name)
		state = self.get_state(state_name)	# get state for the given state name

		# Here's a part that's a bit tricky: active states MUST self-complete their state (automatic transition to next state) as their last action. 
		# Hence there must be a check if the state is an active state. If it is, the action to be added with this function cannot be added as the last action, 
		# but must instead be added as the one before the last
		if self.is_acting_state(state_name):
			state.on_enter.insert(-1, action)	# insert before end if it's an acting state -> there is no self-complete at the end
		else:
			state.on_enter.append(action) 		# append to end if it's a wait state -> there is no self-complete at the end


	def test_state_name(self, state_name:StateNames):
		if state_name.name not in self.states:
			raise Exception(f'You are trying to set the state machine to the state "{state_name}". This is not a valid state of the PackML state machine.')
		
	
	def is_acting_state(self, state_name: StateNames):
		if state_name.name in [acting_state.name for acting_state in ActingStateNames]:
			return True
		
		return False