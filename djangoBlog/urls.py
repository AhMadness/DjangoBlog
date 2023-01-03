# PROJECT-LEVEL URLS

from django.contrib import admin
# from django.contrib.auth import views as auth_views
from django.urls import path, include

from blog.views import HomeView, SignUpView, UserEditView, ChangePasswordView, PersonalSite, edit_profile

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("", HomeView.as_view(), name="home"),
    
    # Accounts
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup", SignUpView.as_view(), name="signup"),
    # path("accounts/edit_profile", UserEditView.as_view(), name="edit_profile"), 
    path("accounts/edit_profile/", edit_profile, name="edit_profile"),
    
    # path("accounts/password", auth_views.PasswordChangeView.as_view(template_name="registration/change_password.html")),  
    path("accounts/password/", ChangePasswordView.as_view(template_name="registration/change_password.html"), name="change_password"),  
    
    # Site
    path("personal_site/", PersonalSite.as_view(), name="personal_site"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
