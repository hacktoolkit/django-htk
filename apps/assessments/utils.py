# HTK Imports
from htk.apps.assessments.enums import QuestionType
from htk.utils.enums import get_enum_symbolic_name


def build_question_type_choices():
    choices = [
        (
            type.value,
            get_enum_symbolic_name(type),
        )
        for type in QuestionType
    ]
    return choices
