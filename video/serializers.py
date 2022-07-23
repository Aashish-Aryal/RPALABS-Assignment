from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Video
        fields = ('id', 'title', 'video', 'uploaded_date')
    def get_video(self, instance):
        request = self.context.get('request', None)
        if not request:
            return instance.video.url
        video_url = instance.video.url
        return request.build_absolute_uri(video_url)
