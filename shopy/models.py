from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse # 1. استيراد دالة reverse الهامة جداً
# Create your models here.
class Catagory(models.Model):
    name = models.CharField('التصنيف',max_length=50)
    
    def __str__(self):
        return self.name   
#--------------------------------------------------------
#--------------------------------------------------------
class Info(models.Model):
    header = models.CharField('العنوان',max_length=50)
    content = CKEditor5Field('المحتوى', config_name='extends')
    catagory = models.ForeignKey(Catagory,verbose_name='التصنيف', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.header
def get_absolute_url(self):
    return reverse('law', args=[self.id])
    
    
# class Product(models.Model):
#     x = [
#         ("1", "dress"),
#         ("2", "bag"),
#         ("3", "shoes"),
#         ("4", "other"),]

#     name = models.CharField(max_length=30,null=False)
#     size = models.CharField(max_length=10,blank=True,default='all')
#     price = models.IntegerField(default=999)
#     catagories = models.CharField(max_length=2,choices=SEMESTER_CHOICES,default='1')
#     photo = models.ImageField(upload_to='photos/%y/%m/%d',default='404.png')
#     description = models.TextField(null=True,default='none')