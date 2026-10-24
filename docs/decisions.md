# Decision log

Newest decisions go at the bottom. If a decision changes, don't delete the old entry: mark it **Superseded** and add a new entry explaining what changed and why.

Entries marked `TODO (yours)` need the reason written in your own words. If you can't write it, that's a gap to review.

---

## 1. Scope: one college, no outsiders

- **Date:** 2026-10-24
- **Context:** External events (other colleges) usually have their own sites.
- **Options:** College-only accounts vs. open sign-up for anyone.
- **Decision:** College-only. Accounts need a verified college email and register ID.
- **Reason:** External participation isn't the problem being solved, and it adds identity and abuse issues.
- **Tradeoff:** Guests from other colleges can't use the platform. Revisit if that becomes a need.

## 2. PostgreSQL instead of SQLite

- **Date:** 2026-10-24
- **Options:** SQLite / PostgreSQL / MongoDB.
- **Decision:** PostgreSQL, run in Docker locally.
- **Reason:** The data is relational (users, clubs, events, registrations), and the project needs constraints, transactions, and row locking (team and capacity checks). Same engine locally and in production.
- **Tradeoff:** More setup than SQLite (a container, port mapping, credentials in `.env`).

## 3. Custom User model, email as login

- **Date:** 2026-10-24
- **Options:** Default Django User / extend `AbstractUser` / `AbstractBaseUser`.
- **Decision:** `AbstractUser` with `username` removed, `email` as `USERNAME_FIELD`, plus `name` and `register_id` (unique), with a custom `UserManager`.
- **Reason:** Students log in with college email. A custom user model must exist before the first migration because swapping it later is very painful.
- **Tradeoff:** `first_name` and `last_name` remain unused. Technical debt. `AbstractBaseUser` would be cleaner but needs more boilerplate.

## 4. Roles: student, club admin, platform admin

- **Date:** 2026-10-24
- **Options:** Add a faculty role / keep three roles.
- **Decision:** Three roles. No faculty role in the MVP.
- **Reason:** TODO (yours): why is faculty not needed?
- **Tradeoff:** No faculty approval or oversight of events.

## 5. Club membership is a join table

- **Date:** 2026-10-24
- **Options:** Store members and roles on `Club` / a many-to-many with extra data (`ClubMembership`).
- **Decision:** `ClubMembership` (user, club, role, optional title), unique on (user, club).
- **Reason:** A user can be admin of one club and a plain member or non-member of another, so the role belongs to the user-club pair, not to either side.
- **Tradeoff:** One more table and join.
  title is free text because it’s display only, role is a fixed list because code depends on it, and display_order is deliberately not unique so reordering stays simple.

## 6. Excom is membership rows with a title

- **Date:** 2026-10-24
- **Options:** Separate display-only excom table / reuse `ClubMembership` with a `title`.
- **Decision:** Reuse `ClubMembership`. Permission role (admin/member) is separate from display title (Chairman, Secretary).
- **Reason:** Clubs name their leads differently, so "admin" is the generic permission and the title is only a label.
- **Tradeoff:** Excom members must have accounts.

## 7. Derived data is not stored

- **Date:** 2026-10-24
- **Decision:** A club's "recent events" and stats (event counts, participant counts) are computed by queries, not stored as fields on `Club`.
- **Reason:** Stored copies can disagree with the real data.
- **Tradeoff:** Queries cost time as data grows. Revisit with indexes or caching if needed.

## 8. Solo vs team is chosen per event

- **Date:** 2026-10-24
- **Decision:** The event admin picks solo or team when creating the event. For team events, one user creates a team (becoming leader) and shares a join code; friends type the code to join.
- **Reason:** Matches how real events work (hackathons vs. quizzes).
- **Tradeoff:** Needs unique, unguessable codes and team-size rules (see open questions).

## 9. Custom registration forms stored relationally

- **Date:** 2026-10-24
- **Options:** JSON form definition and JSON answers / `FormField` and `FormAnswer` tables.
- **Decision:** Relational tables.
- **Reason:** TODO (yours): why relational over JSON?
- **Tradeoff:** More tables and joins. An answer can point to a field from a different event than its registration, so this needs validation.

## 10. Registration and attendance are separate facts

- **Date:** 2026-10-24
- **Decision:** Registration has its own status. Attendance is a separate fact, stored as a `checked_in_at` timestamp on `Registration` for the MVP.
- **Reason:** Someone can be registered and never show up, so "attended" isn't a state a registration moves into.
- **Tradeoff:** A single timestamp can't represent multi-session events. Revisit with a separate table if needed.

## 11. Out of MVP

- **Date:** 2026-10-24
- **Decision:** Payments, per-event custom URLs and themes, certificates, and announcements are postponed.
- **Reason:** The MVP should solve the organizer pain first: manual forms, participant lists, and RSVP groups.

## 12. Configuration in `.env`

- **Date:** 2026-10-24
- **Decision:** Secrets and per-machine settings live in `.env` (read with python-decouple) and are never committed.
- **Reason:** The same code runs locally and in production, and only the configuration differs.

---

## Learnings

- Docker and a local Postgres install both used port 5432, so Django connected to the wrong server. Fix: map the container to 5433.
- `.gitignore` only applies to untracked files. Files already committed (like `__pycache__` and `db.sqlite3`) must be removed from tracking with `git rm -r --cached`.
- Check where the repo root actually is before creating config files.
- `django-admin startproject name .` (with the dot) avoids the extra nested folder.
