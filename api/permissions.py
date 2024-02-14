from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Quiz


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'teacher')
    




class IsQuizOwner(BasePermission):
    def has_permission(self, request, view):
        secret_key = view.kwargs.get('secret_key')
        quiz = get_object_or_404(Quiz, secret_key=secret_key)
        return request.user == quiz.teacher.custom_user
