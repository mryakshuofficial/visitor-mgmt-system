from django.shortcuts import render , redirect , get_object_or_404
from .models import tbl_Visitors

# Create your views here.
def index(request):
    if request.method == 'POST':
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
    visitors = tbl_Visitors.objects.order_by('-id')
    return render(request,'visitors/index.html',{'visitors':visitors})

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