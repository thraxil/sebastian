from django.contrib import admin

from .models import Card, Deck, Face, UserCard, UserCardTest

admin.site.register(Face)
admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(UserCard)
admin.site.register(UserCardTest)
