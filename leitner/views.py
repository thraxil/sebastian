# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from forms import AddFaceForm

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


# @login_required
# def add_image(request):
#     if request.method == "POST":
#         if request.POST.get("slug","") == "":
#             request.POST['slug'] = slugify(request.POST.get("title"))
#         form = AddImageForm(request.POST,request.FILES)
#         if form.is_valid():
#             img = form.save()
#             for key in request.POST.keys():
#                 if key.startswith("gallery_"):
#                     g = get_object_or_404(Gallery,id=key[len("gallery_"):])
#                     img.add_to_gallery(g)
#             return HttpResponseRedirect(img.get_absolute_url())
#         else:
#             print "not valid"
#             galleries = Gallery.objects.all()
#             return render_to_response("add_image.html",dict(galleries=galleries,
#                                                             form=form))
#     else:
#         galleries = Gallery.objects.all()
#         return render_to_response("add_image.html",dict(galleries=galleries,
#                                                    form=AddImageForm()))

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

        front_form = AddFaceForm(request.POST,request.FILES,prefix="front")
        back_form = AddFaceForm(request.POST,request.FILES,prefix="back")
        if front_form.is_valid() and back_form.is_valid():
            front = front_form.save()
            back = back_form.save()
            card = Card.objects.create(front=front,back=back)
            dc = DeckCard.objects.create(deck=deck,card=card)
            uc = UserCard.objects.create(card=card,user=request.user,
                                         due=datetime.now(),
                                         priority=int(request.POST.get('priority','1')))
            return HttpResponseRedirect("/add_card/")
    else:
        front_form = AddFaceForm(prefix="front")
        back_form = AddFaceForm(prefix="back")
    return render_to_response("add_card.html",dict(decks=user_decks(request.user),
                                                   front=front_form,back=back_form))

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

def munin_due(request):
    # hardcode for now
    user = get_object_or_404(User,username='anders')
    if request.GET.get('config',False):
        return HttpResponse("""graph_title Cards Due
graph_vlabel cards
graph_category Sebastian
total_due.label Cards Due
""")
    else:
        return HttpResponse("total_due.value " + str(total_due(user)))

def munin_percent(request):
    # hardcode for now
    user = get_object_or_404(User,username='anders')
    if request.GET.get('config',False):
        return HttpResponse("""graph_title Percent Correct
graph_vlabel %
graph_category Sebastian
graph_args --upper-limit 100 -l 0
graph_scale no
percent_right.label Percent Right
""")
    else:
        return HttpResponse("percent_right.value " + str(percent_right(user)))

def munin_tested(request):
    # hardcode for now
    user = get_object_or_404(User,username='anders')
    if request.GET.get('config',False):
        return HttpResponse("""graph_title Tested
graph_vlabel cards
graph_category Sebastian
graph_args -l 0
total_tested.label Total Tested
total_tested.draw AREA
total_untested.label Total Untested
total_untested.draw STACK
""")
    else:
        return HttpResponse("total_tested.value " + str(total_tested(user)) + "\n"\
                                + "total_untested.value " + str(total_untested(user)))

def munin_rungs(request):
    # hardcode for now
    user = get_object_or_404(User,username='anders')
    rungs = list(rungs_stats(user))
    rungs.sort(lambda a,b: cmp(b['rung'],a['rung']))
    if request.GET.get('config',False):
        return HttpResponse("""graph_title Rungs
graph_vlabel cards
graph_category Sebastian
rung10.label Rung 10
rung10.draw AREA
rung9.label Rung 9
rung9.draw STACK
rung8.label Rung 8
rung8.draw STACK
rung7.label Rung 7
rung7.draw STACK
rung6.label Rung 6
rung6.draw STACK
rung5.label Rung 5
rung5.draw STACK
rung4.label Rung 4
rung4.draw STACK
rung3.label Rung 3
rung3.draw STACK
rung2.label Rung 2
rung2.draw STACK
rung1.label Rung 1
rung1.draw STACK
rung0.label Rung 0
rung0.draw STACK
""")
    else:
        parts = []
        for rung in rungs:
            parts.append("rung%d.value %d" % (rung['rung'],rung['cards']))
        return HttpResponse("\n".join(parts))

def munin_ease(request):
    # hardcode for now
    user = get_object_or_404(User,username='anders')
    ease = list(ease_stats(user))
    ease.sort(lambda a,b: cmp(b['ease'],a['ease']))
    if request.GET.get('config',False):
        return HttpResponse("""graph_title Ease
graph_vlabel cards
graph_category Sebastian
ease10.label Ease 10
ease10.draw AREA
ease9.label Ease 9
ease9.draw STACK
ease8.label Ease 8
ease8.draw STACK
ease7.label Ease 7
ease7.draw STACK
ease6.label Ease 6
ease6.draw STACK
ease5.label Ease 5
ease5.draw STACK
ease4.label Ease 4
ease4.draw STACK
ease3.label Ease 3
ease3.draw STACK
ease2.label Ease 2
ease2.draw STACK
ease1.label Ease 1
ease1.draw STACK
ease0.label Ease 0
ease0.draw STACK
""")
    else:
        parts = []
        for e in ease:
            parts.append("ease%d.value %d" % (e['ease'],e['cards']))
        return HttpResponse("\n".join(parts))

