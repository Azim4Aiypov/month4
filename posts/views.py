from django.shortcuts import render, HttpResponse
import random
from posts.models import Post, Category, Tag 
from posts.forms import PostForm, PostForm2, PostBaseForm, PostModelForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required 
def test_view(request):
    return HttpResponse(f'hello, this is a test view, {random.randint(1, 100)}')

def homepage_view(request):
    if request.method == "GET":
        return render(request, 'base.html')

def post_detail_view(request, post_id):
    if request.method == "GET":
        try:
            post = Post.objects.get(id=post_id)
        except:
            return HttpResponse("Post not found")
        return render(request, "posts/post_detail.html", context={"post": post})
    
def post_create_view(request):
    if request.method == "GET":
        form = PostForm2()
        return render(request, "posts/post_create.html", context={"form": form})
    if request.method == "POST":
        form = PostForm2(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")    # исправлено
            content = form.cleaned_data.get("content")
            image = form.cleaned_data.get("image")
            Post.objects.create(
                image=image,
                title=title,
                content=content
            )
            return HttpResponse("Post created")

        else:
            return render(request, "posts/post_create.html", context={"form": form})
        
def post_create_forms_form(request):
    if request.method == "GET":
        form = PostBaseForm() 
        return render(request, "posts/post_create_forms.html", {"form": form})
    
    elif request.method == "POST":
        form = PostBaseForm(request.POST, request.FILES) 
        if form.is_valid():
        
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data.get('image') 
            Post.objects.create(title=title, content=content, image=image)
            return HttpResponse("Пост успешно создан с помощью forms.Form!")
        
        else:
        
            return render(request, "posts/post_create_forms.html", {"form": form})
        
def post_create_model_form(request):
    if request.method == "GET":
        form = PostModelForm() 
        return render(request, "posts/post_create_model_form.html", {"form": form})
    
    elif request.method == "POST":
        form = PostModelForm(request.POST, request.FILES) # Передаем данные из запроса и файлы
        if form.is_valid():
            # Для ModelForm достаточно просто вызвать save()
            # Это создаст и сохранит новый объект Post в базе данных
            form.save() 
            return HttpResponse("Пост успешно создан с помощью ModelForm!")
            # return redirect('posts_list')
        else:
            # Форма невалидна, отображаем ее снова с ошибками
            return render(request, "posts/post_create_model_form.html", {"form": form})        
        
@login_required
def posts_list_view(request):
    posts = Post.objects.all()

    # --- Поиск ---
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
    )


    # --- Фильтрация ---
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)

    tag_id = request.GET.get('tag')
    if tag_id:
        posts = posts.filter(tags__id=tag_id)

    # --- Сортировка ---
    sort = request.GET.get('sort')
    if sort == 'title':
        posts = posts.order_by('title')
    elif sort == 'new':
        posts = posts.order_by('-created_at')
    elif sort == 'old':
        posts = posts.order_by('created_at')

    # --- Пагинация ---
    paginator = Paginator(posts, 5)  # 5 постов на страницу
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
    return render(request, 'posts/posts_list.html', context)