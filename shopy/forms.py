from django import forms
from .models import Info

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['header', 'catagory', 'slug', 'content']
        
        # يمكنك إضافة تخصيصات للعناصر (Widgets) لتتوافق مع تصميمك
        widgets = {
            'header': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل عنوان المقال هنا...'
            }),
            'catagory': forms.Select(attrs={
                'class': 'form-control'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اختياري: سيتم توليده تلقائياً إذا تركته فارغاً'
            }),
        }