from django.urls import path
from .views import signup_func

urlpatterns = [
    path('signup/', signup_func),
]