# Python Standard Library Imports
import re
import urllib

# Third Party (PyPI) Imports
import requests
import rollbar

# Django Imports
from django.conf import settings

# HTK Imports
from htk.lib.google.youtube.constants import GOOGLE_APIS_YOUTUBE_VIDEOS_URL


def extract_youtube_video_id(youtube_video_url):
    try:
        # Ref to build regex: https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486
        re_match = re.search(
            r'(?:v=|youtu\.be\/|\/v\/|\/e\/|\/watch\?v=|\/watch\?si=|\/watch\?|\/shorts\/)([0-9A-Za-z_-]+)',
            youtube_video_url,
        )
    except Exception as e:
        youtube_video_id = None
        rollbar.report_message(
            'Failed to extract video ID from YouTube URL',
            extra_data={
                'video_url': youtube_video_url,
                'error': f'{e}',
            },
        )
    else:
        youtube_video_id = re_match.group(1) if re_match else None

    return youtube_video_id


def build_youtube_api_url(youtube_video_id):
    query = urllib.parse.urlencode(
        {
            'id': youtube_video_id,
            'part': 'contentDetails',
            'key': settings.HTK_GOOGLE_SERVER_API_KEY[0],
        }
    )
    url = f'{GOOGLE_APIS_YOUTUBE_VIDEOS_URL}?{query}'

    return url


def get_youtube_video_duration(youtube_video_url):
    duration = None
    try:
        youtube_video_id = extract_youtube_video_id(youtube_video_url)
        api_url = build_youtube_api_url(youtube_video_id)

        response = requests.get(api_url)
        data = response.json()
    except Exception as e:
        rollbar.report_message(
            'Failed to fetch YouTube video duration',
            extra_data={
                'video_url': youtube_video_url,
                'error': f'{e}',
            },
        )
    else:
        if 'items' in data and len(data['items']) > 0:
            duration = data['items'][0]['contentDetails']['duration']
        else:
            rollbar.report_message(
                'Failed to get expected API response for the video url',
                extra_data={
                    'video_url': youtube_video_url,
                    'response_data': data,
                },
            )

    return duration
