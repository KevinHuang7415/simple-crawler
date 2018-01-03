'''
Main functions for crawler.
'''
import config
import file_helper
import ptt

CONFIG = config.Config()
SECTION = 'Crawler'


def setup():
    '''Setup configurations.'''
    try:
        CONFIG.load()
    except ValueError:
        CONFIG.use_default = True

    file_helper.create_dir_if_not_exist(CONFIG.get(SECTION, 'data_path'))


def crawler():
    '''Grab all articles in recent days.'''
    term_date = CONFIG.getint(SECTION, 'term_date')
    board_name = CONFIG.get(SECTION, 'board')
    board = ptt.Board(board_name, term_date)

    while board.url:
        board.retrieve_dom(0)
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

    board_name = CONFIG.get(SECTION, 'board')
    article = ptt.Article(board_name, **article_meta)
    article.retrieve_dom()
    return article.format_article()


def save_article(article, **meta):
    '''Save cached article to file.'''
    if article:
        # to avoid the titles collision
        # format PTT_URL/..../M.number.A.RND.html, take the number part
        title_id = meta['href'].split('/')[-1].split('.')[1]
        title = ' - '.join([meta['date'], meta['title'], title_id])

        data_path = CONFIG.get(SECTION, 'data_path')
        file_helper.write_article(article, title, data_path)


def main():
    '''Main function.'''
    setup()
    crawler()


if __name__ == '__main__':
    main()
