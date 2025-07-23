from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from masterstudent.models import MasterStudent
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt  

# Create your views here.

def submit_feedback(request):
    if request.method == 'POST':
        gr_no = request.POST.get('gr_no')
        request.session['gr_no'] = gr_no  #  Store in session

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)

            student = MasterStudent.objects.get(gr_no=gr_no)
            feedback.student = student
            feedback.save()

            return render(request, 'feedback/feedback_thank.html', {'student': student})  # Pass student

    else:
        form = FeedbackForm()

    return render(request, 'feedback/submit_feedback.html', {'form': form})

@login_required  # optional
def view_all_feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'feedback/view_all_feedbacks.html', {'feedbacks': feedbacks})

@csrf_exempt  #optionall
def toggle_feedback_status(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.is_solved = not feedback.is_solved
        feedback.save()
    return redirect('view_all_feedbacks')