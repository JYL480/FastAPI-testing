FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 
# Base image

WORKDIR /app 

# within the container

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 4000

COPY ./app /app