FROM python:3.8

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.1.13

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction

EXPOSE 8000

CMD ["python","-u", "main.py"]
