from django.shortcuts import render , redirect , get_object_or_404
from .models import tbl_Visitors
from django.db.models import Q  # Needed for OR search
import calendar
from django.db.models.functions import ExtractMonth, ExtractYear

# Create your views here.
def index(request):
    if request.method == 'POST':
        visitors = tbl_Visitors.objects.all()
        name = request.POST.get("name")
        visiting_whom = request.POST.get("visiting_whom")
        purpose = request.POST.get("purpose")
        in_time = request.POST.get("in_time")
        out_time = request.POST.get("out_time")

        visitor = tbl_Visitors(
            name=name,
            visiting_whom=visiting_whom,
            purpose = purpose,
            in_time = in_time,
            out_time = out_time
        )
        visitor.save()
        return redirect('/')
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

def edit(request,id):
    visitor = get_object_or_404(tbl_Visitors, id=id)  # ✅ Don't overwrite 'request'
    if request.method == 'POST':
        visitor.name = request.POST.get("name")
        visitor.visiting_whom = request.POST.get("visiting_whom")
        visitor.purpose = request.POST.get("purpose")
        visitor.in_time = request.POST.get("in_time")
        visitor.out_time = request.POST.get("out_time")

        visitor.save()
        return redirect('/')
    return render(request,'visitors/edit.html', {'visitor': visitor})

def delete(request,id):
    visitor = get_object_or_404(tbl_Visitors, id=id)  # ✅ Don't overwrite 'request'
    visitor.delete()
    return redirect('/')