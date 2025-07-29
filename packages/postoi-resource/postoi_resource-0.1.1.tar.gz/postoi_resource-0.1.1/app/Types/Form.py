from typing     import TypedDict, List, Dict, Union
from enum       import Enum, unique

from .          import ID_TYPE


@unique
class FormType(Enum):
    UNKNOWN         = 'UNKNOWN TYPE!'
    REGULAR_TEXT    = 'Простой текст'
    REGULAR_FIELD   = 'Поле для заполнения'
    DYNAMIC_FIELD   = 'Поле для заполнения динамическое'
    BUTTON          = 'Кнопка действия'
    SINGLE_CHOICE   = 'Кнопка единичного выбора'
    MULTI_CHOICE    = 'Кнопка множественного выбора'


class Form(TypedDict, total=True):
    id              : ID_TYPE
    name            : str
    type            : FormType
    text            : str
    state_id        : ID_TYPE
    tags            : Union[List[str], None]


def get_dummy_form() -> Form:
    return {
        'id'            : '0',
        'name'          : 'dummy',
        'type'          : FormType.UNKNOWN,
        'text'          : str,
        'state_id'      : '0',
        'tags'          : None,
    }

