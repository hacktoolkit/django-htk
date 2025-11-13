# Assessments App

Quiz and assessment management system for knowledge testing.

## Quick Start

```python
from htk.apps.assessments.models import (
    AbstractAssessment,
    AbstractAssessmentQuestion,
    AbstractAssessmentQuestionAnswerOption
)

# Create assessment
assessment = AbstractAssessment.objects.create(
    name='Django Fundamentals Quiz',
    description='Test your Django knowledge',
    passing_score=70
)

# Create question
question = AbstractAssessmentQuestion.objects.create(
    assessment=assessment,
    text='What is Django?',
    order=1
)

# Add answer options
AbstractAssessmentQuestionAnswerOption.objects.create(
    question=question,
    text='Python web framework',
    is_correct=True,
    order=1
)

AbstractAssessmentQuestionAnswerOption.objects.create(
    question=question,
    text='Database system',
    is_correct=False,
    order=2
)
```

## Building Assessments

### Create Assessment

```python
from htk.apps.assessments.models import AbstractAssessment

# Create quiz
assessment = AbstractAssessment.objects.create(
    name='Company Values Assessment',
    description='Assess your understanding of company values',
    passing_score=60,
    time_limit=600  # seconds
)
```

### Add Questions

```python
from htk.apps.assessments.models import AbstractAssessmentQuestion

# Single choice question
question = AbstractAssessmentQuestion.objects.create(
    assessment=assessment,
    text='Which is our core value?',
    question_type='single_choice',
    order=1
)

# Multiple choice question
question = AbstractAssessmentQuestion.objects.create(
    assessment=assessment,
    text='Select all that apply',
    question_type='multiple_choice',
    order=2
)

# Free text question
question = AbstractAssessmentQuestion.objects.create(
    assessment=assessment,
    text='Explain your answer',
    question_type='text',
    order=3
)
```

### Add Answer Options

```python
from htk.apps.assessments.models import AbstractAssessmentQuestionAnswerOption

# Create options for question
options_data = [
    ('Innovation', True),
    ('Profit Only', False),
    ('Customer Focus', True),
]

for text, is_correct in options_data:
    AbstractAssessmentQuestionAnswerOption.objects.create(
        question=question,
        text=text,
        is_correct=is_correct
    )
```

## Taking Assessments

### Track User Responses

```python
from htk.apps.assessments.models import AbstractAssessmentResponse

# Submit answer
response = AbstractAssessmentResponse.objects.create(
    assessment=assessment,
    user=user,
    question=question,
    selected_option=option,
    is_correct=option.is_correct
)
```

### Score Assessment

```python
from htk.apps.assessments.models import AbstractAssessment, AbstractAssessmentResponse

# Calculate score
assessment = AbstractAssessment.objects.get(id=assessment_id)
user_responses = AbstractAssessmentResponse.objects.filter(
    assessment=assessment,
    user=user
)

total_questions = assessment.questions.count()
correct_answers = user_responses.filter(is_correct=True).count()
score_percentage = (correct_answers / total_questions) * 100

passed = score_percentage >= assessment.passing_score
```

## Common Patterns

### Assessment Analytics

```python
from django.db.models import Avg, Count
from htk.apps.assessments.models import AbstractAssessment, AbstractAssessmentResponse

# Get assessment statistics
assessment = AbstractAssessment.objects.get(id=assessment_id)
responses = AbstractAssessmentResponse.objects.filter(assessment=assessment)

stats = {
    'total_attempts': AbstractAssessmentResponse.objects.values('user').distinct().count(),
    'average_score': responses.filter(is_correct=True).count() / responses.count() * 100,
    'pass_rate': (
        AbstractAssessmentResponse.objects.filter(
            assessment=assessment,
            score__gte=assessment.passing_score
        ).values('user').distinct().count() /
        AbstractAssessmentResponse.objects.filter(
            assessment=assessment
        ).values('user').distinct().count() * 100
    )
}
```

### Difficulty Analysis

```python
from django.db.models import Avg, Count
from htk.apps.assessments.models import AbstractAssessmentQuestion

# Get most difficult questions
questions = AbstractAssessmentQuestion.objects.filter(
    assessment=assessment
).annotate(
    correct_count=Count(
        'assessmentresponse',
        filter=Q(assessmentresponse__is_correct=True)
    )
)

# Sort by difficulty (fewer correct answers = harder)
difficult = questions.order_by('correct_count')
```

### Timed Assessments

```python
from django.utils import timezone
from datetime import timedelta

# Track time taken
start_time = timezone.now()

# Check time limit
assessment_response = {
    'assessment': assessment,
    'user': user,
    'started_at': start_time,
    'time_limit': assessment.time_limit
}

# Check if time expired
elapsed = (timezone.now() - start_time).total_seconds()
time_remaining = assessment.time_limit - elapsed
expired = time_remaining <= 0
```

### Adaptive Questions

```python
from htk.apps.assessments.models import AbstractAssessmentQuestion

# Show next question based on performance
def get_next_question(user, assessment):
    # Get answered questions
    answered = AbstractAssessmentResponse.objects.filter(
        user=user,
        assessment=assessment
    ).values_list('question_id', flat=True)

    # Get unanswered questions
    next_question = AbstractAssessmentQuestion.objects.filter(
        assessment=assessment
    ).exclude(
        id__in=answered
    ).first()

    return next_question
```

### Generate Certificates

```python
from django.utils import timezone

# Award certificate on passing
def check_and_award_certificate(user, assessment):
    from htk.apps.assessments.models import AssessmentCertificate

    score = calculate_score(user, assessment)
    if score >= assessment.passing_score:
        cert = AssessmentCertificate.objects.create(
            user=user,
            assessment=assessment,
            score=score,
            awarded_at=timezone.now()
        )
        return cert
```

## Models

### AbstractAssessment

```python
class AbstractAssessment(models.Model):
    name = CharField(max_length=200)
    description = TextField(blank=True)
    passing_score = IntegerField(default=60)  # Percentage
    time_limit = IntegerField(null=True, blank=True)  # Seconds
    created = DateTimeField(auto_now_add=True)
```

### AbstractAssessmentQuestion

```python
class AbstractAssessmentQuestion(models.Model):
    assessment = ForeignKey(AbstractAssessment, on_delete=models.CASCADE)
    text = TextField()
    question_type = CharField(max_length=50)  # 'single_choice', 'multiple_choice', 'text'
    order = IntegerField()
```

### AbstractAssessmentQuestionAnswerOption

```python
class AbstractAssessmentQuestionAnswerOption(models.Model):
    question = ForeignKey(AbstractAssessmentQuestion, on_delete=models.CASCADE)
    text = CharField(max_length=500)
    is_correct = BooleanField()
    order = IntegerField()
```

## Configuration

```python
# settings.py
ASSESSMENT_PASSING_SCORE = 70
ASSESSMENT_QUESTION_TYPES = [
    ('single_choice', 'Single Choice'),
    ('multiple_choice', 'Multiple Choice'),
    ('text', 'Free Text'),
]

ASSESSMENT_RANDOMIZE_QUESTIONS = True
ASSESSMENT_RANDOMIZE_OPTIONS = True
ASSESSMENT_SHOW_CORRECT_ANSWERS = True  # After completion
```

## Best Practices

1. **Clear questions** - Write unambiguous assessment questions
2. **Balanced difficulty** - Mix easy and hard questions
3. **Multiple options** - Provide plausible distractor options
4. **Set passing score** - Define clear passing criteria
5. **Provide feedback** - Show correct answers after completion
6. **Track analytics** - Monitor question difficulty
7. **Time limits** - Use for timed assessments

## Related Modules

- `htk.apps.accounts` - User management
- `htk.apps.notifications` - Notify on completion
