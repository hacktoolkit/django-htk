# Local Imports
from utils.features import Feature


FEATURE_EARLY_ACCESS = Feature(
    name='early_access',
    label='Early Access',
    description=(
        'Allow users to request early access to the app. '
        'This feature should be disabled after the app is released.'
    ),
)
