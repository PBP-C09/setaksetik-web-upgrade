from django.contrib import admin
from .models import ReviewEntry  # Import your model

class ReviewEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'menu', 'place', 'description')  # Adjust fields as necessary
    search_fields = ('id',)  # Add a comma to make it a tuple

# Register your model with the admin site
admin.site.register(ReviewEntry, ReviewEntryAdmin)
