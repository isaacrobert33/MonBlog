from django.urls import path
from . import views

app_name = 'restapi'

urlpatterns = [
    path('subjects/',
        views.SubjectListView.as_view(),
        name="subject_list"),
    path(
        'subject/<int:subject_id>',
        views.SingleSubject.as_view(),
        name="single_subject"
    )
]
