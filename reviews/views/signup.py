from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def signup_view(request):
    redirect_url = request.GET.get('to', '/')

    template = 'signup.html'

    if request.user.is_authenticated:
        return redirect(redirect_url)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, template, {'error': 'Les mots de passe ne correspondent pas.'})

        if User.objects.filter(username=username).exists():
            return render(request, template, {'error': 'Ce nom d\'utilisateur est déjà pris.'})

        if User.objects.filter(email=email).exists():
            return render(request, template, {'error': 'Cet email est déjà utilisé.'})

        user = User.objects.create_user(
            username=username, email=email, password=password)

        user.save()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(redirect_url)

    return render(request, template)
