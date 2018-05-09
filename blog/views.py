from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.forms import PostForm
from blog.modelforms import PostModelForm
from .models import Post

# Create your views here.

# views.py 안의 method 는 request 를 parameter로 받고 HttpResponse 를 리턴한다.

# 글 목록 조회
def post_list(request):
    # name = 'Django'
    # return HttpResponse('''<h1>Hello {myname}!!!</h1>'''.format(myname=name))

    # queryset 사용해서 Post 목록 가져요기
    # posts = Post.objects.all()
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date') # ascending,   -publish_date 하면 descending
    return render(request, 'blog/post_list.html', { 'posts' : posts })

# 글 상세 조회
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', { 'post' : post })

# 글 등록 (ModelForm 사용)
def post_new(request):
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: # GET
        form = PostModelForm()
        # print(form)
    return render(request, 'blog/post_edit.html', {'form':form})

# 글 등록 (Form 사용)
def post_new_form(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        # print(form)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post(
                author=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                publish_date=timezone.now()
            )
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            print(form.errors)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form':form})