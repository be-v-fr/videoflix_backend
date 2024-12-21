from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Video, VideoCompletion

class VideoResource(resources.ModelResource):
    
    class Meta:
        model = Video
        exclude = ('duration_in_seconds',)

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
     resource_class = VideoResource
     readonly_fields = ('duration_in_seconds',)

admin.site.register(VideoCompletion)