'''
Main functions for crawler.
'''
import asyncio
import config
import datetimehelper as dh
import logger
import ptt
from data import services

CONFIG = config.Config()
SECTION = 'Crawler'
LOGGER = logger.get_logger(__name__)
LOOP = asyncio.get_event_loop()


def setup():
    '''Setup configurations.'''
    try:
        CONFIG.load()
    except ValueError:
        CONFIG.load_default()

    logger.load_config()

    services.launch_database()


def shutdown():
    '''Prepare for shutdown.'''
    ptt.CLIENT.close()
    services.terminate_database()
    logger.shutdown()


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
        article_meta_list = parse_board(board)

        count = len(article_meta_list)
        LOGGER.info('[%d] articles\' meta retrieved.', count)
        total += count

        retrieve_articles(*article_meta_list)

    pending = asyncio.Task.all_tasks()
    LOOP.run_until_complete(asyncio.gather(*pending))

    LOGGER.info('%d articles handled.', total)
    LOGGER.info('Job finished.')


def parse_board(board):
    '''Parse board page for required information.'''
    if not board:
        return None

    try:
        board.find_prev_page_url()
        return board.all_articles_meta()
    except ValueError:
        return list()


def retrieve_articles(*article_meta_list):
    '''Retrieve articles content.'''
    for article_meta in article_meta_list:
        article = ptt.Article(**article_meta)

        article.retrieve_dom()
        LOOP.create_task(save_article(article))


async def save_article(article):
    '''Save article with newly retrieved data.'''
    try:
        content, create_time, last_edit_time = article.parse_content()
    except ValueError:
        LOGGER.warning('Failed to parse for article [%s]', article)
        return

    row_article = models.find_article(article.meta['href'])
    if not row_article:
        models.create_article(
            article.meta['date'],
            article.meta['author'],
            article.meta['title'],
            article.meta['href'],
            content,
            create_time,
            last_edit_time
        )
    else:
        update_article(
            row_article,
            article.meta['title'],
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

    models.update_article(article, title, content, last_edit_time)


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

    from data import models
    main()
