from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from core.models import User
from application.models import Post, Like, Comment, Follow
from django.contrib import messages


@login_required(login_url='signin')
def index(request):
    posts = Post.objects.all()
    for post in posts:
        post.likes_count = post.likes.all().count()

    return render(request, 'index.html', {'user_profile': request.user, 'posts': posts})

@login_required(login_url='signin')
def add_likes(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        try:
            like = Like.objects.get(post=post, user=request.user)
        except:
            Like.objects.create(post=post, user=request.user)
        else:
            like.delete()
        return HttpResponseRedirect(reverse('index'))


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('signin'))

@login_required(login_url='signin')
def upload_post(request):
    if request.method == 'POST':
        caption = request.POST.get('post-caption')
        image = request.FILES.get('post-image')
        if caption is None:
            messages.info(request, 'Add the caption')
            return HttpResponseRedirect(reverse('index'))
        elif image is None:
            messages.info(request, 'Add the Image')
            return HttpResponseRedirect(reverse('index'))
        post = Post.objects.get_or_create(user=request.user, caption=caption, image=image)
        print(post)

        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='signin')
def profile(request, user_id):
    get_user = User.objects.get(id=user_id)
    user_posts = Post.objects.filter(user=get_user).all()
    no_user_posts = Post.objects.filter(user=get_user).all().count()
    following = get_user.followings.all().count()
    followers = get_user.followers.all().count()
    if Follow.objects.filter(follower=request.user, following=get_user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    context =  {
        "button_text": button_text,
        "current_user": request.user,
        "user": get_user,
        "user_posts": user_posts,
        "no_of_user_posts": no_user_posts,
        "following": following,
        "followers": followers
            }
    return render(request, "profile.html", context)

@login_required(login_url='signin')
def follow_user(request):
    if request.method == 'POST':
        user_email = request.POST.get('follower')
        user = User.objects.get(email=user_email)
        try:
            obj = Follow.objects.get(follower=request.user, following=user)
        except:
            Follow.objects.create(follower=request.user, following=user)
        else:
            obj.delete()
    return HttpResponseRedirect(f'/app/profile/{user.id}')




@login_required(login_url='signin')
def settings(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        profile_photo = request.FILES.get('profile-photo')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        if email is not None:
            request.user.email = email
        if first_name is not None:
            request.user.first_name = first_name
        if last_name is not None:
            request.user.last_name = last_name
        if profile_photo is not None:
            print('start')
            print(profile_photo)
            print('start')
            request.user.profile_photo = profile_photo
        if bio is not None:
            request.user.bio = bio
        if location is not None:
            request.user.location = location
        request.user.save()
        return HttpResponseRedirect(reverse('settings'))
    return render(request, 'setting.html', {'user_profile':request.user} )