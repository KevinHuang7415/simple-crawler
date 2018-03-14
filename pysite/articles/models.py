'''
Model definition for ptt articles.
'''
from django.db import models


class AbstractArticle(models.Model):
    '''Abstract article model.'''

    class Meta(object):
        '''Model meta.'''
        abstract = True

    date = models.CharField(max_length=5)
    author = models.CharField(max_length=35)
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=65, unique=True)
    content = models.TextField()
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.date!r}, {self.url!r})'


class SoftJob(AbstractArticle):
    '''SoftJob model.'''

    class Meta(object):
        '''Model meta.'''
        db_table = 'SoftJob'
        ordering = ['-create_time']
        get_latest_by = '-create_time'
