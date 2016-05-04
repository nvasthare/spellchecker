from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from sets import Set

def post_list(request):
	langs = range(5)
	langs = [int(i) for i in langs]
	return render(request,'docs/post_list.html', {'langs': langs})

def post_edit(request,l, words):
	form = PostForm()
	print l
	print words
	if words == '0':
		if l == '0':
			return render(request, 'docs/post_edit.html', {'form': form})
		elif l == '1':
			return render(request,'docs/post_edit1.html', {'form': form})
		elif l == '2':
			return render(request,'docs/post_edit2.html', {'form': form})
		elif l == '3':
			return render(request,'docs/post_edit3.html', {'form': form})
		elif l == '4':
			return render(request,'docs/post_edit4.html', {'form': form})
	elif words == '1':
		if l == '0':
			return render(request, 'docs/post_edit00.html', {'form': form})
		elif l == '1':
			return render(request,'docs/post_edit01.html', {'form': form})
		elif l == '2':
			return render(request,'docs/post_edit02.html', {'form': form})
		elif l == '3':
			return render(request,'docs/post_edit03.html', {'form': form})
		elif l == '4':
			return render(request,'docs/post_edit04.html', {'form': form})
	else:
		return render(request, 'docs/post_edit.html', {'form': form})
