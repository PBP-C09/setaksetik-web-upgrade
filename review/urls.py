from django.urls import path
from . import views
from review.views import create_review_flutter, delete_review_flutter, show_review, add_review_entry_ajax, create_review_entry, show_review_menu, show_review_owner_flutter, show_xml, show_json, show_json_by_id, show_xml_by_id, get_review, submit_reply_flutter, update_reply_flutter, show_review_owner, get_review_entries

app_name = 'review'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('create-review-entry', create_review_entry, name="create_review_entry"),
    path('create-review-entry-ajax', add_review_entry_ajax, name='create-review-entry-ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('json/<int:menu_id>/', get_review_entries, name='get_review_entries'),
    path('get_reviews_from_owner/', views.get_review_from_owner, name='get_reviews_from_owner'),
    path('pantaureview/', show_review_owner, name='show_review_owner'),
    path('pantau-review-owner/', show_review_owner_flutter, name='show_review_owner_flutter'),
    path('submit_reply/', views.submit_reply, name='submit_reply'),
    path('edit-review/<uuid:id>', views.edit_review, name='edit_review'),
    path('delete-review/<uuid:id>', views.delete_review, name='delete_review'),
    path('get_review/', get_review, name='get_review'),
    path('<int:menu_id>/', show_review, name='show_review_menu'),
    path('create-review-flutter/', create_review_flutter, name='create_review_flutter'),
    path('show-review-flutter/', views.show_review_flutter, name='show_review_flutter'),
    path('update-reply/', views.update_reply, name='update_reply'),
    path('submit-reply-flutter/', submit_reply_flutter, name='submit_reply_flutter'),
    path('delete-review-flutter/', delete_review_flutter, name='delete_review_flutter'),
    path('update-reply-flutter/', update_reply_flutter, name='update_reply_flutter'),
]