from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
import cv2
# Create your views here.


def validate(video_size, video_length, video_type):
    response = {"error": False, "message": ""}
    try:
        if(not(isinstance(video_size, int) or isinstance(video_size, float)) or video_size <= 0):
            response["error"] = True
            response["message"] = "size must be greater than 0"
        elif(not(isinstance(video_length, int) or isinstance(video_length, float)) or video_length <= 0):
            response["error"] = True
            response["message"] = "length must be greater than 0"
        elif(video_type == None or not(video_type == "mp4" or video_type == "mkv")):
            response["error"] = True
            response["message"] = "type must be mp4 or mkv"
    except Exception:
        response["error"] = True
        response["message"] = "invalid data passed"
    return response


def get_charge(video_size, video_length):
    charge = 0
    if(video_size > 500):
        # charge 12.5$ above 500MB
        charge += 12.5
    else:
        # charge 5$ above 500MB
        charge += 5
    if(video_length < 6.3):
        # charge 12.5$ above 6 minutes 18 second which is 6.3 minutes
        charge += 12.5
    else:
        # charge 20$ above 6 minutes 18 second
        charge += 20
    return charge


@api_view(["POST"])
def post_video(request):
    try:
        # this removes the first handler (MemoryFileUploadHandler....)
        request.upload_handlers.pop(0)
        body = request.data
        title = body.get("title", None)
        video = body.get("video", None)
        if(title == None):
            return Response({"message": "title is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if(video == None or not (video.content_type == "video/mp4" or video.content_type == "video/mkv")):
            return Response({"message": "video is required and must be mp4 or mkv"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        size_in_bytes = video.size
        # 1gb = 1000000000 bytes
        size_in_gb = size_in_bytes / 1000000000
        if(size_in_gb > 1):
            return Response({"message": "video size cannot exceed 1gb"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        cap = cv2.VideoCapture(video.temporary_file_path())
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps
        # 10minutes = 60seconds
        if(duration > 600):
            return Response({"message": "video size cannot exceed 10minute length"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # charge for the video
        # 1mb = 1000000 bytes
        video_size = size_in_bytes / 1000000
        # 1min = 60sec
        video_length = duration / 60
        charge = get_charge(video_size, video_length)
        created_video = Video.objects.create(title=title, video=video)
        serializer = VideoSerializer(
            created_video, many=False, context={'request': request})
        return Response({ "video": serializer.data, "charge": f"charge for the video is {charge}$"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"message": "failed to upload video"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_videos(request):
    try:
        videos = Video.objects.all()
        serializer = VideoSerializer(
            videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return Response({"message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def charge(request):
    body = request.data
    # video_size must be passed in MB
    video_size = body.get('video_size', None)
    # video_length must be passed in minutes
    video_length = body.get('video_length', None)
    video_type = body.get('video_type', None)
    response = validate(video_size, video_length, video_type)
    if(response["error"]):
        return Response({"message": response["message"]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    charge = get_charge(video_size, video_length)
    return Response({"message": f"charge for the video is {charge}$"}, status=status.HTTP_200_OK)