from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Post, Category, Tag, Comment, Like, ContactMessage
from .forms import PostForm, CategoryForm, TagForm, CommentForm, ContactForm
from .decorators import admin_login_required


# ===================== PUBLIC VIEWS =====================

def home(request):
    featured_posts = Post.objects.filter(status='published', is_featured=True)[:3]
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'page_title': 'Home',
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.views += 1
    post.save()

    comments = post.comments.filter(is_active=True)
    comment_form = CommentForm()

    liked = False
    if 'like_session' in request.session:
        liked = Like.objects.filter(post=post, session_key=request.session['like_session']).exists()

    if request.method == 'POST':
        if 'like' in request.POST:
            if not liked:
                Like.objects.create(post=post, session_key=request.session.session_key or '')
                liked = True
                request.session['like_session'] = request.session.session_key or ''
            return redirect('post_detail', slug=slug)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                messages.success(request, 'Your comment has been submitted and is awaiting approval.')
                return redirect('post_detail', slug=slug)

    related_posts = Post.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
        'related_posts': related_posts,
        'page_title': post.title,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category, status='published')
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'category': category,
        'page_title': f'Category: {category.name}',
    }
    return render(request, 'blog/category.html', context)


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts_list = Post.objects.filter(tags=tag, status='published')
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'tag': tag,
        'page_title': f'Tag: {tag.name}',
    }
    return render(request, 'blog/tag.html', context)


def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query),
            status='published'
        )
    else:
        posts_list = Post.objects.filter(status='published')
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'query': query,
        'page_title': f'Search: {query}' if query else 'Search',
    }
    return render(request, 'blog/search.html', context)


def about(request):
    context = {'page_title': 'About'}
    return render(request, 'blog/about.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    context = {'form': form, 'page_title': 'Contact'}
    return render(request, 'blog/contact.html', context)


# ===================== DASHBOARD VIEWS =====================

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'dashboard/login.html', {'page_title': 'Admin Login'})


def dashboard_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('dashboard_login')


@admin_login_required
def dashboard_home(request):
    total_posts = Post.objects.count()
    total_categories = Category.objects.count()
    total_comments = Comment.objects.count()
    total_users = User.objects.count()
    total_messages = ContactMessage.objects.filter(is_read=False).count()
    recent_posts = Post.objects.order_by('-created_at')[:5]
    recent_comments = Comment.objects.filter(is_active=False)[:5]
    context = {
        'total_posts': total_posts,
        'total_categories': total_categories,
        'total_comments': total_comments,
        'total_users': total_users,
        'total_messages': total_messages,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)


@admin_login_required
def dashboard_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {'posts': posts, 'page_title': 'Manage Posts'}
    return render(request, 'dashboard/posts.html', context)


@admin_login_required
def dashboard_post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect('dashboard_posts')
    else:
        form = PostForm()
    context = {'form': form, 'page_title': 'Create Post', 'is_edit': False}
    return render(request, 'dashboard/post_form.html', context)


@admin_login_required
def dashboard_post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('dashboard_posts')
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post, 'page_title': 'Edit Post', 'is_edit': True}
    return render(request, 'dashboard/post_form.html', context)


@admin_login_required
def dashboard_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard_posts')
    context = {'post': post, 'page_title': 'Delete Post'}
    return render(request, 'dashboard/post_confirm_delete.html', context)


@admin_login_required
def dashboard_categories(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('dashboard_categories')
    else:
        form = CategoryForm()
    context = {'categories': categories, 'form': form, 'page_title': 'Manage Categories'}
    return render(request, 'dashboard/categories.html', context)


@admin_login_required
def dashboard_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('dashboard_categories')


@admin_login_required
def dashboard_tags(request):
    tags = Tag.objects.all().order_by('name')
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag added successfully!')
            return redirect('dashboard_tags')
    else:
        form = TagForm()
    context = {'tags': tags, 'form': form, 'page_title': 'Manage Tags'}
    return render(request, 'dashboard/tags.html', context)


@admin_login_required
def dashboard_tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    messages.success(request, 'Tag deleted successfully!')
    return redirect('dashboard_tags')


@admin_login_required
def dashboard_comments(request):
    comments = Comment.objects.all().order_by('-created_at')
    context = {'comments': comments, 'page_title': 'Manage Comments'}
    return render(request, 'dashboard/comments.html', context)


@admin_login_required
def dashboard_comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_active = True
    comment.save()
    messages.success(request, 'Comment approved!')
    return redirect('dashboard_comments')


@admin_login_required
def dashboard_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, 'Comment deleted!')
    return redirect('dashboard_comments')


@admin_login_required
def dashboard_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    context = {'messages_list': messages_list, 'page_title': 'Contact Messages'}
    return render(request, 'dashboard/messages.html', context)


@admin_login_required
def dashboard_message_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    return redirect('dashboard_messages')
