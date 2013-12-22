# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Deck, UserCard, UserCardTest, Card, Face, User
from .models import next_card, total_due, first_due, user_decks
from .models import first_deck_due, next_deck_card, total_deck_due
from .models import rungs_stats, ease_stats, percent_right, priority_stats
from .models import total_tested, total_untested
from .models import next_hour_due, next_six_hours_due, next_day_due
from .models import next_week_due, next_month_due, recent_tests
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from forms import AddFaceForm
from annoying.decorators import render_to



class LoggedInMixin(object):
    @method_decorator(login_required)

    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(LoggedInMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        return dict(user=self.request.user)


@login_required
@render_to("test.html")
def test(request, id=None):
    deck = None
    if id:
        deck = get_object_or_404(Deck, id=id)
    if request.method == "POST":
        uc = get_object_or_404(UserCard, id=request.POST.get('card'))
        if request.POST.get("right", "no") == "yes":
            # got it right
            uc.test_correct()
        else:
            # got it wrong
            uc.test_wrong()
        if deck:
            return HttpResponseRedirect("/decks/%d/test/" % deck.id)
        else:
            return HttpResponseRedirect("/test/")
    else:
        if deck:
            return dict(
                card=next_deck_card(request.user, deck),
                total_due=total_deck_due(request.user, deck),
                first_due=first_deck_due(request.user, deck),
                recent_tests=recent_tests(request.user, 100),
            )
        else:
            return dict(
                card=next_card(request.user),
                total_due=total_due(request.user),
                first_due=first_due(request.user),
                recent_tests=recent_tests(request.user, 100),
            )


class DecksView(LoggedInMixin, ListView):
    template_name = "decks.html"

    def get_queryset(self):
        return user_decks(self.request.user)


@login_required
@render_to("deck.html")
def deck(request, id):
    deck = get_object_or_404(Deck, id=id)
    return dict(deck=deck,
                usercards=deck.usercards(request.user))


@login_required
@render_to("card.html")
def card(request, id):
    card = get_object_or_404(UserCard, id=id)
    if request.method == "POST":
        card.card.front.content = request.POST.get('front', u'')
        card.card.front.save()
        card.card.back.content = request.POST.get('back', u'')
        card.card.back.save()
        card.priority = request.POST.get('priority', '5')
        card.save()
        return HttpResponseRedirect(card.get_absolute_url())
    return dict(card=card)


@login_required
@render_to("add_card.html")
def add_card(request):
    if request.method == "POST":
        u = request.user
        deck_name = request.POST.get("deck", "")
        if deck_name == "":
            deck_name = request.POST.get("new_deck", "no deck")
        try:
            deck = Deck.objects.get(name=deck_name, user=u)
        except ObjectDoesNotExist:
            deck = Deck.objects.create(name=deck_name, user=u)

        front_form = AddFaceForm(request.POST, request.FILES, prefix="front")
        back_form = AddFaceForm(request.POST, request.FILES, prefix="back")
        if front_form.is_valid() and back_form.is_valid():
            front = front_form.save()
            back = back_form.save()
            card = Card.objects.create(front=front, back=back,
                                       deck=deck)
            UserCard.objects.create(
                card=card, user=request.user,
                due=datetime.now(),
                priority=int(request.POST.get('priority', '1')))
            return HttpResponseRedirect("/add_card/")
    else:
        front_form = AddFaceForm(prefix="front")
        back_form = AddFaceForm(prefix="back")
    return dict(decks=user_decks(request.user),
                front=front_form, back=back_form)


@login_required
def add_multiple_cards(request):
    u = request.user
    deck_name = request.POST.get("deck", "")
    if deck_name == "":
        deck_name = request.POST.get("new_deck", "no deck")

    try:
        deck = Deck.objects.get(name=deck_name, user=u)
    except ObjectDoesNotExist:
        deck = Deck.objects.create(name=deck_name, user=u)

    cards = request.POST.get("cards", "")
    for line in cards.split("\n"):
        parts = line.split("|")
        front_content = parts[0]
        back_content = "|".join(parts[1:])
        front = Face.objects.create(content=front_content)
        back = Face.objects.create(content=back_content)
        card = Card.objects.create(front=front, back=back,
                                   deck=deck)
        UserCard.objects.create(card=card, user=request.user,
                                due=datetime.now(),
                                priority=int(request.POST.get('priority',
                                                              '1')))

    return HttpResponseRedirect("/add_card/")


@login_required
@render_to("stats.html")
def stats(request):
    rungs = list(rungs_stats(request.user))
    max_rung = max([r['cards'] for r in rungs])
    ease = list(ease_stats(request.user))
    max_ease = max([r['cards'] for r in ease])
    return dict(
        rungs=rungs,
        max_rung=max_rung,
        ease=ease,
        max_ease=max_ease,
        percent_right=percent_right(request.user),
        priorities=priority_stats(request.user),
        total_tested=total_tested(request.user),
        total_untested=total_untested(request.user),
        total_due=total_due(request.user),
        first_due=first_due(request.user),
        next_hour_due=next_hour_due(request.user),
        next_six_hours_due=next_six_hours_due(request.user),
        next_day_due=next_day_due(request.user),
        next_week_due=next_week_due(request.user),
        next_month_due=next_month_due(request.user),
        recent_tests=UserCardTest.objects.filter(
            usercard__user=request.user).order_by("-timestamp")[:1000],
    )
