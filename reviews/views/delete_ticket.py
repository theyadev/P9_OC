from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models.Ticket import Ticket


@login_required(login_url='/login')
def delete_ticket_view(request, ticket_id):
    next_path = request.GET.get('next', 'index')

    if not ticket_id:
        return redirect('index')

    if not Ticket.objects.filter(id=ticket_id).exists():
        return redirect('index')

    ticket = Ticket.objects.get(id=ticket_id)

    if not ticket.user == request.user:
        return redirect('index')

    ticket.review.all().delete()
    ticket.delete()

    return redirect(next_path)
