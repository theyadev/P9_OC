from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.shortcuts import render

from itertools import chain

from ..models.Ticket import Ticket
from ..models.Review import Review


def get_users_viewable_reviews(user):
    if not user.is_authenticated:
        return Ticket.objects.none()

    return Review.objects.filter(user=user)


def get_users_viewable_tickets(user):
    if not user.is_authenticated:
        return Ticket.objects.none()
    return Ticket.objects.filter(user=user)


@login_required(login_url='/login')
def posts_view(request):
    template = 'posts.html'

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
