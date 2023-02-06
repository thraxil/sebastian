import django.contrib.auth.views as auth_views
import django.views.static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

import sebastian.leitner.views as views

admin.autodiscover()

urlpatterns = [
    re_path(r"^login/$", auth_views.LoginView.as_view()),
    re_path(r"^logout/$", auth_views.LogoutView.as_view()),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r"^$", views.IndexView.as_view()),
    re_path(r"smoketest/", include("smoketest.urls")),
    re_path(r"^add_card/$", views.AddCardView.as_view()),
    re_path(r"^add_multiple_cards/$", views.AddMultipleCardsView.as_view()),
    re_path(r"^test/$", views.TestView.as_view()),
    re_path(r"^decks/$", views.DecksView.as_view()),
    re_path(r"^decks/(?P<pk>\d+)/$", views.DeckView.as_view()),
    re_path(r"^decks/(?P<id>\d+)/test/$", views.TestView.as_view()),
    re_path(r"^decks/(?P<id>\d+)/export/$", views.ExportDeckView.as_view()),
    re_path(
        r"^cards/(?P<id>\d+)/$", views.CardView.as_view(), name="card-detail"
    ),
    re_path(r"^stats/$", views.StatsView.as_view()),
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^uploads/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
