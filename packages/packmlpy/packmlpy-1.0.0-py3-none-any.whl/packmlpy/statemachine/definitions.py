import enum

class StateNames(enum.Enum):
	Idle = 0
	Starting = 1
	Execute = 2
	Holding = 3
	Held = 4
	Unholding = 5
	Suspending = 6
	Suspended = 7
	Unsuspending = 8
	Completing = 9
	Complete = 10
	Resetting = 11
	Stopping = 12
	Stopped = 13
	Aborting = 14
	Aborted = 15
	Clearing = 16

class ActingStateNames(enum.Enum):
	Starting = 1, 
	Execute = 2,
	Completing = 9, 
	Holding = 3,
	Unholding = 5, 
	Suspending = 6,
	Unsuspending = 8,
	Aborting = 14, 
	Clearing = 16,
	Stopping = 12,
	Resetting = 11, 

transitions = [
    { 'trigger': 'start', 'source': StateNames.Idle, 'dest': StateNames.Starting },
    { 'trigger': '_starting_sc', 'source': StateNames.Starting, 'dest': StateNames.Execute },
    { 'trigger': '_execute_sc', 'source': StateNames.Execute, 'dest': StateNames.Completing },
    { 'trigger': '_completing_sc', 'source': StateNames.Completing, 'dest': StateNames.Complete },
    { 'trigger': 'reset', 'source': StateNames.Complete, 'dest': StateNames.Resetting },
    { 'trigger': '_resetting_sc', 'source': StateNames.Resetting, 'dest': StateNames.Idle },

    { 'trigger': 'hold', 'source': StateNames.Execute, 'dest': StateNames.Holding },
    { 'trigger': '_holding_sc', 'source': StateNames.Holding, 'dest': StateNames.Held },
    { 'trigger': 'unhold', 'source': StateNames.Held, 'dest': StateNames.Unholding },
    { 'trigger': '_unholding_sc', 'source': StateNames.Unholding, 'dest': StateNames.Execute },

    { 'trigger': 'suspend', 'source': StateNames.Execute, 'dest': StateNames.Suspending },
    { 'trigger': '_suspending_sc', 'source': StateNames.Suspending, 'dest': StateNames.Suspended },
    { 'trigger': 'unsuspend', 'source': StateNames.Suspended, 'dest': StateNames.Unsuspending },
    { 'trigger': '_unsuspending_sc', 'source': StateNames.Unsuspending, 'dest': StateNames.Execute },

    { 'trigger': 'stop', 'source': StateNames.Idle, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Starting, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Execute, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Completing, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Complete, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Resetting, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Holding, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Held, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Unholding, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Suspending, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Suspended, 'dest': StateNames.Stopping },
	{ 'trigger': 'stop', 'source': StateNames.Unsuspending, 'dest': StateNames.Stopping },
    { 'trigger': '_stopping_sc', 'source': StateNames.Stopping, 'dest': StateNames.Stopped },
    { 'trigger': 'reset', 'source': StateNames.Stopped, 'dest': StateNames.Resetting },

	{ 'trigger': 'abort', 'source': StateNames.Idle, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Starting, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Execute, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Completing, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Complete, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Resetting, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Holding, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Held, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Unholding, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Suspending, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Suspended, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Unsuspending, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Clearing, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Stopping, 'dest': StateNames.Aborting },
	{ 'trigger': 'abort', 'source': StateNames.Stopped, 'dest': StateNames.Aborting },
    { 'trigger': '_aborting_sc', 'source': StateNames.Aborting, 'dest': StateNames.Aborted },
    { 'trigger': 'clear', 'source': StateNames.Aborted, 'dest': StateNames.Clearing },
    { 'trigger': '_clearing_sc', 'source': StateNames.Clearing, 'dest': StateNames.Stopped },
]