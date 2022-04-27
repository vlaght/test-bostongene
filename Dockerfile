FROM python:3.9

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
COPY . /code
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

CMD python3.9 -m uvicorn rest:app --reload