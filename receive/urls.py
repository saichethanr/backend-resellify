from django.urls import path
from .views import RegisterUserView,LoginUserView,ProductView,CustomerOrdersView,MerchantOrdersView
urlpatterns = [
    path('register/',RegisterUserView.as_view()),
    path('login/',LoginUserView.as_view()),
    path('addproduct/',ProductView.as_view()),
    path('corders/',CustomerOrdersView.as_view()),
    path('morders/',MerchantOrdersView.as_view())
]
