import sys

import requests
from bs4 import BeautifulSoup

import file_helper

PTT_URL = 'https://www.ptt.cc'
SOFTJOB_URI = '/bbs/Soft_Job/index.html'
DIR = ''

def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid URL:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom):
    soup = BeautifulSoup(dom, 'html.parser')

    # articles under separation (aka pinned posts) should be ignored
    list_sep = soup.find('div', 'r-list-sep')
    divs = list_sep.find_all_previous('div', 'r-ent')

    # reserve to the original order
    divs = divs[::-1]
    article_links = []
    for div in divs:
        # to avoid situation like <div class="title"> (本文已被刪除) [author] </div>
        if div.find('a'):
            href = div.find('a')['href']
            title = div.find('a').string
            article_links.append({
                'title': title,
                'href': href,
            })
    return article_links


def main():
    DIR = file_helper.get_dir(sys.argv)
    file_helper.create_dir_if_not_exist(DIR)

    board_page = get_web_page(PTT_URL + SOFTJOB_URI)
    if board_page:
        article_links = get_articles(board_page)

        article_meta = article_links[-1]
        article_page = get_web_page(PTT_URL + article_meta['href'])
        if article_page:
            soup = BeautifulSoup(article_page, 'html.parser')
            article = soup.find(id='main-content')
            file_helper.write_article(article.prettify(), article_meta['title'], DIR)

if __name__ == '__main__':
    main()
