from django.shortcuts import get_object_or_404, redirect, render
from base.models import Cart, User, Ad, Favorite, Category, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import AdForm, ReviewForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

# Count Num Of Ads In Pages (My Ads, Favorite Ads, Pennding Approval, Archived Ads)
def getcounts(user):
    p1 = user.ad_set.filter(
        Q(status__icontains='active')&
        Q(pending_approval=False)
    ).count()
    try:
        p2 = Favorite.objects.get(user=user).favorite_ads.all().count()
    except:
        p2 = 0
    p3 = user.ad_set.filter(
        Q(pending_approval=True)
    ).count()
    p4 = user.ad_set.filter(
        Q(status__icontains='archived')&
        Q(pending_approval=False)
    ).count()
    return p1, p2, p3, p4

# My Ads View
@login_required(login_url='login')
def dashHome(request):
    page_name = 'My Ads'
    user = User.objects.get(id=request.user.id)
    ads = user.ad_set.filter(
        Q(status__icontains='active')&
        Q(pending_approval=False)
    )
    p1, p2, p3, p4 = getcounts(user)

    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    context = {'user': user, 'ads': ads, 'page_name': page_name, 'p1': p1, 'p2': p2, 'p3': p3, 'p4' :p4}
    
    return render(request, 'dashboard/dashboard.html', context)

# Favorite Ads View
@login_required(login_url='login')
def favoriteAds(request):
    page_name = 'Favourite Ads'
    user = User.objects.get(id=request.user.id)
    fav = Favorite.objects.get(user=user)
    ads = fav.favorite_ads.all()
    p1, p2, p3, p4 = getcounts(user)
    
    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    context = {'user': user, 'ads': ads, 'page_name': page_name, 'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4}
    return render(request, 'dashboard/dashboard.html', context)

# Add ad to my favorite
@login_required(login_url='login')
def addAdToFav(request, pk):
    user = request.user
    ad = Ad.objects.get(id=pk)
    fav = Favorite.objects.get(user=user)
    all_ads = fav.favorite_ads.all()
    # Check if the ad in my fav
    if ad not in all_ads:
        fav.favorite_ads.add(ad)
        return redirect('ad_view', pk=pk)
    else: 
        messages.error(request, 'This ad is on your favorite.')
        return redirect('404')

# Delete ad to my favorite
@login_required(login_url='login')
def deleteAdFromFav(request, pk):
    user = request.user
    ad = Ad.objects.get(id=pk)
    fav = Favorite.objects.get(user=user)
    all_ads = fav.favorite_ads.all()
    # Check if the ad in my fav
    if ad in all_ads:
        fav.favorite_ads.remove(ad)
        return redirect('ad_view', pk=ad.id)
    else: 
        messages.error(request, 'This ad is not exist in your favorite.')
        return redirect('404')

# Pennding approval View
@login_required(login_url='login')
def pendingApproval(request):
    page_name = 'Pending Approval'
    user = User.objects.get(id=request.user.id)
    ads = user.ad_set.filter(
        Q(pending_approval=True)
    )
    p1, p2, p3, p4 = getcounts(user)

    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    context = {'user': user, 'ads': ads, 'page_name': page_name, 'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4}
    
    return render(request, 'dashboard/dashboard.html', context)

# Archived Ads View
@login_required(login_url='login')
def archivedAds(request):
    page_name = 'Archived Ads'
    user = User.objects.get(id=request.user.id)
    ads = user.ad_set.filter(
        Q(status__icontains='archived')&
        Q(pending_approval=False)
    )
    p1, p2, p3, p4 = getcounts(user)
 
    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    context = {'user': user, 'ads': ads, 'page_name': page_name, 'p1': p1, 'p2': p2, 'p3': p3, 'p4' :p4}
    
    return render(request, 'dashboard/dashboard.html', context)

# Page: http://127.0.0.1:8000/dashboard/ad_list/ 
# This Page where you can publish your ad through
@login_required(login_url='login')
def adList(request):
    page = 'Post Your Ad'
    form = AdForm()
    # Split the form
    l1 = ['name', 'price', 'category', 'brand', 'model_year']
    l2 = [ 'location', 'details', 'img']
    if request.method == 'POST':
        form = AdForm(request.POST,  request.FILES)
        if form.is_valid():
            ad = Ad()
            # Values From the form
            ad.name = form.cleaned_data['name']
            ad.price = float(form.cleaned_data['price'])
            ad.category = form.cleaned_data['category']
            ad.brand = form.cleaned_data['brand']
            ad.model_year = int(form.cleaned_data['model_year'])
            ad.location = form.cleaned_data['location']
            ad.details = form.cleaned_data['details']
            ad.img = form.cleaned_data['img']
            # Defalut Values
            ad.status = 'Active'
            ad.user = request.user
            ad.pending_approval = True
            ad.save()
            return redirect('dashboard')
        else:
            return redirect('404')
    context = {'form': form, 'l1': l1, 'l2': l2, 'page': page}
    return render(request, 'dashboard/ad_listing.html', context)


def adView(request, pk):
    ad = Ad.objects.get(id=pk)
    categories = Category.objects.all()
    try:
        fav = Favorite.objects.get(user=request.user)
        all_ads = fav.favorite_ads.all()
        in_fav = False
        
        if ad in all_ads:
            in_fav = True
        
        cart = Cart.objects.get(user=request.user)
        all_ads = cart.cart_ads.all()
        in_cart = False
        
        if ad in all_ads:
            in_cart = True
        # Check if he has review
        try:
            user_review = Review.objects.get(user=request.user, ad=ad)
            has_review = True
        except:
            user_review = None
            has_review = False
        # Review form
        form = ReviewForm()
        if request.method == 'POST':
            if has_review == False:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    user_review = Review()
                    user_review.user = request.user
                    user_review.ad = ad
                    user_review.rating = form.cleaned_data['rating']
                    user_review.review = form.cleaned_data['review']
                    user_review.save()
                    return redirect('ad_view', pk=pk)
                else:
                    return redirect('404')
            else:
                return redirect('404')
        context = {'ad': ad, 'in_fav': in_fav,'in_cart': in_cart, 'categories': categories, 'form': form, 'has_review': has_review, 'user_review': user_review}
    except:
        context = {'ad': ad, 'categories': categories}
    if ad.pending_approval == False:
        return render(request, 'dashboard/ad_view.html', context)
    else: 
        if request.user.is_superuser or ad.user == request.user:
            return render(request, 'dashboard/ad_view.html', context)
        else:
            return redirect('404')
    



@login_required(login_url='login')
def editAd(request, pk):
    page = 'Update Your Ad'
    ad = Ad.objects.get(id=pk)
    form = AdForm(instance=ad)
    # Split the form
    l1 = ['name', 'price', 'category', 'brand', 'model_year']
    l2 = [ 'location', 'details', 'img']
    if request.method == 'POST':
        form = AdForm(request.POST,  request.FILES, instance=ad)
        values = []
        for i in form:
            values.append(i.value())
        if form.is_valid():
            # Values From the form
            ad.name = form.cleaned_data['name']
            ad.price = float(form.cleaned_data['price'])
            ad.category = form.cleaned_data['category']
            ad.brand = form.cleaned_data['brand']
            ad.model_year = int(form.cleaned_data['model_year'])
            ad.location = form.cleaned_data['location']
            ad.details = form.cleaned_data['details']
            new_img = form.cleaned_data['img']
            if values[7] != '' :
                old_img_path = ad.img.path
                try:
                    if ad.img != new_img:
                        if os.path.exists(old_img_path):
                            os.remove(old_img_path)
                        else:
                            pass
                    else:
                        pass
                except:
                    return redirect('404')
                ad.img = new_img
            # Defalut Values
            ad.status = 'Active'
            ad.user = request.user
            ad.pending_approval = True
            ad.save()
            return redirect('dashboard')

    context = {'form': form, 'l1': l1, 'l2': l2, 'page': page}
    return render(request, 'dashboard/ad_listing.html', context)


@login_required(login_url='login')
def deleteAd(request, pk):
    ad = Ad.objects.get(id=pk)
    if ad.user == request.user:
        status = ad.status.lower()
        if status != 'archived':
            ad.delete()
            return redirect('dashboard')
        else:
            return redirect('404')
    else:
        return redirect('404')

@login_required(login_url='login')
def editReview(request, pk):
    user_review = get_object_or_404(Review, id=pk)
    
    form = ReviewForm(instance=user_review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            user_review.rating = form.cleaned_data['rating']
            user_review.review = form.cleaned_data['review']
            user_review.save()
            return redirect('ad_view', pk=user_review.ad.id)
        else:
            return redirect('404')

    context = {'user_review': user_review, 'form': form}

    return render(request, 'dashboard/edit_review.html', context)
        
@login_required(login_url='login')
def deleteReview(request, pk):
    user_review = get_object_or_404(Review, id=pk)
    if user_review.user == request.user:
        ad_id = user_review.ad.id
        user_review.delete()
        return redirect('ad_view', pk=ad_id)
    else:
        return redirect('404')


