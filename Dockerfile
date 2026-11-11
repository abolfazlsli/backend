FROM python:3.11-slim


ENV PIP_INDEX_URL=https://package-mirror.liara.ir/repository/pypi/simple
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     libpq-dev \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# نصب دیپندنسی‌ها (جدا از کد، برای استفاده بهتر از cache لایه‌ها)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# کپی کد پروژه
COPY . .

# پوشه‌ی آپلود (در صورت نیاز)
RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
