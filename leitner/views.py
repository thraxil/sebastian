# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

@login_required
def index(request):
    return render_to_response("index.html",dict(user=request.user))

@login_required
def test(request):
    if request.method == "POST":
        uc = get_object_or_404(UserCard,id=request.POST.get('card'))
        if request.POST.get("right","no") == "yes":
            # got it right
            uc.test_correct()
        else:
            # got it wrong
            uc.test_wrong()
        return HttpResponseRedirect("/test/")
    else:
        return render_to_response("test.html",dict(card=next_card(request.user),
                                                   total_due=total_due(request.user),
                                                   first_due=first_due(request.user)))

@login_required
def decks(request):
    return render_to_response("decks.html",dict(decks=user_decks(request.user)))

@login_required
def deck(request,id):
    deck = get_object_or_404(Deck,id=id)
    return render_to_response("deck.html",dict(deck=deck,
	   usercards=deck.usercards(request.user)))

@login_required
def card(request,id):
    card = get_object_or_404(UserCard,id=id)
    return render_to_response("card.html",dict(card=card))


@login_required
def add_card(request):
    if request.method == "POST":
        u = request.user
        deck_name = request.POST.get("deck","")
        if deck_name == "":
            deck_name = request.POST.get("new_deck","no deck")
        try:
            deck = Deck.objects.get(name=deck_name,user=u)
        except ObjectDoesNotExist:
            deck = Deck.objects.create(name=deck_name,user=u)

        front = Face.objects.create(content=request.POST.get("front_content",""),
                                    tex=request.POST.get("front_tex",""))
        back = Face.objects.create(content=request.POST.get("back_content",""),
                                    tex=request.POST.get("back_tex",""))
        card = Card.objects.create(front=front,back=back)
        dc = DeckCard.objects.create(deck=deck,card=card)
        uc = UserCard.objects.create(card=card,user=request.user,
                                     due=datetime.now(),
                                     priority=int(request.POST.get('priority','1')))

        return HttpResponseRedirect("/add_card/")

    else:
        return render_to_response("add_card.html",dict(decks=user_decks(request.user)))

@login_required
def add_multiple_cards(request):
    u = request.user
    deck_name = request.POST.get("deck","")
    if deck_name == "":
        deck_name = request.POST.get("new_deck","no deck")

    try:
        deck = Deck.objects.get(name=deck_name,user=u)
    except ObjectDoesNotExist:
        deck = Deck.objects.create(name=deck_name,user=u)

    cards = request.POST.get("cards","")
    for line in cards.split("\n"):
        parts = line.split("|")
        front_content = parts[0]
        back_content = "|".join(parts[1:])
        front = Face.objects.create(content=front_content,tex="")
        back = Face.objects.create(content=back_content,tex="")
        card = Card.objects.create(front=front,back=back)
        dc = DeckCard.objects.create(deck=deck,card=card)
        uc = UserCard.objects.create(card=card,user=request.user,
                                     due=datetime.now(),
                                     priority=int(request.POST.get('priority','1')))

    return HttpResponseRedirect("/add_card/")

@login_required
def stats(request):
    rungs = list(rungs_stats(request.user))
    max_rung = max([r['cards'] for r in rungs])
    ease = list(ease_stats(request.user))
    max_ease = max([r['cards'] for r in ease])
    return render_to_response("stats.html",dict(
        rungs=rungs,
        max_rung=max_rung,
        ease=ease,
        max_ease=max_ease,
        percent_right=percent_right(request.user),
        priorities=priority_stats(request.user),
	due_dates=clumped_due_dates(request.user),
	overdue_dates=clumped_overdue_dates(request.user),
        total_tested=total_tested(request.user),
        total_untested=total_untested(request.user),
        total_due=total_due(request.user),
        first_due=first_due(request.user),
        next_hour_due=next_hour_due(request.user),
        next_six_hours_due=next_six_hours_due(request.user),
        next_day_due=next_day_due(request.user),
        next_week_due=next_week_due(request.user),
        next_month_due=next_month_due(request.user),                
        ))




