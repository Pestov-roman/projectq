FROM python:3.12-slim

ENV POETRY_VERSION=2.1.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y curl build-essential libpq-dev gcc \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --with dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "src.config.wsgi:application", "--bind", "0.0.0.0:8000"]
