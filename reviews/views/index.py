from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value, Q
from django.shortcuts import render

from itertools import chain

from ..models.Ticket import Ticket
from ..models.Review import Review
from ..models.UserFollows import UserFollows


def get_users_viewable_reviews(user):
    if not user.is_authenticated:
        return Ticket.objects.none()

    follows = [x['followed_user_id'] for x in UserFollows.objects.filter(
        user=user).values('followed_user_id')]
    return Review.objects.filter(Q(user=user) | Q(ticket__user=user) | Q(user__in=follows))


def get_users_viewable_tickets(user):
    if not user.is_authenticated:
        return Ticket.objects.none()

    follows = [x['followed_user_id'] for x in UserFollows.objects.filter(
        user=user).values('followed_user_id')]
    return Ticket.objects.filter(Q(user=user) | Q(user__in=follows))


@login_required(login_url='/login')
def index_view(request):
    template = 'index.html'

    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        'posts': posts
    }

    return render(request, template, context)
