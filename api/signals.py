from django.dispatch import receiver
from api import models
from django.db.models.signals import post_save


@receiver(post_save, sender=models.CustomUser)
def teacher_student_signal_handler(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'teacher':
            teacher = models.Teacher(custom_user=instance)
            teacher.save()
        elif instance.role == 'student':
            student = models.Student(custom_user=instance)
            student.save()