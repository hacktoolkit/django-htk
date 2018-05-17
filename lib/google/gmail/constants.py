GMAIL_RESOURCES = {
    # labels - https://developers.google.com/gmail/api/v1/reference/users/labels
    'labels_list' : 'https://www.googleapis.com/gmail/v1/users/%(user_id)s/labels',
    # messages - https://developers.google.com/gmail/api/v1/reference/users/messages
    'message_get' : 'https://www.googleapis.com/gmail/v1/users/%(user_id)s/messages/%(message_id)s',
    'message_modify' : 'https://www.googleapis.com/gmail/v1/users/%(user_id)s/messages/%(message_id)s/modify',
    'messages_list' : 'https://www.googleapis.com/gmail/v1/users/%(user_id)s/messages',
    # threads - https://developers.google.com/gmail/api/v1/reference/users/threads
    'thread_get' : 'https://www.googleapis.com/gmail/v1/users/%(user_id)s/threads/%(thread_id)s',
    'threads_list' : 'https://www.googleapis.com/gmail/v1/users/%(user_id)s/threads',
}
