'''
Main functions for crawler.
'''
import logging
import logging.config
import config
import datetimehelper as dh
import log_config
import ptt
import data.services

CONFIG = config.Config()
SECTION = 'Crawler'
if __package__:
    LOGGER = logging.getLogger('.'.join(['crawler', __package__, __name__]))
else:
    LOGGER = logging.getLogger('.'.join(['crawler', __name__]))


def setup():
    '''Setup configurations.'''
    try:
        CONFIG.load()
    except ValueError:
        CONFIG.load_default()

    logging.config.dictConfig(log_config.LOGGING)

    data.services.start()


def shutdown():
    '''Prepare for shutdown.'''
    data.services.stop()
    logging.shutdown()


def crawler():
    '''Grab all articles in recent days.'''
    term_date = CONFIG.getint(SECTION, 'term_date')
    LOGGER.info('Start date:[%s]', dh.to_ptt_date())
    LOGGER.info('Term date as [%d] days.', term_date)

    board_name = CONFIG.get(SECTION, 'board')
    board = ptt.Board(board_name, term_date)
    LOGGER.info('Retrive articles from board [%s].', board_name)

    while board.has_prev_page:
        board.retrieve_dom(0)
        articles_meta = parse_board(board)
        LOGGER.info('[%d] articles\' meta retrieved.', len(articles_meta))

        for article_meta in articles_meta:
            article = retrieve_article(**article_meta)
            save_article(article, **article_meta)

    LOGGER.info('Job finished.')


def parse_board(board):
    '''Parse board page for required information.'''
    if not board:
        return None

    board.find_prev_page_url()
    return board.get_articles_meta()


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
        data.models.save_article(
            meta['date'],
            meta['author'],
            meta['title'],
            meta['href'],
            article['content'],
            dh.to_datetime(article['create_time']),
            dh.to_datetime(article['last_edit_time'])
        )


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
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    # Setup Django manually is required when using some modules standalone
    import django
    django.setup()

    import data.models
    main()
