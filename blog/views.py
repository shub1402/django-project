from collections import namedtuple
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import widgets
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,BlogPost
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django import forms
from django.forms import Textarea
from django.views.generic import ListView

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

class PostForm(ModelForm):
    class Meta:
        model=BlogPost
        fields={'posted_by','title','content'}
        exclude=['posted_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-box'}),
            'content': Textarea(attrs={'cols': 80, 'rows': 20,'class': 'content-box'}),
        }

def index(request):
    
    return render(request, "blog/index.html",{
        'posts':BlogPost.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "blog/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "blog/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "blog/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blog/register.html")

def about(request):
    
    return render(request, "blog/about.html")

def profile(request,username):
    user=User.objects.get(username=username)
    return render(request, "blog/profile.html",{'user':user})

@login_required
def createPost(request):
    user=request.user
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("login"))
    
    elif request.method=='GET':
        return render(request, "blog/createPost.html", {
            "form":PostForm()
        })
    else:
        form=PostForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            postCreated = BlogPost.objects.create(
                posted_by=request.user,
                title=title, 
                content=content, 
            )
        return HttpResponseRedirect(reverse("index"))
@login_required
def updateProfile(request):
    user=User.objects.get(username = request.user.username)
    if not request.user.is_authenticated: 
        return HttpResponseRedirect(reverse("login"))
    
    elif request.method=='GET':
        return render(request, "blog/updateProfile.html",{'user':user})
    elif request.method=='POST':
        username = request.POST["username"]
        email = request.POST["email"]
        image_url = request.POST['image_url']
        user.image_url  = image_url
        try:
            user.username = username
            user.email = email
            user.save()
        except IntegrityError:
            return render(request, "blog/updateProfile.html", {
                "message": "Username already taken."
            })
        return render(request, "blog/profile.html",{'user':user})
def updatePost(request,post):
    p = BlogPost.objects.get(id = post)
    if not request.user.is_authenticated: 
        return HttpResponseRedirect(reverse("login"))
    elif request.method=='GET':
        return render(request, "blog/updatePost.html",{'post':p})
    elif request.method=='POST':
        title = request.POST["title"]
        content = request.POST["content"]
        p.title = title
        p.content =content
        p.save()
        return render(request, "blog/post.html",{'post':p})

def viewPost(request,post):
    p = BlogPost.objects.get(id = post)
    return render(request, "blog/post.html",{'post':p})

def disablePost(request,post):
    p = BlogPost.objects.get(id = post)
    p.closed = True
    p.save()
    return HttpResponseRedirect(reverse("index"))

def changePassword(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.user.username
        currentPassword = request.POST["currentPassword"]
        user = authenticate(request, username=username, password=currentPassword)
        if user is not None:
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "blog/changePassword.html", {
                "message": "Passwords must match."
            })
            else:
                user.password = confirmation
                return render(request, "blog/changePassword.html", {
                "message": "Password changed"
            })
        else:
            return render(request, "blog/changePassword.html", {
                "message": "Invalid Current Password."
            })
    else:
        return render(request, "blog/changePassword.html")