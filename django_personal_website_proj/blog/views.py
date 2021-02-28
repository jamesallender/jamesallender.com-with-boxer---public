from django.shortcuts import render
from .models import Post
from django.http import HttpResponse

#
# posts=[
#     {
#         'author': 'james',
#         'title': 'blog post 1',
#         'content': 'this is a test post!!',
#         'date_posted': 'aug 11,2019'
#     },
# {
#         'author': 'wam bam',
#         'title': 'blog post 2',
#         'content': 'this is a second test post!! omg!',
#         'date_posted': 'aug 28,2019'
#     }
# ]

def home(request):
    context={
        'posts': Post.objects.all()
    }
    return render(request=request, template_name='blog/home.html', context=context)

def about(request):
    return render(request=request, template_name='blog/about.html')
