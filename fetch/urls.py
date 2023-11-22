from django.urls import path
from .views import ProductDetailsView,ReviewsView,IssuesView

urlpatterns = [
    path('products/',ProductDetailsView.as_view()),
    path('reviews/',ReviewsView.as_view()),
    path('issues/',IssuesView.as_view())
]
