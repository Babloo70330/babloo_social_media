# ConnectSphere - Mini Social Media App (Facebook-style)

Django-based social media web app with profiles, friends, posts feed, likes and comments.

## Setup

1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser (for /admin/):
   ```
   python manage.py createsuperuser
   ```

5. Run the server:
   ```
   python manage.py runserver
   ```

6. Visit http://127.0.0.1:8000/accounts/signup/ to create an account.

## App structure

- `accounts/` — user Profile model, signup/login/logout, profile view + edit
- `friends/`  — FriendRequest & Friendship models, send/accept/reject, friends list, suggestions
- `posts/`    — Post/Like/Comment models, news feed, like toggle, add comment, delete post
- `chat/`     — Message model, inbox, 1-to-1 conversation (friends only), AJAX-polled near-real-time updates

## Features included (v1 - MVP)

- Signup / Login / Logout (Django auth)
- Profile page with bio, location, profile pic, cover pic + edit form
- Friend requests: send, accept, reject; friend list; "people you may know" suggestions
- News feed showing your posts + friends' posts (text + optional image)
- Like / Unlike posts
- Comment on posts
- Delete your own posts
- Chat: inbox of conversations, 1-to-1 messaging with friends, auto-refreshes every 3s (no page reload needed)

## Not included yet (possible v2)

- Real-time push notifications (chat uses simple polling, not WebSockets)
- Stories
- Photo albums
- Post editing (only delete currently)
- Group chats (only 1-to-1 currently)

## Notes

- Uses SQLite by default (`db.sqlite3`) — fine for dev/college project. Switch to MySQL/Postgres for production.
- Media files (profile pics, post images) are stored in `media/` — served via Django dev server only when `DEBUG=True`.
- Admin panel: `/admin/` (create a superuser to log in).
- Templates use Bootstrap 5 (CDN) + custom CSS in `static/css/style.css` (class prefix: `sw-`).
