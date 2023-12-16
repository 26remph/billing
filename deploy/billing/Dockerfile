FROM python:3.10 as base


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    GID=ugc \
    UID=ugc

RUN pip install poetry

WORKDIR /opt/app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev,research --no-interaction --no-ansi

COPY .. .

EXPOSE 8080

RUN groupadd -r ${GID} \
    && useradd -d /home/${UID} -r -g ${GID} ${UID} \
    && chown ${UID}:${UID} -R /opt
USER ${UID}

ENTRYPOINT [ "bash", "entrypoint.sh" ]