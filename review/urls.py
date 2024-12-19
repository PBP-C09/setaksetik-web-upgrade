from django.urls import path
from . import views
from review.views import create_review_flutter, show_review, add_review_entry_ajax, create_review_entry, show_xml, show_json, show_json_by_id, show_xml_by_id, get_review

app_name = 'review'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('create-review-entry', create_review_entry, name="create_review_entry"),
    path('create-review-entry-ajax', add_review_entry_ajax, name='create-review-entry-ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('submit_reply/', views.submit_reply, name='submit_reply'),
    path('edit-review/<uuid:id>', views.edit_review, name='edit_review'),
    path('delete-review/<uuid:id>', views.delete_review, name='delete_review'),
    path('get_review/', get_review, name='get_review'),
    # path('update-reply/', views.update_reply, name='update_reply'),
    path('create-review-flutter/', create_review_flutter, name='create_review_flutter'),
    path('update-reply/', views.update_reply, name='update_reply'),
]