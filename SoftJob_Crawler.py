import sys
import time

import requests
from bs4 import BeautifulSoup

import file_helper

PTT_URL = 'https://www.ptt.cc'
SOFTJOB_URI = '/bbs/Soft_Job/index.html'
LATEST_PAGE = True
DIR = ''


def set_data_path():
    global DIR
    DIR = file_helper.get_dir(sys.argv)
    file_helper.create_dir_if_not_exist(DIR)

def crawler():
    curr_page_url = PTT_URL + SOFTJOB_URI

    board_page = get_web_page(curr_page_url)
    if board_page:
        articles_meta = get_articles_meta(board_page)
        LATEST_PAGE = False

        for article_meta in articles_meta:
            article = get_article_content(PTT_URL + article_meta['href'])
            if article:
                global DIR
                file_helper.write_article(article, article_meta['title'], DIR)

def get_web_page(url):
    # to avoid being detected as DDOS
    time.sleep(0.5)  

    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid URL:', resp.url)
        return None
    else:
        return resp.text

def get_articles_meta(dom):
    soup = BeautifulSoup(dom, 'html.parser')


    def find_prev_page_url(soup):
        div_paging = soup.find('div', 'btn-group btn-group-paging')
        # 0: earliest, 1: previous, 2: next, 3: latest
        btn_prev_page = div_paging.find_all('a')[1]
    
        if 'href' in btn_prev_page.attrs:
            return btn_prev_page['href']
        else:
            return None

    prev_page_url = find_prev_page_url(soup)

    # articles under separation (aka pinned posts) should be ignored
    list_sep = soup.find('div', 'r-list-sep')
    if LATEST_PAGE and list_sep:
        divs = list_sep.find_all_previous('div', 'r-ent')
        # reserve to the original order
        divs = divs[::-1]
    else:
        divs = soup.find_all('div', 'r-ent')


    def get_article_meta(dom):
        prop_a = dom.find('a')

        if prop_a:
            href = prop_a['href']
            title = prop_a.string

            # date format mm/dd and prefix for m is space instead of 0
            date = dom.find('div', 'date').string.strip()
            return title, href, date
        else:
            return None, None, None

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

    return articles_meta

def get_article_content(url):
    article_page = get_web_page(url)
    if article_page:
        soup = BeautifulSoup(article_page, 'html.parser')
        article = soup.find(id='main-content')
        return article.prettify()
    else:
        return None

def main():
    set_data_path()
    crawler()

if __name__ == '__main__':
    main()
