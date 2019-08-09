from django.contrib import admin
from django import forms
from editor.models import Invite, PythonCode

from .widgets import HtmlEditor
from .models import *

class AppAdminForm(forms.ModelForm):
    model = PythonCode
    class Meta:
        fields = '__all__'
        widgets = {
            'script': HtmlEditor(attrs={'style': 'width: 90%; height: 100%;'}),
        }

class AppAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = AppAdminForm

class AppLabAdminForm(forms.ModelForm):
    model = PythonLab
    class Meta:
        fields = '__all__'
        widgets = {
            'script': HtmlEditor(attrs={'style': 'width: 90%; height: 100%;'}),
        }

class AppLabAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = AppLabAdminForm



#admin.site.register(Invite)
#admin.site.register(PythonCode)
admin.site.register(PythonCode, AppAdmin)
admin.site.register(PythonLab, AppLabAdmin)