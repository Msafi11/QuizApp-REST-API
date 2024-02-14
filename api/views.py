from rest_framework import viewsets
from api.models import CustomUser, Teacher, Student , Quiz, QuizQuestion, QuizGrade
from api.serializers import CustomUserDetailsSerializer, CustomRegisterSerializer, QuizSerializer, QuizQuestionSerializer, QuizGradeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView
from .permissions import IsTeacher, IsQuizOwner
from django.utils import timezone



class CustomUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = CustomUserDetailsSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs.get('pk'))
        user.delete()

        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    




class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer 
    
    

class QuizCreateView(APIView):
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        teacher = request.user.teacher

        request_data = request.data.copy()
        request_data['teacher'] = teacher.id

        serializer = QuizSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        secret_key = request.data.get('secret_key')
        quiz = get_object_or_404(Quiz, secret_key=secret_key)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizSolutionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        secret_key = request.data.get('secret_key')
        quiz = get_object_or_404(Quiz, secret_key=secret_key)
        student_answers = request.data.get('answers', [])
        student = request.user.student

        if quiz.end_time and timezone.now() > quiz.end_time:
            QuizGrade.objects.create(student=student, secret_key=secret_key, grade=0, pass_status='Failed')
            return Response({'message': 'The quiz time has ended.', 'grade': 0, 'pass_status': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        existing_quiz_grade = QuizGrade.objects.filter(student=student, secret_key=secret_key).first()
        if existing_quiz_grade:
            return Response({'message': 'You have already solved this quiz.'}, status=status.HTTP_400_BAD_REQUEST)
        
        correct_answers = [question.correct_answer_index for question in quiz.questions.all()]
        num_correct = sum(1 for i, answer in enumerate(student_answers) if answer == correct_answers[i])
        total_questions = quiz.questions.count()
        grade = (num_correct / total_questions) * 100
        pass_status = 'Passed' if grade >= 50 else 'Failed'
         
        QuizGrade.objects.create(student=student, secret_key=secret_key, grade=grade, pass_status=pass_status)

        return Response({'grade': grade, 'pass_status': pass_status}, status=status.HTTP_200_OK)
    

class QuizGradesBySecretKeyView(APIView):
    permission_classes = (IsAuthenticated,IsTeacher ,IsQuizOwner)

    def get(self, request, secret_key):
        quiz_grades = QuizGrade.objects.filter(secret_key=secret_key) 
        
        serializer = QuizGradeSerializer(quiz_grades, many=True)
        
        return Response(serializer.data)



