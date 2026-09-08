# settings_test.py
from core.settings import *

# ==========================================
# Test Database - override تنظیمات اصلی
# ==========================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}