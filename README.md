# Clubbed

A single platform for college clubs to publish events and for students to discover, register for, and attend them. Built for one college (Christ College of Engineering) to replace scattered WhatsApp posts and per-event forms.

This is a learning project: the goal is to design and understand a real backend, not to ship fast. The reasoning behind each major choice is in [`docs/decisions.md`](docs/decisions.md).

## Stack

- Python, Django, Django REST Framework (API layer comes later)
- PostgreSQL (run locally in Docker)
- python-decouple for configuration

## Run locally

Prerequisites: Python 3 and Docker Desktop (it must be running).

1. Create and activate a virtual environment (PowerShell):
   ```
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file (never commit it). Use these keys, with your own values:
   ```
   SECRET_KEY=generate-your-own
   DEBUG=True
   DB_NAME=clubbed
   DB_USER=clubbed
   DB_PASSWORD=changeme
   DB_HOST=localhost
   DB_PORT=5433
   ```
   Generate a secret key with:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
4. Start the database:
   ```
   docker compose up -d
   ```
   The container maps host port 5433 to Postgres's 5432, to avoid clashing with a local Postgres install.
5. From the folder containing `manage.py`:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
   Admin is at `http://127.0.0.1:8000/admin/`.

## Project layout

| App | Purpose |
|---|---|
| `accounts` | Custom `User` model (email login, name, register ID) |
| `clubs` | Clubs and club memberships |
| `events` | Events and custom registration form fields (not built yet) |
| `registrations` | Registrations, teams, form answers, check-in (not built yet) |

## Docs

- [Decision log](docs/decisions.md): what was chosen and why
- [Open questions](docs/open-questions.md): unresolved design points
- ER diagram: `docs/diagrams/ER1.png` (first draft, known corrections listed in open questions)