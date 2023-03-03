from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from blogapp.models import Post,Comment,CustomUser
from blogapp.models import BlogAdmin
from django.db.models import Count,Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Create your views here    

@login_required(login_url="/login")
def  home(request):
    user = CustomUser.objects.get(id=request.user.id)
    author_id = BlogAdmin.objects.get(admin=user)
    post_count= Post.objects.filter(author=author_id).count()
    commment_count = Comment.objects.filter(post=post_count).count()
    
    html_posts = Post.objects.filter(categories="HTML").order_by('-publish')[:5]
    css_posts = Post.objects.filter(categories="CSS").order_by('-publish')[:5]
    js_posts = Post.objects.filter(categories="JS").order_by('-publish')[:5]
    python_posts = Post.objects.filter(categories="PYTHON").order_by('-publish')[:5]
    django_posts = Post.objects.filter(categories="DJANGO").order_by('-publish')[:5]
    html_count = html_posts.count()
    css_count = css_posts.count()
    js_count = js_posts.count()
    python_count = python_posts.count()
    django_count = django_posts.count()
    
    return render(request,'admin_templates/index.html', {
        'author_id':author_id,'post_count':post_count,'commment_count':commment_count,'html_posts':html_posts,'html_count':html_count,'css_posts':css_posts,'css_count':css_count,'user':user,
        'js_posts':js_posts,'js_count':js_count,'python_posts':python_posts,'python_count':python_count,'django_posts':django_posts,'django_count':django_count,})

@login_required(login_url="/login")    
def add_post(request):
    users=Post.objects.filter(author=request.user.id)
    author_obj=BlogAdmin.objects.get(admin=request.user.id)
    blog_status = Post.Status.values
    categories = Post.Categories.labels
    posts = Post.objects.all()
    return render(request, 'admin_templates/add_post.html', {'users':users,'author_obj':author_obj,'blog_status':blog_status,'posts':posts})      
    
@login_required(login_url="/login")
@csrf_exempt   
def save_post(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        title = request.POST.get("title")
        author_name = request.POST.get("author_name")
        post_body = request.POST.get("post_body")
        extra_body= request.POST.get("extra_body")
        post_video= request.POST.get("post_video")
        categories= request.POST.get("categories")
        status= request.POST.get("status")
        publish_date= request.POST.get("status")
        slug= request.POST.get("slug")
        tags= request.POST.get("tags")
        #saving files in  form
        post_pic=request.FILES['post_image']
        fs=FileSystemStorage()
        pic_file=fs.save(post_pic.name,post_pic)
        post_pic_url=fs.url(pic_file)
        
        post_vid=request.FILES['post_video']
        fs=FileSystemStorage()
        vid_file=fs.save(post_vid.name,post_vid)
        post_vid_url=fs.url(vid_file)
        # try:
        author_id = BlogAdmin.objects.filter(admin=author_name)
        post = Post.objects.create(
            title=title,
            author =author_name,
            body=  post_body,
            extra=extra_body,
            image=post_pic_url,
            video=post_vid_url,
            categories=categories,
            status=status,
            publish=publish_date,
            slug=slug,
            tags=tags
        )
        post.save()
        messages.success(request,"Successfully Added Post")
        return HttpResponseRedirect(reverse("blog_admin:add_post"))
        # except:
        #     messages.error(request,"Failed to Add Post")
        #     return HttpResponseRedirect(reverse("blog_admin:add_post"))
             
@login_required(login_url="/login")
@csrf_exempt
def check_title_exist(request):
    title = request.POST.get('title')
    post_obj =  Post.objects.filter(title=title).exists()
    if post_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)    
    
@login_required(login_url="/login")
def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin_id = BlogAdmin.objects.get(admin=user)
    post_count= Post.objects.filter(author=request.user.id).count()
    commment_count = Comment.objects.filter(post=post_count).count()
    return render(request, 'admin_templates/admin_profile.html', {'user':user,'admin_id':admin_id,'post_count':post_count,'comment_count':commment_count})   

@login_required(login_url="/login")
def edit_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    admin = BlogAdmin.objects.get(admin=user)
    return render(request, 'admin_templates/edit-profile.html', {'user':user,'admin':admin})

@login_required(login_url="/login")
def save_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("blog_admin:edit_profile"))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone_num = request.POST.get('phone_num')
        if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
        else:
            profile_pic_url=None
        # try:
        user= CustomUser.objects.get(id=request.user.id)
        user.first_name= first_name
        user.last_name= last_name
        if password!= None and password!="":
            user.set_password(password)
        user.save()  
            #### saving admin data via admin user
        admin =  BlogAdmin.objects.get(id=user.id)
        admin.phone_no = phone_num
        if profile_pic_url!= None:
            admin.profile_pic = profile_pic_url
        admin.save()   
        messages.success(request, "Profiled Saved!")
        return HttpResponseRedirect(reverse("blog_admin:edit_profile"))
        # except:
        #     messages.error(request, "Profiled Failed To Saved!")
        #     return HttpResponseRedirect(reverse("blog_admin:edit_profile"))