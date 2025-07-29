from typing      import (
    Union, 
    Dict, 
    List, 
    Optional, 
    Tuple,
)
from .Types      import (
    State, 
    StateType, 
    StateBehavior, 
    Transition, 
    TransitionType, 
    Form, 
    FormType, 
    Doc, 
    ID_TYPE,
)
from .Exceptions import (
    StartNodeAlreadyExists, 
    EndNodeAlreadyExists, 
    SourceNodeNotInGraph, 
    TargetNodeNotInGraph
)
from .Loader.Errors import Errors


class Graph():
    def __init__(self):
        self.start_node_id : Union[ID_TYPE, None] = None
        self.end_node_ids  : List[ID_TYPE]        = list()
        self.always_open_ids : List[ID_TYPE]      = list()

        self.states      : Dict[ID_TYPE, State]      = dict()
        self.transitions : Dict[ID_TYPE, Transition] = dict()
        self.errors      : List[Tuple[str, Optional]] = list()

    def AddState(self, state : State) -> State:
        if state['id'] in self.states:
            return state 

        if state['type'] == StateType.START and self.start_node_id:
            self.errors.append(
                (Errors.GRAPH_START_NODE_ALREADY_EXISTS,
                 state['name'])
            )
            return None
            #raise StartNodeAlreadyExists(state) 

        self.states[state['id']] = state

        if    state['type'] == StateType.START:
            self.start_node_id = state['id'] 
        elif  state['type'] == StateType.END:
            #self.end_node_id   = state['id'] 
            self.end_node_ids.append(state['id'])
        elif  state['type'] == StateType.ALWAYS_OPEN:
            self.always_open_ids.append(state['id'])

        return state

    def AddTransition(self, 
                transition: Transition) -> Transition:
        if transition['id'] in self.transitions:
            return transition

        if not self.states.get(transition['source_id'], None):
            self.errors.append(
                (Errors.GRAPH_SOURCE_NODE_NOT_IN_GRAPH,
                 transition['name'])
            )
            return None
            #raise SourceNodeNotInGraph(transition['source_id'])
        if not self.states.get(transition['target_id'], None):
            self.errors.append(
                (Errors.GRAPH_TARGET_NODE_NOT_IN_GRAPH,
                 transition['name'])
            )
            return None
            #raise TargetNodeNotInGraph(transition['target_id'])
        
        self.transitions[transition['id']] = transition

        return transition

    def AttachAnotherGraph(self, another, ext_state):
        for idx, end_id in enumerate(self.end_node_ids):
            if end_id == ext_state['id']:
                self.end_node_ids.pop(idx)
                break
        else:
            self.errors.append(
                (Errors.GRAPH_EXTEND_NOT_END_STATE,
                 ext_state['name'])
            )
            return None
            #raise RuntimeError(f"State {ext_state['name']} is not an end state!")

        if ext_state['id'] not in self.states:
            self.errors.append(
                (Errors.GRAPH_EXTEND_END_STATE_NOT_IN_GRAPH,
                 ext_state['name'])
            )
            return None
            #raise RuntimeError(f"State {ext_state['name']} is not in graph!")

        original_state = self.states[ext_state['id']]
        repleace_state = another.states[another.start_node_id]
        for k, v in self.transitions.items():
            if v['target_id'] == original_state['id']:
                v['target_id'] = repleace_state['id']
                break
        else:
            self.errors.append(
                (Errors.GRAPH_EXTEND_END_STATE_IS_NOT_A_TARGET,
                 ext_state['name'])
            )
            return None
            #raise RuntimeError(f"State {ext_state['name']} is not a target of any transition!")
        self.states.pop(ext_state['id'])

        self.end_node_ids.extend(another.end_node_ids)
        self.always_open_ids.extend(another.always_open_ids)
        self.states.update(another.states)
        self.transitions.update(another.transitions)
        #self.errors.extend(another.errors)



if __name__ == '__main__':
    pass

