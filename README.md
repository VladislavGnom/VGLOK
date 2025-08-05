# README for VGLOK Social Network

# VGLOK Social Network

VGLOK is a modern social networking platform currently in development. It offers core social media functionalities with a clean, responsive interface and real-time features.

![Project Status](https://img.shields.io/badge/status-active%20development-yellowgreen) ![Django Version](https://img.shields.io/badge/django-4.0+-green) ![Python Version](https://img.shields.io/badge/python-3.9+-blue)

## Key Features

### 🚀 Core Functionality
- **User Profiles** with personal post feeds
- **CRUD Operations** for posts (Create, Read, Update, Delete)
- **Like System** with HTMX for seamless interaction
- **Commenting System** on posts

### 🔍 Discovery
- **User Search** functionality to find and connect with others
- **Chat System** (coming soon for recommendations feed)

### 💬 Real-Time Communication
- **Instant Messaging** between users
- **WebSocket-based Chat** using Django Channels
- **Chat History Loading** for continuous conversation
- **Online Status Indicators** (planned)

## Technology Stack

### Backend
- **Python 3.9+**
- **Django** (Web Framework)
- **Django Channels** (WebSockets support)
- **Daphne** (ASGI server)
- **Redis** (WebSocket server & caching)

### Frontend
- **HTMX** for dynamic content without full page reloads
- **JavaScript** for enhanced interactivity
- **HTML5 & CSS3** for structure and styling

### Database
- **SQLite** (Development - will migrate to PostgreSQL in production)

## Project Structure

```
VGLOK/
├── mainapp/               # Main application directory
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   ├── consumers.py       # WebSocket consumers
│   └── ...                # Other Django app files
├── vglok/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── asgi.py            # ASGI configuration
│   └── ...                # Other project files
├── manage.py              # Django management script
└── ...                    # Other project files
```

## Getting Started

### Prerequisites
- Python 3.9+
- Redis server
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/VladislavGnom/VGLOK.git
   cd VGLOK
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables in `.env` file:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. In a separate terminal, start the Redis server and Daphne:
   ```bash
   redis-server
   daphne -p 8001 vglok.asgi:application
   ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [x] Basic user profiles and posts
- [x] Like and comment system
- [x] User search functionality
- [x] Real-time chat
- [ ] Recommendations feed
- [ ] Notifications system
- [ ] Media uploads (images/videos)
- [ ] Mobile application

## License

This project is currently unlicensed. All rights reserved.

## Contact

Project Maintainer: [VladislavGnom](https://github.com/VladislavGnom)

For questions or support, please open an issue on GitHub.
```

This README provides:
1. Clear project overview
2. Feature highlights
3. Technology stack details
4. Installation instructions
5. Contribution guidelines
6. Project roadmap
7. Contact information

The formatting uses GitHub-flavored Markdown with badges for visual appeal. You can customize the license section once you decide on one, and add more screenshots as the project develops.
