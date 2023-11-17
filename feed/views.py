from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class HomePage(ListView):
    http_method_name = ["get"]
    template_name= "feed/homepage.html"
    model = Post
    context_object_name= "posts"
    queryset = Post.objects.all().order_by("-id")[0:30]
class PostDetailView(DetailView):
    http_method_name=["get"]
    template_name="feed/detail.html"
    model = Post
    context_object_name ="post"