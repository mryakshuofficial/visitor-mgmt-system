from django.shortcuts import render ,redirect , HttpResponse , get_object_or_404
from django.contrib.auth.decorators import login_required
from . import urls
# for QR code
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from .models import FeePayment
from django.views.decorators.csrf import csrf_exempt
import base64
from django.utils.crypto import get_random_string
#pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
# for EMAIL
from django.core.mail import EmailMessage

#fetch data from master page
from django.http import JsonResponse
from masterstudent.models import MasterStudent

def fees_index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        student_class = request.POST.get('student_class')
        amount = request.POST.get('amount')
        email = request.POST.get('email')     

        # Create unique payment ID
        payment_id = get_random_string(10).upper()    

        payment = FeePayment.objects.create(
            student_name=name,
            student_class=student_class,
            amount=amount,
            email=email,
            payment_id=payment_id,
            is_paid=False,
        )
        # Generate UPI QR Code 
        upi_link = f'upi://pay?pa=yash0808080808-1@okicici&pn=Yash%20Prajapati&am={amount}&cu=INR'
        qr_img = qrcode.make(upi_link)
        buffer = BytesIO()
        qr_img.save(buffer)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # return HttpResponse("Payment confirmed!")

        return render(request, 'fees_management/show_qr.html', {
            'payment': payment,
            'qr_data': img_base64,
            'upi_link': upi_link,
        })

    return render(request,"fees_management/index.html")

def generate_pdf_receipt(payment):
    template_path = 'fees_management/pdf_receipt.html'
    context = {'payment': payment}
    template = get_template(template_path)
    html = template.render(context)

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    
    if not pisa_status.err:
        return buffer.getvalue()
    return None

@csrf_exempt
def confirm_payment(request, payment_id):
    payment = get_object_or_404(FeePayment, id=payment_id)

    if request.method == 'POST':
        payment.is_paid = True
        payment.save()

        # Generate PDF
        pdf_data = generate_pdf_receipt(payment)
        if pdf_data:
            # Send Email
            subject = 'Hostel Fee Payment Receipt'
            body = f'Dear {payment.student_name},\n\nThank you for your payment of ₹{payment.amount}.\nPlease find your receipt attached.\n\nRegards,\nHostel Admin'
            from_email = 'yash0808080808@gmail.com'         # ✅ same as EMAIL_HOST_USER
            to_email = [payment.email]

            email = EmailMessage(subject, body, from_email, to_email)
            email.attach(f"receipt_{payment.payment_id}.pdf", pdf_data, 'application/pdf')
            email.send()

            # Also show in browser
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="receipt_{payment.payment_id}.pdf"'
            return response
        else:
            return HttpResponse("Error generating PDF")
    return redirect('fees_index')

def fetch_student_data(request, grno):
    try:
        student = MasterStudent.objects.get(gr_no=grno)
        data = {
            'name': student.fname + ' ' + student.lname,
            'student_class': student.student_class,
            'email': student.email,
            'village': student.village,
            'mobile': student.mobile,
        }
        return JsonResponse(data)
    except MasterStudent.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    return redirect('fees_index')
