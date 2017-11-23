OEMBED_URL_SCHEME_REGEXPS = {
    'slideshare' : r'https?://(?:www\.)?slideshare\.(?:com|net)/.*',
    'soundcloud' : r'https?://soundcloud.com/.*',
    'vimeo' : r'https?://(?:www\.)?vimeo\.com/.*',
    'youtube' : r'https?://(?:(www\.)?youtube\.com|youtu\.be)/.*',
}

OEMBED_BASE_URLS = {
    'slideshare' : 'https://www.slideshare.net/api/oembed/2?url=%(url)s',
    'soundcloud' : 'https://soundcloud.com/oembed?url=%(url)s&format=json',
    'vimeo' : 'https://vimeo.com/api/oembed.json?url=%(url)s&maxwidth=400&maxheight=350',
    'youtube' : 'https://www.youtube.com/oembed?url=%(url)s&format=json',
}
