from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            user = authenticate(request, username = cd["username"], password = cd["password"]) 
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("Вы вошли в систему")
                else: 
                    return HttpResponse("Вы где-то накосячили")
            else:
                return HttpResponse("You shall not pass")
    else:
        form = LoginForm()
    return render (request, 'account/login.html', {'form':form})