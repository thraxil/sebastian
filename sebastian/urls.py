import django.contrib.auth.views as auth_views
import django.views.static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import sebastian.leitner.views as views

admin.autodiscover()

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.IndexView.as_view(), name="index"),
    path("smoketest/", include("smoketest.urls")),
    path("add_card/", views.AddCardView.as_view(), name="add-card"),
    path(
        "add_multiple_cards/",
        views.AddMultipleCardsView.as_view(),
        name="add-multiple-cards",
    ),
    path("test/", views.TestView.as_view(), name="test"),
    path("decks/", views.DecksView.as_view(), name="decks-list"),
    path("decks/<int:pk>/", views.DeckView.as_view(), name="deck-detail"),
    path("decks/<int:id>/test/", views.TestView.as_view(), name="deck-test"),
    path(
        "decks/<int:id>/export/",
        views.ExportDeckView.as_view(),
        name="deck-export",
    ),
    path("cards/<int:id>/", views.CardView.as_view(), name="card-detail"),
    path("stats/", views.StatsView.as_view(), name="stats"),
    path("admin/", admin.site.urls),
    path(
        "uploads/<path:path>",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT},
        name="uploads",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
