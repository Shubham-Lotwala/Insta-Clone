import asyncio
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from bs4 import BeautifulSoup
import aiohttp
from django.contrib import messages
from django.db.models import Count
from .forms import *


def home_view(request):
    posts = Post.objects.all()
    top_posts = Post.objects.annotate(like_count=Count("likes")).order_by(
        "-like_count"
    )[:5]
    context = {
        "posts": posts,
        "top_posts": top_posts,
    }
    return render(request, "post/home.html", context)


@login_required
def sidebar_view(request):
    # Get top posts ordered by the number of likes
    top_posts = Post.objects.annotate(like_count=Count("likes")).order_by(
        "-like_count"
    )[
        :5
    ]  # Top 5 posts

    context = {
        "top_posts": top_posts,
    }

    return render(request, "snippets/sidebar.html", context)


async def fetch_website_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def parse_website_content(content):
    sourcecode = BeautifulSoup(content, "lxml")
    image = sourcecode.select_one('meta[content^="https://live.staticflickr.com/"]')
    title = sourcecode.select_one("h1.photo-title")

    return image["content"] if image else None, (
        title.text.strip() if title else "Untitled"
    )


@login_required
def post_create_view(request):
    form = PostCreateForm()

    if request.method == "POST":
        form = PostCreateForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            url = form.cleaned_data["url"]
            user_title = form.cleaned_data["title"]

            # Fetch website content
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(fetch_website_content(url))

            # Parse website content
            image = parse_website_content(content)

            # Use user-provided title if available, otherwise use parsed title
            post.title = user_title
            post.image = image
            post.author = request.user
            post.save()
            form.save_m2m()

            return redirect("home")

    return render(request, "post/post_create.html", {"form": form})


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    context = {"post": post}

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("home")
    return render(request, "post/post_delete.html", context)


def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostEditForm(instance=post)
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect("home")

    context = {"post": post, "form": form}

    return render(request, "post/post_edit.html", context)


@login_required
def post_page_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    commentform = CommentCreteForm()
    replyform = ReplyCreteForm()
    top_posts = Post.objects.annotate(like_count=Count("likes")).order_by(
        "-like_count"
    )[:5]

    context = {
        "post": post,
        "commentform": commentform,
        "replyform": replyform,
        "top_posts": top_posts,
    }
    return render(request, "post/post_page.html", context)


def reply_sent(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReplyCreteForm(request.POST)
        if form.is_valid():
            # Create a new Reply instance but don't commit to the database yet
            reply = form.save(commit=False)
            # Set the parent_comment field correctly
            reply.parent_comment = comment
            reply.author = request.user
            # Save the reply to the database
            reply.save()
    # Use comment.parent_post.pk instead of comment.parent.post.pk
    return redirect("post-page", comment.parent_post.pk)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentCreteForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent_post = post
            comment.author = request.user
            comment.save()
    return redirect("post-page", post.pk)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)

    context = {"comment": comment}

    if request.method == "POST":
        parent_post = comment.parent_post  # Assuming Comment model has 'parent_post'
        comment.delete()
        messages.success(request, "Comment deleted successfully")
        return redirect("post-page", parent_post.pk)  # Redirect to the parent post

    return render(request, "post/comment_delete.html", context)


@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, pk=pk, author=request.user)

    context = {"reply": reply}

    if request.method == "POST":
        parent_post = (
            reply.parent_comment.parent_post
        )  # Assuming Comment model has 'parent_post'
        reply.delete()
        messages.success(request, "Reply deleted successfully")
        return redirect("post-page", parent_post.pk)
    return render(request, "post/reply_delete.html", context)


@login_required
def like_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_exists = post.likes.filter(username=request.user.username).exists()

    if post.author != request.user:
        if user_exists:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    context = {"post": post}

    return render(request, "snippets/likes.html", context)


@login_required
def like_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment_exists = comment.likes.filter(username=request.user.username).exists()

    if comment.author != request.user:
        if comment_exists:
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

    context = {"comment": comment}

    return render(request, "snippets/like_comment.html", context)


@login_required
def like_reply_view(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply_exists = reply.likes.filter(username=request.user.username).exists()

    if reply.author != request.user:
        if reply_exists:
            reply.likes.remove(request.user)
        else:
            reply.likes.add(request.user)

    context = {"reply": reply}

    return render(request, "snippets/like_reply.html", context)
