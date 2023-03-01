FROM python:3.8.10

ENV PYTHONPATH ./src

COPY requirements.txt /app/
COPY README.md /app/
COPY poetry.lock /app/
COPY pyproject.toml /app/
COPY ./src /app/src

WORKDIR /app

RUN pip install -r requirements.txt
RUN poetry install

ENTRYPOINT [ "poetry", "run", "python", "-m", "helium_positioning_api", "serve" ]

EXPOSE 8000