'''
Helper functions for file operations.
'''

import sys
import time

import requests
from bs4 import BeautifulSoup

import datetime_helper
import file_helper
import ptt

PTT_URL = 'https://www.ptt.cc'
BOARD_NAME = 'Soft_Job'

AUTHOR = '作者'
BOARD = '看板'
TITLE = '標題'
TIME = '時間'


def setup_path():
    '''Set path for saving files.'''
    dir_path = file_helper.get_dir(sys.argv)
    file_helper.create_dir_if_not_exist(dir_path)


def crawler():
    '''Grab all articles in recent days.'''
    board = ptt.Board(BOARD_NAME, 5)

    while board.url:
        board.get_dom()
        articles_meta = parse_board(board)

        for article_meta in articles_meta:
            article = get_article_content(article_meta)
            save_article(article, article_meta)


def parse_board(board):
    if not board:
        return None

    board.find_prev_page_url()
    articles_meta = board.get_articles_meta()
    return board.remove_expired(articles_meta)


def get_web_page(url, t=0.4):
    '''Get web page content.'''
    # to avoid being detected as DDOS
    time.sleep(t)
    resp = requests.get(PTT_URL + url)

    if resp.status_code == 200:
        return resp.text
    print('Invalid URL:', resp.url)
    return None


def get_article_content(article_meta):
    '''Get complete article content.'''

    def get_create_time(dom):
        metalines = dom.find_all('div', 'article-metaline')

        for metaline in metalines:
            article_meta_tag = metaline.find('span', 'article-meta-tag')

            if article_meta_tag.text == TIME:
                return metaline.find('span', 'article-meta-value').text

        return None # TODO gen_date

    def combine(prefix, meta):
        return '  '.join([prefix, meta])

    def format_article(dom):
        before, sep, after = dom.text.partition('\n')
        create_time = get_create_time(dom)

        meta = []
        meta.append(combine(AUTHOR, article_meta['author']))
        meta.append(combine(BOARD, BOARD_NAME))
        meta.append(combine(TITLE, article_meta['title']))
        meta.append(combine(TIME, create_time) + '\n\n')
        meta.append(after)

        return sep.join(meta)

    article_page = get_web_page(article_meta['href'])

    if article_page:
        soup = BeautifulSoup(article_page, 'html.parser')
        article = soup.find(id='main-content')
        return format_article(article)

    return None


def save_article(article, meta):
    '''Save cached article to file.'''
    if article:
        # to avoid the titles collision
        # format PTT_URL/..../M.number.A.RND.html, take the number part
        title_id = meta['href'].split('/')[-1].split('.')[1]
        title = ' - '.join([meta['date'], meta['title'], title_id])
        dir_path = file_helper.get_dir(sys.argv)
        file_helper.write_article(article, title, dir_path)


def main():
    '''Main function.'''
    setup_path()
    crawler()


if __name__ == '__main__':
    main()
