from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import Teacher, QuizQuestion, Quiz, Student, QuizGrade

User = get_user_model()

class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup(self):
        signup_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'student' 
        }
        url = reverse('rest_register')
        response = self.client.post(url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_count = User.objects.filter(username='testuser').count()
        self.assertEqual(user_count, 1)
        created_user = User.objects.get(username='testuser')
        self.assertEqual(created_user.email, 'test@example.com')



class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_user_login(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        url = reverse('rest_login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'test@example.com')



class QuizCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = Teacher.objects.create(custom_user=User.objects.create(username='teacher', role='teacher'))
        self.client.force_login(self.teacher.custom_user)

    def test_quiz_creation(self):
        quiz_data = {
            'teacher': self.teacher.id,
            'secret_key': '123456',
            'questions': []  
        }
        url = reverse('quiz-create')
        response = self.client.post(url, quiz_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class QuizDetailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = Teacher.objects.create(custom_user=User.objects.create(username='teacher', role='teacher'))
        self.quiz = Quiz.objects.create(teacher=self.teacher, secret_key='123456')
        

    def test_quiz_detail(self):
        self.client.force_login(self.teacher.custom_user)
        url = reverse('quiz-detail')
        response = self.client.post(url, {'secret_key': '123456'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher'], self.teacher.id)
        self.assertEqual(response.data['secret_key'], '123456')



class QuizSolutionTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()
        self.teacher = Teacher.objects.create(custom_user=User.objects.create(username='teacher', role='teacher'))
        self.student = Student.objects.create(custom_user=User.objects.create(username='student', role='student'))
        self.quiz = Quiz.objects.create(teacher=self.teacher, secret_key='123456')

        self.question1 = QuizQuestion.objects.create(
            text='What is the capital of France?',
            options=['Paris', 'London', 'Berlin', 'Rome'],
            correct_answer_index=0
        )
        self.question2 = QuizQuestion.objects.create(
            text='Who wrote "Romeo and Juliet"?',
            options=['William Shakespeare', 'Charles Dickens', 'Jane Austen', 'Leo Tolstoy'],
            correct_answer_index=0
        )
        self.quiz.questions.add(self.question1, self.question2)

    def test_quiz_solution(self):
        student_answers = [0, 0]
        self.client.force_login(self.student.custom_user)
        url = reverse('quiz-solution')
        data = {'secret_key': '123456', 'answers': student_answers}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('grade' in response.data)



class QuizGradesBySecretKeyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = Teacher.objects.create(custom_user=User.objects.create(username='teacher', role='teacher'))
        self.student1 = Student.objects.create(custom_user=User.objects.create(username='student1', role='student'))
        self.student2 = Student.objects.create(custom_user=User.objects.create(username='student2', role='student'))
        self.quiz = Quiz.objects.create(teacher=self.teacher, secret_key='123456')
        self.grade1 = QuizGrade.objects.create(student=self.student1, secret_key='123456', grade=90)
        self.grade2 = QuizGrade.objects.create(student=self.student2, secret_key='123456', grade=85)

    def test_quiz_grades_by_secret_key(self):
        self.client.force_login(self.teacher.custom_user)
        secret_key = '123456'
        url = reverse('quiz_grades_by_secret_key', kwargs={'secret_key': secret_key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)