'''
Model definition for ptt articles.
'''
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import datetimehelper as dh


class Article(models.Model):
    '''Article model.'''

    date = models.CharField(max_length=5)
    author = models.CharField(max_length=35)
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=65, unique=True)
    content = models.TextField()
    length = models.IntegerField()
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.date!r}, {self.url!r})'


def save_article(date, author, title, url, content, create_time, edit_time):
    '''Helper to do create.'''
    Article.objects.create(
        date=date,
        author=author,
        title=title,
        url=url,
        content=content,
        length=len(content),
        create_time=create_time,
        edit_time=edit_time
    )


def find_article(url):
    '''Find article at URL in database.'''
    try:
        return Article.objects.get(url=url)
    except ObjectDoesNotExist:
        return None


def update_article(row, article):
    '''Update query result row.'''
    row.content = article['content']
    row.length = len(article['content'])
    row.edit_time = dh.to_datetime(article['last_edit_time'])
    row.save()
