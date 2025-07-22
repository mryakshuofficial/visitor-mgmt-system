from django.shortcuts import render , redirect , get_object_or_404
from .models import tbl_Visitors
from django.db.models import Q  # Needed for OR search
import calendar
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template            #pdf
from django.http import HttpResponse                        #pdf
from xhtml2pdf import pisa  
import os                                    #pdf
from django.conf import settings 

# Create your views here.

@login_required
def visitors_index(request):
    if request.method == 'POST':
        visitors = tbl_Visitors.objects.all()
        name = request.POST.get("name")
        visiting_whom = request.POST.get("visiting_whom")
        purpose = request.POST.get("purpose")
        in_time = request.POST.get("in_time")
        out_time = request.POST.get("out_time")
        photo = request.FILES.get("photo")  

        visitor = tbl_Visitors(
            name=name,
            visiting_whom=visiting_whom,
            purpose = purpose,
            in_time = in_time,
            out_time = out_time,
            photo = photo
        )
        visitor.save()
        return redirect('visitors_index')
    # SEARCH BAAR START
    search = request.GET.get('search')
    if search:
        visitors = tbl_Visitors.objects.filter(
            Q(name__icontains=search) | Q(visiting_whom__icontains=search)
        )
    else:
        visitors = tbl_Visitors.objects.all()
    # SEARCH BAAR END

    # DROPDOWNLIST START

    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    selected_whom = request.GET.get('whom')

    if selected_month:
        visitors = visitors.filter(in_time__month=selected_month)
    if selected_year:
        visitors = visitors.filter(in_time__year=selected_year)
    if selected_whom:
        visitors = visitors.filter(visiting_whom=selected_whom)

    visitors = visitors.order_by('-id')

    months = [f"{i:02}" for i in range(1, 13)]
    years = tbl_Visitors.objects.annotate(y=ExtractYear('in_time')).values_list('y', flat=True).distinct()
    whoms = tbl_Visitors.objects.values_list('visiting_whom', flat=True).distinct()


    # visitors = tbl_Visitors.objects.order_by('-id')
    return render(request, 'visitors/index.html', {
        'visitors': visitors,
        'months': months,
        'years': years,
        'whoms': whoms,
    })

@login_required
def edit(request,id):
    visitor = get_object_or_404(tbl_Visitors, id=id)  # ✅ Don't overwrite 'request'
    if request.method == 'POST':
        visitor.name = request.POST.get("name")
        visitor.visiting_whom = request.POST.get("visiting_whom")
        visitor.purpose = request.POST.get("purpose")
        visitor.in_time = request.POST.get("in_time")
        visitor.out_time = request.POST.get("out_time")
        if request.FILES.get('photo'):
            visitor.photo = request.FILES.get("photo")

        visitor.save()
        return redirect('visitors_index')
    return render(request,'visitors/edit.html', {'visitor': visitor})

@login_required
def delete(request,id):
    visitor = get_object_or_404(tbl_Visitors, id=id)  # ✅ Don't overwrite 'request'
    visitor.delete()
    return redirect('visitors_index')

def login_user(request):
    #  Agar already logged in ho, to redirect to index
    if request.user.is_authenticated:
        return redirect('visitors_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user :
            login(request,user)
            return redirect('visitors_index')
        else:
            return render(request, 'visitors/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'visitors/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)

    
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback  
    )
    if pisa_status.err:
        return HttpResponse('Error generating PDF: %s' % pisa_status.err)
    return response

def export_pdf(request):
    visitors = tbl_Visitors.objects.all().order_by('-id')
    context = {'visitors': visitors}
    return render_to_pdf('visitors/pdf.html', context)

def link_callback(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

