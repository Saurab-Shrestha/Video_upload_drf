from django.shortcuts import render,redirect
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView,ListAPIView
from .serializers import VideoSerializer
from .models import Video
from django.views.generic import ListView
from .forms import VideoUploadForm

def VideoUploadView(request):

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = VideoUploadForm()

    return render(request,'index.html',{'form':form})


class VideoListView(ListView):
    model = Video
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

from rest_framework import filters, status


class VideoView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'created_at']

class VideoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class  = VideoSerializer


class VideoUpload(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
import os
class VideoDownloadListAPIView(ListAPIView):

    def get(self,request,pk,format=None):
        queryset = Video.objects.get(pk = pk)
        file_handle = os.path.join(settings.MEDIA_ROOT,queryset)

        if os.path.exists(file_handle):
            document = open(file_handle,'rb')
            response = HttpResponse(FileWrapper(document),content_type='whatever')
            response['Content-Disposition'] = 'attachment; filename="%s"' % document.name

        return response