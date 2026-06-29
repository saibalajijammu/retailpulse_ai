# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", "--server.address=0.0.0.0"]