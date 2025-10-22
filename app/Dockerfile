FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app.py .

# 데이터 디렉토리 생성
RUN mkdir -p /data

# 포트 노출
EXPOSE 8080

# Gunicorn으로 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
