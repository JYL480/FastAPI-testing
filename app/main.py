from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, Path, File, UploadFile
from typing import Annotated, Optional
from model import predictImg
from fastapi.responses import FileResponse
import os
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
# Create a check first
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8081",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = "uploads"
latest_img_path = ""

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/")
def read_root():
    return {"Message": "Hello World"}


# let me try uploading a picture!
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        return {"message": f"There was an error uploading the file: {e}"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/files/{filename}")
def read_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"message": "File not found"}



@app.post("/predict")
async def predict():
    files = os.listdir(UPLOAD_DIRECTORY)
    if(files == []):
        return {"Message": "Please upload an image first!"}
    # print(files)
    img_path = os.path.join(UPLOAD_DIRECTORY, files[len(files)-1])
    # print(img_path)
    msg, time =predictImg(img_path)
    return {"Message": msg, "Time": time}

   