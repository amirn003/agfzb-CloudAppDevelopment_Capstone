from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    #path(route='', view=views.get_index, name='index'),

    path('', views.get_dealerships, name='index'),
    path('view/', views.static_page, name='my-view'),

    # path for about view
    path('about/', views.about, name='about'),
    # path for contact us view
    path('contact/', views.contact, name='contact'),
    # path for registration
    path('registration/', views.registration_request, name='registration'),
    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    #path('dealer/', views.get_dealerships, name='dealer'),

    path('dealership/<int:dealer_id>/', views.get_dealership_by_id, name='dealer_details'),
    # path for dealer reviews view

    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),
    #path('dealer/add_review/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
