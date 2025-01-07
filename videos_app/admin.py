from django.contrib import admin
from django import forms
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Video, VideoCompletion

class VideoResource(resources.ModelResource):
    
    class Meta:
        model = Video
        exclude = ('duration_in_seconds',)

class VideoAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    
    class Meta:
        model = Video
        fields = '__all__'

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    form = VideoAdminForm
    resource_class = VideoResource
    readonly_fields = ('duration_in_seconds',)

admin.site.register(VideoCompletion)