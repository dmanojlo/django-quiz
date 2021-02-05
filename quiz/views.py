from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F #F() expressions are good for memory
from django.core.mail import send_mail

# Create your views here.



# Create your views here.

def home_view(request):
    return render(request, 'quiz/home.html', {})
