from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', views.get_dealerships, name='index'),

    # Auth routes
    path(route='login/', view=views.login_user, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    path(route='register/', view=views.registration, name='register'),

    # Cars
    path(route='get_cars/', view=views.get_cars, name='get_cars'),

    # Dealerships
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
