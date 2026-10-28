from django.shortcuts import render,get_object_or_404,redirect
from .models import Info
from django.http import HttpResponse , JsonResponse , HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User , Permission
from django.contrib.auth.decorators import permission_required, user_passes_test , login_required
from .forms import InfoForm
# دالة تختصر الشرطين: هل مسجل دخول + هل هو مشرف/طاقم؟
admin_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff)
#.............
@csrf_exempt
def ping(request):
    return HttpResponse('ping', content_type="text/plain")

def main(request):
    queryset = Info.objects.all().order_by('-id')[:5]
    return render(request,'main.html',context={'page_obj':queryset})

def law(request,pk,slug):
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


def Consult(request):
    return render(request,'consult.html')

@admin_required
def dashboard_home(request):
    return render(request,'dashboard.html')

@admin_required
def users_list(request):
    # 1. جلب كل المستخدمين من قاعدة البيانات
    all_users = User.objects.all().order_by('-id')
    perms=[]
    for x in all_users:
        if x.has_perm('shopy.add_info'):
            perms.append(x.username)
    # 2. إنشاء كائن التقسيم وتحديد 20 مستخدمًا في كل صفحة
    paginator = Paginator(all_users, 20)
    
    # 3. جلب رقم الصفحة الحالية من الـ URL (افتراضياً 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number) # يجلب 20 مستخدمًا للصفحة المحددة فقط
    
    context = {
        'users': page_obj,          # قائمة الـ 20 مستخدمًا الخاصة بهذه الصفحة
        'page': page_obj.number,    # رقم الصفحة الحالية
        'has_next': page_obj.has_next(), # هل توجد صفحة تالية؟ (لتفعيل زر التالي)
        'perms':perms
    }
    return render(request, 'dashboard_users.html', context)
@admin_required
def activate_user(request , user_id):
    x = User.objects.get(pk = user_id)
    x.is_active = True
    x.save()
    return redirect('users_list')

@admin_required
def deactivate_user(request, user_id):
    x = User.objects.get(pk = user_id)
    x.is_active = False
    x.save()
    return redirect('users_list')

@admin_required
def delete_user(request, user_id):
    x = User.objects.get(pk = user_id)
    x.delete()
    return redirect('users_list')

@admin_required
def Topics(request):
    all_topics = Info.objects.all().order_by('-id') # جلب كل الأخبار من الأحدث للأقدم
    paginator = Paginator(all_topics,12) # عرض 15 خبر في كل صفحة
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'topics.html',{'page_obj':page_obj})

@login_required
@permission_required('shopy.add_info')
def Add_Topic(request):
    user_has_perm = request.user.has_perm('shopy.add_info')
    if user_has_perm:
        if request.method == 'POST':
            form = InfoForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
                return redirect('archive') # اسم مسار صفحة عرض المقالات
        else:
            form = InfoForm()
            
        context = {
            'form': form
        }
        return render(request, 'new_topic.html', context)
    else:
        return HttpResponseForbidden('لا تملك الصلاحية')
    
@login_required
@permission_required('shopy.add_info')
def Delete_Topic(request,topic_id):
    x = Info.objects.get(pk = topic_id)
    if request.user == x.author or request.user.username == 'admin':
        x.delete()
        return redirect('archive')
    else:
        return HttpResponseForbidden('لست صاحب المقال')

@login_required
@permission_required('shopy.add_info')
def Edit_Topic(request, pk):
    # جلب المقال المراد تعديله عبر الـ pk، أو إظهار صفحة 404 إذا لم يتم العثور عليه
    topic = get_object_or_404(Info, pk=pk)
    if request.user == topic.author or request.user.username == 'admin':
        if request.method == 'PUT':
            # ربط الـ form بالبيانات الجديدة ومع بيانات المقال الحالي (instance=topic)
            form = InfoForm(request.PUT, instance=topic)
            if form.is_valid():
                form.save()
                return redirect('archive')  # العودة لصفحة عرض المقالات بعد الحفظ
        else:
            # ملء الحقول تلقائياً ببيانات المقال القديمة لتعديلها
            form = InfoForm(instance=topic)

        context = {
            'form': form,
            'is_edit': True
        }
        return render(request, 'edit_topic.html', context)
    else:
        return HttpResponseForbidden('لست صاحب المقال')

from django.core.mail import send_mail

def send_verification_email(user_email, activation_link):
    send_mail(
        subject="تفعيل حسابك",
        message=f"مرحباً، انقر على الرابط التالي لتفعيل حسابك: {activation_link}",
        from_email=None,  # سيستخدم تلقائياً قيمة DEFAULT_FROM_EMAIL
        recipient_list=[user_email],
        fail_silently=False,
    )

@login_required
def toggle_topic_permission(request,pk):
    # فرضنا أن اسم الصلاحية المراد إعطاؤها هو 'view_topics'
    # يمكنك استبدالها بالصلاحية الخاصة بك
    if request.method == 'POST':
        try:
            permission = Permission.objects.get(codename='add_info')
            user = User.objects.get(pk=pk)
            
        
        # التحقق مما إذا كان المستخدم يملك الصلاحية مسبقاً
            if user.has_perm('shopy.add_info'): # استبدل app_name باسم التطبيق لديك
                user.user_permissions.remove(permission)
                return HttpResponse('تم حذف اذن انشاء المقالات من المستخدم ')
            else:
                user.user_permissions.add(permission)
                return HttpResponse('تم منح اذن انشاء المقالات الى المستخدم')
            
        except Permission.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'الصلاحية غير موجودة في النظام'}, status=400)