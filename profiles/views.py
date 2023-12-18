
from django import http

from django.views.generic import DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User



from feed.models import Post
from follower.models import Follower
from profiles.models import Profile

class ProfileDetailView(DetailView):
    http_method_name= ["get"]
    template_name= "profiles/detail.html"
    model= User
    context_object_name= "user"
    slug_field = "username"
    slug_url_kwarg= "username"
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts']= Post.objects.filter(author=user).count
        context['total_follower'] = Follower.objects.filter(following=user).count
        return context

   


class FollowView(LoginRequiredMixin, View ):
    http_method_names = ["post"]
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missinng data")
        try:
            other_user= User.objects.get(username =data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        if data["action"]=="follow":
            follower,created = Follower.objects.get_or_create(
                followed_by=request.user,
                following = other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following= other_user,
                )
            except Follower.DoesNotExist:
                follower= None
            if follower:
                follower.delete()
        return JsonResponse({
            'success': True,
            'wording':"Unfollow" if data['action']== 'follow' else 'follow'
        })

class MyProfileView(LoginRequiredMixin, UpdateView):
    http_method_names=["get","put","post"]
    template_name="profile/myprofile.html"
    model = Profile
    fields=['name', 'tagline', 'id', 'image', 'cover']
    context_object_name="myprofile"
    slug_field="id"
    slug_url_kwarg="id"
    success_url="/"

    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user=self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user.user).count
        context['total_followers'] = Follower.objects.filter(following=user.user).count
        return context
    

