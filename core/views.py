from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf-password')
        if password == conf_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'User with email already exists')
                return HttpResponseRedirect(reverse('signup'))

            user = User.objects.create_user(email=email, password=password)
            login(request, user)  # Log the user in
            print(user.password)
            return HttpResponseRedirect(reverse('index'))  # Redirect to the user's profile or any other page
        else:
            messages.info(request, 'Passwords do not match')
            return HttpResponseRedirect(reverse('signup'))

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.info(request, 'Incorrect Password')
                return HttpResponseRedirect(reverse('signin'))

        else:
            messages.info(request, 'User does not exist')
            return HttpResponseRedirect(reverse('signin'))


    return render(request, 'signin.html')

