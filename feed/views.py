from django.views.generic import ListView
from .models import Post

# Create your views here.
class HomePage(ListView):
    http_method_name = ["get"]
    template_name= homepage.html
    model = Post
    context_object_name= "posts"
    queryset = Post.objects.all().order_by("-id")[0:30]
