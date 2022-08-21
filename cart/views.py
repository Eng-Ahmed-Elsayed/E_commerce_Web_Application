from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from base.models import Cart, Ad
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# Count Ads in pages (My Cart, My Purchases)
def getcounts(user):
    cart = Cart.objects.get(user=user)
    p1 = cart.cart_ads.filter(
        Q(status__icontains='active')&
        Q(pending_approval=False)
    ).count()
    p2 = cart.cart_ads.filter(
        Q(status__icontains='archived')&
        Q(pending_approval=False)
    ).count()
    return p1, p2

@login_required(login_url='login')
def myCart(request):
    page_name = 'My Cart'
    user = request.user
    cart = Cart.objects.get(user=user)
    ads = cart.cart_ads.filter(
        Q(status__icontains='active')&
        Q(pending_approval=False)
    )
    p1, p2 = getcounts(user)
    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    context = {'page_name': page_name, 'user': user, 'cart': cart, 'ads': ads, 'p1': p1, 'p2': p2}
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login')
def myPurchases(request):
    page_name = 'My Purchases'
    user = request.user
    cart = Cart.objects.get(user=user)
    ads = cart.cart_ads.filter(
        Q(status__icontains='archived')&
        Q(pending_approval=False)
    )
    p1, p2 = getcounts(user)
    paginator = Paginator(ads, 4)
    page = request.GET.get('page')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    context = {'page_name': page_name, 'user': user, 'cart': cart, 'ads': ads, 'p1': p1, 'p2': p2}
    return render(request, 'cart/cart.html', context)



@login_required(login_url='login')
def addToCart(request, pk):
    user = request.user
    cart = Cart.objects.get(user=user)
    ad = Ad.objects.get(id=pk)
    ad_id = ad.id
    try:
        if ad.status.lower() == 'active' and ad.pending_approval ==False:
            if ad not in cart.cart_ads.all():
                if user != ad.user:
                    cart.cart_ads.add(ad)
                    return redirect('ad_view', pk=ad_id)
                else:
                    return redirect('404')
            return redirect('my_cart')
        else:
            return redirect('404')
    except:
        messages.error(request, 'This ad is not active or pending approval.')
    return redirect('404')

    


@login_required(login_url='login')
def deleteFromCart(request, pk):
    user = request.user
    cart = Cart.objects.get(user=user)
    ad = Ad.objects.get(id=pk)
    try:
        if ad.status.lower() == 'active' and ad.pending_approval ==False:
            cart.cart_ads.remove(ad)
            return redirect('my_cart')
        else:
            return redirect('404')
    except:
        messages.error(request, 'This ad is not exist in your cart.')
        return redirect('404')
   


@login_required(login_url='login')
def buyAd(request, pk):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
        ad = Ad.objects.get(id=pk)
        if ad in cart.cart_ads.all():
            if ad.status.lower() == 'active' and ad.pending_approval ==False:
                ad.status = 'Archived'
                ad.save()
                return redirect('my_cart')
            else:
                return redirect('404')
    except:
        return redirect('404')
    
@login_required(login_url='login')    
def paypal(request, pk):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
        ad = Ad.objects.get(id=pk)
        if ad in cart.cart_ads.all():
            if ad.status.lower() == 'active' and ad.pending_approval ==False:
                context = {'cart': cart, 'ad': ad}
                return render(request, 'cart/paypal.html', context)
                

            else:
                return redirect('404')
    except:
        return redirect('404')

   