from django import forms
from django.forms.widgets import Textarea

from codemirror import CodeMirrorTextarea

from blog.models import Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            "body": CodeMirrorTextarea(),
            "meta_description": Textarea(),
        }
        exclude = []
