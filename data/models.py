'''
Model definition for ptt articles.
'''
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class AbstractArticle(models.Model):
    '''Abstract article model.'''

    class Meta:
        '''Model meta.'''
        abstract = True

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


class SoftJob(AbstractArticle):
    '''SoftJob model.'''

    class Meta:
        '''Model meta.'''
        db_table = 'SoftJob'
        ordering = ["create_time"]
        get_latest_by = "create_time"


def save_article(date, author, title, url, content, create_time, edit_time):
    '''Helper to do create.'''
    SoftJob.objects.create(
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
        return SoftJob.objects.get(url=url)
    except ObjectDoesNotExist:
        return None


def update_article(row, title, article_content, last_edit_time):
    '''Update query result row.'''
    row.title = title
    row.content = article_content
    row.length = len(article_content)
    row.edit_time = last_edit_time
    row.save()
