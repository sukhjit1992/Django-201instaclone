from django.contrib.auth.models import User
from django.views.generic import DetailView

class ProfileDetailView(DetailView):
    http_method_name= ["get"]
    template_name= "profiles/detail.html"
    model= User
    context_object_name= "user"
    slug_field = "username"
    slug_url_kwarg= "username"

