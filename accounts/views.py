from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView,DetailView,UpdateView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Friendship
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .forms import ProfileForm



class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

class ProfileCreateView(CreateView):
    model = Profile
    template_name = "create_profile.html"
    fields = ["category", "first_name",'last_name','birth_date','profile_image']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.user.profile_user.posts.all()
        context['posts'] = posts
        return context
    

class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    fields = ['category','first_name','last_name','birth_date','profile_image',]
    

@login_required
def AddFriend(request, user_id):
    friend_profile = get_object_or_404(Profile, id=user_id)
    if request.method == 'POST':
        Friendship.objects.create(
            user1=request.user.profile_user,
            user2=friend_profile,
        )
        return redirect("profile_detail",pk= user_id)
    else:
        return HttpResponseBadRequest('Invalid request method')
    

@login_required
def deletefriend(request,user_id):
    friend_profile = get_object_or_404(Profile,id = user_id)
    if request.method == 'POST':
        try:
            frienship =  Friendship.objects.get(user2=request.user.profile_user,user1=friend_profile)
        except:
            frienship =  Friendship.objects.get(user1=request.user.profile_user,user2=friend_profile)
        frienship.delete()
    
    return redirect("profile_detail",pk = user_id,)
            

def search_users(request):
    name = request.GET['name_of_user']
    profiles = Profile.objects.filter(first_name = name)

    return render(request,'searched_users.html',{'profiles': profiles,'name':name})

