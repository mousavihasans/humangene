from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.contenttypes.admin import GenericStackedInline

from cms.models import Page, Tag, Category, News, Comment, CustomerCompanies, Service, Feature, CompanyMembers, Slider, \
    SliderItem, ContactMessage


class CommentInline(GenericStackedInline):
    model = Comment
    # fields = ('user', 'is_approved', 'enabled')
    # readonly_fields = ('user', 'created_at', 'text', 'is_approved',
    #                    'supervised_by', 'supervised_date', 'enabled')
    # extra = 0


@register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title_fa', 'title_en', 'text_fa', 'image', 'category', 'published_date')
    # readonly_fields = ('title',)


@register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


@register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    pass


@register(Slider)
class SliderAdmin(admin.ModelAdmin):
    pass


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@register(CustomerCompanies)
class CustomerCompaniesAdmin(admin.ModelAdmin):
    pass


@register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


@register(CompanyMembers)
class CompanyMemberAdmin(admin.ModelAdmin):
    pass


@register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    pass
