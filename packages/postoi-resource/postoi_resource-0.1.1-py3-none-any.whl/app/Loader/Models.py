class StateFieldsConsts():
    NAME                = 'Название'
    BEHAVIOR            = 'Поведение'
    FORMS               = 'Форма'
    IN_TRANSITIONS      = 'Входящие переходы'
    OUT_TRANSITIONS     = 'Выходящие переходы'
    EXTERANL_TABLE_DATA = 'Внешняя таблица'


class StateBehaviorConsts():
    FORM                = 'Форма'
    INPUT_CHECK         = 'Проверка ввода'
    EXTERNAL            = 'Внешняя таблица'


class TransitionFieldConsts():
    NAME                = 'Название'
    SOURCE              = 'Откуда'
    TARGET              = 'Куда'
    FORM_CONDITIONS     = 'Эллемент формы'
    TRANSITION_CONDITION= 'Условие перехода'


class TransitionTypesConsts():
    CONDITIONAL         = 'Условный'
    UNCONDITIONAL       = 'Безусловный'
    STRICT              = 'Строгий'


class FormFieldConsts():
    NAME                = 'Название'
    TYPE                = 'Тип'
    TEXT                = 'Описание'
    STATE_ID            = 'Состояние'
    TAGS                = 'jinja tags'


class DocFieldConsts():
    NAME                = 'Название'
    TAG                 = 'Тэг'

