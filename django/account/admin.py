from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account



    
# class ProfileInline(admin.TabularInline):
#     model = Profile
#     extra = 1

    
class AccountAdmin(UserAdmin):
    # inlines = [
    #     ProfileInline
    # ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name")}),
        (
            "مجوزها",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("تاریخ های مهم", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ("id", "last_name", "first_name", "email", "is_active", "is_staff", "is_superuser")
    search_fields = ["last_name"]
    ordering = ["last_name"]
    list_filter = ("is_staff", "is_superuser", "is_active")
    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)
