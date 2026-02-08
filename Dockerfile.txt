FROM python:3.11
WORKDIR /project
COPY ./requirements.txt ./requirements.txt
RUN apt update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg && \
    rm -rf /var/lib/apt/lists/*
COPY . .
RUN python -O main.py > /dev/null 2>&1 || true

CMD ["python", "-u", "main.py"]

