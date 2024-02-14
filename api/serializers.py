from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import CustomUser, Teacher, Student, Quiz, QuizQuestion, QuizGrade
from collections import OrderedDict
from django.utils import timezone
from datetime import timedelta


class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=[('teacher', 'teacher'), ('student', 'student')])

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['role'] = self.validated_data.get('role', '')
        return data_dict

    def save(self, request):
        user = super().save(request)
        role = self.validated_data.get('role', '')
        
        if role == 'teacher':
            teacher = Teacher.objects.create(custom_user=user)
            teacher.save()
        if role == 'student':
            student = Student.objects.create(custom_user=user)
            student.save()
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('role',)



class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['text', 'options', 'correct_answer_index']

    def create(self, validated_data):
        return super().create(validated_data)

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)
    end_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Quiz
        fields = ['teacher', 'secret_key', 'questions', 'time_limit', 'end_time']
        read_only_fields = ['end_time']

    def create(self, validated_data):
        time_limit = validated_data.pop('time_limit')
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(time_limit=time_limit, **validated_data)

        quiz.end_time = timezone.now() + timedelta(minutes=time_limit)
        quiz.save()

        for question_data in questions_data:
            question = QuizQuestion.objects.create(quiz=quiz, **question_data)
            quiz.questions.add(question)
        return quiz
    

class QuizGradeSerializer(serializers.ModelSerializer):
    student_username = serializers.SerializerMethodField()
    class Meta:
        model = QuizGrade
        fields = ['id','student', 'student_username', 'secret_key', 'grade', 'pass_status']


    def get_student_username(self, obj):
        return obj.student.custom_user.username    