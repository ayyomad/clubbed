from django.contrib import admin
from .models import Club
from .models import ClubMembership

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "club", "role", "title", "display_order")
    list_select_related = ("user", "club")