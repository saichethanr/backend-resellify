from django.urls import path
from .views import RegisterUserView,LoginUserView,ProductView
urlpatterns = [
    path('register/',RegisterUserView.as_view()),
    path('login/',LoginUserView.as_view()),
    path('addproduct/',ProductView.as_view())
]
