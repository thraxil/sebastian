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
    return render_to_response("test.html",dict(card=next_card(request.user)))

@login_required
def add_card(request):
    if request.method == "POST":
        deck_name = request.POST.get("deck","no deck")
        try:
            deck = Deck.objects.get(name=deck_name)
            print "retrieved deck"
        except ObjectDoesNotExist:
            print "creating deck"
            deck = Deck.objects.create(name=deck_name)

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
        return render_to_response("add_card.html",dict())

@login_required
def stats(request):
    return render_to_response("stats.html",dict())




