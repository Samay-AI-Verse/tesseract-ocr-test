# === Use an official Python image ===
FROM python:3.10-slim

# === Install system dependencies ===
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    tesseract-ocr-hin \
    tesseract-ocr-mar \
    tesseract-ocr-mal \
    && rm -rf /var/lib/apt/lists/*

# === Set working directory ===
WORKDIR /app

# === Copy dependency file and install Python deps ===
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# === Copy app code ===
COPY . /app

# === Expose port and start FastAPI ===
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
