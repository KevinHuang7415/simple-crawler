'''
Operations on DOM which parsed by BeautifulSoup.
'''
from bs4 import BeautifulSoup

_TIME = '時間'


def get_board_content(page):
    '''Get complete article content'''
    return BeautifulSoup(page, 'html.parser')


def get_article_content(page):
    '''Get complete article content.'''
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find(id='main-content')


def find_prev_page_url(board_dom):
    '''Find URL of previous page.'''
    div_paging = board_dom.find('div', 'btn-group btn-group-paging')
    # 0: earliest, 1: previous, 2: next, 3: latest
    btn_prev_page = div_paging.find_all('a')[1]
    return btn_prev_page['href']


def get_article_blocks(board_dom, latest_page):
    '''Get all blocks that contain article meta.'''
    # articles under separation (aka pinned posts) should be ignored
    list_sep = board_dom.find('div', 'r-list-sep')

    if latest_page:
        if list_sep:
            article_blocks = list_sep.find_all_previous('div', 'r-ent')
            # reserve to the original order
            article_blocks = article_blocks[::-1]
    else:
        article_blocks = board_dom.find_all('div', 'r-ent')

    return article_blocks


def get_article_meta(article_block):
    '''Get article meta.'''
    prop_a = article_block.find('a')
    article_meta = {}

    article_meta['title'] = prop_a.text
    article_meta['href'] = prop_a['href']
    # date format mm/dd and prefix for m is space instead of 0
    article_meta['date'] = article_block.find('div', 'date').text.lstrip()
    article_meta['author'] = article_block.find('div', 'author').text

    return article_meta


def get_create_time(article_dom):
    '''Get create time of this article.'''
    metalines = article_dom.find_all('div', 'article-metaline')
    return next(
        (metaline.find('span', 'article-meta-value').text
         for metaline in metalines
         if metaline.find('span', 'article-meta-tag').text == _TIME),
        None
    )
