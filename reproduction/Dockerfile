FROM python:3.13.10-slim

WORKDIR /app

COPY .env .
COPY reproduction/ ./reproduction/
COPY reproduction_input/ ./reproduction_input/

RUN python3 -m pip install -r ./reproduction/requirements.txt

CMD ["python3", "-m", "reproduction", "reproduction_input", "reproduction_output"]