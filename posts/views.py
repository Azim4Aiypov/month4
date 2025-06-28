from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import random
from posts.models import Post, Category, Tag 
from posts.forms import PostForm, PostForm2, PostBaseForm, PostModelForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def test_view(request):
    return HttpResponse(f'hello, this is a test view, {random.randint(1, 100)}')


def homepage_view(request):
    return render(request, 'base.html')


def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/post_detail.html", {"post": post})


@login_required
def post_create_view(request):
    if request.method == "GET":
        form = PostForm2()
        return render(request, "posts/post_create.html", {"form": form})

    form = PostForm2(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user  # добавлено: текущий пользователь становится автором
        post.save()
        form.save_m2m()
        return HttpResponse("Пост создан")
    return render(request, "posts/post_create.html", {"form": form})


@login_required
def post_create_forms_form(request):
    if request.method == "GET":
        form = PostBaseForm() 
        return render(request, "posts/post_create_forms.html", {"form": form})

    form = PostBaseForm(request.POST, request.FILES) 
    if form.is_valid():
        post = Post(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            image=form.cleaned_data.get('image'),
            author=request.user  # обязательно указываем автора
        )
        post.save()
        return HttpResponse("Пост успешно создан с помощью forms.Form!")
    return render(request, "posts/post_create_forms.html", {"form": form})


@login_required
def post_create_model_form(request):
    if request.method == "GET":
        form = PostModelForm() 
        return render(request, "posts/post_create_model_form.html", {"form": form})

    form = PostModelForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user  # добавляем автора
        post.save()
        form.save_m2m()
        return HttpResponse("Пост успешно создан с помощью ModelForm!")
    return render(request, "posts/post_create_model_form.html", {"form": form})


@login_required
def posts_list_view(request):
    posts = Post.objects.all()

    # Поиск
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    # Фильтрация
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)

    tag_id = request.GET.get('tag')
    if tag_id:
        posts = posts.filter(tags__id=tag_id)

    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'title':
        posts = posts.order_by('title')
    elif sort == 'new':
        posts = posts.order_by('-created_at')
    elif sort == 'old':
        posts = posts.order_by('created_at')

    # Пагинация
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'query': query,
        'current_category': category_id,
        'current_tag': tag_id,
        'current_sort': sort,
    }
    return render(request, 'posts/post_list.html', context)
