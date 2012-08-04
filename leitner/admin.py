from django.contrib import admin
from models import Face, Card, Deck, DeckCard, UserCard, UserCardTest


class FaceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Face, FaceAdmin)


class CardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Card, CardAdmin)


class DeckAdmin(admin.ModelAdmin):
    pass
admin.site.register(Deck, DeckAdmin)


class DeckCardAdmin(admin.ModelAdmin):
    pass
admin.site.register(DeckCard, DeckCardAdmin)


class UserCardAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserCard, UserCardAdmin)


class UserCardTestAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserCardTest, UserCardTestAdmin)
