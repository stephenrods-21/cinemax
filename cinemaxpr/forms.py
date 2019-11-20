from django import forms
from .models import AttachmentDetail

class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = AttachmentDetail
        fields = ('attachment',)