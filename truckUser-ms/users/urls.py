
from django.urls import path
from .views import RegisterView,LoginView

urlpatterns = [
    path('registertruck',RegisterView.as_view()),
    path('logintruck',LoginView.as_view()),
    
]
