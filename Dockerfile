FROM python:3.9

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
COPY . /code
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

VOLUME ["/media"]
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD python3.9 -m uvicorn rest:app --reload --host 0.0.0.0 --port 8000