'''
Definitions about HTML BBS elements.
'''
import logging
import time
import requests
from bs4 import BeautifulSoup
import datetime_helper

LOGGER = logging.getLogger('.'.join(['crawler', __name__]))


class AbstractPage:
    """description of class"""

    PTT_URL = 'https://www.ptt.cc'

    def __init__(self):
        self.url = None
        self.set_url()

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
        self.url = None
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
            self.dom = BeautifulSoup(page, 'html.parser')
        else:
            self.dom = None

    def find_prev_page_url(self):
        '''Find URL of previous page.'''
        if not self.dom:
            LOGGER.error('No content for parsing previous page link.')
            raise ValueError

        div_paging = self.dom.find('div', 'btn-group btn-group-paging')

        # 0: earliest, 1: previous, 2: next, 3: latest
        btn_prev_page = div_paging.find_all('a')[1]

        if btn_prev_page['href']:
            self.url = btn_prev_page['href']
            return

        LOGGER.info('No previous page link found.')
        self.url = None

    def get_articles_meta(self):
        '''Retrieve meta for all articles in current page.'''

        # not to retrieve delete article which looks like
        # <div class="title"> (本文已被刪除) [author] </div>
        return [
            self._get_article_meta(article_block)
            for article_block in self._get_article_blocks()
            if article_block.find('a')
        ]

    def _get_article_blocks(self):
        '''Get all blocks that contain article meta.'''
        dom = self.dom
        if not dom:
            LOGGER.error('No content for parsing article blocks.')
            raise ValueError

        # articles under separation (aka pinned posts) should be ignored
        list_sep = dom.find('div', 'r-list-sep')

        if self.latest_page:
            if list_sep:
                article_blocks = list_sep.find_all_previous('div', 'r-ent')
                # reserve to the original order
                article_blocks = article_blocks[::-1]

            self.latest_page = False
        else:
            article_blocks = dom.find_all('div', 'r-ent')

        return article_blocks

    def _get_article_meta(self, dom):
        '''Get article meta in precise DOM area.'''
        prop_a = dom.find('a')
        article_meta = {}

        article_meta['title'] = prop_a.text
        article_meta['href'] = prop_a['href']
        # date format mm/dd and prefix for m is space instead of 0
        article_meta['date'] = dom.find('div', 'date').text.lstrip()
        article_meta['author'] = dom.find('div', 'author').text

        return article_meta

    def remove_expired(self, articles_meta):
        '''Remove data in dates which is expired.'''
        count = len(articles_meta)

        while articles_meta:
            article_date = articles_meta[0]['date']
            if datetime_helper.check_expired(article_date, self.term_date):
                articles_meta.pop(0)
            else:
                break

        if count > len(articles_meta):
            LOGGER.info('Term date reached.')
            self.set_url()

        return articles_meta


_AUTHOR = '作者'
_BOARD = '看板'
_TITLE = '標題'
_TIME = '時間'


def _combine(key, value):
    '''A helper function to combine key-value pair'''
    return '  '.join([key, value])


class Article(AbstractPage):
    """description of class"""

    def __init__(self, board_name, **meta):
        super().__init__()
        self.board_name = board_name
        self.url = None
        self.set_url(meta['href'])
        self.meta = meta
        self.dom = None

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.meta!r})'

    def _get_content(self, page):
        '''Get complete article content.'''
        if page:
            soup = BeautifulSoup(page, 'html.parser')
            self.dom = soup.find(id='main-content')
        else:
            self.dom = None

    def format_article(self):
        '''Get complete article content.'''
        dom = self.dom
        if not dom:
            LOGGER.error('No content for parsing article.')
            raise ValueError

        _, sep, after = dom.text.partition('\n')
        create_time = self._get_create_time()
        LOGGER.debug(
            'Article [%s](%s) created at [%s]',
            self.meta['title'],
            self.url,
            create_time)

        contents = []
        contents.append(_combine(_AUTHOR, self.meta['author']))
        contents.append(_combine(_BOARD, self.board_name))
        contents.append(_combine(_TITLE, self.meta['title']))
        contents.append(_combine(_TIME, create_time) + '\n\n')
        contents.append(after)

        return sep.join(contents)

    def _get_create_time(self):
        '''Get create time of this article.'''
        dom = self.dom
        if not dom:
            LOGGER.error('No content for parsing create time.')
            raise ValueError

        metalines = dom.find_all('div', 'article-metaline')
        return next(
            (metaline.find('span', 'article-meta-value').text
             for metaline in metalines
             if metaline.find('span', 'article-meta-tag').text == _TIME),
            None
        )
