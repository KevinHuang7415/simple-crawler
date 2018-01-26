'''
Main functions for crawler.
'''
import logging
import logging.config
import config
import datetimehelper as dh
import logger
import ptt
import data.services

CONFIG = config.Config()
SECTION = 'Crawler'
LOGGER = logger.get_logger(__name__)


def setup():
    '''Setup configurations.'''
    try:
        CONFIG.load()
    except ValueError:
        CONFIG.load_default()

    logger.load_config()

    data.services.launch_database()


def shutdown():
    '''Prepare for shutdown.'''
    data.services.terminate_database()
    logging.shutdown()


def crawler():
    '''Grab all articles in recent days.'''
    term_date = CONFIG.getint(SECTION, 'term_date')
    LOGGER.info('Start date:[%s]', dh.to_ptt_date())
    LOGGER.info('Term date as [%d] days.', term_date)

    board_name = CONFIG.get(SECTION, 'board')
    board = ptt.Board(board_name, term_date)
    LOGGER.info('Retrive articles from board [%s].', board_name)

    total = 0
    while board.has_prev_page:
        board.retrieve_dom(0)

        articles_meta = parse_board(board)
        count = len(articles_meta)
        LOGGER.info('[%d] articles\' meta retrieved.', count)
        total += count

        retrieve_articles(*articles_meta)

    LOGGER.info('%d articles handled.', total)
    LOGGER.info('Job finished.')


def parse_board(board):
    '''Parse board page for required information.'''
    if not board:
        return None

    board.find_prev_page_url()
    return board.get_articles_meta()


def retrieve_articles(*articles_meta):
    '''Retrieve articles content.'''
    new_article = False
    board_name = CONFIG.get(SECTION, 'board')

    for article_meta in articles_meta:
        article = ptt.Article(board_name, **article_meta)

        article.retrieve_dom()
        content, create_time, last_edit_time = article.parse_content()

        row_article = data.models.find_article(article_meta['href'])
        # the follow-up to new article can only be new too
        if not new_article and not row_article:
            new_article = True

        if new_article:
            data.models.create_article(
                article_meta['date'],
                article_meta['author'],
                article_meta['title'],
                article_meta['href'],
                content,
                create_time,
                last_edit_time
            )
        else:
            update_article(
                row_article,
                article_meta['title'],
                content,
                last_edit_time
            )


def update_article(article, title, content, last_edit_time):
    '''Check which column to update then do update.'''
    if article.title == title:
        title = None

    if len(article.content) == len(content) and article.content == content:
        content = None

    if article.edit_time == last_edit_time:
        last_edit_time = None

    data.models.update_article(article, title, content, last_edit_time)


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
