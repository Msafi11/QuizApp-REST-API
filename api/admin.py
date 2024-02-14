from django.contrib import admin
from api.models import CustomUser, Teacher, Student, Quiz, QuizQuestion

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)


