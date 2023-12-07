from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from feed.models import Post
from django.http import JsonResponse
from follower.models import Follower  


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


