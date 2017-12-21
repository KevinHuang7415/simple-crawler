'''
Helper functions for file operations.
'''

import sys
import time

import requests
from bs4 import BeautifulSoup

import file_helper
import datetime_helper

PTT_URL = 'https://www.ptt.cc'
SOFTJOB_URI = '/bbs/Soft_Job/index.html'
LATEST_PAGE = True


def setup_path():
    '''Set path for saving files.'''
    dir_path = file_helper.get_dir(sys.argv)
    file_helper.create_dir_if_not_exist(dir_path)

def crawler():
    '''Grab all articles in recent days.'''
    curr_page_url = SOFTJOB_URI

    while curr_page_url:
        board_page = get_web_page(curr_page_url, 0)

        if board_page:
            curr_page_url, articles_meta = get_articles_meta(board_page)
            global LATEST_PAGE
            LATEST_PAGE = False

            for article_meta in articles_meta:
                article = get_article_content(article_meta['href'])
                save_article(article, article_meta)

def get_web_page(url, t=0.4):
    '''Get web page content.'''
    # to avoid being detected as DDOS
    time.sleep(t)

    resp = requests.get(PTT_URL + url)
    if resp.status_code == 200:
        return resp.text
    print('Invalid URL:', resp.url)
    return None

def get_articles_meta(dom):
    '''Retrieve meta for all articles in current page.'''

    def remove_expired(articles_meta):
        '''Remove data in dates which are expired.'''
        while articles_meta:
            if datetime_helper.check_expired(articles_meta[0]['date']):
                articles_meta.pop(0)
            else:
                break

        return articles_meta

    def get_article_meta(dom):
        '''Get article meta.'''
        prop_a = dom.find('a')

        if prop_a:
            href = prop_a['href']
            title = prop_a.text
            # date format mm/dd and prefix for m is space instead of 0
            date = dom.find('div', 'date').text.strip()
            return title, href, date
        return None, None, None

    def find_prev_page_url(dom):
        '''Find URL of previous page.'''
        div_paging = dom.find('div', 'btn-group btn-group-paging')
        # 0: earliest, 1: previous, 2: next, 3: latest
        btn_prev_page = div_paging.find_all('a')[1]

        if btn_prev_page['href']:
            return btn_prev_page['href']
        return None


    soup = BeautifulSoup(dom, 'html.parser')

    # articles under separation (aka pinned posts) should be ignored
    list_sep = soup.find('div', 'r-list-sep')
    global LATEST_PAGE
    if LATEST_PAGE and list_sep:
        divs = list_sep.find_all_previous('div', 'r-ent')
        # reserve to the original order
        divs = divs[::-1]
    else:
        divs = soup.find_all('div', 'r-ent')

    articles_meta = []
    for div in divs:
        title, href, date = get_article_meta(div)
        # to avoid situation like <div class="title"> (本文已被刪除) [author] </div>
        if href:
            articles_meta.append({
                'title': title,
                'href': href,
                'date': date
            })

    if datetime_helper.check_expired(articles_meta[0]['date']):
        articles_meta = remove_expired(articles_meta[1:])
        return None, articles_meta

    prev_page_url = find_prev_page_url(soup)
    return prev_page_url, articles_meta

def get_article_content(url):
    '''Get complete article content.'''
    article_page = get_web_page(url)
    if article_page:
        soup = BeautifulSoup(article_page, 'html.parser')
        article = soup.find(id='main-content')
        return article.text
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

