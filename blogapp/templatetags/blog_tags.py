from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('blog_templates/sidebar/trending.html')
def show_trending_post(count=6):
    trending_posts = Post.trending.all().order_by('?')[:count]
    return{'trending_posts':trending_posts }

@register.inclusion_tag("blog_templates/sidebar/latest.html")
def show_latest_posts(count=6):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return { 'latest_posts':latest_posts }

@register.inclusion_tag("blog_templates/sidebar/base.html")
def show_recent_posts(count=3):
    recent_posts = Post.objects.all().order_by('-publish')[:count]
    return { 'recent_posts':recent_posts }

@register.simple_tag
def get_most_commented_post(count=6):
    return Post.objects.annotate(total_comments=Count('comment')).order_by('-total_comments')[:count]