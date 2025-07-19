OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL = (
    'Target reading grade level: {target_reading_grade_level}'
)

OPENAI_PROMPT_INSTRUCTION__EXPECTED_RESPONSE_FORMAT = (
    'Expected response format:'
)

OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE = 'The response content MUST ONLY contain strictly valid JSON, no wrapping text or delimiters, and MUST be able to be parsed directly using standard Python: `json.loads(response_content)`.'  # noqa: E501
