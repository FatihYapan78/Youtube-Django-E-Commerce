from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def ProductQuantity(request):
    if request.user.is_authenticated:
        return BasketProduct.objects.filter(user=request.user)
    else:
        return None

def index(request):
    products = Product.objects.all()
    favori_products = Favorite.objects.all()
    if request.method == "POST":
        productid = request.POST.get("product_id")

        product = Product.objects.get(id=productid)

        if request.POST.get("submit") == "btnbasket":

            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)
                basket_product.quantity += 1
                basket_product.save()
                return redirect("index")
            else:
                basketproduct = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
                basketproduct.save()
                return redirect("index")
        elif request.POST.get("submit") == "btnfavori":

            if Favorite.objects.filter(product=product).exists():
                favori = Favorite.objects.get(product=product)
                favori.delete()
                return redirect("index")
            else:
                favori = Favorite.objects.create(user=request.user, product=product)
                favori.save()
                return redirect("index")

    context={
        "products":products,
        "favori_products":favori_products,
        "productquantity":ProductQuantity(request)
    }
    return render(request, "index.html", context)

def category(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    genders = Gender.objects.all()
    colors = Color.objects.all()
    case_shapes = CaseShape.objects.all()
    strap_types = StrapType.objects.all()
    glass_features = GlassFeature.objects.all()
    styles = Style.objects.all()
    mechanisms = Mechanism.objects.all()
    favori_products = Favorite.objects.all()

    filters = Q()

    if "marka" in request.GET:
        # Birden fazla marka seçilebileceği için getlist() yönetimini kullanarak tüm seçimleri alıyoruz.
        markalar = request.GET.getlist("marka")
        # Marka seçimlerini Q nesnesine ekliyoruz.
        for marka in markalar:
            filters |= Q(brand__brand=marka)

    if "cinsiyet" in request.GET:
        filters &= Q(gender=request.GET.get("cinsiyet"))

    if "renk" in request.GET:
        renkler = request.GET.getlist("renk")
        for renk in renkler:
            filters |= Q(color__color=renk)

    if "kasa_sekli" in request.GET:
        kasa_sekilleri = request.GET.getlist("kasa_sekli")
        for kasa_sekli in kasa_sekilleri:
            filters |= Q(case_shape__case_shape=kasa_sekli)

    if "kayis_tipi" in request.GET:
        kayis_tipleri = request.GET.getlist("kayis_tipi")
        for kayis_tipi in kayis_tipleri:
            filters |= Q(strap_type__strap_type=kayis_tipi)

    if "cam_ozellik" in request.GET:
        cam_ozellikleri = request.GET.getlist("cam_ozellik")
        for cam_ozellik in cam_ozellikleri:
            filters |= Q(glass_feature__glass_feature=cam_ozellik)

    if "tarz" in request.GET:
        tarzlar = request.GET.getlist("tarz")
        for tarz in tarzlar:
            filters |= Q(tarz__tarz=tarz)

    if "mekanizma" in request.GET:
        mekanizmalar = request.GET.getlist("mekanizma")
        for mekanizma in mekanizmalar:
            filters |= Q(mechanism__mechanism=mekanizma)

    if "fiyat_min" in request.GET and "fiyat_max" in request.GET and request.GET.get("fiyat_max") != "":
        fiyat_min = request.GET.get("fiyat_min")
        fiyat_max = request.GET.get("fiyat_max")

        if fiyat_min == "":
            fiyat_min = 0

        filters &= Q(price__gte=fiyat_min, price__lte=fiyat_max)

    products = Product.objects.filter(filters)

    if request.method == "POST":
        productid = request.POST.get("product_id")

        product = Product.objects.get(id=productid)

        if request.POST.get("submit") == "btnbasket":

            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)
                basket_product.quantity += 1
                basket_product.save()
                return redirect("category")
            else:
                basketproduct = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
                basketproduct.save()
                return redirect("category")
        elif request.POST.get("submit") == "btnfavori":

            if Favorite.objects.filter(product=product).exists():
                favori = Favorite.objects.get(product=product)
                favori.delete()
                return redirect("category")
            else:
                favori = Favorite.objects.create(user=request.user, product=product)
                favori.save()
                return redirect("category")
        
    paginator = Paginator(products, 1)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    context = {
        "products":products,
        "brands":brands,
        "genders":genders,
        "colors":colors,
        "case_shapes":case_shapes,
        "strap_types":strap_types,
        "glass_features":glass_features,
        "styles":styles,
        "mechanisms":mechanisms,
        "favori_products":favori_products,
        "productquantity":ProductQuantity(request)
    }

    return render(request, "category.html",context)

@login_required(login_url='/login/')
def basket(request):
    basket_products = BasketProduct.objects.filter(user=request.user)

    kargo = 29.99
    product_total_price = 0
    total_price = 0
    for product in basket_products:
        product_total_price += product.product.price * float(product.quantity)
    total_price = kargo + product_total_price

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if request.POST.get("submit") == "btndel":
            basket_product = BasketProduct.objects.get(id=product_id)
            basket_product.delete()
            return redirect("basket")
        
        elif request.POST.get("submit") == "minus":
            product = BasketProduct.objects.get(id=product_id)

            product.quantity -= 1
            product.save()

            return redirect("basket")
        
        elif request.POST.get("submit") == "plus":

            product = BasketProduct.objects.get(id=product_id)

            product.quantity += 1
            product.save()
            return redirect("basket")

    context={
        "basket_products":basket_products,
        "product_total_price":product_total_price,
        "total_price":total_price,
        "kargo":kargo,
        "productquantity":ProductQuantity(request)
    }
    return render(request, "basket.html", context)

@login_required(login_url='/login/')
def profil(request):
    user = User.objects.get(username=request.user)
    profil = Profil.objects.get(user=request.user)
    adress = Adress.objects.get(user=request.user)

    if request.method == "POST":
        if request.POST.get("btnsubmit") == "btnpass":
            oldpass = request.POST.get("oldpass")
            newpass = request.POST.get("newpass")
            rnewpass = request.POST.get("rnewpass")

            print(oldpass)
            print(newpass)

            if newpass == rnewpass:
                print("Buırada")
                if user.check_password(oldpass):
                    print("Burar2")
                    user.set_password(newpass)
                    user.save()
                    logout(request)
                    return redirect("login")
                else:
                    messages.error(request, "Eski Şifreniz Yanlış! Tekrar Deneyiniz")
            else:
                messages.error(request, "Şifreler Uyumsuz! Tekrar Deneyiniz")

        elif request.POST.get("btnsubmit") == "btnprofil":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone_number = request.POST.get("phone_number")
            birtdate = request.POST.get("birtdate")

            if user.email != email:
                if not User.objects.filter(email=email).exists():
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    profil.phone_number = phone_number
                    profil.birtdate = birtdate
                    user.save()
                    profil.save()
                    return redirect("profil")
                else:
                    messages.error(request, "Bu E-Posta Adresi Başka Bir Kullanıcı Tarafından Kullanılıyor.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                profil.phone_number = phone_number
                profil.birtdate = birtdate
                user.save()
                profil.save()
                return redirect("profil")
        elif request.POST.get("btnsubmit") == "btnadress":
            adres = request.POST.get("adress")
            province = request.POST.get("province")
            district = request.POST.get("district")
            neighbourhood = request.POST.get("neighbourhood")

            adress.adress = adres
            adress.province = province
            adress.district = district
            adress.neighbourhood = neighbourhood

            adress.save()
            return redirect("profil")

    context={
        "profil":profil,
        "adress":adress,
        "productquantity":ProductQuantity(request)
    }
    return render(request, "user/profil.html",context)

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product)
    comment_user = None
    for comment in comments:
        if comment.user == request.user:
            comment_user = comment.user

    if request.method == "POST":
        
        if request.POST.get("submit") == "btnbasket":
            productid = request.POST.get("productid")
            quantity = int(request.POST.get("quantity"))

            product = Product.objects.get(id=productid)

            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)
                basket_product.quantity += quantity
                basket_product.save()
                return redirect(f"/product-detail/{product_id}")
            else:
                basketproduct = BasketProduct.objects.create(user=request.user, product=product, quantity=quantity)
                basketproduct.save()
                return redirect(f"/product-detail/{product_id}")
        
        elif request.POST.get("submit") == "btncomment":
            comment = request.POST.get("comment")

            new_comment = Comment.objects.create(user=request.user,first_name=request.user.first_name,last_name=request.user.last_name, product=product,comment=comment)
            new_comment.save()
            return redirect(f"/product-detail/{product_id}")
        
        elif request.POST.get("submit") == "commentupdate":
            comment_id = request.POST.get("comment_id")
            comment = request.POST.get("comment")

            update_comment = Comment.objects.get(id=comment_id)
            update_comment.comment = comment
            update_comment.save()
            return redirect(f"/product-detail/{product_id}")

    context={
        "product":product,
        "comments":comments,
        "comment_user":comment_user,
        "productquantity":ProductQuantity(request)
    }

    return render(request, "product-detail.html",context)

def favorite(request):
    favorites = Favorite.objects.filter(user=request.user)

    context={
        "favorites":favorites
    }

    return render(request, "favorite.html",context)




def Login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user is not None:
                    login(request, user)
                    return redirect("index")
            else:
                messages.error(request, "Şifreniz Hatalı! Lütfen Tekrar Deneyiniz.")
        else:
            messages.error(request, "E-Posta Adresiniz Hatalı! Lütfen Tekrar Deneyiniz.")


    return render(request, "user/login.html")

def Register(request):

    if request.method == "POST":
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(password)

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=email, first_name=first_name,last_name=last_name,email=email, password=password)

            user.save()
            login(request,user)
            return redirect("index")
        else:
            messages.error(request, "Bu E-Posta Adresi Başka Bir Kullanıcı Tarafından Kullanılıyor.")

    return render(request, "user/register.html")

def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))

def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response
