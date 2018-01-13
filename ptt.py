'''
Definitions about HTML BBS elements.
'''
import logging
import time
import requests
import datetimehelper as dh
import domparser as op

LOGGER = logging.getLogger('.'.join(['crawler', __name__]))


class AbstractPage:
    """description of class"""

    PTT_URL = 'https://www.ptt.cc'

    def __init__(self):
        self.url = None

    def __repr__(self):
        return f'{self.__class__.__name__}('')'

    def set_url(self, uri=None):
        '''Setup the URL with full uri.'''
        self.url = uri

    def retrieve_dom(self, sleep_time=0.4):
        '''Retrieve DOM from URL.'''
        page = self._get_web_page(sleep_time)
        self._get_content(page)

    def _get_web_page(self, sleep_time=0.4):
        '''Get web page content.'''
        if not self.url:
            LOGGER.error('URL is not set.')
            raise ValueError

        # to avoid being detected as DDOS
        time.sleep(sleep_time)
        resp = requests.get(self.PTT_URL + self.url)

        if resp.status_code == 200:
            return resp.text

        LOGGER.warning(
            'Invalid URL:[%s] , status code [%d]',
            resp.url,
            resp.status_code
        )
        return None

    def _get_content(self, page):
        raise NotImplementedError


class Board(AbstractPage):
    """description of class"""

    def __init__(self, board_name, term_date=10):
        super().__init__()
        self.board_name = board_name
        self.set_url(board_name)
        self.term_date = term_date
        self.latest_page = True
        self.dom = None

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.board_name!r}, \
{self.term_date!r}, {self.url!r}, {self.latest_page!r})'
        )

    def set_url(self, uri=None):
        '''Setup the URL with board name.'''
        if uri:
            self.url = '/'.join(['/bbs', uri, 'index.html'])
        else:
            self.url = None

    def _get_content(self, page):
        '''Transfer HTML content to BeautifulSoup object'''
        if page:
            self.dom = op.get_board_content(page)
        else:
            self.dom = None

    def find_prev_page_url(self):
        '''Find URL of previous page.'''
        dom = self.dom
        if not dom:
            LOGGER.error('No content for parsing previous page link.')
            raise ValueError

        self.url = op.find_prev_page_url(dom)
        if not self.url:
            LOGGER.info('No previous page link found.')

    def get_articles_meta(self):
        '''Retrieve meta for all articles in current page.'''
        dom = self.dom
        if not dom:
            LOGGER.error('No content for parsing article blocks.')
            raise ValueError

        articles_meta = op.get_articles_meta(dom, self.latest_page)
        self.latest_page = False

        before_remove = len(articles_meta)

        while articles_meta:
            article_date = articles_meta[0]['date']
            if dh.check_expired(article_date, self.term_date):
                articles_meta.pop(0)
            else:
                break

        if before_remove > len(articles_meta):
            LOGGER.info('Term date reached.')
            self.set_url()

        return articles_meta


class Article(AbstractPage):
    """description of class"""

    def __init__(self, board_name, **meta):
        super().__init__()
        self.board_name = board_name
        self.set_url(meta['href'])
        self.meta = meta
        self.dom = None

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.meta!r})'

    def _get_content(self, page):
        '''Get complete article content.'''
        if page:
            self.dom = op.get_article_content(page)
        else:
            self.dom = None

    def format_article(self):
        '''Get complete article content.'''
        dom = self.dom
        if not dom:
            LOGGER.error('No content for parsing article.')
            raise ValueError

        result = op.parse_article(dom)

        # both create_time and last_edit_time will not be None at same time
        if not result['last_edit_time']:
            result['last_edit_time'] = result['create_time']
        elif not result['create_time']:
            result['create_time'] = dh.to_full_datetime(self.meta['date'])

        return result['content']
