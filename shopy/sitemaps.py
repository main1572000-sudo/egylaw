from django.contrib.sitemaps import Sitemap
from .models import Info # استبدل Post بموديل المقالات أو الصفحات لديك

class PostSitemap(Sitemap):
    changefreq = "weekly" # معدل تغير المحتوى (يومي، أسبوعي، شهري)
    priority = 0.8        # أهمية الروابط من 0.0 إلى 1.0

    def items(self):
        return Info.objects.all() # جلب جميع العناصر التي تريد أرشفتها

    def lastmod(self, obj):
        return obj.updated_at # تاريخ آخر تحديث للمقال (تأكد من وجود حقل تاريخ في الموديل)