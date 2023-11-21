from django.urls import path
from .views import ProductDetailsView

urlpatterns = [
    path('products/',ProductDetailsView.as_view())
]
