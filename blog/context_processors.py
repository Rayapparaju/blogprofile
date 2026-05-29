from .models import Category, Tag, Post


def blog_context(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    recent_posts = Post.objects.filter(status='published')[:5]
    return {
        'all_categories': categories,
        'all_tags': tags,
        'recent_posts': recent_posts,
    }
