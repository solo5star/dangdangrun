FROM python:3.9

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 3355

ENTRYPOINT ["python", "/app/entrypoint.py"]