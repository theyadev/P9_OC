from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    redirect_url = request.GET.get('next', '/')

    if request.user.is_authenticated:
        return redirect(redirect_url)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(redirect_url)
        else:
            return render(request, 'login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})

    return render(request, 'login.html')
