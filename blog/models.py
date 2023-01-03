from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from ckeditor.fields import RichTextField

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# class UserProfiles(User):
#     bio = models.TextField(blank=True, null=True)
#     pfp = models.ImageField(verbose_name='Profile Picture', blank=True, null=True, upload_to="images/profile")
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    pfp = models.ImageField(verbose_name='Profile Picture', blank=True, null=True, upload_to="images/profile")
    bg = models.ImageField(verbose_name='Background Image', blank=True, null=True, upload_to="images/background")

    # For following 
    # follows = models.ManyToManyField("self", related_name="followed_by", blank=True, symmetrical=False,)  # if symmetrical is True it means that both must follow each other, as in the case of "add friend"
    
    # For website display
    # website = models.CharField(max_length=64, null=True, blank=True)
    # facebook = models.CharField(max_length=64, null=True, blank=True)
    # instagram = models.CharField(max_length=64, null=True, blank=True)
    
    # def __str__(self):
    #     return str(self.user)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    

class BlogPost(models.Model):
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128)
    # body = models.TextField()
    body = RichTextField()
    
    choices = [("general", "General"), ("philosophy", "Philosophy"), ("science", "Science"), 
                   ("history", "History"), ("politics", "Politics"), ("economics", "Economics"), ("other", "Other")]
    category = models.CharField(max_length=32, choices=choices)

    # slug = models.SlugField()
    # title_tag = models.CharField(max_length=32, default="Ahmad's Blog")  # This gives the title shown in the browser tab
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="blog_posts")
    img = models.ImageField(verbose_name='Image',blank=True, null=True, upload_to="images/")
    
    class Meta:
        verbose_name_plural = "Posts"
        
    def __str__(self):
        return self.title + " | " + self.author.username
    
    def total_likes(self):
        return self.likes.count()
    
    # class Meta:
    #     ordering = ('-date',)
    
    # def get_absolute_url(self):
    #     return reverse("home", kwargs={"pk": self.pk})
    

class CommentPost(models.Model):
    post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)  
    commentor = models.ForeignKey(User, related_name="commentor", on_delete=models.CASCADE) 
    body = models.TextField(verbose_name="", blank=False, null=False)
    # body = RichTextField(verbose_name="", blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.post.title} - {self.commentor.username} "