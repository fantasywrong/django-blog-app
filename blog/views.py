from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.

# views.py 안의 method 는 request 를 parameter로 받고 HttpResponse 를 리턴한다.
def post_list(request):
    # name = 'Django'
    # return HttpResponse('''<h1>Hello {myname}!!!</h1>'''.format(myname=name))

    # queryset 사용해서 Post 목록 가져요기
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date') # ascending,   -publish_date 하면 descending
    return render(request, 'blog/post_list.html', { 'posts' : posts })
