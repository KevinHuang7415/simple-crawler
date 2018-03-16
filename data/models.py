'''
Model definition for ptt articles.
'''
from django.core.exceptions import ObjectDoesNotExist
from pysite.articles.models import SoftJob
import logger

LOGGER = logger.get_logger(__name__)


def create_article(date, author, title, url, content, create_time, edit_time):
    '''Helper to do create.'''
    LOGGER.debug(
        'Create article at [%s] with create time [%s]', url, create_time
    )
    SoftJob.objects.create(
        date=date,
        author=author,
        title=title,
        url=url,
        content=content,
        create_time=create_time,
        edit_time=edit_time
    )


def find_article(url):
    '''Find article at URL in database.'''
    try:
        return SoftJob.objects.get(url=url)
    except ObjectDoesNotExist:
        return None


def update_article(row, title=None, content=None, last_edit_time=None):
    '''Update query result row.'''
    if not title and not content and not last_edit_time:
        return

    if title:
        row.title = title
    if content:
        row.content = content
    if last_edit_time:
        row.edit_time = last_edit_time

    LOGGER.debug('Update article at [%s]', row.url)
    row.save()
