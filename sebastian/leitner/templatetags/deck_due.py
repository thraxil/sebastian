from typing import Dict, cast

from django import template
from django.contrib.auth.models import User

from ..models import Deck

register = template.Library()


@register.simple_tag(takes_context=True)
def num_deck_cards_due(context: Dict[str, object], deck: Deck) -> int:
    user = cast(User, context["user"])
    return deck.num_cards_due(user=user)
