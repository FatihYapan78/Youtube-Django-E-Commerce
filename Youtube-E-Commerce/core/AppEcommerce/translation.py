from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('model', 'description')

@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('brand',)

@register(Gender)
class GenderTranslationOptions(TranslationOptions):
    fields = ('gender',)

@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ('color',)

@register(CaseShape)
class CaseShapeTranslationOptions(TranslationOptions):
    fields = ('case_shape',)

@register(StrapType)
class StrapTypeTranslationOptions(TranslationOptions):
    fields = ('strap_type',)

@register(GlassFeature)
class GlassFeatureTranslationOptions(TranslationOptions):
    fields = ('glass_feature',)

@register(Style)
class StyleTranslationOptions(TranslationOptions):
    fields = ('style',)

@register(Mechanism)
class MechanismTranslationOptions(TranslationOptions):
    fields = ('mechanism',)