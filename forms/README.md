# Forms

## Classes
- **`AbstractModelInstanceUpdateForm`** (forms/classes.py) - An abstract class for manipulating Model instances

## Functions
- **`save`** (forms/classes.py) - Saves this form
- **`clean_model_instance_field`** (forms/utils.py) - Called from within the clean method of a ModelInstanceField or CharField
- **`set_input_attrs`** (forms/utils.py) - Set various attributes on form input fields
- **`set_input_placeholder_labels`** (forms/utils.py) - Set placeholder attribute to the field label on form input fields, if it doesn't have a placeholder set
- **`get_form_errors`** (forms/utils.py) - Return a list of errors on the form
- **`get_form_error`** (forms/utils.py) - Return the first error of a form
