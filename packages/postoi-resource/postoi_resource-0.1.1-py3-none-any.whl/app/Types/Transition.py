from typing     import TypedDict, List, Dict, Union
from enum       import Enum, unique

from .          import ID_TYPE


@unique
class TransitionType(Enum):
    UNKNOWN         = 'UNKNOWN'
    CONDITIONAL     = 'CONDITIONAL'
    STRICT          = 'STRICT'
    UNCONDITIONAL   = 'UNCONDITIONAL'


class Transition(TypedDict, total=True):
    id              : ID_TYPE
    name            : str
    type            : TransitionType
    source_id       : ID_TYPE
    target_id       : ID_TYPE
    form_elem_ids   : List[ID_TYPE]

def get_dummy_transition() -> Transition:
    return {
        'id'            : '',
        'name'          : 'dummy',
        'type'          : TransitionType.UNKNOWN,
        'source_id'     : '',
        'target_id'     : '',
        'form_elem_ids' : list(),
    }

