from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.forms import PostForm
from blog.modelforms import PostModelForm, CommentForm
from .models import Post, Comment


# Create your views here.

# views.py 안의 method 는 request 를 parameter로 받고 HttpResponse 를 리턴한다.


# 글 목록 조회
def post_list(request):
    # name = 'Django'
    # return HttpResponse('''<h1>Hello {myname}!!!</h1>'''.format(myname=name))

    # queryset 사용해서 Post 목록 가져요기
    # posts = Post.objects.all()
    # posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date') # ascending
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')  # descending
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
            # 방법1 : Post 객체 생성 후 save() 호출
            # post = Post(
            #     author=request.user,
            #     title=form.cleaned_data['title'],
            #     text=form.cleaned_data['text'],
            #     publish_date=timezone.now()
            # )
            # post.save()
            # 방법2 : Post.objects.create() 호출.
            post = Post.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                publish_date=timezone.now()
            )
            return redirect('post_detail', pk=post.pk)
        else:
            print(form.errors)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form':form})

# 글 수정 (ModelForm 사용)
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

# 글 삭제
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method== "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post= post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk= comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)