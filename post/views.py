from django.shortcuts import render, HttpResponse
from .models import post

# Create your views here.

def post_index(request):
    post1 = post.objects.all()

    query = request.GET.get('search')
    if query:
        post1 = post1.filter(id=query)

    return render(request, 'post/index.html', {'posts': post1})

def post_detail(request, id):
    posts = post.objects.get(id=id)
    return render(request, 'post/detail.html', {'post': posts})

def post_create(request):
    return HttpResponse('Burası Post Create ')

def post_update(request):
    return HttpResponse('Burası Post Update')

def post_delete(request):
    return HttpResponse('Burası Post Delete')

