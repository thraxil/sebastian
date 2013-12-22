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
    (r'^add_card/$', 'sebastian.leitner.views.add_card'),
    (r'^add_multiple_cards/$', 'sebastian.leitner.views.add_multiple_cards'),
    (r'^test/$', 'sebastian.leitner.views.test'),
    (r'^decks/$', views.DecksView.as_view()),
    (r'^decks/(?P<id>\d+)/$', 'sebastian.leitner.views.deck'),
    (r'^decks/(?P<id>\d+)/test/$', 'sebastian.leitner.views.test'),
    (r'^cards/(?P<id>\d+)/$', 'sebastian.leitner.views.card'),
    (r'^stats/$', 'sebastian.leitner.views.stats'),
    (r'^admin/', include(admin.site.urls)),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
