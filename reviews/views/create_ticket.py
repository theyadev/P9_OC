from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models.Ticket import Ticket


@login_required(login_url='/login')
def create_ticket_view(request):
    template = 'create_ticket.html'

    context = {}

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image', None)

        if not title:
            context['error'] = 'Le titre est obligatoire.'

        if not description:
            context['error'] = 'La description est obligatoire.'

        if context.get('error', False):
            return render(request, template, context)

        Ticket.objects.create(
            title=title, description=description, user=request.user, image=image)

        return redirect('index')

    return render(request, template)
