from django.shortcuts import render,HttpResponse, get_object_or_404, redirect, Http404
from .models import Author, Article, Category, Comment
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CreateForm, userRegisterForm, createAuthor, commentForm, categoryForm
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token

# Create your views here.

def index(request):
    posts = Article.objects.all().order_by('-posted_on')
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


def getupdateprofile(request, id):
    u = get_object_or_404(Author, id=request.user.id)
    if request.user.is_authenticated:
        form = createAuthor(request.POST or None, instance=u)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,'Your profile is updated successfully.')
            return redirect('profile')
       
        context = {
            'form':form
        }
        return render(request, 'blog/updateprofile.html', context)
    else:
        return redirect('login')


def getregister(request):
    form = userRegisterForm(request.POST or None)
    if form.is_valid():
        instance =  form.save(commit=False)
        instance.is_active = False
        instance.save()
        site = get_current_site(request)
        mail_subject = 'Confirmation message for blog'
        message = render_to_string('blog/confirm_email.html',{
            'user':instance,
            'domain':site.domain,
            'uid':instance.id,
            'token':activation_token.make_token(instance)
        })
        to_email = form.cleaned_data.get('email')
        to_list = [to_email]
        form_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, message,form_email, to_list, fail_silently=True)
        return HttpResponse('<h1>Thank you, for your Registration, A confirmation email was send to your email.</h1>')
    context={
        'form':form,
    }
    return render(request, 'blog/register.html', context)


def gettopic(request):
    topics = Category.objects.all()
    return render(request,'blog/topic.html', {'topics':topics})


def getnewtopic(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = categoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request,'Created a new topic successfully')
                return redirect('topics')
            return render(request,'blog/create_topic.html', {'form':form})
        else:
            raise Http404('You are not authorized to this page')

    else:
        return redirect('login')

def getupdatetopic(request, name):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, name=name)
        form = categoryForm(request.POST or None, instance=category)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,'Category is updated successfully.')
            return redirect('topics')
       
        context = {
            'form':form
        }
        return render(request, 'blog/create_topic.html', context)
    else:
        return redirect('login')

def getdeletetopic(request, name):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, name=name)
        category.delete()
        messages.success(request,'Category is deleted successfully.')
        return redirect('topics')
    else:
        return redirect('login')

def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No user found.")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'blog/confirmation_success.html')
    else:
        return HttpResponse('<h3>Invalid activation link </h3>')