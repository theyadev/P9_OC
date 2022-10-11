from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models.Ticket import Ticket
from ..models.Review import Review


@login_required(login_url='/login')
def create_review_view(request, ticket_id=None, review_id=None):
    template = 'create_review.html'

    context = {}

    ticket = None

    if Ticket.objects.filter(id=ticket_id).exists():
        ticket = Ticket.objects.get(id=ticket_id)
        context['ticket'] = ticket

    if review_id:
        if not Review.objects.filter(id=review_id).exists():
            return redirect('index')

        review = Review.objects.get(id=review_id)

        if not review.user == request.user:
            return redirect('index')

        ticket = review.ticket

        context['review'] = review
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

        if review_id:
            review.headline = headline
            review.body = body
            review.rating = rating
            review.save()
        else:
            Review.object.create(
                ticket=ticket,
                user=request.user,
                headline=headline,
                body=body,
                rating=rating
            )

        return redirect('index')

    return render(request, template, context)
