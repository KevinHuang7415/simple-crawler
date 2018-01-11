'''
Operations on DOM which parsed by BeautifulSoup.
'''
import re
from bs4 import BeautifulSoup
import datetime_helper

EDIT = '※ 編輯'
PATTERN_TIME = re.compile('時間')
PATTERN_EDIT = re.compile(EDIT)


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


def parse_article(dom):
    '''Retreive formatted content and time information of article.'''

    def get_create_time(dom):
        '''Find create time of article.'''
        has_metaline = False
        if dom.find('div', 'article-metaline'):
            has_metaline = True

            # Sun Sep  3 00:39:06 2017
            create_time = find_in_article_meta_tag(dom)
            if create_time:
                return True, create_time

        # Sun Nov 12 23:54:16 2017
        create_time = find_in_modified_metalines(dom)
        if create_time:
            return has_metaline, create_time

        # 12/26/2017 15:56:57
        create_time = find_last_in_f2(dom, '※ 轉錄者')
        if create_time:
            create_time = create_time.partition(', ')[2].strip()
            return has_metaline, datetime_helper.alt_to_full(create_time)

        return has_metaline, None

    def find_in_article_meta_tag(dom):
        '''Find article-meta-tag in page content'''
        tag = dom.find(
            lambda tag: __find_tag(tag, 'span', 'article-meta-tag') and
            PATTERN_TIME.search(tag.text)
        )
        if tag:
            return tag.next_sibling.text.strip()
        return None

    def find_in_modified_metalines(dom):
        '''Find modified metalines in page content'''
        tag = dom.find(
            lambda tag: __find_tag(tag, 'span', 'f4', 'b7') and
            PATTERN_TIME.search(tag.text)
        )
        if tag:
            return tag.next_sibling.text.strip()
        return None

    def find_last_in_f2(dom, start_str):
        '''Find last f2 tag in page content'''
        f2_startswith = lambda tag:\
            __find_tag(tag, 'span', 'f2') and tag.text.startswith(start_str)

        return next((f2.text for f2 in dom.find_all(f2_startswith)[::-1]), None)

    def get_last_edit_time(dom):
        '''Find last edit time in page content'''
        last_edit_time = find_last_in_f2(dom, EDIT)
        if last_edit_time:
            return last_edit_time.partition(', ')[2].strip()

        elements = dom.find_all(lambda tag: PATTERN_EDIT.match(tag.text))
        if not elements:
            return None

        element = elements[-1]
        after = element.text.partition(', ')[2].strip()
        if after != '':
            return after

        # very rare condition
        element = element.next_element
        return element.text.partition(', ')[2].strip()

    has_metaline, create_time = get_create_time(dom)
    # 09/03/2017 00:39:26
    last_edit_time = get_last_edit_time(dom)
    if last_edit_time:
        last_edit_time = datetime_helper.alt_to_full(last_edit_time)

    if has_metaline:
        metalines = []
        # all metalines contain in one line in original text,
        # separate them manually
        for meta_tag in dom.find_all('span', 'article-meta-tag'):
            line = '  '.join([meta_tag.text, meta_tag.next_sibling.text])
            metalines.append(line)
            meta_tag.previous_element.extract()

        metalines.append(dom.text)
        return {
            'content': '\n'.join(metalines),
            'create_time': create_time,
            'last_edit_time': last_edit_time
        }

    return {
        'content': dom.text,
        'create_time': create_time,
        'last_edit_time': last_edit_time
    }


def __find_tag(tag, name, *classnames):
    '''Helper for find series functions.'''
    # It's fine to use set operation here
    return tag.name == name and set(classnames).issubset(tag['class'])
