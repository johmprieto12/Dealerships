from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', views.get_dealerships, name='index'),

    # Auth routes
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration, name='register'),

    # Cars
    path('get_cars/', views.get_cars, name='getcars'),

    # Dealerships
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),

    # Dealer details & reviews
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),

    # Add review
    path('add_review', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
