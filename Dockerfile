FROM python:3.10-slim

# Environment hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# System deps (important for ML / FAISS / numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (cache friendly)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
