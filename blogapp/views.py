from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from blogapp.models import Post, Comment, CustomUser
from blogapp.forms import CommentForm,ShareForm,SearchForm
from django.views.decorators.http import require_POST
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout
from django.urls import reverse
from adminapp.EmailBackEnd import EmailBackEnd
from django.core.mail import EmailMessage
from django.contrib.postgres.search import SearchVector,SearchRank,SearchQuery

# Create your views here.
def index(request):
     sliders = Post.objects.all().order_by('-publish')[:5]
     css_single = Post.objects.get(title="Designing Webpages with CSS")
     html_single = Post.objects.get(title="HTMl For Beginners")
     # js_single = Post.objects.get(title="Arithmetic in JavaScript")
     search_form = SearchForm()
     html_posts = Post.published.filter(categories="HTML")[:3]
     html_trending = Post.trending.filter(categories="HTML")[:3]
     css_trending = Post.trending.filter(categories="CSS")[:2]
     css_publish = Post.published.all().order_by('?')
     trending_posts = Post.trending.all().order_by('?')
     paginator = Paginator(trending_posts, 4)
     page_number = request.GET.get("page")
     page_object = paginator.get_page(page_number)
     
     return render(request, 'blog_templates/index.html', {
                                                          'html_trending':html_trending,'html_single':html_single,'html_posts':html_posts,'css_trending':css_trending,'sliders':sliders,
                                                          'css_publish':css_publish,'css_single':css_single,'page_object':page_object,'search_form':search_form})

def post_detail(request,year,month,day,post):
     post= get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)
     comments = post.comment.filter(active=True)
     search_form = SearchForm()
     share_form = ShareForm()
     form = CommentForm()
     post_tags_ids = post.tags.values_list('id', flat=True)
     similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
     similars = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
     return render(request, 'blog_templates/single-post.html', {'post':post,'form':form,'comments':comments,'share_form':share_form,'similars':similars,'search_form':search_form})

def categories(request, tag_slug=None):
     search_form = SearchForm()
     query = None
     results = []
     if 'query' in request.GET:
          search_form = SearchForm(request.GET)
          if search_form.is_valid():
               query = search_form.cleaned_data['query']
               # form is cleaned and ready for process
               search_vector = SearchVector('title',weight='A') + SearchVector('body', weight='B')
               # search for words in the title and body
               search_query = SearchQuery(query)
               results = Post.objects.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                    ).filter(rank__gte=0.3).order_by('-rank') 
     search_paginator = Paginator(results, 4) # show 5 posts per page.
     search_page_number = request.GET.get('page')
     try:
          search_page_object = search_paginator.get_page(search_page_number)
     except PageNotAnInteger: # if it has no ID of a number returns to the first page
          search_page_object = search_paginator.page(1)
     except EmptyPage: # if it is out of range return to the last page
          search_page_object = search_paginator.page(search_paginator.num_pages)      
     all_posts = Post.objects.all().order_by('?')
     tag = None
     if tag_slug:
          tag = get_object_or_404(Tag, slug=tag_slug)
          all_posts = all_posts.filter(tags__in=[tag])
     paginator = Paginator(all_posts, 4) # show 5 posts per page.
     
     page_number = request.GET.get('page')
     try:
          page_object = paginator.get_page(page_number)
     except PageNotAnInteger: # if it has no ID of a number returns to the first page
         page_object = paginator.page(1)
     except EmptyPage: # if it is out of range return to the last page
          page_object = paginator.page(paginator.num_pages)  
     return render(request, 'blog_templates/category.html', {'page_object':page_object,'search_page_object':search_page_object,'tag':tag,'search_form':search_form,'query':query,'results':results})

def share_post(request, post_id):
     post = get_object_or_404(Post, id=post_id)
     sent = False
     if request.method == 'POST':
          form = ShareForm(request.POST)
          if form.is_valid():
               cd = form.cleaned_data
               post_url = request.build_absolute_uri(
                    post.get_absolute_url()
               )
               subject = f="{['name']} Recommends you read " f"{post.title}"
               message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
               em = EmailMessage(subject, message, to=[cd['to']])
               em.send()
               sent = True
          else:
               form = ShareForm()     
               return render(request, 'blog_templates/single-post.html', {'post':post, 'form':form})
          
def html(request):
     search_form = SearchForm()
     html_posts = Post.objects.filter(categories='HTML')
     paginator = Paginator(html_posts, 6)
     page_number = request.GET.get('page')
     try:
          page_object = paginator.get_page(page_number)
     except PageNotAnInteger:
          page_object = paginator.page(1)
     except EmptyPage:
          page_object = paginator.page(paginator.num_pages)          
     
     return render(request, 'blog_templates/categories/html.html', {'html_posts':html_posts,'page_object':page_object,'search_form':search_form})

def css(request):
     search_form = SearchForm()
     css_posts = Post.objects.filter(categories='CSS')
     paginator = Paginator(css_posts, 6)
     page_number = request.GET.get('page')
     try:
          page_object = paginator.get_page(page_number)
     except PageNotAnInteger:
          page_object = paginator.page(1)
     except EmptyPage:
          page_object = paginator.page(paginator.num_pages)          
     
     return render(request, 'blog_templates/categories/css.html', {'css_posts':css_posts,'page_object':page_object,'search_form':search_form})

def js(request):
     search_form = SearchForm()
     js_posts = Post.objects.filter(categories='JS')
     paginator = Paginator(js_posts, 6)
     page_number = request.GET.get('page')
     try:
          page_object = paginator.get_page(page_number)
     except PageNotAnInteger:
          page_object = paginator.page(1)
     except EmptyPage:
          page_object = paginator.page(paginator.num_pages)          
     
     return render(request, 'blog_templates/categories/js.html', {'js_posts':js_posts,'page_object':page_object,'search_form':search_form})

def python(request):
     search_form = SearchForm()
     python_posts = Post.objects.filter(categories='PYTHON')
     paginator = Paginator(python_posts, 6)
     page_number = request.GET.get('page')
     try:
          page_object = paginator.get_page(page_number)
     except PageNotAnInteger:
          page_object = paginator.page(1)
     except EmptyPage:
          page_object = paginator.page(paginator.num_pages)          
     
     return render(request, 'blog_templates/categories/python.html', {'python_posts':python_posts,'page_object':page_object,'search_form':search_form})

def django(request):
     search_form = SearchForm()
     django_posts = Post.objects.filter(categories='DJANGO')
     paginator = Paginator(django_posts, 6)
     page_number = request.GET.get('page')
     try:
          page_object = paginator.get_page(page_number)
     except PageNotAnInteger:
          page_object = paginator.page(1)
     except EmptyPage:
          page_object = paginator.page(paginator.num_pages)          
     
     return render(request, 'blog_templates/categories/django.html', {'django_posts':django_posts,'page_object':page_object,'search_form':search_form})

def about(request):
     search_form = SearchForm()
     return render(request, 'blog_templates/about.html', {'search_form':search_form})

def contact(request):
    search_form = SearchForm()
    return render(request, 'blog_templates/contact.html', {'search_form':search_form})

@require_POST
def post_comment(request, post_id):
     post = get_object_or_404(Post, id=post_id)
     comment = None
     form = CommentForm(data=request.POST)
     if form.is_valid():
          comment = form.save(commit=False)
          comment.post = post
          comment.save()
     return render(request, 'blog_templates/single-post.html',{'post':post,'form':form,'comment':comment})

def user_login(request):
     return render(request, 'blog_templates/login.html')

def DoLogin(request):
    if request.method != "POST":
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        user = EmailBackEnd.authenticate(request,username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None:
            login(request, user)
            if user.user_type =="1":
                return HttpResponseRedirect(reverse("blog_admin:admin_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect(reverse("blog:login"))
 
def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/')     