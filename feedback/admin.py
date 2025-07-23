from django.contrib import admin
from .models import Feedback
# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'submitted_at')
    # We do NOT show student field here to others — only for dev use