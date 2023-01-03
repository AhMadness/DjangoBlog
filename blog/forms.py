from django import forms
from django.forms import ModelForm, widgets
from .models import CommentPost, BlogPost, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("title", "subtitle", "category", "img", "body")
        widgets = {
            "title": forms.TextInput(attrs={'class':'form-control'}),
            "subtitle": forms.TextInput(attrs={'class':'form-control'}),
            "category": forms.Select(attrs={"class":"form-control"}),
            "body": forms.Textarea(attrs={'class':'form-control'}),
            "img": forms.FileInput(attrs={'class':'form-control'}),
        }
        
        
class CommentForm(ModelForm):
    class Meta:
        model = CommentPost
        fields = ["body",]
        widgets = {
            "body": forms.Textarea(attrs={'class':'form-control', 'rows':6, "placeholder":"Add a comment..."}),
        }
        def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)
            self.fields["body"].label = ""
            
            
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"example@example.com"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']  
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists!")
        return email   
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists! Please try another.")
        return username
   
      
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = 'form-control'
        
        self.fields["password1"].widget.attrs["class"] = 'form-control'
        self.fields["password1"].widget.attrs["placeholder"] = 'Must be 8 letters or more.'
        self.error_messages['password_mismatch'] = "Passwords did not match! Please try again."
        
        self.fields["password2"].label = "Confirm Password"
        self.fields["password2"].widget.attrs["class"] = 'form-control'
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
            
class ProfileForm(forms.ModelForm):
    pfp = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    bg = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control", 'rows':5, "placeholder":"Write something about yourself..."}))
    class Meta:
        model = UserProfile
        fields = ("pfp", "bg", "bio")
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["pfp"].label = "Profile Picture"
        self.fields["bg"].label = "Background Image"
        self.fields["bio"].label = "About Me"
        
    
class EditProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"example@example.com"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=None
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', "username", "email"] 
    
    
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "type":"password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "type":"password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "type":"password"}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', "new_password2"]
        
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].label = "Current Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm Password"

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
                self.fields[fieldname].help_text = None
                
                
class ContactForm(forms.Form):
    name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    subject = forms.CharField(max_length=64, widget=forms.TextInput(attrs={"class":"form-control"}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control", 'rows':5, "placeholder":"Write your message here..."}))