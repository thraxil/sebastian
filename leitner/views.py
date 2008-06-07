# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *

def index(request):
    return render_to_response("index.html",dict())

