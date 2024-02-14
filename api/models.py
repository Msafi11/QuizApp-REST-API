from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('teacher', 'teacher'), ('student', 'student')], null=False, blank=False)

class Teacher(models.Model):
    custom_user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)


class Student(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class QuizQuestion(models.Model):
    text = models.TextField()
    options = models.JSONField()
    correct_answer_index = models.PositiveIntegerField()

class Quiz(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=100,unique=True)
    questions = models.ManyToManyField(QuizQuestion)
    time_limit = models.PositiveIntegerField()
    end_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Set the end time for the quiz based on the time limit
        if not self.pk and self.time_limit:
            self.end_time = timezone.now() + timedelta(minutes=self.time_limit)
        super().save(*args, **kwargs)

class QuizGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=255)
    grade = models.FloatField()
    pass_status = models.CharField(max_length=10, choices=[('Passed', 'Passed'), ('Failed', 'Failed')])

    def __str__(self):
        return f"{self.student.username}'s Grade for Quiz with Secret Key: {self.secret_key}"


    
