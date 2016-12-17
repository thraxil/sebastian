from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def num_deck_cards_due(context, deck):
    user = context['user']
    return deck.num_cards_due(user)
