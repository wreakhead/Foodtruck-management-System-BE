
from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,AddTruck

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('admin',UserView.as_view()),
    path('logout',LogoutView.as_view()),
    path('addtruck',AddTruck.as_view())
]
