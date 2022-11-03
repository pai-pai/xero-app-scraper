"""Module contains next spiders:

AppApiSpider -- to collect app links and some app data,
AppDetailsSpider -- to get ommited in API data.

"""
import pathlib
import scrapy


DOMAIN = "apps.xero.com"

APP_LINKS_FILE = pathlib.Path('app_links.csv')
APP_DETAILS_FILE = pathlib.Path('app_details.csv')


class AppApiSpider(scrapy.Spider):
    """Spider which collects start urls for AppDetailsSpider.
    Also it gets some of app's data:
    - Name of app
    - Appstore URL
    - App URL
    - Reviews
    - Reviews score
    - Categories

    """
    name = "app-api-spider"
    domain = DOMAIN
    allowed_domains = [domain]
    custom_settings = {
        'FEEDS': {
            APP_LINKS_FILE: {
                'format': 'csv',
                'overwrite': True,
                'fields': [
                    'name', 'appstore_url', 'app_url', 'reviews',
                    'reviews_score', 'categories',
                ]
            }
        }
    }
    apps_api_url = 'https://apps.xero.com/api/apps/uk'
    apps_url = 'https://apps.xero.com/uk/{}/{}/app/{}'
    start_urls = [apps_api_url]

    def parse(self, response, **kwargs):
        apps_json = response.json()
        for item in apps_json['items']:
            functions = item.get('functions')
            industries = item.get('industries')
            if not item['hasListing'] or not (functions or industries):
                continue
            appstore_url_params = ('function', functions[0]['id']) if functions else \
                ('industry', industries[0]['id'])
            appstore_url = self.apps_url.format(*appstore_url_params, item['slug'])
            yield {
                'name': item['name'],
                'appstore_url': appstore_url,
                'app_url': item['landingPageUrl'],
                'reviews': item['reviewCount'],
                'reviews_score': item['rating'],
                'categories': ', '.join([i['name'] for i in industries] +
                                        [f['name'] for f in functions]),
            }
        pagination = apps_json['pagination']
        page = pagination['page']
        page_count = pagination['pageCount']
        if page < page_count:
            page += 1
        url = f'{self.apps_api_url}?page={page}'
        yield scrapy.Request(url=url, callback=self.parse)


class AppDetailsSpider(scrapy.Spider):
    """This spider gets missed in API data:
    - Root domain
    - Added in year
    - Support email

    """
    name = "app-details-spider"
    domain = DOMAIN
    allowed_domains = [domain]
    custom_settings = {
        'FEEDS': {
            APP_DETAILS_FILE: {
                'format': 'csv',
                'overwrite': True,
                'fields': [
                    'appstore_url', 'root_domain', 'added_in_year',
                    'support_email',
                ]
            }
        }
    }

    def start_requests(self):
        with open(APP_LINKS_FILE, 'r', encoding='utf-8') as links_file:
            for index, row in enumerate(links_file):
                if index == 0:
                    continue
                row = row.replace("\n", "")
                if row:
                    url = row.split(',')[1]
                    yield scrapy.Request(f'{url}', callback=self.parse)

    def parse(self, response, **kwargs):
        root_domain = response.xpath(
            '//section[contains(@class, "mp-app-listing-header")]'
            '//div[contains(text(), "By ")]/a/@href').get()
        if root_domain:
            root_domain = root_domain.replace("https://", "").replace("http://", "")
        yield {
            'appstore_url': response.url,
            'root_domain': root_domain,
            'added_in_year': response.xpath(
                '//section[contains(text(), "Added in")]/em/text()').get(),
            'support_email': response.xpath(
                '//section[contains(h3/text(), "Support")]'
                '/a[contains(@href, "mailto")]/text()').get(),
        }
