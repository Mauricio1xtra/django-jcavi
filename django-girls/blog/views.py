from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' :post})

def post_new(request):
    return _post_new_edit(request)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return _post_new_edit(request, post)


def _post_new_edit(request, post=None):
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) if post else PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post) if post else PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
