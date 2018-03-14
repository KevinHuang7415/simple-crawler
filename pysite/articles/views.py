from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import SoftJob

def articles_listing(request, page=1):
    '''Page of articles list.'''
    articles_list = SoftJob.objects.all()

    paginator = Paginator(articles_list, 20)
    if page not in paginator.page_range:
        return render(request, 'Error.html', {
            'reason': 'Wrong page.',
            'year': datetime.now().year
        })

    articles = paginator.get_page(page)
    return render(request, 'Index.html', {
        'articles': articles,
        'year': datetime.now().year
    })


def article_detail(request, id):
    '''Page of article details, including content and source URL.'''
    try:
        article = SoftJob.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'Error.html', {
            'reason': 'Wrong ID.',
            'year': datetime.now().year
        })
    else:
        url_full = f'https://www.ptt.cc{article.url}'
        return render(request, 'Details.html', {
            'article': article,
            'url_full': url_full,
            'year': datetime.now().year
        })
