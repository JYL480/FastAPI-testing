FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 
# Base image

WORKDIR /app 

# within the container

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8000

COPY ./api /app

CMD [ "fastapi", "dev", "api/main.py"]