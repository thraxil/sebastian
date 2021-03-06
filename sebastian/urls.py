import django.contrib.auth.views as auth_views
import django.views.static

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.urls import path
import sebastian.leitner.views as views

admin.autodiscover()

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view()),
    url(r'^logout/$', auth_views.LogoutView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.IndexView.as_view()),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^add_card/$', views.AddCardView.as_view()),
    url(r'^add_multiple_cards/$', views.AddMultipleCardsView.as_view()),
    url(r'^test/$', views.TestView.as_view()),
    url(r'^decks/$', views.DecksView.as_view()),
    url(r'^decks/(?P<pk>\d+)/$', views.DeckView.as_view()),
    url(r'^decks/(?P<id>\d+)/test/$', views.TestView.as_view()),
    url(r'^decks/(?P<id>\d+)/export/$', views.ExportDeckView.as_view()),
    url(r'^cards/(?P<id>\d+)/$', views.CardView.as_view(), name='card-detail'),
    url(r'^stats/$', views.StatsView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
