import django.contrib.auth.views
import django.views.static

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import sebastian.leitner.views as views

admin.autodiscover()

urlpatterns = [
    url(r'^login/$', django.contrib.auth.views.login),
    url(r'^accounts/login/$', django.contrib.auth.views.login),
    url(r'^logout/$', django.contrib.auth.views.logout),
    url(r'^accounts/password_change/$',
        django.contrib.auth.views.password_change),
    url(r'^accounts/password_change/done/$',
        django.contrib.auth.views.password_change_done),
    url(r'^$', views.IndexView.as_view()),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^add_card/$', views.AddCardView.as_view()),
    url(r'^add_multiple_cards/$', views.AddMultipleCardsView.as_view()),
    url(r'^test/$', views.TestView.as_view()),
    url(r'^decks/$', views.DecksView.as_view()),
    url(r'^decks/(?P<pk>\d+)/$', views.DeckView.as_view()),
    url(r'^decks/(?P<id>\d+)/test/$', views.TestView.as_view()),
    url(r'^cards/(?P<id>\d+)/$', views.CardView.as_view()),
    url(r'^stats/$', views.StatsView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]
