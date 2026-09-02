# ۱. انتخاب Base Image سبک و رسمی
FROM python:3.14-slim

# ۲. جلوگیری از نوشتن بایت‌کد و بافر نشدن لاگ‌ها (حیاتی برای مشاهده زنده لاگ‌ها)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ۳. تعیین دایرکتوری کاری در کانتینر
WORKDIR /app

# ۴. نصب وابستگی‌های سیستمی مورد نیاز (مثل درایورهای دیتابیس)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ۵. اول کپی کردن فایل نیازمندی‌ها (جهت استفاده حداکثری از کش داکر در تغییرات بعدی سورس‌کد)
COPY requirements.txt .

# ۶. نصب پکیج‌های پایتون
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ۷. کپی کردن بقیه سورس‌کد پروژه
COPY . .

# ۸. اکسپوز کردن پورت ارتباطی
EXPOSE 8000

# ۹. کامند اجرای برنامه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
