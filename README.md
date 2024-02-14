# QUIZ MANAGMENT REST API

## Project Overview

The Quiz Management System is built using Python and the Django framework. It allows teachers to create quizzes with questions and time limits, and students can solve these quizzes and receive grades. The application provides security features such as user authentication and permissions to ensure that only authorized users can access certain functionalities.

## How to Run the Project

Follow these steps to run the project on your local machine:
1. Install [Python 3.11](https://www.python.org/downloads/release/python-3110/) and [Git](https://git-scm.com/download/win).
2. Clone the repo in a new folder
   ```
   git clone https://github.com/Msafi11/QuizApp-REST-API.git
   ```
3. Create a virtual environment on your machine and activate it.
   ```
   python3 -m venv myenv
   source myenv/bin/activate  # On macOS/Linux
   myenv\Scripts\activate       # On Windows
   ```
   *note*: If you find an error while activating myenv :
      - Open powershell as adminstrator.
      - Write this command then 'y'.
        ```
        Set-ExecutionPolicy RemoteSigned
        ```
4. Navigate to the project directory in your terminal. `cd QuizApp-REST-API`
5. Install project dependencies by running `pip install -r requirements.txt`.
6. Apply database migrations by running `python manage.py makemigrations` followed by `python manage.py migrate`.
7. Create a superuser account by running `python manage.py createsuperuser` and follow the prompts to create a user with administrative privileges.
8. Start the development server by running `python manage.py runserver`.

## Endpoints

- **POST /api/signup/**: Allows users to sign up.
- **POST /api/auth/login/**: Allows users to log in.
- **POST /api/auth/logout/**: Allows users to log out.
- **POST /api/quizzes/create/**: Allows creation of a new quiz.
- **GET /api/quizzes/detail/**: Retrieves the quiz detail secret-key and questions.
- **POST /api/quizzes/solution/**: Allows students to solve the quiz and submit it.
- **GET /api/quiz-grades/{secret_key}/**: Allows teachers to view the quiz grade with the provided {secret__key}.
- **GET /api/users/**: Lists all users.

## Usage

- Sign up for an account using the `/api/signup/` endpoint.
- Log in using the `/api/auth/login/` endpoint.
- Use the appropriate endpoints based on your role:
  - Teachers: Create quizzes and access grades list using `/api/quizzes/create/` , `/api/quiz-grades/{secret_key}/` endpoints respectively.
  - Students: View quiz detail, solve the quiz using `/api/quizzes/detail/`, `/api/quizzes/solution/` endpoints respectively.
- Log out using the `/api/auth/logout/` endpoint when done.


**Note:** Ensure that you have appropriate permissions to access certain endpoints based on your role (teacher/student).
