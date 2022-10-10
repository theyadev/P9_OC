from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models.Ticket import Ticket
from ..models.Review import Review


@login_required(login_url='/login')
def create_review_view(request, ticket_id=None):
    template = 'create_review.html'

    context = {}

    ticket = None

    if Ticket.objects.filter(id=ticket_id).exists():
        ticket = Ticket.objects.get(id=ticket_id)
        context['ticket'] = ticket

    if request.method == 'POST':
        headline = request.POST['headline']
        body = request.POST['body']
        rating = request.POST['rating']

        if not ticket:
            title = request.POST['title']
            description = request.POST['description']
            image = request.FILES.get('image', None)

            ticket = Ticket.objects.create(
                title=title,
                description=description,
                image=image,
                user=request.user
            )

        review = Review(
            ticket=ticket,
            user=request.user,
            headline=headline,
            body=body,
            rating=rating
        )

        review.save()

        return redirect('index')

    return render(request, template, context)
