from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import CharField
from django.urls import reverse
from taggit.managers import TaggableManager
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save 


class CustomUser(AbstractUser):
    user_type_data = ((1,'Admin'), (2,'User'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
 
 
class BlogAdmin(models.Model):
    id = models.AutoField(primary_key=True)  
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=225)
    profile_pic = models.ImageField(blank=True, null=True, default=None, upload_to='admin_img/')
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.admin.username
    
    
class BlogUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  
    profile_pic = models.ImageField(blank=True, null=True, default=None, upload_to='user_img/')
    phone_no = models.CharField(max_length=225)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length= 225)
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()   
 
     
class PublishedManager(models.Manager):
     def get_queryset(self):
         return super().get_queryset().filter(status=Post.Status.PUBLISHED)
     
class TrendingManager(models.Manager):
     def get_queryset(self):
         return super().get_queryset().filter(status=Post.Status.TRENDING)    
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        TRENDING = 'TRENDING', 'Trending'
    class Categories(models.TextChoices):
        HTML = 'HTML', 'Html'
        CSS = 'CSS', 'Css'
        JAVASCRIPTS = 'JS', 'JavaScripts'
        PYTHON = 'PYTHON', 'Python'
        DJANGO = 'DJANGO', 'django'
    title = models.CharField(max_length=250)
    author = models.ForeignKey(BlogAdmin, on_delete=models.CASCADE)
    body = models.TextField()
    extra = models.TextField()
    image= models.ImageField(blank=True, null=True, default=None, upload_to='blog_img/')
    video = models.FileField(default=None, upload_to='blog_vid/')
    categories = models.CharField(max_length=10, choices=Categories.choices)
    status = models.CharField(max_length=10, choices=Status.choices)
    publish = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishedManager()
    trending = TrendingManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-publish',]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
         return reverse('blog:post_detail',args=[self.publish.year,
                                             self.publish.month,
                                             self.publish.day,
                                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    name = models.CharField(max_length=100)
    body = models.TextField()
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'     
    
    
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(created,instance,sender, **kwargs):
    if created:
        if instance.user_type ==1:
            BlogAdmin.objects.create(admin=instance, phone_no="", profile_pic="")
        if instance.user_type ==2:
            BlogUser.objects.create(admin=instance, profile_pic="", phone_no="",address="",date_of_birth="")  
            
@receiver(post_save, sender=CustomUser)  
def save_user_profile(instance,sender, **kwargs):
    if instance.user_type == 1:
        instance.blogadmin.save()
    if instance.user_type == 2:
        instance.bloguser.save()       