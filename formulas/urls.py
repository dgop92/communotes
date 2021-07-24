
from django.urls import path, re_path
from formulas import views

urlpatterns = [
    path('photos/',
        views.PhotoList.as_view(),
        name=views.PhotoList.name
    ),
    re_path(r'^photos/(?P<pk>[0-9]+)$',
        views.PhotoDetail.as_view(),
        name=views.PhotoDetail.name
    ),

    path('photo-classifications/',
        views.PhotoClassificationList.as_view(),
        name=views.PhotoClassificationList.name
    ),
    re_path(r'^photo-classifications/(?P<pk>[0-9]+)$',
        views.PhotoClassificationDetail.as_view(),
        name=views.PhotoClassificationDetail.name
    ),

    path('photo-contexts/',
        views.PhotoContextList.as_view(),
        name=views.PhotoContextList.name
    ),
    re_path(r'^photo-contexts/(?P<pk>[0-9]+)$',
        views.PhotoContextDetail.as_view(),
        name=views.PhotoContextDetail.name
    ),

    path('profile/',
        views.ProfileDetail.as_view(),
        name=views.ProfileDetail.name
    ),

    path('reviews/',
        views.ReviewList.as_view(),
        name=views.ReviewList.name
    ),
    re_path(r'^reviews/(?P<pk>[0-9]+)$',
        views.ReviewDetail.as_view(),
        name=views.ReviewDetail.name
    ),

    path('subjects/',
        views.SubjectList.as_view(),
        name=views.SubjectList.name
    ),
    re_path(r'^subjects/(?P<pk>[0-9]+)$',
        views.SubjectDetail.as_view(),
        name=views.SubjectDetail.name
    ),

    path('tags/',
        views.TagList.as_view(),
        name=views.TagList.name
    ),
    re_path(r'^tags/(?P<pk>[0-9]+)$',
        views.TagDetail.as_view(),
        name=views.TagDetail.name
    ),


]
