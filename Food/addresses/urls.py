from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AddressView
from . import views


urlpatterns = [
    
    path('home/', AddressView.as_view(), name='home'),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='addresses/login.html'), name='login'),   
    path('logout/', views.logout, name='logout'),
    path('addngo/', views.addngo, name='addngo'),
    path('addevent/', views.addevent, name='addevent'),
    path('ngohome/', views.ngohome, name='ngohome'),
    path('eventhome/', views.eventhome, name='eventhome'),
    path('deleteevent/<ename>/', views.deleteevent, name='deleteevent'),
]
