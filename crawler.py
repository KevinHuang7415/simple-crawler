'''
Main functions for crawler.
'''
import asyncio
import config
import datetimehelper as dh
import logger

LOGGER = logger.get_logger(__name__)


def setup():
    '''Setup configurations.'''
    config.load_config()

    logger.load_config()


def shutdown():
    '''Prepare for shutdown.'''
    ptt.close_session()

    logger.shutdown()


def crawler():
    '''Grab all articles in recent days.'''
    config_ = config.Config()
    config_section = 'Crawler'

    term_date = config_.getint(config_section, 'term_date')
    LOGGER.info('Start date:[%s]', dh.to_ptt_date())
    LOGGER.info('Term date as [%d] days.', term_date)

    board_name = config_.get(config_section, 'board')
    board = ptt.Board(board_name, term_date)
    LOGGER.info('Retrive articles from board [%s].', board_name)

    total = 0
    while board.has_prev_page:
        board.retrieve_dom()
        article_meta_list = board.parse_board()

        count = len(article_meta_list)
        LOGGER.info('[%d] articles\' meta retrieved.', count)
        total += count

        loop = asyncio.get_event_loop()

        for article_meta in article_meta_list:
            article = ptt.Article(**article_meta)

            article.retrieve_dom()
            loop.create_task(article.save_article())

    LOGGER.info('%d articles handled.', total)
    LOGGER.info('Job finished.')


def main():
    '''Main function.'''
    try:
        setup()
        crawler()
    except Exception:
        LOGGER.exception('Unexpected error.')
    finally:
        shutdown()


if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    # Setup Django manually is required when using some modules standalone
    import django
    django.setup()

    import ptt
    main()
