'''
View functions for this application.
'''
from datetime import datetime
import string
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
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
            'reason': 'Wrong page.'
        })

    articles = paginator.get_page(page)
    LOGGER.info('Return page [%d].', page)
    return render(request, 'index.html', {
        'articles': articles
    })


def article_detail(request, article_id):
    '''Page of article details, including content and source URL.'''
    try:
        article = SoftJob.objects.get(id=article_id)
    except ObjectDoesNotExist:
        LOGGER.info('No article with ID [%d].', article_id)

        return render(request, 'error.html', {
            'reason': 'Wrong ID.'
        })
    else:
        url_full = f'https://www.ptt.cc{article.url}'

        LOGGER.info('Return article [%d] with source [%s].',
                    article_id, url_full)

        return render(request, 'detail.html', {
            'article': article,
            'url_full': url_full
        })


def articles_search(request, key_word='', page=1):
    '''Page of articles search list.'''
    if not acceptable_key_word(key_word):
        LOGGER.info('Key word [%s] is in ill form.', key_word)
        return render(request, 'Error.html', {
            'reason': f'Non-acceptable word: "{key_word}"'
        })

    articles_list = SoftJob.objects.filter(
        Q(title__contains=key_word) | Q(content__contains=key_word)
    )

    paginator = Paginator(articles_list, 20)
    if page not in paginator.page_range:
        LOGGER.info('Page [%d] is out of range.', page)
        return render(request, 'Error.html', {
            'reason': 'Wrong page.'
        })

    articles = paginator.get_page(page)
    LOGGER.info('Return page [%d] of search result for [%s].', page, key_word)
    return render(request, 'search.html', {
        'articles': articles,
        'key_word': key_word
    })


def acceptable_key_word(key_word):
    '''Check if the key word for searching is acceptable.'''
    return key_word and\
        isinstance(key_word, str) and\
        len([ch for ch in key_word if ch in string.punctuation]) == 0
