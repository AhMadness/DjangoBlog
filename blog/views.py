from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, FormView, CreateView, ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy 
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from blog.models import BlogPost, CommentPost, UserProfile
from .forms import UserRegisterForm, CommentForm, PostForm, EditProfileForm, ChangePasswordForm, ProfileForm, ContactForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail

# Create your views here.

# HOMEPAGE

# def home(request):
#     posts = BlogPost.objects.all()
#     return render(request, "blog/home.html", context=posts)

class HomeView(ListView):
    template_name = "blog/home.html"
    model = BlogPost
    # queryset = BlogPost.objects.all()
    context_object_name = "posts"
    ordering = ["-date"]  # "-id" also works since latest post id is equal to previous post id + 1
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return BlogPost.objects.all().order_by("-date")
        else:
            following = self.request.user.userprofile.following.all()
            following_users = User.objects.filter(userprofile__in=following)
            # return BlogPost.objects.filter(author__in=following_users)
            return BlogPost.objects.filter(Q(author__in=following_users) | Q(author=self.request.user)).order_by("-date")
        
# ABOUT

# def about(requests):
#     return render(request, "blog/about.html")

class AboutView(TemplateView):
    template_name = "blog/about.html"
    
# CONTACT

# def contact(request):
#     return render(request, "blog/contact.html")
    
# class ContactView(TemplateView):
#     form_class = CommentForm
#     template_name = "blog/contact.html"
    
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            recipients = ['ahmad.jommaa95@gmail.com']
            send_mail(subject, message, email, recipients)
            return render(request, 'blog/contact.html', {'success': 'Message sent successfully'})
    else:
        if request.user.is_authenticated:
            initial_data = {
                'email': request.user.email,
                'name': request.user.get_full_name(),
            }
        else:
            initial_data = {}
        form = ContactForm(initial=initial_data)
    return render(request, 'blog/contact.html', {'form': form})

class PostView(FormMixin, DetailView):
    template_name = "blog/post.html"
    model = BlogPost
    context_object_name = "post"
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        
        likes = get_object_or_404(BlogPost, id=self.kwargs["pk"])
        total_likes = likes.total_likes()
        liked = False
        if likes.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        context['form'] = CommentForm(initial={'post': self.object})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.commentor = self.request.user
        comment = form.save(commit=False)
        comment.save()
        return redirect("blog:post_detail", self.object.id)
    
# CREATE POST
class NewPostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = PostForm
    template_name = "blog/new_post.html"
    # fields = ["title", "subtitle", "body"]  # Not required anymore because we taking form_class
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

# EDIT POST
class EditPostView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = PostForm
    template_name = "blog/edit_post.html"
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


# DELETE POST 
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blog/remove_post.html"
    context_object_name = "post"
    success_url = reverse_lazy("home")
    
    
# UPDATE COMMENT
def update_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(CommentPost, pk=comment_pk)
    if comment.commentor != request.user and request.user.id != 1:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_post.html', {"form":form})

    
# DELETE COMMENT
def delete_comment(request, post_pk, comment_pk):
    post = get_object_or_404(BlogPost, pk=post_pk)
    comment = get_object_or_404(CommentPost, pk=comment_pk, post=post)
    if comment.commentor != request.user and request.user.id != 1:
        # Return an error message if the comment was not made by the current user
        return HttpResponseForbidden()
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=post.pk)
    return render(request, 'blog/remove_post.html', {'comment': comment, "post":post})
    
    
# CATEGORY
# blog/category/<str:genre>
def CategoryView(request, genre):
    # all_categories = [category[1] for category in BlogPost.choices]
    list_by_category = BlogPost.objects.filter(category=genre).order_by("-date")
    return render(request, "blog/categories.html", {"genre":genre, "list_by_category":list_by_category})


# PROFILE
def ProfileView(request, username):
    user_posts = BlogPost.objects.filter(author__username=username).order_by("-date")
    num_posts = user_posts.count()
    host = User.objects.get(username=username)
    if request.user.is_authenticated:
        current_user = request.user.userprofile
    num_followers = host.userprofile.followers.count()
    num_following = host.userprofile.following.count()
    if request.method == "POST":
        action = request.POST["follow"]
        if action == "unfollow":
            user_profile = UserProfile.objects.get(user__username=username)
            current_user.following.remove(user_profile)
        elif action == "follow":
            user_profile = UserProfile.objects.get(user__username=username)
            current_user.following.add(user_profile)
        return redirect("blog:user_posts", host.username)
    return render(request, "blog/user_posts.html", {"username":username, "user_posts":user_posts, "host":host, 'num_posts':num_posts, 'num_followers':num_followers, 'num_following':num_following})

# FOLLOWERS

def FollowersView(request, username):
    host = User.objects.get(username=username)
    host_profile = UserProfile.objects.get(user=host)
    followers = host_profile.followers.all()
    current_user = request.user.userprofile

    for follower in followers:
        follower.num_posts = BlogPost.objects.filter(author=follower.user).count()
        follower.num_followers = follower.user.userprofile.followers.count()
        follower.num_following = follower.user.userprofile.following.count()
        
    if request.method == "POST":
        action = request.POST.get("follow")
        follower_id = request.POST.get("follower_id")
        follower_user = UserProfile.objects.get(id=follower_id)
        if action == "unfollow":
            current_user.following.remove(follower_user)
        elif action == "follow":
            current_user.following.add(follower_user)
        current_user.save()
        return redirect("blog:followers", host.username)

    return render(request, "blog/followers.html", {"username":username, "host":host, "followers": followers, "current_user": current_user})

# FOLLOWING

def FollowingView(request, username):
    host = User.objects.get(username=username)
    host_profile = UserProfile.objects.get(user=host)
    following = host_profile.following.all()
    current_user = request.user.userprofile

    for follows in following:
        follows.num_posts = BlogPost.objects.filter(author=follows.user).count()
        follows.num_followers = follows.user.userprofile.followers.count()
        follows.num_following = follows.user.userprofile.following.count()

    if request.method == "POST":
        action = request.POST.get("follow")
        following_id = request.POST.get("following_id")
        following_user = UserProfile.objects.get(id=following_id)
        if action == "unfollow":
            current_user.following.remove(following_user)
        elif action == "follow":
            current_user.following.add(following_user)
        current_user.save()
        return redirect("blog:following", host.username)

    return render(request, "blog/following.html", {"username":username, "host":host, "following": following, "current_user": current_user})


# LIKE
def LikeView(request, pk):
    post = get_object_or_404(BlogPost, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("blog:post_detail", args=[int(pk)]))


# REGISTER
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = 'Account created successfully! Please login.'
    
    
# Edit PROFILE
class UserEditView(UpdateView):
    pass
#     form_class = EditProfileForm
#     template_name = "registration/edit_profile.html"
#     # success_url = reverse_lazy("home")
    
#     def get_success_url(self):
#         return reverse_lazy('blog:user_posts', kwargs={'username': self.object.username})
    
#     def get_object(self):
#         return self.request.user
    
    
# Edit Profile with UserProfile fields
@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == "POST":
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)   
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            current_user = request.user.username
            return redirect('blog:user_posts', current_user)
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, "registration/edit_profile.html", {"user_form":user_form, "profile_form": profile_form})


# CHANGE PASSWORD 
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = ChangePasswordForm
    success_url = reverse_lazy("login")
    success_message = 'Password changed successfully! Please login.'

    def form_valid(self, form):
        form.save()
        self.request.session.flush()
        logout(self.request)
        return super().form_valid(form)
    

from django.db.models import Q
def search(request):
    query = request.GET.get("query", "")
    posts = BlogPost.objects.filter(Q(title__icontains=query) | Q(subtitle__icontains=query) | Q(body__icontains=query) | Q(author__username__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query) | Q(category__icontains=query))
    return render(request, "blog/search.html", {"posts":posts, "query":query})
    
    
# PERSONAL SITE
class PersonalSite(TemplateView):
    template_name = "blog/personal_site.html"