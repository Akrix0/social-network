# Social Network

A Django-based social networking platform with real-time messaging, community boards, posts, and notifications.

## Description

This is a full-featured social network implemented as a Django application. It supports user accounts, content sharing via posts, community boards, private and group messaging with WebSockets, and real-time notifications.

The project uses Django class-based views, templates with Bootstrap, and ASGI for WebSocket support.

## Features

### Posts
- Create posts with title, text, optional file attachments, and user tags.
- Like posts and comments.
- View counters.
- Edit and delete own content.
- Infinite scroll for browsing.

### Boards (Communities)
- Create and join community boards with name, description, slug, and tags.
- Board owners and admins manage content; members can view and follow discussions.
- Infinite scroll for messages within boards.
- Independent tags support.

### Messenger
- Real-time private and group chats via WebSockets.
- Message reactions (single emoji per user).
- Customizable chat settings including name and background for groups.

### Notifications
- Real-time notifications for interactions (likes, comments, mentions, etc.).
- Track read status.

### Accounts and Profiles
- Two-step registration.
- User profiles with avatar, bio, phone, date of birth, and username-based slug.
- Follow and friend relationships.
- Basic activity statistics.

### Main Page
- Feed with tabs for all posts or friends-only.
- Search functionality.
- Sections for popular boards, trending tags, suggested users.

## Tech Stack

**Backend**
- Python
- Django (class-based views)
- Django Channels / WebSockets for real-time features
- Django signals
- ASGI (uvicorn)

**Frontend**
- HTML, CSS, JavaScript
- Bootstrap 5

**Database**
- SQLite (development)
- PostgreSQL (production)

**Media**
- Cloudinary (deployment)

## Project Structure

```
social-network/
├── accounts/          # User management
├── boards/            # Community boards
├── messenger/         # Real-time chat
├── notifications/     # Notifications
├── posts/             # Post functionality
├── main/              # Main app views and templates
├── social_network/    # Project settings
├── templates/         # HTML templates
├── static/            # Static assets
├── media/default/     # Default media files
├── docs/screenshots/  # Example screenshots
├── manage.py
├── requirements.txt
└── .env.example
```

##  Screenshots

| Main page | Messenger |
|-----------|-----------|
| ![Main page](docs/screenshots/main-page.png) | ![Messenger](docs/screenshots/messenger.png) |

| Notifications | Board detail |
|---------------|--------------|
| ![Notifications](docs/screenshots/notifications.png) | ![Board detail](docs/screenshots/board-detail.png) |

| Post detail | User profile |
|-------------|--------------|
| ![Post detail](docs/screenshots/post-detail.png) | ![User profile](docs/screenshots/user-profile.png) |

| Boards list | Registration |
|-------------|----------------|
| ![Boards list](docs/screenshots/boards-list.png) | ![Registration](docs/screenshots/register-step1.png) |

> Screenshots are stored in [`docs/screenshots/`](docs/screenshots/).  
> Live demo: [social-network-kddy.onrender.com](https://social-network-kddy.onrender.com/)—out of work


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Akrix0/social-network.git
   cd social-network
   ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit `.env` to set `DJANGO_SECRET_KEY` and other required settings (e.g., Cloudinary if using media).

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. (Optional) Create superuser:
   ```
   python manage.py createsuperuser
   ```

7. Collect static files:
   ```
   python manage.py collectstatic --noinput
   ```

8. Run the server:
   ```
   # Recommended: HTTP + WebSockets
   uvicorn social_network.asgi:application --reload

   # Alternative: Django dev server (HTTP only)
   python manage.py runserver
   ```

## Usage

After starting the server, access the application at `http://127.0.0.1:8000/`.

Register an account and explore the feed, create posts, join boards, or start chats.

## Development

- Run tests: `python manage.py test`
- The project uses Django's standard structure with separate apps for major features.
- Real-time functionality relies on Django Channels/WebSockets.

## Future Improvements

- TODO: Improve performance and optimize queries.
- TODO: Add file attachments to board messages.
- TODO: Extend real-time features where needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed by [Akrix0](https://github.com/Akrix0).
