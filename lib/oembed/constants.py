SLIDESHARE_URL_REGEXP = r'https?://(?:www\.)?slideshare\.(?:com|net)/.*'
VIMEO_URL_REGEXP = r'https?://(?:www\.)?vimeo\.com/.*'
YOUTUBE_URL_REGEXP = r'https?://(?:(www\.)?youtube\.com|youtu\.be)/.*'

OEMBED_BASE_URLS = {
    'slideshare' : 'http://www.slideshare.net/api/oembed/2?url=%s',
    'vimeo' : 'http://vimeo.com/api/oembed.json?url=%s&maxwidth=400&maxheight=350',
    'youtube' : 'http://www.youtube.com/oembed?url=%s&format=json',
}
