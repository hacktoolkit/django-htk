# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.assessments.enums import QuestionType
from htk.apps.assessments.utils import build_question_type_choices
from htk.utils import htk_setting


class AbstractAssessment(models.Model):
    """Abstract model for Assessments app to extend from.

    Possible use cases include:
    - Quizzes and Exams
    - Surveys
    """

    name = models.CharField(max_length=255, blank=True)
    # Tracks the version of the assessment
    version = models.IntegerField(default=1)
    # Number of attempts allowed: 0 for unlimited attempts, 1 for only 1.
    num_allowed_attempts = models.PositiveIntegerField(default=0)
    # When `True` and `num_allowed_attempts` == 1, previous responses are overwritten
    is_repeat_allowed = models.BooleanField(default=False)
    # Optional "Exit message" to display when an incorrect answer is provided
    knockout_message = models.TextField(blank=True, null=True, max_length=512)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} (Version {self.version})"


class AbstractAssessmentQuestion(models.Model):
    """Represents one question in an Assessment."""

    ASSESSMENT_MODEL = htk_setting('HTK_ASSESSMENT_MODEL')

    assessment = models.ForeignKey(
        ASSESSMENT_MODEL, related_name='questions', on_delete=models.CASCADE
    )
    text = models.TextField(max_length=256)
    question_type = models.PositiveSmallIntegerField(
        default=QuestionType.UNSPECIFIED.value,
        choices=build_question_type_choices(),
    )
    # If `min_choices` is 0, then none of the answer options are required
    # If `min_choices` > 0, then at least that many answer options must be selected
    min_choices = models.PositiveSmallIntegerField(default=0)
    # If `max_choices` is 0, then all answer options can be selected
    # If `max_choices` > 0, then at most that many answer options can be selected
    max_choices = models.PositiveSmallIntegerField(default=0)
    # Specifies the order of questions within an assessment
    order = models.IntegerField(default=0)
    # Must be `True` to allow empty text responses or "No Entry" for multiple choice
    is_optional = models.BooleanField(default=False)
    # Indicates if this is a knockout question
    is_knockout = models.BooleanField(default=False)
    # Optional "Exit message" to display when an incorrect answer is provided,
    # overrides `AbstractAssessment.knockout_message`
    knockout_message = models.TextField(blank=True, null=True, max_length=512)
    # Must be `True` for a new question
    # Set it to `False` when disabling the question or the question is answered and then subsequently modified
    is_enabled = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return self.text

    @property
    def knockout_message_text(self):
        return self.knockout_message or self.assessment.knockout_message


class AbstractAssessmentQuestionAnswerOption(models.Model):
    """Represents the options for a multiple-choice question."""

    ASSESSMENT_QUESTION_MODEL = htk_setting('HTK_ASSESSMENT_QUESTION_MODEL')

    question = models.ForeignKey(
        ASSESSMENT_QUESTION_MODEL,
        related_name='answer_options',
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=255)
    # Indicates if this choice is the correct answer
    is_correct = models.BooleanField(default=False)
    # Optional color for controlling the UI
    # This is a flexible field and can store any value up to the character limit.
    # As a suggestion, it can store either `None`, or one of the following:
    # - Color name (e.g.`'red'`, `'yellow'`, `'green'`)
    # - Hex color code (e.g. `#ff0000`)
    # - RGBA (e.g. `rgba(255, 0, 0, 0.25)`)
    color = models.CharField(max_length=25, blank=True)
    # Tracks the order of options
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return self.text


class AbstractAssessmentAttempt(models.Model):
    ASSESSMENT_MODEL = htk_setting('HTK_ASSESSMENT_MODEL')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assessment_attempts',
        on_delete=models.CASCADE,
    )
    assessment = models.ForeignKey(
        ASSESSMENT_MODEL, related_name='attempts', on_delete=models.CASCADE
    )
    # Indicates if the attempt has been completed
    is_completed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user.username} - {self.assessment.name}'


class AbstractAssessmentAnswer(models.Model):
    ASSESSMENT_ATTEMPT_MODEL = htk_setting('HTK_ASSESSMENT_ATTEMPT_MODEL')
    ASSESSMENT_QUESTION_MODEL = htk_setting('HTK_ASSESSMENT_QUESTION_MODEL')
    ASSESSMENT_QUESTION_ANSWER_OPTION_MODEL = htk_setting(
        'HTK_ASSESSMENT_QUESTION_ANSWER_OPTION_MODEL'
    )

    attempt = models.ForeignKey(
        ASSESSMENT_ATTEMPT_MODEL,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        ASSESSMENT_QUESTION_MODEL,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    option = models.ForeignKey(
        ASSESSMENT_QUESTION_ANSWER_OPTION_MODEL,
        related_name='selected_options',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )  # For MC and Y/N
    free_response_text = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.question.question_type == QuestionType.FREE_RESPONSE.value:
            result = self.free_response_text
        else:  # MC or Y/N
            result = str(self.option) if self.option else 'No answer'

        return result

    @property
    def is_correct(self):
        if self.question.question_type in [
            QuestionType.MULTIPLE_CHOICE.value,
            QuestionType.YES_OR_NO.value,
        ]:
            result = self.option and self.option.is_correct
        else:
            # Free response grading can be subjective and might need manual review
            result = None

        return result
