from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass
    # group_fieldsets = True 
    # class Media:
    #     js = (
    #         'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    #         'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
    #         'modeltranslation/js/tabbed_translation_fields.js',
    #     )
    #     css = {
    #         'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
    #     }

@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    pass

@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    pass

@admin.register(CaseShape)
class CaseShapeAdmin(TranslationAdmin):
    pass

@admin.register(StrapType)
class StrapTypeAdmin(TranslationAdmin):
    pass

@admin.register(GlassFeature)
class GlassFeatureAdmin(TranslationAdmin):
    pass

@admin.register(Style)
class StyleAdmin(TranslationAdmin):
    pass

@admin.register(Mechanism)
class MechanismAdmin(TranslationAdmin):
    pass
