# Ticket System API

REST API for managing support tickets, built with **Python, FastAPI, SQLAlchemy and PostgreSQL**.

The application allows users to register, log in, create and manage tickets, add comments, and control access through JWT authentication and role-based authorization.

This is an updated version of my first project, **Backend-Ticket-System**.

## Features

- User registration and login.
- JWT authentication (Bearer Token).
- Password hashing with bcrypt.
- Role-based authorization: `user` and `admin`.
- Ticket creation, retrieval, updating and soft deletion.
- Comments associated with tickets.
- Soft deletion for tickets and comments.
- Input validation with Pydantic.
- Ticket filtering by title.
- Pagination using `offset` and `limit`.
- HTTP error handling.
- Interactive API documentation with Swagger UI.
- PostgreSQL configuration using Docker Compose.
- Automated tests with Pytest.

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT (python-jose) |
| Password hashing | bcrypt |
| Validation | Pydantic |
| Containers | Docker and Docker Compose |
| Testing | Pytest and HTTPX |

## Project Structure

```text
.
├── app/
│   ├── auth/          # Authentication and JWT
│   ├── config/        # Environment variables
│   ├── database/     # Database connection and sessions
│   ├── exceptions/   # Custom exceptions
│   ├── models/       # SQLAlchemy models
│   ├── routers/      # API endpoints
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Reusable business logic
│   └── main.py       # Application entry point
├── tests/             # Automated tests
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
└── requirements.txt
```

## Getting Started

### Option 1: Docker Compose (recommended)

Requirements:
- Docker
- Docker Compose

Clone the repository:

```bash
git clone https://github.com/JoaKomar/Updated-Backend-Ticket-System.git
cd Updated-Backend-Ticket-System
```

Create the environment file:

```bash
cp .env.example .env
```

Before starting the application, configure the environment variables and replace the example values with your own.

Build and start the containers:

```bash
docker compose up --build
```

This starts PostgreSQL and the API.

Interactive API documentation:

http://localhost:8000/docs

Stop the containers:

```bash
docker compose down
```

To also remove the persistent PostgreSQL data volume:

```bash
docker compose down -v
```

**Warning:** the last command deletes the database volume and its stored data.

### Option 2: Local Setup

Requirements:
- Python 3.12
- PostgreSQL

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a PostgreSQL database and configure the `.env` file:

```bash
cp .env.example .env
```

Set `DATABASE_URL` to your local PostgreSQL connection string.

Start the application:

```bash
uvicorn app.main:app --reload
```

Interactive API documentation:

http://127.0.0.1:8000/docs

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `ALGORITHM` | Algorithm used to sign JWTs |
| `SECRET_KEY_TOKEN` | Secret key used to sign tokens |
| `POSTGRES_USER` | PostgreSQL username for Docker |
| `POSTGRES_PASSWORD` | PostgreSQL password for Docker |
| `POSTGRES_DB` | PostgreSQL database name for Docker |

Never commit your real `.env` file. Use `.env.example` as a template.

## API Endpoints

### Authentication

| Method | Route | Description | Access |
|---|---|---|---|
| POST | `/auth/register` | Register a user | Public |
| POST | `/auth/login` | Log in | Public |

### Tickets

| Method | Route | Description | Access |
|---|---|---|---|
| GET | `/tickets/me` | Get own profile | Authenticated user |
| POST | `/tickets/create` | Create a ticket | Authenticated user |
| GET | `/tickets/` | List tickets | Authenticated user |
| GET | `/tickets/{ticket_id}` | Retrieve a ticket | Owner or admin |
| PUT | `/tickets/{ticket_id}` | Update a ticket | Owner or admin |
| DELETE | `/tickets/{ticket_id}` | Soft-delete a ticket | Admin |

The ticket listing supports the `title`, `offset` and `limit` query parameters.

### Comments

| Method | Route | Description | Access |
|---|---|---|---|
| POST | `/comments/create/{ticket_id}` | Create a comment | Ticket owner or admin |
| GET | `/comments/{comment_id}` | Retrieve a comment | Ticket owner or admin |
| PUT | `/comments/{comment_id}` | Update a comment | Author or admin |
| DELETE | `/comments/{comment_id}` | Soft-delete a comment | Admin |

## Authentication

The API uses JWT to protect private endpoints.

To test the API through Swagger:

1. Register a user using `POST /auth/register`.
2. Log in using `POST /auth/login`.
3. Copy the `access_token` value.
4. Click the **Authorize** button in Swagger.
5. Enter the token and confirm.

Once authenticated, you can access protected endpoints according to your user role and permissions.

## Testing

Run the automated tests with Pytest:

```bash
python -m pytest -v
```

A dedicated test database should be configured through `DATABASE_URL` to prevent tests from modifying development data.

## Author

**Joaquín**  
GitHub: [@JoaKomar](https://github.com/JoaKomar)