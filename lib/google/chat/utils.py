# Third Party (PyPI) Imports
import requests


def google_chat_webhook_call(webhook_url, payload):
    response = requests.post(webhook_url, json=payload)

    return response
