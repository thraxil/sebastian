from django.test import Client, TestCase, override_settings
from django.urls import reverse

from sebastian.leitner.models import Card, UserCard

from .factories import (
    CardFactory,
    DeckFactory,
    FaceFactory,
    UserCardFactory,
    UserFactory,
)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestIndexView(TestCase):
    def test_get(self):
        user = UserFactory()
        client = Client()
        client.force_login(user)
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestDecksView(TestCase):
    def test_get(self):
        user = UserFactory()
        deck = DeckFactory(user=user)
        client = Client()
        client.force_login(user)
        response = client.get(reverse("decks-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "decks.html")
        self.assertIn("object_list", response.context)
        self.assertEqual(list(response.context["object_list"]), [deck])


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestDeckView(TestCase):
    def test_get(self):
        user = UserFactory()
        deck = DeckFactory(user=user)
        client = Client()
        client.force_login(user)
        response = client.get(reverse("deck-detail", kwargs={"pk": deck.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "deck.html")
        self.assertEqual(response.context["deck"], deck)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestStatsView(TestCase):
    def test_get(self):
        user = UserFactory()
        client = Client()
        client.force_login(user)
        response = client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stats.html")
        self.assertIn("rungs", response.context)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestCardView(TestCase):
    def test_get(self):
        user = UserFactory()
        user_card = UserCardFactory(user=user)
        client = Client()
        client.force_login(user)
        response = client.get(
            reverse("card-detail", kwargs={"id": user_card.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "card.html")

    def test_post_update(self):
        user = UserFactory()
        user_card = UserCardFactory(user=user)
        client = Client()
        client.force_login(user)
        data = {
            "front": "new front content",
            "back": "new back content",
            "priority": "5",
        }
        response = client.post(
            reverse("card-detail", kwargs={"id": user_card.id}), data
        )
        self.assertEqual(response.status_code, 302)
        user_card.refresh_from_db()
        self.assertEqual(user_card.card.front.content, "new front content")
        self.assertEqual(user_card.card.back.content, "new back content")
        self.assertEqual(user_card.priority, 5)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestAddCardView(TestCase):
    def test_get(self):
        user = UserFactory()
        client = Client()
        client.force_login(user)
        response = client.get(reverse("add-card"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_card.html")

    def test_post_new_card(self):
        user = UserFactory()
        deck = DeckFactory(user=user)
        client = Client()
        client.force_login(user)
        data = {
            "deck": deck.name,
            "priority": "1",
            "front-content": "front content",
            "back-content": "back content",
        }
        response = client.post(reverse("add-card"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(UserCard.objects.count(), 1)

    def test_post_new_card_new_deck(self):
        user = UserFactory()
        client = Client()
        client.force_login(user)
        data = {
            "new_deck": "a new deck",
            "priority": "1",
            "front-content": "front content",
            "back-content": "back content",
        }
        response = client.post(reverse("add-card"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(UserCard.objects.count(), 1)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestAddMultipleCardsView(TestCase):
    def test_post(self):
        user = UserFactory()
        deck = DeckFactory(user=user)
        client = Client()
        client.force_login(user)
        data = {
            "deck": deck.name,
            "priority": "1",
            "cards": "front1|back1\nfront2|back2",
        }
        response = client.post(reverse("add-multiple-cards"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 2)
        self.assertEqual(UserCard.objects.count(), 2)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestTestView(TestCase):
    def test_get(self):
        user = UserFactory()
        UserCardFactory(user=user)
        client = Client()
        client.force_login(user)
        response = client.get(reverse("test"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "test.html")

    def test_post_right(self):
        user = UserFactory()
        user_card = UserCardFactory(user=user)
        client = Client()
        client.force_login(user)
        response = client.post(
            reverse("test"), {"card": user_card.id, "right": "yes"}
        )
        self.assertEqual(response.status_code, 302)
        user_card.refresh_from_db()
        self.assertEqual(user_card.rung, 1)

    def test_post_wrong(self):
        user = UserFactory()
        user_card = UserCardFactory(user=user)
        client = Client()
        client.force_login(user)
        response = client.post(
            reverse("test"), {"card": user_card.id, "right": "no"}
        )
        self.assertEqual(response.status_code, 302)
        user_card.refresh_from_db()
        self.assertEqual(user_card.rung, 0)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TestExportDeckView(TestCase):
    def test_get(self):
        user = UserFactory()
        client = Client()
        client.force_login(user)
        deck = DeckFactory(user=user)
        card = CardFactory(deck=deck)
        response = client.get(reverse("deck-export", kwargs={"id": deck.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("Content-Type"), "text/plain")
        self.assertIn(card.front.content, str(response.content))
