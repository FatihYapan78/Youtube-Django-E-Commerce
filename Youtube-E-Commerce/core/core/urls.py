from django.contrib import admin
from django.urls import path
from AppEcommerce.views import *
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index")
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    ]
