# 🕵️‍♂️ BlackBox Logger

![PyPI](https://img.shields.io/pypi/v/blackbox-logger)
![License](https://img.shields.io/github/license/avi9r/blackbox_logger)


A universal request/response logger for **Django**, **Flask**, **FastAPI**, and other Python apps.  
Automatically logs requests and responses, user info, IP address, and more — with **masked sensitive data** — into a log file and SQLite database.

---

## 🚀 Features

- ✅ Logs all HTTP requests and responses  
- ✅ Logs to both `blackbox.log` file and SQLite DB (`blackbox_logs.db`)  
- ✅ Automatically masks sensitive fields (e.g., `password`, `token`, etc.)  
- ✅ Logs user (if available), IP address, and user agent  
- ✅ Skips HTML content in logs to avoid noise  
- ✅ Works out-of-the-box in **Django**  
- ⚙️ Easy integration in **Flask** and **FastAPI**

---

## 📦 Installation

```bash
pip install blackbox-logger
Or install directly from GitHub:
```
```bash
pip install git+https://github.com/avi9r/blackbox_logger.git
```

## 📁 Logs
- After running, you’ll find:

📄 log/blackbox.log — clean file logs

🗃 log/blackbox_logs.db — SQLite DB (table: logs)

# ⚙️ Usage
## 🟩 Django
 - Add middleware:
# your_project/middleware.py
```bash
    from django.utils.deprecation import MiddlewareMixin
    from blackbox_logger.logger import HTTPLogger

    logger = HTTPLogger()

    class BlackBoxLoggerMiddleware(MiddlewareMixin):
        def process_request(self, request):
            logger.log_request(
                request.method,
                request.path,
                dict(request.headers),
                request.body,
                request
            )

        def process_response(self, request, response):
            logger.log_response(
                request.method,
                request.path,
                dict(request.headers),
                response.content,
                response.status_code,
                request
            )
            return response
```
## Enable middleware in settings.py:

```bash
MIDDLEWARE = [
    'your_project.middleware.BlackBoxLoggerMiddleware',
    ...
]
```
## 🟦 Flask
(Optional) Install Flask-Login for user tracking:

```bash
pip install flask-login
```
## Initialize the logger in app.py:
```bash
from flask import Flask, request
from flask_login import current_user
from blackbox_logger.logger import HTTPLogger

logger = HTTPLogger(
    get_user=lambda headers, request=None: current_user.username if current_user.is_authenticated else "Anonymous"
)

app = Flask(__name__)

@app.before_request
def log_req():
    logger.log_request(
        request.method,
        request.path,
        dict(request.headers),
        request.get_data(),
        request
    )

@app.after_request
def log_resp(response):
    logger.log_response(
        request.method,
        request.path,
        dict(request.headers),
        response.get_data(),
        response.status_code,
        request
    )
    return response
```
## 🟨 FastAPI
- Add middleware in main.py:
```bash
from fastapi import FastAPI, Request, Response
from blackbox_logger.logger import HTTPLogger

logger = HTTPLogger()

app = FastAPI()

@app.middleware("http")
async def blackbox_logger_middleware(request: Request, call_next):
    # Optional: Attach user to request.state (e.g., after auth)
    request.state.user = "Anonymous"

    body = await request.body()
    logger.log_request(request.method, str(request.url), dict(request.headers), body, request)

    response = await call_next(request)
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    response.body_iterator = iter([response_body])

    logger.log_response(request.method, str(request.url), dict(request.headers), response_body, response.status_code, request)
    return response
```
# 🔐 Masking Sensitive Data
- By default, the following fields are masked:
```bash
["password", "token", "access_token", "secret", "authorization", "csrfmiddlewaretoken"]
```
- You can update this in masking.py if needed.
## 📜 License
- MIT License

<!-- rm -rf build dist *.egg-info-->
<!-- python -m build -->
<!-- twine upload dist/* -->