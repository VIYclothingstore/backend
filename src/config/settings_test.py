# src/config/settings_test.py

import os

from google.oauth2 import service_account

from .settings import *  # Импортируем все настройки из основного файла

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.getenv("GCLOUD_CREDENTIALS_PATH", "/Users/jabko/Desktop/projects/backend/gcloud-secret.json")
)
if hasattr(settings, "GS_CREDENTIALS"):
    # GS_CREDENTIALS exists
    print("GS_CREDENTIALS found in settings")
else:
    # GS_CREDENTIALS not found
    print("GS_CREDENTIALS not found in settings")
# Настройки базы данных для тестов
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # Используем SQLite для тестов
    }
}

# Если настройки для базы данных уже есть в settings.py, то их можно не переписывать. Они будут переопределены
