from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProfileEditForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from post.models import Post

# Create your views here.
@login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    
    posts = profile.user.posts.all()

    # Handling HTMX request
    if 'HX-Request' in request.headers:
        if 'posts' in request.GET:
            posts = profile.user.posts.annotate(like_count=Count('likes')).order_by('-created_at')
            return render(request, 'snippets/loop_profile_post.html', {'posts': posts})
        
        elif 'liked-posts' in request.GET:  # Correct key
            liked_posts = Post.objects.filter(likedpost__user=profile.user).order_by('-likedpost__created')

            # Check if liked_posts is empty
            if not liked_posts.exists():
                # Pass a message to the template if no liked posts are found
                return render(request, 'snippets/loop_profile_post.html', {'message': 'No posts liked'})
            
            return render(request, 'snippets/loop_profile_post.html', {'posts': liked_posts})

    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)




@login_required
def profile_edit_view(request):
    form=ProfileEditForm(instance=request.user.profile)

    if request.method=='POST':
        form=ProfileEditForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
    context={
        'form': form
    }
    return render(request, 'users/profile_edit.html',context)




