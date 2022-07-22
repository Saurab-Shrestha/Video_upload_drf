from django.urls import path
from .views import VideoView,VideoUploadView, VideoListView, \
    VideoDetail,VideoUpload, VideoDownloadListAPIView
urlpatterns = [
    path('',VideoView.as_view(),name='video'),
    path('upload/',VideoUploadView,name='video_upload'),
    path('list/',VideoListView.as_view(),name='video_list'),
    path('<int:pk>/',VideoDetail.as_view(),name='video_detail'),
    path('create/',VideoUpload.as_view()),
    path('download/<int:pk>',VideoDownloadListAPIView.as_view())
]