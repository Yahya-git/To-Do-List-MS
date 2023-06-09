FROM python:3.10.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-deps --no-cache-dir -r requirements.txt
COPY . .