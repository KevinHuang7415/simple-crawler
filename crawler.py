'''
Main functions for crawler.
'''
import sys

import file_helper
import ptt

BOARD_NAME = 'Soft_Job'


def setup_path():
    '''Set path for saving files.'''
    dir_path = file_helper.get_dir(sys.argv)
    file_helper.create_dir_if_not_exist(dir_path)


def crawler():
    '''Grab all articles in recent days.'''
    board = ptt.Board(BOARD_NAME)

    while board.url:
        board.retrieve_dom()
        articles_meta = parse_board(board)

        for article_meta in articles_meta:
            article = retrieve_article(**article_meta)
            save_article(article, **article_meta)


def parse_board(board):
    '''Parse board page for required information.'''
    if not board:
        return None

    board.find_prev_page_url()
    articles_meta = board.get_articles_meta()
    return board.remove_expired(articles_meta)


def retrieve_article(**article_meta):
    '''Retrieve article content.'''
    if not article_meta:
        return None

    article = ptt.Article(BOARD_NAME, **article_meta)
    article.retrieve_dom()
    return article.format_article()


def save_article(article, **meta):
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
