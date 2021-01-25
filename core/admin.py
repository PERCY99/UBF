from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
import nested_admin
from . import models

admin.site.site_header = 'UPSCBasicFunda'


# add_fieldsets = (
#     (None, {
#         'fields': ('email', 'username', 'is_student', 'is_teacher', 'password1', 'password2')
#     }),
#     ('Permissions', {
#         'fields': ('is_superuser', 'is_staff')
#     })
# )
# fieldsets = (
#     (None, {
#         'fields': ('email', 'username', 'is_student', 'is_teacher', 'password')
#     }),
#     ('Permissions', {
#         'fields': ('is_superuser', 'is_staff')
#     })
# )

class UserAdmin(BaseUserAdmin):

    list_display = ['email', 'username', 'mobile']
    list_display_links = ['email', 'username']
    search_fields = ('email', 'username')
    ordering = ('email',)

class PDFInline(nested_admin.NestedTabularInline):
	model = models.PDF
	extra = 4


class MCQInline(nested_admin.NestedTabularInline):
	model = models.MCQ
	extra = 4


class SummaryInline(nested_admin.NestedTabularInline):
	model = models.Summary
	extra = 4



class SubCategoryInline(nested_admin.NestedTabularInline):
	model = models.SubCategory
	inlines = [PDFInline,SummaryInline, MCQInline]
	extra = 5


class CategoryAdmin(nested_admin.NestedModelAdmin):
	inlines = [SubCategoryInline,]


class SubCategoryAdmin(nested_admin.NestedModelAdmin):
    inlines = [PDFInline, SummaryInline, MCQInline]


admin.site.register(models.User)
# admin.site.unregister(Group)
admin.site.register(models.TeamMember)
admin.site.register(models.TeamForm)
admin.site.register(models.ContactUs)
admin.site.register(models.Feedback)
admin.site.register(models.FAQ)
admin.site.register(models.Article)
admin.site.register(models.News)
admin.site.register(models.Newsletter)

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.PDF)
admin.site.register(models.MCQ)
admin.site.register(models.Summary)
admin.site.register(models.Session)
admin.site.register(models.UserSubscriptions)