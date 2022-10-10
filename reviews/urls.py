from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('subscriptions', views.subscriptions_view, name='subscriptions'),
    path('create_ticket', views.create_ticket_view, name='create_ticket'),
    path('create_review', views.create_review_view, name='create_review'),
    path('create_review/<int:ticket_id>', views.create_review_view,
         name='create_review_by_ticket_id'),
    path('posts', views.posts_view, name='posts'),
]
