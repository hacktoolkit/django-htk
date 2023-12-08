# Third Party (PyPI) Imports
import requests

# HTK Imports
from htk.compat import b64decode
from htk.lib.google.gmail.constants import GMAIL_RESOURCES
from htk.utils import refresh
from htk.utils.cache_descriptors import CachedAttribute
from htk.utils.regex import Re


# isort: off


class GmailAuthenticationException(Exception):
    pass


class GmailAPI(object):
    """Interface to Gmail API

    https://developers.google.com/gmail/api/v1/reference/
    """
    def __init__(self, user, email=None):
        self.user = user
        self.email = email
        self.g_social_auth = user.profile.get_social_user('google-oauth2', email)
        if self.g_social_auth is None:
            raise GmailAuthenticationException()
        self.labels_map = None
        self.label_names_map = None

    def get_resource_url(self, resource_name, **kwargs):
        user_id = self.email if self.email else 'me'
        values = {
            'user_id' : user_id,
        }
        values.update(kwargs)
        url = GMAIL_RESOURCES[resource_name] % values
        return url

    def get_authorization_headers(self):
        headers = {}
        if self.g_social_auth:
            # refreshes token if necessary
            if self.g_social_auth.access_token_expired():
                from social_django.utils import load_strategy
                access_token = self.g_social_auth.get_access_token(load_strategy())
                self.g_social_auth = refresh(self.g_social_auth)
            headers['Authorization'] = '%(token_type)s %(access_token)s' % self.g_social_auth.extra_data
        return headers

    def do_request(self, method, resource_name, resource_args=None, headers=None, params=None, data=None, json_data=None):
        method = method.lower()
        action = getattr(requests, method, None)
        if action is None:
            raise Exception('Invalid request method specified: %s' % method)
        if resource_args is None:
            resource_args = {}
        url = self.get_resource_url(resource_name, **resource_args)
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        headers.update(self.get_authorization_headers())
        response = action(url, headers=headers, params=params, data=data, json=json_data)
        return response

    def get_labels_map(self, refresh_labels=False):
        if self.labels_map is None or refresh_labels:
            self._update_labels_map()
        return self.labels_map

    def get_label_names_map(self, refresh_labels=False):
        if self.label_names_map is None or refresh_labels:
            self._update_labels_map()
        return self.label_names_map

    def _update_labels_map(self):
        labels = self.labels_list()
        self.labels_map = {
            label['name'] : label['id']
            for label in labels
        }
        self.label_names_map = {
            label['id'] : label['name']
            for label in labels
        }

    ##
    # Users.drafts
    # https://developers.google.com/gmail/api/v1/reference/#Users.drafts

    ##
    # Users.history
    # https://developers.google.com/gmail/api/v1/reference/#Users.history

    ##
    # User.labels
    # https://developers.google.com/gmail/api/v1/reference/#Users.labels

    def labels_list(self):
        """https://developers.google.com/gmail/api/v1/reference/users/labels/list
        """
        resource_name = 'labels_list'
        response = self.do_request('get', resource_name)
        if response.status_code == 200:
            response_json = response.json()
            labels = response_json['labels']
            labels = sorted(labels, key=lambda label: label['name'])
        elif response.status_code == 401:
            # unauthorized
            labels = []
        else:
            labels = []
        return labels

    ##
    # Users.messages
    # https://developers.google.com/gmail/api/v1/reference/#Users.messages

    def messages_list(self, q=''):
        """https://developers.google.com/gmail/api/v1/reference/users/messages/list
        """
        resource_name = 'messages_list'
        params = {}
        if q:
            params['q'] = q
        response = self.do_request('get', resource_name, params=params)
        if response.status_code == 200:
            response_json = response.json()
            messages = response_json.get('messages', [])
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            messages = []
        else:
            messages = []
        return messages

    def message_get(self, message_id, params=None):
        """https://developers.google.com/gmail/api/v1/reference/users/messages/get
        """
        resource_name = 'message_get'
        if params is None:
            params = {}
        resource_args = {
            'message_id' : message_id,
        }
        response = self.do_request('get', resource_name, params=params, resource_args=resource_args)
        if response.status_code == 200:
            response_json = response.json()
            message = GmailMessage(self, message_id, response_json)
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            message = None
        else:
            message = None
        return message

    def message_modify(self, message_id, add_labels=None, remove_labels=None, refresh_labels=False):
        """Adds or removes labels to a message

        https://developers.google.com/gmail/api/v1/reference/users/messages/modify#python
        """
        self.get_labels_map()

        json_data = {}
        if add_labels:
            add_label_ids = [self.labels_map[label] for label in add_labels]
            json_data['addLabelIds'] = add_label_ids
        if remove_labels:
            remove_label_ids = [self.labels_map[label] for label in remove_labels]
            json_data['removeLabelIds'] = remove_label_ids

        resource_name = 'message_modify'
        resource_args = {
            'message_id' : message_id,
        }
        response = self.do_request('post', resource_name, resource_args=resource_args, json_data=json_data)
        result = response.json()
        return result

    def message_trash(self, message_id, params=None):
        """https://developers.google.com/gmail/api/v1/reference/users/messages/trash
        """
        resource_name = 'message_trash'
        if params is None:
            params = {}
        resource_args = {
            'message_id' : message_id,
        }
        response = self.do_request('post', resource_name, params=params, resource_args=resource_args)
        if response.status_code == 200:
            response_json = response.json()
            message = GmailMessage(self, message_id, response_json)
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            message = None
        else:
            message = None
        return message

    def message_untrash(self, message_id, params=None):
        """https://developers.google.com/gmail/api/v1/reference/users/messages/untrash
        """
        resource_name = 'message_untrash'
        if params is None:
            params = {}
        resource_args = {
            'message_id' : message_id,
        }
        response = self.do_request('post', resource_name, params=params, resource_args=resource_args)
        if response.status_code == 200:
            response_json = response.json()
            message = GmailMessage(self, message_id, response_json)
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            message = None
        else:
            message = None
        return message

    ##
    # Users.messages.attachments
    # https://developers.google.com/gmail/api/v1/reference/#Users.messages.attachments

    ##
    # Users.threads
    # https://developers.google.com/gmail/api/v1/reference/#Users.threads

    def threads_list(self, q=''):
        """https://developers.google.com/gmail/api/v1/reference/users/threads/list
        """
        resource_name = 'threads_list'
        params = {}
        if q:
            params['q'] = q
        response = self.do_request('get', resource_name, params=params)
        if response.status_code == 200:
            response_json = response.json()
            threads = response_json.get('threads', [])
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            threads = []
        else:
            threads = []
        return threads

    def thread_get(self, thread_id, params=None):
        """https://developers.google.com/gmail/api/v1/reference/users/threads/get
        """
        resource_name = 'thread_get'
        if params is None:
            params = {}
        resource_args = {
            'thread_id' : thread_id,
        }
        response = self.do_request('get', resource_name, params=params, resource_args=resource_args)
        if response.status_code == 200:
            response_json = response.json()
            thread = GmailThread(self, thread_id, response_json)
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            thread = None
        else:
            thread = None
        return thread

    def thread_modify(self, thread_id, add_labels=None, remove_labels=None, refresh_labels=False):
        """Adds or removes labels to a thread

        https://developers.google.com/gmail/api/v1/reference/users/threads/modify#python
        """
        self.get_labels_map()

        json_data = {}
        if add_labels:
            add_label_ids = [self.labels_map[label] for label in add_labels]
            json_data['addLabelIds'] = add_label_ids
        if remove_labels:
            remove_label_ids = [self.labels_map[label] for label in remove_labels]
            json_data['removeLabelIds'] = remove_label_ids

        resource_name = 'thread_modify'
        resource_args = {
            'thread_id' : thread_id,
        }
        response = self.do_request('post', resource_name, resource_args=resource_args, json_data=json_data)
        result = response.json()
        return result

    def thread_trash(self, thread_id, params=None):
        """https://developers.google.com/gmail/api/v1/reference/users/threads/trash
        """
        resource_name = 'thread_trash'
        if params is None:
            params = {}
        resource_args = {
            'thread_id' : thread_id,
        }
        response = self.do_request('post', resource_name, params=params, resource_args=resource_args)
        if response.status_code == 200:
            response_json = response.json()
            thread = GmailThread(self, thread_id, response_json)
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            thread = None
        else:
            thread = None
        return thread

    def thread_untrash(self, thread_id, params=None):
        """https://developers.google.com/gmail/api/v1/reference/users/threads/untrash
        """
        resource_name = 'thread_untrash'
        if params is None:
            params = {}
        resource_args = {
            'thread_id' : thread_id,
        }
        response = self.do_request('post', resource_name, params=params, resource_args=resource_args)
        if response.status_code == 200:
            response_json = response.json()
            thread = GmailThread(self, thread_id, response_json)
        elif response.status_code in (400, 401,):
            # bad request, unauthorized
            thread = None
        else:
            thread = None
        return thread

    ##
    # Users.settings
    # https://developers.google.com/gmail/api/v1/reference/#Users.settings

    ##
    # Users.settings.forwardingAddresses
    # https://developers.google.com/gmail/api/v1/reference/#Users.settings.forwardingAddresses

    ##
    # Users
    # https://developers.google.com/gmail/api/v1/reference/#Users

    ##
    # Users.settings.filters
    # https://developers.google.com/gmail/api/v1/reference/#Users.settings.filters

    ##
    # Users.settings.sendAs
    # https://developers.google.com/gmail/api/v1/reference/#Users.settings.sendAs


class GmailMessage(object):
    def __init__(self, api, message_id, message_data):
        self.api = api
        self.message_id = message_id
        self.message_data = message_data

    def json_encode(self):
        data = {
            'id' : self.message_id,
            'date' : self.date,
            'sender' : self.sender,
            'subject' : self.subject,
            'snippet' : self.snippet,
            'labels' : self.labels,
            'html' : self.get_html(),
        }
        return data

    def get_html(self):
        """Returns the HTML part of a message from the API

        https://developers.google.com/gmail/api/v1/reference/users/messages/get
        """
        content_type = self.content_type
        #is_multipart_alternative = content_type == 'multipart/alternative'
        #is_multipart_mixed = content_type = 'multipart/mixed'

        html_part = None
        payload = self.message_data['payload']

        def _extract_html_part(parts):
            # extract the HTML part out of a multipart email
            # examine each part and check the `mimeType`
            html_part = None
            for part in parts:
                mime_type = part['mimeType']
                has_nested_parts = 'parts' in part

                if mime_type == 'text/html':
                    html_part = part
                elif mime_type == 'multipart/alternative' and has_nested_parts:
                    nested_parts = part['parts']
                    html_part = _extract_html_part(nested_parts)
                else:
                    pass

                if html_part is not None:
                    break
            return html_part

        if 'parts' in payload:
            # multipart email
            html_part = _extract_html_part(payload['parts'])
        else:
            # regular email, assume just one part
            html_part = payload

        if html_part:
            message_body_data = html_part['body']['data']
            message_html = b64decode(message_body_data.replace('-', '+').replace('_', '/'))
        else:
            message_html = None

        return message_html

    def get_text(self):
        """Returns the text part of the message from the API

        https://developers.google.com/gmail/api/v1/reference/users/messages/get
        """
        content_type = self.content_type
        #is_multipart_alternative = content_type == 'multipart/alternative'
        #is_multipart_mixed = content_type = 'multipart/mixed'

        html_part = None
        payload = self.message_data['payload']

        def _extract_text_part(parts):
            # extract the HTML part out of a multipart email
            # examine each part and check the `mimeType`
            text_part = None
            for part in parts:
                mime_type = part['mimeType']
                has_nested_parts = 'parts' in part

                if mime_type == 'text/plain':
                    text_part = part
                elif mime_type == 'multipart/alternative' and has_nested_parts:
                    nested_parts = part['parts']
                    text_part = _extract_text_part(nested_parts)
                else:
                    pass

                if text_part is not None:
                    break
            return text_part

        if 'parts' in payload:
            # multipart email
            text_part = _extract_text_part(payload['parts'])
        else:
            # regular email, assume just one part
            text_part = payload

        if text_part:
            message_body_data = text_part['body']['data']
            message_text = b64decode(message_body_data.replace('-', '+').replace('_', '/'))
        else:
            # fallback to HTML
            message_text = self.get_html()

        return message_text

    ##
    # Computed Properties

    @property
    def headers(self):
        headers = self.message_data.get('payload', {}).get('headers', [])
        return headers

    @property
    def date(self):
        date = int(self.message_data.get('internalDate'))
        return date

    @property
    def content_type(self):
        content_type = None
        for header in self.headers:
            if header['name'] == 'Content-Type':
                content_type = header['value']
                break
        return content_type

    @property
    def sender(self):
        sender = None
        for header in self.headers:
            if header['name'] == 'From':
                sender = header['value']
                break
        return sender

    @property
    def sender_name(self):
        sender = self.sender
        name = sender
        if sender:
            gre = Re()
            gre.match(r'(.*) <(.*)>', sender)
            if gre.last_match:
                name = gre.last_match.group(1)
                # strip off quotes around sender name
                gre.match(r'"(.*)"', name)
                if gre.last_match:
                    name = gre.last_match.group(1)
            else:
                pass
        return name

    @property
    def sender_email(self):
        sender = self.sender
        email = sender
        if sender:
            gre = Re()
            gre.match(r'(?:.*) <(.*)>', sender)
            if gre.last_match:
                email = gre.last_match.group(1)
            else:
                pass
        return email

    @property
    def reply_to(self):
        sender = None
        for header in self.headers:
            if header['name'] == 'Reply-To':
                sender = header['value']
                break
        return sender

    @property
    def reply_to_name(self):
        reply_to = self.reply_to
        name = reply_to
        if reply_to:
            gre = Re()
            gre.match(r'(.*) <(.*)>', reply_to)
            if gre.last_match:
                name = gre.last_match.group(1)
                # strip off quotes around reply_to name
                gre.match(r'"(.*)"', name)
                if gre.last_match:
                    name = gre.last_match.group(1)
            else:
                pass
        return name

    @property
    def reply_to_email(self):
        reply_to = self.reply_to
        email = reply_to
        if reply_to:
            gre = Re()
            gre.match(r'(?:.*) <(.*)>', reply_to)
            if gre.last_match:
                email = gre.last_match.group(1)
            else:
                pass
        return email

    @property
    def subject(self):
        subject = None
        for header in self.headers:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        return subject

    @property
    def snippet(self):
        snippet = self.message_data['snippet']
        return snippet

    @property
    def labels(self):
        label_names_map = self.api.get_label_names_map()
        labels = [label_names_map[label_id] for label_id in self.message_data['labelIds']]
        return labels

    ##
    # Labels

    def change_labels(self, add_labels=None, remove_labels=None):
        result = self.api.message_modify(self.message_id, add_labels=add_labels, remove_labels=remove_labels)
        return result

    def add_labels(self, labels):
        return self.change_labels(add_labels=labels)

    def remove_labels(self, labels):
        return self.change_labels(remove_labels=labels)

    def archive(self):
        return self.remove_labels(['INBOX',])

    def move_to_inbox(self):
        return self.add_labels(['INBOX',])

    def mark_read(self):
        return self.remove_labels(['UNREAD',])

    def mark_unread(self):
        return self.add_labels(['UNREAD',])

    def trash(self):
        result = self.api.message_trash(self.message_id)
        return result

    def untrash(self):
        result = self.api.message_untrash(self.message_id)
        return result


class GmailThread(object):
    def __init__(self, api, thread_id, thread_data):
        self.api = api
        self.thread_id = thread_id
        self.thread_data = thread_data

    def json_encode(self, inflate_messages=False):
        data = {
            'id' : self.thread_id,
            'num_messages' : self.num_messages,
            'last_message' : {
                'date' : self.last_message.date,
                'sender' : self.last_message.sender,
                'subject' : self.last_message.subject,
                'snippet' : self.last_message.snippet,
                'labels' : self.last_message.labels,
            },
        }
        if inflate_messages:
            data['messages'] = [message.json_encode() for message in self.messages]
        return data

    @CachedAttribute
    def num_messages(self):
        num_messages = len(self.thread_data['messages'])
        return num_messages

    @CachedAttribute
    def last_message(self):
        last_message_id = self.thread_data['messages'][-1]['id']
        message = self.api.message_get(last_message_id)
        return message

    @property
    def messages(self):
        messages = [
            self.api.message_get(m['id'])
            for m
            in self.thread_data['messages']
        ]
        return messages

    ##
    # Labels

    def change_labels(self, add_labels=None, remove_labels=None):
        result = self.api.thread_modify(self.thread_id, add_labels=add_labels, remove_labels=remove_labels)
        return result

    def add_labels(self, labels):
        return self.change_labels(add_labels=labels)

    def remove_labels(self, labels):
        return self.change_labels(remove_labels=labels)

    def archive(self):
        return self.remove_labels(['INBOX',])

    def move_to_inbox(self):
        return self.add_labels(['INBOX',])

    def mark_read(self):
        return self.remove_labels(['UNREAD',])

    def mark_unread(self):
        return self.add_labels(['UNREAD',])
