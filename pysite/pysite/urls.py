"""pysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
# from articles.demo_index import this_is_a_demo
from articles.views import articles_listing, article_detail, articles_search

urlpatterns = [
    # path('demo/', this_is_a_demo),
    path('', articles_listing),
    path('articles/', articles_listing),
    path('articles/<int:page>', articles_listing),
    path('articles/detail/<int:article_id>', article_detail),
    path('articles/search/', articles_search),
    path('articles/search/<str:key_word>/', articles_search),
    path('articles/search/<str:key_word>/<int:page>', articles_search),
]
