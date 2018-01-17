'''
Model definition for ptt articles.
'''
from django.db import models


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
