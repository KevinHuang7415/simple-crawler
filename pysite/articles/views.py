'''
View functions for this application.
'''
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render
import loggers.helpers as log_helper
from .models import SoftJob

LOGGER = log_helper.get_logger(__name__)


def articles_listing(request, page=1):
    '''Page of articles list.'''
    articles_list = SoftJob.objects.all()

    paginator = Paginator(articles_list, 20)
    if page not in paginator.page_range:
        LOGGER.info('Page [%d] is out of range.', page)
        return render(request, 'Error.html', {
            'reason': 'Wrong page.',
            'year': datetime.now().year
        })

    articles = paginator.get_page(page)
    LOGGER.info('Return page [%d].', page)
    return render(request, 'index.html', {
        'articles': articles,
        'year': datetime.now().year
    })


def article_detail(request, article_id):
    '''Page of article details, including content and source URL.'''
    try:
        article = SoftJob.objects.get(id=article_id)
    except ObjectDoesNotExist:
        LOGGER.info('No article with ID [%d].', article_id)

        return render(request, 'error.html', {
            'reason': 'Wrong ID.',
            'year': datetime.now().year
        })
    else:
        url_full = f'https://www.ptt.cc{article.url}'

        LOGGER.info('Return article [%d] with source [%s].',
                    article_id, url_full)

        return render(request, 'detail.html', {
            'article': article,
            'url_full': url_full,
            'year': datetime.now().year
        })
