# 🩺 Nobatify

**Nobatify** is a Django-based online doctor appointment booking platform designed to simplify the process of finding doctors, viewing available time slots, booking appointments, and managing patient accounts.

The project is built with a focus on **clean architecture, database design, authentication, testing, and production-oriented development**.

---

## 🚀 Features

### 👨‍⚕️ Doctor Management
- Doctor profiles
- Doctor specialities
- Doctor ratings and comments
- Average rating calculation
- Comment count
- Available appointment time slots

### 📅 Appointment System
- View available time slots
- Book an appointment
- Appointment status management
- Pending, confirmed, cancelled, and completed states
- Prevention of duplicate time-slot bookings

### 👤 User & Authentication
- Custom User model
- User registration and login
- Email-based authentication
- OTP validation
- User wallet
- Wallet recharge functionality

### ⭐ Reviews & Ratings
- Users can submit comments for doctors
- Rating system from 1 to 5
- Automatic average-rating calculation
- Validation for invalid ratings

### 🛠️ Admin Management
- Doctor management
- Speciality management
- Time-slot management
- Appointment management
- User management
- Administrative dashboard

### 🧪 Testing
The project includes automated tests for:

- Models
- Forms
- Views
- Validation
- Appointment logic
- Doctor-related functionality
- Authentication-related behavior

The testing structure is designed to make the application easier to maintain and refactor safely.

---

## 🏗️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Web framework |
| PostgreSQL | Database |
| Docker | Containerization |
| Docker Compose | Multi-container development |
| HTML / CSS | Frontend |
| JavaScript | Client-side functionality |
| Django ORM | Database interaction |
| Django Test Framework | Automated testing |
| Git & GitHub | Version control |

---

## 📂 Project Structure

```text
Nobatify/
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│
├── doctors/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│       ├── test_models.py
│       ├── test_forms.py
│       └── test_views.py
│
├── appointments/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── templates/
├── static/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/amirhosseineilat/Nobatify.git
cd Nobatify
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DEBUG=True

SECRET_KEY=your-secret-key

DB_NAME=nobatify
DB_USER=nobatify_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 🐳 Running with Docker

Nobatify can also be run using Docker and Docker Compose.

Build and start the containers:

```bash
docker compose up --build
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 🧪 Running Tests

Run the complete test suite:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test doctors
```

For example, to run the doctors forms tests:

```bash
python manage.py test doctors.tests.test_forms
```

Run a specific test class:

```bash
python manage.py test doctors.tests.test_forms.CommentFormTest
```

---

## 🔬 Testing Strategy

Nobatify uses Django's testing framework to verify application behavior.

Tests are separated according to responsibility:

```text
tests/
├── test_models.py
├── test_forms.py
└── test_views.py
```

### Model Tests

Model tests verify:

- Object creation
- Field validation
- Model relationships
- `__str__` behavior
- Calculated properties
- Aggregations
- Database constraints

### Form Tests

Form tests verify:

- Valid input
- Invalid input
- Required fields
- Boundary values
- Custom validation logic
- Form `clean()` behavior

### View Tests

View tests verify:

- HTTP status codes
- Template rendering
- Context data
- Authentication requirements
- URL behavior
- Database interactions

---

## 🧠 Architecture

Nobatify follows Django's **MVT architecture**:

```text
Request
   │
   ▼
 URL
   │
   ▼
 View
   │
   ├──── Form
   │
   ├──── Service / Business Logic
   │
   └──── Model ──── PostgreSQL
   │
   ▼
Template
   │
   ▼
Response
```

The project also uses Django ORM features such as:

- `select_related`
- `prefetch_related`
- `Prefetch`
- `annotate`
- `Avg`
- `Count`
- Database constraints

to improve database access and application performance.

---

## 🔐 Security

The project uses Django's built-in security mechanisms including:

- CSRF protection
- Authentication and authorization
- Password hashing
- Environment-based secret configuration
- Django form validation
- Database constraints

Sensitive configuration values are stored in environment variables rather than committed to the repository.

---

## 📌 Current Development Branch

The project is actively developed using feature and development branches.

Current testing work:

```text
dev/unit_test2_zizi
```

This branch focuses on improving the project's automated test coverage and reliability.

---

## 🎯 Project Goals

The main goals of Nobatify are:

- Build a realistic Django application
- Practice professional backend development
- Apply database design principles
- Implement authentication and authorization
- Write maintainable automated tests
- Work with PostgreSQL
- Containerize the application using Docker
- Improve code quality and architecture
- Build a production-oriented portfolio project

---

## 🔮 Future Improvements

Possible future improvements include:

- REST API using Django REST Framework
- Redis caching
- Celery background tasks
- Email and SMS notifications
- Online payment integration
- Advanced doctor search and filtering
- API documentation with Swagger / OpenAPI
- CI/CD pipeline
- Automated deployment
- Monitoring and logging
- Rate limiting
- More comprehensive test coverage

---

## 👩‍💻 Contributors

Developed as a collaborative Django project with contributions from the project team.

---

## 📄 License

This project is intended for educational and development purposes.