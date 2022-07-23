from django.urls import path
from .views import post_video, get_videos, charge

urlpatterns = [
    path('upload', post_video, name="post-video"),
    path('list', get_videos, name="get-videos"),
    path('charge', charge, name="get-charge")
]