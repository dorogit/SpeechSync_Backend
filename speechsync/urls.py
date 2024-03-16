from django.urls import path

from .api import DownloadVideoView, HealthCheck, UploadVideoView

urlpatterns = [
    path("", HealthCheck.as_view(), name="health"),
    path("upload_video/", UploadVideoView.as_view(), name="upload_video"),
    path("download_video/", DownloadVideoView.as_view(), name="download_video"),
]
