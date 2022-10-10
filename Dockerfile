FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

WORKDIR /app
COPY req.txt /app/
RUN pip install -U --no-cache-dir --upgrade pip &&  \
    pip install -U --no-cache-dir -r /app/req.txt &&  \
    mkdir /app/logs && mkdir /app/management

COPY *.py /app/
EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "api:app"]

# docker build -t scripter:latest .
# docker run -d -v "$HOME"/management/logs/:/app/logs/ -v "$HOME"/management/:/app/management/ --network host -p 8000:8000 --name scripter fenick/scripter:latest
