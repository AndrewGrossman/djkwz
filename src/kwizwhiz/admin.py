from django.contrib import admin
from .models import *

# Register all of our models

class KwizWhizAdmin(admin.ModelAdmin):
    """This custom model allows us to exclude tracking fields"""
    exclude = ('created_by',)

admin_site = admin.sites.site

admin_site.register(Lesson, KwizWhizAdmin)
admin_site.register(LessonPrinciple, KwizWhizAdmin)
admin_site.register(Question, KwizWhizAdmin)
admin_site.register(Quiz, KwizWhizAdmin)
admin_site.register(QuizAttempt, KwizWhizAdmin)

