FROM python:3.11

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app.py app.py

COPY ./basoene_api /app/basoene_api

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]