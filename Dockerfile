FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 
# Base image

WORKDIR /app 

# within the container

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 80

COPY ./app /app

CMD [ "fastapi", "dev", "app/main.py", ]