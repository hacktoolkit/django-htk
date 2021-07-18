HTK_FORM_STYLE = 'bootstrap'  # 'bootstrap', 'pure'

HTK_DEFAULT_FORM_INPUT_CLASS = 'pure-input-1'  # PureCSS (https://purecss.io/)

HTK_FORM_WIDGET_CLASSES = {
    'bootstrap': {
        'default': 'form-control',
        # Checkbox
        'CheckboxInput': 'form-check-input',
        # Text Inputs
        'EmailInput': 'form-control',
        'NumberInput': 'form-control',
        'PasswordInput': 'form-control',
        'TextInput': 'form-control',
        'Textarea': 'form-control',
        'URLInput': 'form-control',
    },
    'pure': {
        'default': 'pure-input-1',
        # Checkbox
        'CheckboxInput': 'pure-input-1',
        # Text Inputs
        'EmailInput': 'pure-input-1',
        'NumberInput': 'pure-input-1',
        'PasswordInput': 'pure-input-1',
        'TextInput': 'pure-input-1',
        'Textarea': 'pure-input-1',
        'URLInput': 'pure-input-1',
    },
}
