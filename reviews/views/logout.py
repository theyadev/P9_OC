from django.shortcuts import render, redirect
from django.contrib.auth import logout


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('index')
