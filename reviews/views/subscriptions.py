from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from ..models.UserFollows import UserFollows


@login_required(login_url='/login')
def subscriptions_view(request):
    template = 'subscriptions.html'

    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)

    context = {
        'following': following,
        'followers': followers,
    }

    if request.method == 'POST':
        if not User.objects.filter(username=request.POST['username']).exists():
            context['error'] = 'Cet utilisateur n\'existe pas.'

            return render(request, template, context)

        selected_user = User.objects.get(username=request.POST['username'])

        if selected_user == request.user:
            context['error'] = 'Vous ne pouvez pas vous suivre vous-même.'

            return render(request, template, context)

        follow_line = UserFollows.objects.filter(
            user=request.user, followed_user=selected_user).exists()

        if 'follow' in request.POST:
            if follow_line:
                context['error'] = 'Vous suivez déjà cet utilisateur.'

                return render(request, template, context)

            UserFollows.objects.create(
                user=request.user, followed_user=selected_user)
        elif 'unfollow' in request.POST:
            if not follow_line:
                context['error'] = 'Vous ne suivez pas cet utilisateur.'

                return render(request, template, context)

            UserFollows.objects.get(
                user=request.user, followed_user=selected_user).delete()

        following = UserFollows.objects.filter(user=request.user)
        context['following'] = following

    return render(request, template, context)
