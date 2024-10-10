FROM python:3.12

WORKDIR /app

# Python and poetry installation
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=3.12

ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"

RUN echo "done 0" \
    && curl https://pyenv.run | bash \
    && echo "done installing pyenv" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "done installing pythbon ${PYTHON_VERSION}" \
    && pyenv global ${PYTHON_VERSION} \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true

COPY ./pyproject.toml ./poetry.lock /app/

RUN poetry install --no-root --no-dev

COPY ./api /app/api

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]