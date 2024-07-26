from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from blog.models import Post, Comment, Message
from blog.forms import CommentForm, MessageForm

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def about(request):
    context = {}
    return render(request, "blog/about.html", context=context)

def message_success(request, pk):
    message = get_object_or_404(Message, pk=pk)
    context = {"message": message}
    return render(request, "blog/message_success.html", context=context)

def contact(request):
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                author=form.cleaned_data["author"],
                topic=form.cleaned_data["topic"],
                email=form.cleaned_data["email"],
                body=form.cleaned_data["body"]
            )
            if message is not None:
                message.save()
                return redirect("message_success", pk=message.pk)

    context = {"form": form}
    return render(request, "blog/contact.html", context=context)

def resume(request):
    context = {}
    return render(request, "blog/resume.html", context=context)

def search(request):
    query = request.GET.get("search") if request.GET.get("search") else ""
    posts = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(body__icontains=query) | 
        Q(categories__name__icontains=query)
    ).distinct()
    context = {"posts": posts}
    return render(request, "blog/index.html", context=context)
