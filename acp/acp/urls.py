"""acp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^faq', views.faq, name='faq'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^create_corpus', views.create_corpus, name='corpus'),
    url(r'^del_corpus/(?P<corpus_id>\d+)/$', views.del_corpus, name='del_corpus'),
    url(r'^corpus/(?P<corpus_id>\d+)/$', views.corpus, name='corpus'),
    url(r'^add_doc/(?P<corpus_id>\d+)/$', views.add_doc, name='add_doc'),
    url(r'^add_cat/(?P<corpus_id>\d+)/$', views.add_cat, name='add_cat'),
    url(r'^del_doc/(?P<doc_id>\d+)/$', views.del_doc, name='del_doc'),
    url(r'^del_cat/(?P<cat_id>\d+)/$', views.del_cat, name='del_cat'),
    url(r'^visualize/$', views.visualize, name='visualize'),
    url(r'^cat/(?P<cat_id>\d+)/$', views.cat, name='cat'),
    url(r'^perm_error/$', views.perm_error, name='perm_error'),
    url(r'^contact', views.contact, name='contact'),
    
]
