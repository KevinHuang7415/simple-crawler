'''
Definitions about HTML BBS elements.
'''
from contextlib import suppress
import asyncio
import aiohttp
import datetimehelper as dh
import domparser as dp
import logger

LOGGER = logger.get_logger(__name__)
CLIENT = aiohttp.ClientSession(loop=asyncio.get_event_loop())


class AbstractPage(object):
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
        task = asyncio.ensure_future(self._request_page(sleep_time))

        loop = asyncio.get_event_loop()
        page = loop.run_until_complete(task)

        self._get_content(page)

    async def _request_page(self, sleep_time=0.4):
        '''Get web page content.'''
        if not self.url:
            LOGGER.error('URL is not set.')
            raise ValueError

        asyncio.sleep(sleep_time)
        try:
            async with CLIENT.get(self.PTT_URL + self.url) as resp:
                if resp.status == 200:
                    return await resp.text()

                LOGGER.warning(
                    'Invalid URL:[%s] , status code [%d]',
                    resp.url,
                    resp.status
                )
                return None
        except aiohttp.ClientError:
            LOGGER.exception('Connection error.')
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
        self.parser = None

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.board_name!r}, \
{self.term_date!r}, {self.url!r}, {self.latest_page!r})'

    @property
    def has_prev_page(self):
        '''A interface to check whether url exist.'''
        return self.url is not None

    def set_url(self, uri=None):
        '''Setup the URL with board name.'''
        if uri:
            self.url = '/'.join(['/bbs', uri, 'index.html'])
        else:
            self.url = None

    def _get_content(self, page):
        '''Transfer HTML content to BeautifulSoup object'''
        with suppress(TypeError):
            self.parser = dp.build_parser(dp.PageType.board, page)

    def find_prev_page_url(self):
        '''Find URL of previous page.'''
        try:
            self.url = self.parser.find_prev_page_url()
        except AttributeError:
            LOGGER.error('No content for parsing previous page link.')
            raise ValueError
        else:
            if not self.url:
                LOGGER.info('No previous page link found.')

    def all_articles_meta(self):
        '''Retrieve meta for all articles in current page.'''
        latest_page = self.latest_page
        try:
            article_meta_list = self.parser.all_articles_meta(latest_page)
        except AttributeError:
            LOGGER.error('No content for parsing article blocks.')
            raise ValueError

        latest_page = False

        before_remove = len(article_meta_list)

        while article_meta_list:
            article_date = article_meta_list[0]['date']
            if dh.check_expired(article_date, self.term_date):
                article_meta_list.pop(0)
            else:
                break

        if before_remove > len(article_meta_list):
            LOGGER.info('Term date reached.')
            self.set_url()

        return article_meta_list


class Article(AbstractPage):
    """description of class"""

    def __init__(self, **meta):
        super().__init__()
        self.set_url(meta['href'])
        self.meta = meta
        self.parser = None

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.meta!r})'

    def _get_content(self, page):
        '''Get complete article content.'''
        with suppress(TypeError):
            self.parser = dp.build_parser(dp.PageType.article, page)

    def parse_content(self):
        '''Get complete article content.'''
        try:
            content, create_time, last_edit_time = self.parser.parse_article()
        except AttributeError:
            LOGGER.error('No content for parsing article.')
            raise ValueError

        # both create_time and last_edit_time will not be None at same time
        if not last_edit_time:
            last_edit_time = create_time
        elif not create_time:
            create_time = dh.to_full_datetime(self.meta['date'])

        return content, dh.to_datetime(create_time),\
            dh.to_datetime(last_edit_time)


def close_session():
    '''Close aiohttp session.'''
    task = asyncio.ensure_future(CLIENT.close())
    wait_completion(task)


def wait_completion(task):
    '''Wait the async task got finished.'''
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(task)
