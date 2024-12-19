from .settings import *

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.getenv(
        "GCLOUD_CREDENTIALS_PATH",
        "/tmp/gcloud-secret.json",
    )
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
