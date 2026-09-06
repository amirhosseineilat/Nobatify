from core.settings import *

# ==========================================
# Test Database
# ==========================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}