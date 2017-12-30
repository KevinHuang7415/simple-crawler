import time
import requests
import datetime_helper

class Page:
    """description of class"""

    PTT_URL = 'https://www.ptt.cc'

    def __init__(self):
        self.set_url(use_join=True)


    def __str__(self):
        return str(self.url)


    def set_url(self, uri=None, use_join=False):
        '''Setup the URL for page.'''
        if not use_join:
            self.url = uri
        else:
            if uri:
                self.url = '/'.join(['/bbs', uri, 'index.html'])
            else:
                self.url = '/bbs/index.html'


    def get_web_page(self, t=0.4):
        '''Get web page content.'''
        if not self.url:
            print('URL is not set.')
            raise ValueError

        # to avoid being detected as DDOS
        time.sleep(t)
        resp = requests.get(self.PTT_URL + self.url)

        if resp.status_code == 200:
            return resp.text
        print('Invalid URL:', resp.url)
        return None


from bs4 import BeautifulSoup


class Board(Page):
    """description of class"""

    def __init__(self, board_name, term_date=10):
        self.board_name = board_name
        self.set_url(board_name, True)
        self.term_date = term_date
        self.latest_page = True
        self.get_dom()


    def __str__(self):
        return str(self.board_name)

    
    def get_dom(self):
        '''Retrieve DOM from URL.'''
        resp = self.get_web_page(0)
        self.page_to_soup(resp)


    def page_to_soup(self, page):
        '''Transfer HTML content to BeautifulSoup object'''
        if page:
            self.dom = BeautifulSoup(page, 'html.parser')
        else:
            self.dom = None


    def find_prev_page_url(self):
        '''Find URL of previous page.'''
        if not self.dom:
            print('No content for parsing.')
            raise ValueError

        div_paging = self.dom.find('div', 'btn-group btn-group-paging')

        # 0: earliest, 1: previous, 2: next, 3: latest
        btn_prev_page = div_paging.find_all('a')[1]

        if btn_prev_page['href']:
            return btn_prev_page['href']
        return None


    def get_articles_meta(self):
        '''Retrieve meta for all articles in current page.'''
        article_blocks = self.get_article_blocks()

        # not to retrieve delete article which looks like
        # <div class="title"> (本文已被刪除) [author] </div>
        return [
            self.get_article_meta(article_block)
            for article_block in article_blocks
            if article_block.find('a')
        ]


    def get_article_blocks(self):
        '''Get all blocks that contain article meta.'''
        dom = self.dom
        if not dom:
            print('No content for parsing.')
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


    def get_article_meta(self, dom):
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
            self.set_url()

        return articles_meta
