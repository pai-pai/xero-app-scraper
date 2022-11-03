"""Scrapy settings for xero project

"""

BOT_NAME = 'xero'

SPIDER_MODULES = ['xero.spiders']
NEWSPIDER_MODULE = 'xero.spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
   'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
              'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
   'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/15.6 Safari/605.1.15'),
   'Upgrade-Insecure-Requests': '1',
}
USER_AGENTS = [
   ('Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 '
    '(KHTML, like Gecko) Version/15.6 Safari/605.1.15'),
]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
    'xero.middlewares.XeroDownloaderMiddleware': 950,
}

LOG_ENABLED = True
LOG_FILE = 'logs.log'
LOG_FILE_APPEND = 'False'
LOG_LEVEL = 'DEBUG'

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

COOKIES_ENABLED = False
