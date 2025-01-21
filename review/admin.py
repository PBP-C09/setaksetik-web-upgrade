from django.contrib import admin
from .models import ReviewEntry
from review.models import ReviewEntry

class ReviewEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'menu', 'place', 'description')
    search_fields = ('id',)

admin.site.register(ReviewEntry, ReviewEntryAdmin)
