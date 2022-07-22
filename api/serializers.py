
from rest_framework import serializers
from .models import Video
from django.core.exceptions import ValidationError
from pymediainfo import MediaInfo


def total_charges(data):
    video_size = data['video_file'].size
    video_size_in_mb = video_size / 1000000

    media_info = MediaInfo.parse(data['video_file'])
    duration_in_ms = media_info.tracks[0].duration
    duration_in_min = duration_in_ms / 60000
    duration_in_sec = duration_in_min * 60
    total = 0
    if video_size_in_mb < 500:
        total += 5
        if duration_in_sec < 378:  # in sec (6min 18 second)
            total += 12.5
        else:
            total += 20
    else:
        total += 12.5
        if duration_in_sec < 378:  # in sec (6min 18 second)
            total += 12.5
        else:
            total += 20
    print("Total cost: ", total)
    return total


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id','title','video_file','created_at')

    def validate(self, data):
        video_size = data['video_file'].size # returns in bytes
        video_size_in_mb = video_size / 1000000
        print("video size:",video_size_in_mb)
        # 1GB =  1073741824 bytes
        if video_size >  1073741824:
            raise ValidationError("Video size exceeded 1GB.")

        media_info = MediaInfo.parse(data['video_file'])
        duration_in_ms = media_info.tracks[0].duration

        duration_in_min = duration_in_ms / 60000
        duration_in_sec = duration_in_min*60
        print("Duration in sec:",duration_in_sec )
        if duration_in_min > 10:
            raise ValidationError("Video length exceeded 10min.")
        total_charges(data)
        return data

