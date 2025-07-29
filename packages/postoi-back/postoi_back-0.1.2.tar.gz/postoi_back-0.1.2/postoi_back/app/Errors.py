from enum           import IntEnum, unique, auto
from .Exceptions    import PROJECTResourceErrors


# this one copies the ones from PROJECT-resource
@unique
class Errors(IntEnum):
    STATES_TABLE_EMPTY=auto()
    TRANSITIONS_TABLE_EMPTY=auto()
    FORMS_TABLE_EMPTY=auto()
    CONFIG_TABLE_EMPTY=auto()

    STATE_NO_BEHAVIOR=auto()
    TRANSITION_NO_BEHAVIOR=auto()

    FORM_TYPE_UNKNOWN=auto()

    GRAPH_START_NODE_ALREADY_EXISTS=auto()
    GRAPH_SOURCE_NODE_NOT_IN_GRAPH=auto()
    GRAPH_TARGET_NODE_NOT_IN_GRAPH=auto()
    GRAPH_EXTEND_NOT_END_STATE=auto()
    GRAPH_EXTEND_END_STATE_NOT_IN_GRAPH=auto()
    GRAPH_EXTEND_END_STATE_IS_NOT_A_TARGET=auto()

def InterpretErrors(errors):
    ret = list()
    for err in errors:
        match err[0]:
            case Errors.STATES_TABLE_EMPTY:
                ret.append(
                    "Таблица состояний пуста!"
                )
            case Errors.TRANSITIONS_TABLE_EMPTY:
                ret.append(
                    "Таблица переходов пуста!"
                )
            case Errors.FORMS_TABLE_EMPTY:
                ret.append(
                    "Таблица форм пуста!"
                )
            case Errors.CONFIG_TABLE_EMPTY:
                ret.append(
                    "Таблица конфига пуста!"
                )
            case Errors.STATE_NO_BEHAVIOR:
                ret.append(
                    f"Состояние не имеет поведения -- {err[1]}"
                )
            case Errors.TRANSITION_NO_BEHAVIOR:
                ret.append(
                    f"Переход не имеет поведения -- {err[1]}"
                )
            case Errors.FORM_TYPE_UNKNOWN:
                ret.append(
                    f"Неизвестный тип формы -- {err[1]}"
                )
            case Errors.GRAPH_START_NODE_ALREADY_EXISTS:
                ret.append(
                    f"Состояние {err[1]} хочет стать начальным, но такое уже есть!"
                )
            case Errors.GRAPH_SOURCE_NODE_NOT_IN_GRAPH:
                ret.append(
                    f"Начальное состояние для перехода {err[1]} не в графе!"
                )
            case Errors.GRAPH_TARGET_NODE_NOT_IN_GRAPH:
                ret.append(
                    f"Конечное состояние для перехода {err[1]} не в графе!"
                )
            case Errors.GRAPH_EXTEND_NOT_END_STATE:
                ret.append(
                    f"В состояние {err[1]} помещается другой граф, но оно не конечное!"
                )
            case Errors.GRAPH_EXTEND_END_STATE_NOT_IN_GRAPH:
                ret.append(
                    f"В состояние {err[1]} помещается другой граф, но оно не в графе!"
                )
            case Errors.GRAPH_EXTEND_END_STATE_IS_NOT_A_TARGET:
                ret.append(
                    f"В состояние {err[1]} помещается другой граф, но в него не приходит ни одно состояние!"
                )
    return ret


def RaiseException(errors):
    mes = "\n".join(errors)
    raise PROJECTResourceErrors(mes)

