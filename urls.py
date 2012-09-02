from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
     (r'^login/$', 'django.contrib.auth.views.login'),
     (r'^accounts/login/$', 'django.contrib.auth.views.login'),
     (r'^logout/$','django.contrib.auth.views.logout'),
     (r'^accounts/password_change/$','django.contrib.auth.views.password_change'),
     (r'^accounts/password_change/done/$','django.contrib.auth.views.password_change_done'),                     
     (r'^$', 'sebastian.leitner.views.index'),
     (r'^add_card/$', 'sebastian.leitner.views.add_card'),
     (r'^add_multiple_cards/$', 'sebastian.leitner.views.add_multiple_cards'),                       
     (r'^test/$', 'sebastian.leitner.views.test'),
     (r'^decks/$', 'sebastian.leitner.views.decks'),
     (r'^decks/(?P<id>\d+)/$', 'sebastian.leitner.views.deck'),
     (r'^decks/(?P<id>\d+)/test/$', 'sebastian.leitner.views.test'),
     (r'^cards/(?P<id>\d+)/$', 'sebastian.leitner.views.card'),                                              
     (r'^stats/$', 'sebastian.leitner.views.stats'),
     (r'^admin/', include(admin.site.urls)),
     (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/sebastian/media/'}),                       
     (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/tmp/sebastian/'}),                       
     (r'^munin/due/$','sebastian.leitner.views.munin_due'),
     (r'^munin/percent/$','sebastian.leitner.views.munin_percent'),
     (r'^munin/tested/$','sebastian.leitner.views.munin_tested'),
     (r'^munin/rungs/$','sebastian.leitner.views.munin_rungs'),
     (r'^munin/ease/$','sebastian.leitner.views.munin_ease'),
)
