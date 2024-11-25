import os

from google.oauth2 import service_account

from .settings import *

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.getenv(
        "GCLOUD_CREDENTIALS_PATH",
        "/tmp/gcloud-secret.json",
    )
)
if hasattr(settings, "GS_CREDENTIALS"):
    # GS_CREDENTIALS exists
    print("GS_CREDENTIALS found in settings")
else:
    # GS_CREDENTIALS not found
    print("GS_CREDENTIALS not found in settings")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
