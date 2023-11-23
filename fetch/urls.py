from django.urls import path
from .views import ProductDetailsView,ReviewsView,IssuesView,CategoryView

urlpatterns = [
    path('products/',ProductDetailsView.as_view()),
    path('reviews/',ReviewsView.as_view()),
    path('issues/',IssuesView.as_view()),
    path('categories/',CategoryView.as_view())
]
