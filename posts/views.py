from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", {"posts": posts})

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect("post-detail", post_id=post.id)
    return render(request, "posts/post_detail.html", {"post": post, "form": form})

@login_required
def post_create_view(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post-list")
    return render(request, "posts/post_create.html", {"form": form})
