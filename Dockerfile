FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY req.txt /app/
RUN python -m venv venv && source venv/bin/activate
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/req.txt

COPY . /app/
EXPOSE 8000

ENTRYPOINT ["uvicorn", "api:app", "--reload"]


# docker run -d -v "$(pwd)"/data:/app/data .