from django.contrib import admin
from .models import MeatupRequest, Wishlist

if not admin.site.is_registered(MeatupRequest):
    class MeatupRequestAdmin(admin.ModelAdmin):
        list_display = ['sender', 'receiver', 'requested_at']
        list_filter = ['sender', 'requested_at']

    admin.site.register(MeatupRequest, MeatupRequestAdmin)

if not admin.site.is_registered(Wishlist):
    class WishlistAdmin(admin.ModelAdmin):
        list_display = ['owner', 'created_at']
        list_filter = ['owner', 'created_at']

    admin.site.register(Wishlist, WishlistAdmin)