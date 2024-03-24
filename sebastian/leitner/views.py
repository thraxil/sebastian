from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import AddFaceForm
from .models import (
    Deck,
    Face,
    UserCard,
    UserCardTest,
)
from .selectors import (
    ease_stats,
    first_deck_due,
    first_due,
    next_card,
    next_day_due,
    next_deck_card,
    next_hour_due,
    next_month_due,
    next_six_hours_due,
    next_week_due,
    recent_tests,
    rungs_stats,
    total_deck_due,
    total_due,
    total_tested,
    total_untested,
    user_decks,
    user_percent_right,
    user_priority_stats,
)
from .service import (
    create_card,
    get_or_create_deck,
    usercard_test_correct,
    usercard_test_wrong,
    usercard_update,
)


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(LoggedInMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        return dict(user=self.request.user)


class DeckHandler(object):
    def __init__(self, deck_id):
        self.deck = get_object_or_404(Deck, id=deck_id)

    def context_dict(self, user: User):
        return dict(
            card=next_deck_card(user, self.deck),
            total_due=total_deck_due(user, self.deck),
            first_due=first_deck_due(user, self.deck),
            recent_tests=recent_tests(user, 100),
        )

    def redirect(self):
        return HttpResponseRedirect("/decks/%d/test/" % self.deck.id)


class NullDeckHandler(object):
    def context_dict(self, user: User):
        return dict(
            card=next_card(user),
            total_due=total_due(user),
            first_due=first_due(user),
            recent_tests=recent_tests(user, 100),
        )

    def redirect(self):
        return HttpResponseRedirect("/test/")


def make_deck_handler(deck_id=None):
    if deck_id is None:
        return NullDeckHandler()
    return DeckHandler(deck_id)


class TestView(LoggedInMixin, View):
    template_name = "test.html"

    def get(self, request, id=None):
        deck_handler = make_deck_handler(id)
        return render(
            request,
            self.template_name,
            deck_handler.context_dict(request.user),
        )

    def post(self, request, id=None):
        deck_handler = make_deck_handler(id)
        uc = get_object_or_404(UserCard, id=request.POST.get("card"))
        if request.POST.get("right", "no") == "yes":
            # got it right
            usercard_test_correct(uc)
        else:
            # got it wrong
            usercard_test_wrong(uc)
        return deck_handler.redirect()


class ExportDeckView(LoggedInMixin, View):
    def get(self, request, id=None):
        deck = get_object_or_404(Deck, id=id)
        cards = [
            "{}|{}".format(c.front.content, c.back.content)
            for c in deck.cards()
        ]
        return HttpResponse("\n".join(cards), content_type="text/plain")


class DecksView(LoggedInMixin, ListView):
    template_name = "decks.html"

    def get_queryset(self):
        return user_decks(self.request.user)


class DeckView(LoggedInMixin, DetailView):
    template_name = "deck.html"
    model = Deck
    context_object_name = "deck"

    def get_context_data(self, **kwargs):
        context = super(DeckView, self).get_context_data(**kwargs)
        context["usercards"] = context["deck"].usercards(self.request.user)
        context["deck_total"] = len(
            context["deck"].usercards(self.request.user)
        )
        context["deck_unlearned"] = context["deck"].num_unlearned(
            self.request.user
        )
        return context


class CardView(LoggedInMixin, View):
    template_name = "card.html"

    def post(self, request, id):
        front_content = request.POST.get("front", "")
        back_content = request.POST.get("back", "")
        priority = request.POST.get("priority", "5")
        card = get_object_or_404(UserCard, id=id)
        usercard_update(card, front_content, back_content, priority)
        return HttpResponseRedirect(card.get_absolute_url())

    def get(self, request, id):
        card = get_object_or_404(UserCard, id=id)
        return render(request, self.template_name, dict(card=card))


def get_deck_name(post) -> str:
    deck_name = post.get("deck", "")
    if deck_name == "":
        return post.get("new_deck", "no deck")
    return deck_name


class AddCardView(LoggedInMixin, View):
    template_name = "add_card.html"

    def post(self, request):
        u = request.user
        deck = get_or_create_deck(get_deck_name(request.POST), u)
        front_form = AddFaceForm(request.POST, request.FILES, prefix="front")
        back_form = AddFaceForm(request.POST, request.FILES, prefix="back")
        if front_form.is_valid() and back_form.is_valid():
            front = front_form.save()
            back = back_form.save()
            create_card(
                front,
                back,
                deck,
                request.user,
                int(request.POST.get("priority", "1")),
            )
            return HttpResponseRedirect("/add_card/")
        return render(
            request,
            self.template_name,
            dict(
                decks=user_decks(request.user),
                front=front_form,
                back=back_form,
            ),
        )

    def get(self, request):
        front_form = AddFaceForm(prefix="front")
        back_form = AddFaceForm(prefix="back")
        return render(
            request,
            self.template_name,
            dict(
                decks=user_decks(request.user),
                front=front_form,
                back=back_form,
            ),
        )


class AddMultipleCardsView(LoggedInMixin, View):
    def post(self, request):
        u = request.user
        deck = get_or_create_deck(get_deck_name(request.POST), u)
        cards = request.POST.get("cards", "")
        for line in cards.split("\n"):
            parts = line.split("|")
            front_content = parts[0]
            back_content = "|".join(parts[1:])
            front = Face.objects.create(content=front_content)
            back = Face.objects.create(content=back_content)
            create_card(
                front,
                back,
                deck,
                request.user,
                int(request.POST.get("priority", "1")),
            )
        return HttpResponseRedirect("/add_card/")


class StatsView(LoggedInMixin, TemplateView):
    template_name = "stats.html"

    def get_context_data(self):
        rungs = list(rungs_stats(self.request.user))
        ease = list(ease_stats(self.request.user))
        return dict(
            rungs=rungs,
            max_rung=max([r["cards"] for r in rungs]),
            ease=ease,
            max_ease=max([r["cards"] for r in ease]),
            percent_right=user_percent_right(self.request.user),
            priorities=user_priority_stats(self.request.user),
            total_tested=total_tested(self.request.user),
            total_untested=total_untested(self.request.user),
            total_due=total_due(self.request.user),
            first_due=first_due(self.request.user),
            next_hour_due=next_hour_due(self.request.user),
            next_six_hours_due=next_six_hours_due(self.request.user),
            next_day_due=next_day_due(self.request.user),
            next_week_due=next_week_due(self.request.user),
            next_month_due=next_month_due(self.request.user),
            recent_tests=UserCardTest.objects.filter(
                usercard__user=self.request.user
            ).order_by("-timestamp")[:1000],
        )
