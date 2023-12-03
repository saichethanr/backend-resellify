from django.urls import path
from .views import RegisterUserView,LoginUserView,ProductView,CustomerOrdersView,MerchantOrdersView,RaiseIssueView,ViewIssuesView,OrdersView,ReviewsView
urlpatterns = [
    path('register/',RegisterUserView.as_view()),
    path('login/',LoginUserView.as_view()),
    path('addproduct/',ProductView.as_view()),
    path('corders/',CustomerOrdersView.as_view()),
    path('morders/',MerchantOrdersView.as_view()),
    path('raiseissue/',RaiseIssueView.as_view()),
    path('getissues/',ViewIssuesView.as_view()),
    path('orders/',OrdersView.as_view()),
    path('reviews/',ReviewsView.as_view()),
]
