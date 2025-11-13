# Assessments App

Quiz and assessment management system.

## Quick Start

```python
from htk.apps.assessments.models import (
    AbstractAssessment,
    AbstractAssessmentQuestion,
    AbstractAssessmentQuestionAnswerOption
)

# Create assessment
assessment = AbstractAssessment.objects.create(
    name='Company Culture Quiz',
    description='Test your knowledge'
)

# Create question
question = AbstractAssessmentQuestion.objects.create(
    assessment=assessment,
    text='What is our core value?',
    order=1
)

# Add answer options
option1 = AbstractAssessmentQuestionAnswerOption.objects.create(
    question=question,
    text='Innovation',
    is_correct=True,
    order=1
)

option2 = AbstractAssessmentQuestionAnswerOption.objects.create(
    question=question,
    text='Profit',
    is_correct=False,
    order=2
)
```

## Models

- **`AbstractAssessment`** - Quiz/assessment
- **`AbstractAssessmentQuestion`** - Question in assessment
- **`AbstractAssessmentQuestionAnswerOption`** - Multiple choice options

## Related Modules

- `htk.apps.accounts` - User assessment results
