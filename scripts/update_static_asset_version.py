"""
Update the StaticAssetVersionCache value

This script is invoked after a deploy, to ensure that visitors to the website won't have stale versions of CSS and JavaScript files in their browser cache
"""
import script_config

from htk.utils import utcnow
from htk.cachekeys import StaticAssetVersionCache
from htk.scripts.utils import job_runner
from htk.scripts.utils import slog

def main():
    # use date as asset_version because it is unique at the time of deploy
    now = utcnow()
    asset_version = now.strftime('%Y%m%d%H%M%S')
    slog('New asset version: %s' % asset_version)
    c = StaticAssetVersionCache()
    c.cache_store(asset_version)

if __name__ == '__main__':
    job_runner(main)
