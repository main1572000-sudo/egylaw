from django.shortcuts import render,get_object_or_404
from .models import Info,Catagory
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
#.............
@csrf_exempt
def ping(request):
    return HttpResponse('ping', content_type="text/plain")

def main(request):
    return render(request,'main.html')

def law(request,pk):
    z = Info.objects.filter(pk = pk)
    data = get_object_or_404(Info,pk=pk)
    return render(request, 'law.html', {'data': data,'subject':z})

def search_results_view(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        results = Info.objects.filter(
            Q(header__icontains=query) | 
            Q(content__icontains=query) | 
            # افترضنا هنا أن اسم الحقل النصي داخل جدول القسم هو name أو title
            # قم بتغيير 'name' إلى اسم الحقل الفعلي داخل جدول الـ Category عندك
            Q(catagory__name__icontains=query) 
        ).distinct()
        
    return render(request, 'search_results.html', {'results': results, 'query': query})

def archive_view(request):
    all_laws = Info.objects.all().order_by('-id') # جلب كل الأخبار من الأحدث للأقدم
    paginator = Paginator(all_laws, 10) # عرض 15 خبر في كل صفحة
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'archive.html', {'page_obj': page_obj})

def Privacy_Policy(request):
    return render(request,'Privacy_Policy.html')

def Terms_and_Conditions(request):
    return render(request,'terms.html')

def About_Us(request):
    return render(request,'aboutus.html')

def Contact_Us(request):
    return render(request,'contactus.html')

def Soon(request):
    return render(request,'soon.html')