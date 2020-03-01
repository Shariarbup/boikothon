from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Article, Category, Comment
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CreateForm, userRegisterForm, createAuthor, commentForm
from django.contrib import messages
# Create your views here.

def index(request):
    posts = Article.objects.all()
    search = request.GET.get('q')
    if search:
        posts = posts.filter(
        Q(title__icontains=search)|
        Q(body__icontains=search)

        )
    paginator = Paginator(posts, 4) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts':page_obj,
    }
    return render(request, 'blog/index.html', context)

def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(Author, name=post_author.id)
    posts = Article.objects.filter(article_author=auth)
    paginator = Paginator(posts, 4) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'auth':auth,
        'posts':page_obj,
    }
    return render(request, 'blog/profile.html', context)

def getsingle(request, id):
    post = get_object_or_404(Article, pk=id)
    first_post = Article.objects.first()
    last_post = Article.objects.last()
    related_posts = Article.objects.filter(category=post.category).exclude(id=id)[:4]
    get_comments = Comment.objects.filter(post=id)
    form = commentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.post = post
        instance.save()
    context = {
        'post':post,
        'first_post':first_post,
        'last_post':last_post,
        'related_posts':related_posts,
        'form':form,
        'comments':get_comments,
    }
    return render(request, 'blog/single.html', context)

def getcategory(request, name):
    cat = get_object_or_404(Category, name=name)
    posts = Article.objects.filter(category=cat.id)
    paginator = Paginator(posts, 4) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts':page_obj,
        'cat':cat,
    }
    return render(request, 'blog/category.html', context)

def getlogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index') 
            else:
                messages.add_message(request, messages.ERROR, 'Username and Password Mismatch.')
                return render(request, 'blog/login.html')
    return render(request, 'blog/login.html')

def getlogout(request):
    logout(request)
    return redirect('index')

def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(Author, name=request.user.id)
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request,'Article is created successfully.')
            return redirect('profile')
        context = {
            'form':form
        }
        return render(request, 'blog/create.html', context)
    else:
        return redirect('login')

def getupdate(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=id)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request,'Article is updated successfully.')
            return redirect('profile')
       
        context = {
            'form':form
        }
        return render(request, 'blog/create.html', context)
    else:
        return redirect('login')

def getdelete(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Article, id=id)
        post.delete()
        messages.success(request,'Article is deleted successfully.')
        return redirect('profile')
    else:
        return redirect('login')

def getprofile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = Author.objects.filter(name=user.id)
        if author_profile:
            author_user = get_object_or_404(Author, name=request.user.id)
            posts = Article.objects.filter(article_author=author_user.id)
            return render(request, 'blog/logged_in_profile.html', context={'posts':posts,'user':author_user})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                return redirect('profile')
            return render(request, 'blog/createauthor.html', context={'form':form})

    else:
        return redirect('login')


def getregister(request):
    form = userRegisterForm(request.POST or None)
    if form.is_valid():
        instance =  form.save(commit=False)
        instance.save()
        messages.success(request, 'Your account has been created. Now please login with your username and password')
        return redirect('login')
    context={
        'form':form,
    }
    return render(request, 'blog/register.html', context)
    