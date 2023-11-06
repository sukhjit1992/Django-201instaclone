from django.urls import path

# Create your views here.
from . import views
app_name = "feed"

urlpatterns = [
    path("", views.HomePage.as_view(), name = "index")
]