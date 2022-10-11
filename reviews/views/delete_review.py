from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models.Review import Review


@login_required(login_url='/login')
def delete_review_view(request, review_id):
    next_path = request.GET.get('next', 'index')

    if not review_id:
        return redirect('index')

    if not Review.objects.filter(id=review_id).exists():
        return redirect('index')

    review = Review.objects.get(id=review_id)

    if not review.user == request.user:
        return redirect('index')

    review.delete()

    return redirect(next_path)
