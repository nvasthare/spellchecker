from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from sets import Set

def post_list(request):
	posts = Post.objects.all()
	return render(request,'docs/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    spellingerrors = []
    for word in post.text.split():
    	spellingerrors.append(word)
    	break
    # spellingerrors.append(post.text.split()[1])
    # spellingerrors.append(post.text.split()[4])
    print post.text.split()
    return render(request, 'docs/post_detail.html', 
    	{'post': post, 'spellingerrors': spellingerrors, 'text': post.text.split()})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            print post.text.split()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'docs/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            print post.text.split()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'docs/post_edit.html', {'form': form})


