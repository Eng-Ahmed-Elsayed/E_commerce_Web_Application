from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User, Favorite, Cart, Category,Ad
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your views here.

# Create new objects every time a new user is created
@receiver(post_save, sender=User)
def create_user_picks(sender, instance, created, **kwargs):
    if created:
        Favorite.objects.create(user=instance)
        Cart.objects.create(user=instance)

# Home
def home(request):
    ads = Ad.objects.all().filter(
        Q(status__icontains='active')&
        Q(pending_approval=False)
    ).order_by('-created')[0:10]
    avg_rating = getavg(ads)
    all_categories = Category.objects.all().order_by('name')
    context = {'ads': ads, 'all_categories': all_categories, 'avg_rating': avg_rating}
    return render(request, 'base/home.html', context)

# 404
def errorPage(request):
    return render(request, 'base/404.html')

# Login
def loginPage(request):
    page_name='login'
    # If user loged in redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    # Login logic
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        except:
            messages.error(request, "Username or password is not correct.")
    
    context = {'page_name': page_name}
    return render(request, 'base/login_register.html', context)

# Logout
def logoutUser(request):
    logout(request)
    return redirect('home')

# Reguster
def registerPage(request):
    page_name='register'
    form = UserForm()
    # If user loged in redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = user.password
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                user.password = make_password(password)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Those passwords didn’t match. Try again.')
        else:
            messages.error(request, 'An error occers during registration')
    context = {'page_name': page_name, 'form': form}
    return render(request, 'base/login_register.html', context)

# Edit User Profile
@login_required(login_url='login')
def editProfile(request):
    user = request.user
    if request.method == 'POST':
        # Edit Personal Information
        if 'changes' in request.POST:
            try:
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.phone = request.POST.get('phone')
                if request.POST.get('avatar') != '':
                    old_img = user.avatar.path
                    try:
                        if old_img[-10:] != 'avatar.svg':
                            if os.path.exists(old_img):
                                os.remove(old_img)
                            else:
                                pass
                    except:
                        return redirect('404')
                    user.avatar = request.FILES['avatar']
                user.save()
                return redirect('edit_profile')
            except:
                messages.error(request, 'Wrong Inputs')
        # Edit Password
        elif 'change_password' in request.POST:
            try:
                old = request.POST.get('current_password')
                if check_password(old, user.password):
                    if request.POST.get('new_password') == request.POST.get('confirm_password'):
                        user.set_password(request.POST.get('new_password'))
                        user.save()
                        logoutUser(request)
                        login(request, user)
                        return redirect('edit_profile')
                    else:
                        messages.error(request, 'Wrong Password')
                else:
                    messages.error(request, 'Wrong Old')
            except:
                messages.error(request, 'Someting wrong')
        # Edit Email Address
        elif 'change_email' in request.POST:
            try:
                if user.email == request.POST.get('current_email'):
                    user.email = request.POST.get('new_email')
                    user.save()
                    return redirect('edit_profile')
            except:
                messages.error(request, 'Wrong Email')
        else:
            return redirect('404')
    context = {'user': user}    
    return render(request, 'base/edit_profile.html', context)

# View user profile
def userProfile(request, pk):
    try:
        user = User.objects.get(id=pk)
        page = user.username.capitalize() + ' Ads' 
        ads = user.ad_set.filter(
            Q(pending_approval=False)
        )
        context = {'user': user, 'ads': ads, 'page': page}
        return render(request, 'base/profile.html', context)
    except:
        return redirect('404')

# Get avg for the ratings then round them
def getavg(ads):
    dict1 = {}
    for ad in ads:
        l = []
        x = ad.review_set.all()
        for i in x:
            l.append(int(i.rating))
        try:
            dict1[ad.id] = round(sum(l)/len(l))
        except:
            dict1[ad.id] = 0
    return dict1

# http://127.0.0.1:8000/ad_list_view/ Page
# See all ads also can search (Pagination works with category filter and search)
def adListView(request):
    all_categories = Category.objects.all().order_by('name')
    all_categories_count = all_categories.count()
    ad_num = dict()
    for category in all_categories:
        ad_num[category.name] = Category.objects.filter(
            Q(ad__category=category) &
            Q(ad__pending_approval=False)
            ).count()
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        category = request.GET.get('category')
        ads = Ad.objects.filter(
            (Q(name__icontains=q)|
            Q(details__icontains=q))&
            Q(category__name__icontains=category)&
            Q(pending_approval=False)
        )
    else:
        q = 'All Ads'
        ads = Ad.objects.filter(pending_approval=False)
    avg_rating = getavg(ads)
    ads_count = ads.count()
    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    
    context= {'all_categories': all_categories, 'ads': ads, 'all_categories_count': all_categories_count, 'ads_count': ads_count,'ad_num': ad_num, 'avg_rating':avg_rating}
    return render(request, 'base/ad_list_view.html', context)

# http://127.0.0.1:8000/category_view/ Page
def categoryView(request):
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'base/category_view.html', context)

    

