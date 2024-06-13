FROM python:3.10

WORKDIR /app

ENV POETRY_HOME=/opt/poetry

RUN python3 -m venv $POETRY_HOME

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-directory

COPY recepto recepto

RUN poetry install --only main

CMD ["fastapi", "run", "recepto/main.py", "--host", "0.0.0.0", "--port", "8000"]