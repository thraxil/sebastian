from django import template

register = template.Library()


class GetDeckDue(template.Node):
    def __init__(self, deck, user, var_name=None):
        self.deck = template.Variable(deck)
        self.user = template.Variable(user)
        self.var_name = var_name

    def render(self, context):
        d = self.deck.resolve(context)
        u = self.user.resolve(context)
        due = d.num_cards_due(u)
        if self.var_name:
            context[self.var_name] = due
            return ''
        else:
            return due


@register.tag('num_deck_cards_due')
def get_deck_cards_due(parser, token):
    deck = token.split_contents()[1:][0]
    user = token.split_contents()[1:][1]
    var_name = None
    if len(token.split_contents()[1:]) > 2:
        # handle "as some_var"
        var_name = token.split_contents()[1:][3]
    return GetDeckDue(deck, user, var_name)
