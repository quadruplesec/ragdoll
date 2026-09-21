FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# First copy and install the requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Only then do we copy the rest of the application code
COPY . .

# FastAPI runs on port 8000 by default
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]