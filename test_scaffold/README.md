# Test_Scaffold

## Classes
- **`FakeTime`** (test_scaffold/models.py) - FakeTime keeps track of only one timestamp (one record) or none
- **`FakePrelaunch`** (test_scaffold/models.py) - FakePrelaunch keeps track of only one boolean (one record) or none
- **`BaseTestCase`** (test_scaffold/tests.py) - Base class for all test cases
- **`BaseWebTestCase`** (test_scaffold/tests.py) - Base class for other Web test cases

## Functions
- **`set_fake_timestamp`** (test_scaffold/models.py) - Fakes the system time by setting it to `timestamp`
- **`create_test_user`** (test_scaffold/utils.py) - Creates a new user with random username for testing
- **`create_test_username`** (test_scaffold/utils.py) - Generates a random username

## Components
**Models** (`models.py`)
