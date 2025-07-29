from typing     import TypedDict, List, Dict, Union
from enum       import Enum, unique

from .          import ID_TYPE


@unique
class StateType(Enum):
    UNKNOWN             = 'UNKNOWN' 
    START               = 'START'
    END                 = 'END'
    REGULAR             = 'REGULAR'
    ALWAYS_OPEN         = 'ALWAYS_OPEN'


class StateBehavior(Enum):
    UNKNOWN             = 'UNKNOWN' 
    FORM                = 'FORM'
    INPUT_CHECK         = 'INPUT_CHECK'
    EXTERNAL            = 'EXTERNAL'


class State(TypedDict):
    id                              : ID_TYPE
    name                            : str
    type                            : StateType
    behavior                        : StateBehavior
    is_start                        : bool
    is_end                          : bool
    forms_ids                       : List[ID_TYPE]
    in_transitions_ids              : List[ID_TYPE]
    out_transitions_ids             : List[ID_TYPE]
    external_table_data             : str


def get_dummy_state() -> State:
    return {
        'id'                    : '',
        'name'                  : 'dummy',
        'type'                  : StateType.UNKNOWN,
        'behavior'              : StateBehavior.UNKNOWN,
        'is_start'              : False,
        'is_end'                : False,
        'forms_ids'             : list(),
        'in_transitions_ids'    : list(),
        'out_transitions_ids'   : list(),
        'external_table_data'   : '' 
    }

