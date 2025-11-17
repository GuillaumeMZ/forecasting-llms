# Base image
FROM mirror.gcr.io/library/python:3.11

# Set working directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    scipy==1.11.4 \
    requests==2.31.0

RUN pip install --no-cache-dir tqdm pandas matplotlib

# Set environment variables
ENV PYTHONUNBUFFERED=1
