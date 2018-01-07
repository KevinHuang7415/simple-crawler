'''
Main functions for crawler.
'''
import logging
import logging.config
import config
import datetime_helper
import file_helper
import log_config
import ptt

CONFIG = config.Config()
SECTION = 'Crawler'
LOGGER = logging.getLogger('.'.join(['crawler', __name__]))


def setup():
    '''Setup configurations.'''
    try:
        CONFIG.load()
    except ValueError:
        CONFIG.load_default()

    logging.config.dictConfig(log_config.LOGGING)

    file_helper.create_dir_if_not_exist(CONFIG.get(SECTION, 'data_path'))


def shutdown():
    logging.shutdown()


def crawler():
    '''Grab all articles in recent days.'''
    term_date = CONFIG.getint(SECTION, 'term_date')
    LOGGER.info('Start date:[%s]', datetime_helper.to_ptt_date_format())
    LOGGER.info('Term date as [%d] days.', term_date)

    board_name = CONFIG.get(SECTION, 'board')
    board = ptt.Board(board_name, term_date)
    LOGGER.info('Retrive articles from board [%s].', board_name)

    while board.url:
        board.retrieve_dom(0)
        articles_meta = parse_board(board)
        LOGGER.info('[%d] articles\' meta retrieved.', len(articles_meta))

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

    board_name = CONFIG.get(SECTION, 'board')
    article = ptt.Article(board_name, **article_meta)
    article.retrieve_dom()
    return article.format_article()


def save_article(article, **meta):
    '''Save cached article to file.'''
    if article:
        # to avoid the titles collision
        # format: PTT_URL/..../M.number.A.RND.html
        # take the number part
        article_id = meta['href'].rpartition('/')[-1].split('.')[1]
        # date - title - title_id
        file_title = ' - '.join([meta['date'], meta['title'], article_id])

        data_path = CONFIG.get(SECTION, 'data_path')
        file_helper.write_article(article, file_title, data_path)


def main():
    '''Main function.'''
    setup()
    try:
        crawler()
    except Exception:
        LOGGER.error('Unexpected error.', exc_info=True)
    finally:
        shutdown()


if __name__ == '__main__':
    main()
