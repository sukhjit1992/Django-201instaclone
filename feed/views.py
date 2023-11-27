from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import CreateView
from .models import Post
from django.shortcuts import render
from django.contrib.auth.mixins import  LoginRequiredMixin

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
class CreateNewPost(CreateView, LoginRequiredMixin):
    template_name = "feed/create.html"
    model = Post
    fields = ["text"]
    success_url= "/"
    def dispatch(self, request, *arg, **kwarg):
        self.request = request
        return super().dispatch(request, *arg, **kwarg)
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save
        return super().form_valid(form)
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            text= request.POST.get("text"),
            author= request.user
        )
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type="application/html" 

        )
