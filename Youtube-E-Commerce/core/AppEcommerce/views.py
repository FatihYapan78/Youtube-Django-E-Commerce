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

def index(request):
    products = Product.objects.all()

    context={
        "products":products
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

    filters = Q()

    if "marka" in request.GET:
        # Birden fazla marka seçilebileceği için getlist() yönetimini kullanarak tüm seçimleri alıyoruz.
        markalar = request.GET.getlist("marka")
        # Marka seçimlerini Q nesnesine ekliyoruz.
        for marka in markalar:
            filters |= Q(brand=marka)

    if "cinsiyet" in request.GET:
        filters &= Q(gender=request.GET.get("cinsiyet"))

    if "renk" in request.GET:
        renkler = request.GET.getlist("renk")
        for renk in renkler:
            filters |= Q(color=renk)

    if "kasa_sekli" in request.GET:
        kasa_sekilleri = request.GET.getlist("kasa_sekli")
        for kasa_sekli in kasa_sekilleri:
            filters |= Q(case_shape=kasa_sekli)

    if "kayis_tipi" in request.GET:
        kayis_tipleri = request.GET.getlist("kayis_tipi")
        for kayis_tipi in kayis_tipleri:
            filters |= Q(strap_type=kayis_tipi)

    if "cam_ozellik" in request.GET:
        cam_ozellikleri = request.GET.getlist("cam_ozellik")
        for cam_ozellik in cam_ozellikleri:
            filters |= Q(glass_feature=cam_ozellik)

    if "tarz" in request.GET:
        tarzlar = request.GET.getlist("tarz")
        for tarz in tarzlar:
            filters |= Q(tarz=tarz)

    if "mekanizma" in request.GET:
        mekanizmalar = request.GET.getlist("mekanizma")
        for mekanizma in mekanizmalar:
            filters |= Q(mechanism=mekanizma)

    if "fiyat_min" in request.GET and "fiyat_max" in request.GET and request.GET.get("fiyat_max") != "":
        fiyat_min = request.GET.get("fiyat_min")
        fiyat_max = request.GET.get("fiyat_max")

        if fiyat_min == "":
            fiyat_min = 0

        filters &= Q(price__gte=fiyat_min, price__lte=fiyat_max)

    products = Product.objects.filter(filters)

    context = {
        "products":products,
        "brands":brands,
        "genders":genders,
        "colors":colors,
        "case_shapes":case_shapes,
        "strap_types":strap_types,
        "glass_features":glass_features,
        "styles":styles,
        "mechanisms":mechanisms
    }

    return render(request, "category.html",context)







def Profil(request):

    return render(request, "user/profil.html")






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

        user = User.objects.create(username=email, first_name=first_name,last_name=last_name,email=email, password=password)

        if User.objects.filter(email=email).exists():
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
