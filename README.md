Ticket System API

REST API for managing support tickets, built with FastAPI, SQLAlchemy and PostgreSQL. It includes JWT authentication, role-based authorization (user and admin), comments on tickets, soft delete, database migrations with Alembic, a Docker setup and automated tests with Pytest.

This is the updated version of my first project, Backend-Ticket-System.

Features
User registration and login, with passwords hashed using bcrypt.
JWT authentication (Bearer token).
Role-based authorization:
user: creates tickets, views and edits their own tickets, and comments on them.
admin: has access to every ticket and comment, and can delete them.
Ticket CRUD with statuses: pending, in_process and completed.
Comments attached to each ticket.
Soft delete: deleted tickets and comments are kept in the database and flagged as deleted.
Input validation with Pydantic.
Consistent HTTP error responses (401, 403, 404, 409, 422).
Database migrations with Alembic.
One-command setup with Docker Compose.
Automatic interactive documentation with Swagger UI (/docs).
Automated tests with Pytest.
Tech stack
Area	Tools
Language	Python
Framework	FastAPI
Database	PostgreSQL
ORM and migrations	SQLAlchemy, Alembic
Authentication	JWT (python-jose), bcrypt
Validation	Pydantic
Containers	Docker, Docker Compose
Testing	Pytest, HTTPX (TestClient)
Project structure
.
├── alembic/             # Migration environment and versions
├── app/
│   ├── auth/            # JWT, password hashing and auth dependencies
│   ├── config/          # Settings and environment variables
│   ├── database/        # Database engine and session
│   ├── exceptions/      # Custom exceptions
│   ├── models/          # SQLAlchemy models (users, tickets, comments)
│   ├── routers/         # Endpoints (auth, tickets, comments)
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Reusable business logic
│   └── main.py          # Application entry point
├── tests/               # Pytest tests
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
Getting started

Clone the repository first:

bash
git clone https://github.com/JoaKomar/Updated-Backend-Ticket-System.git
cd Updated-Backend-Ticket-System
Option 1: Docker (recommended)

Requirements: Docker and Docker Compose.

Create your .env file from the example and set your own values:
bash
cp .env.example .env

To generate a secure secret key:

bash
python -c "import secrets; print(secrets.token_hex(32))"
Build and start the containers:
bash
docker compose up --build

This starts PostgreSQL and the API. Migrations are applied automatically when the API container starts.

Open the interactive docs at http://localhost:8000/docs.

To stop everything, run docker compose down (add -v to also delete the database volume).

Option 2: Local setup

Requirements: Python 3.10 or higher and PostgreSQL.

Create and activate a virtual environment:
bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
Install the dependencies:
bash
pip install -r requirements.txt
Create a PostgreSQL database (for example, ticket_system).
Create your .env file and set DATABASE_URL to your local database:
bash
cp .env.example .env
Apply the database migrations:
bash
alembic upgrade head
Start the server:
bash
uvicorn app.main:app --reload
Open the interactive docs at http://127.0.0.1:8000/docs.
Environment variables
Variable	Description
DATABASE_URL	PostgreSQL connection string used by the API
ALGORITHM	JWT signing algorithm (for example, HS256)
SECRET_KEY_TOKEN	Secret key used to sign tokens. Keep it private
POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB	Credentials for the PostgreSQL container (Docker only)

Never commit your real .env file.

Database migrations

Migrations are managed with Alembic:

bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after changing the models
alembic revision --autogenerate -m "describe your change"

# Revert the last migration
alembic downgrade -1
Trying the API with Swagger
Register a user with POST /auth/register.
Log in with POST /auth/login and copy the access_token value.
Click Authorize, paste the token (without typing "Bearer") and confirm.
You can now call the protected endpoints.

To try the admin routes, change a user's role directly in the database:

sql
UPDATE users SET role = 'admin' WHERE email = 'you@example.com';
Endpoints
Authentication
Method	Route	Description	Access
POST	/auth/register	Register a user	Public
POST	/auth/login	Log in and get an access token	Public
Tickets
Method	Route	Description	Access
GET	/tickets/me	Get the authenticated user's profile	User
POST	/tickets/create	Create a ticket	User
GET	/tickets/{ticket_id}	Get a ticket	Owner or admin
PUT	/tickets/{ticket_id}	Update a ticket	Owner or admin
DELETE	/tickets/{ticket_id}	Delete a ticket (soft delete)	Admin
Comments
Method	Route	Description	Access
POST	/comments/create/{ticket_id}	Comment on a ticket	Ticket owner or admin
GET	/comments/{comment_id}	Get a comment	Ticket owner or admin
PUT	/comments/{comment_id}	Edit a comment	Author or admin
DELETE	/comments/{comment_id}	Delete a comment (soft delete)	Admin
Running the tests

With the local setup active and the migrations applied:

bash
pip install pytest httpx
pytest

The tests run against the database defined in DATABASE_URL, so point it to a dedicated test database.

Roadmap
[ ] Ticket listing with pagination and filters
[ ] More permission and comment tests
[ ] Continuous integration with GitHub Actions
[ ] Deployment
Author

Joaquín — @JoaKomar