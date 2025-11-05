FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# for easy ocr
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY src/ src/
COPY assets/ assets/

# flask port
EXPOSE 8080

# default command
CMD ["python", "src/app.py"]