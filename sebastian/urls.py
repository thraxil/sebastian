from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings
import sebastian.leitner.views as views

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/password_change/$',
     'django.contrib.auth.views.password_change'),
    (r'^accounts/password_change/done/$',
     'django.contrib.auth.views.password_change_done'),
    (r'^$', views.IndexView.as_view()),
    (r'smoketest/', include('smoketest.urls')),
    (r'^add_card/$', views.AddCardView.as_view()),
    (r'^add_multiple_cards/$', views.AddMultipleCardsView.as_view()),
    (r'^test/$', views.TestView.as_view()),
    (r'^decks/$', views.DecksView.as_view()),
    (r'^decks/(?P<pk>\d+)/$', views.DeckView.as_view()),
    (r'^decks/(?P<id>\d+)/test/$', views.TestView.as_view()),
    (r'^cards/(?P<id>\d+)/$', views.CardView.as_view()),
    (r'^stats/$', views.StatsView.as_view()),
    (r'^admin/', include(admin.site.urls)),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
