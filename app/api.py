from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import List
import os
import shutil
from app.utils import extract_text_from_pdf, extract_text_from_pptx, maketopics, mindmap, examkeypoints, clean_up,read_feedback,create_feedback,exampaper
from app.video_processing import video_to_slides, slides_to_pdf
from fastapi.responses import FileResponse
import uuid
from app.utils import get_db
from sqlalchemy.orm import Session

from starlette.background import BackgroundTask
from app.schemas import FeedbackCreate
router = APIRouter()



@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    video_path = f"{uuid.uuid4()}.mp4"
    with open(video_path, "wb") as video_file:
        shutil.copyfileobj(file.file, video_file)
    output_folder_screenshot_path = video_to_slides(video_path)
    pdf_path = slides_to_pdf(output_folder_screenshot_path)
    
    # Define the cleanup task
    cleanup_task = BackgroundTask(clean_up, [video_path, output_folder_screenshot_path, pdf_path])
    
    # Return the FileResponse with the cleanup task
    return FileResponse(pdf_path, media_type='application/pdf', filename=os.path.basename(pdf_path), background=cleanup_task)

@router.post("/topics")
async def upload_files(files: List[UploadFile] = File(...), typeoftopic: str = Form(...), numoftopic: int = Form(...)):
    responses = []
    for file in files:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".pdf", ".pptx"]:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or PPTX files.")
        content = await file.read()
        extracted_text = extract_text_from_pdf(content) if ext == ".pdf" else extract_text_from_pptx(content)
        api_response = maketopics(extracted_text, typeoftopic, numoftopic)
        responses.append({"filename": filename, "api_response": api_response})
    return {"responses": responses}

@router.post("/mindmap")
async def upload_files(files: List[UploadFile] = File(...)):
    responses = []
    for file in files:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".pdf", ".pptx"]:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or PPTX files.")
        content = await file.read()
        extracted_text = extract_text_from_pdf(content) if ext == ".pdf" else extract_text_from_pptx(content)
        api_response = mindmap(extracted_text)
        responses.append({"filename": filename, "api_response": api_response})
    return {"responses": responses}

@router.post("/examkeypoints")
async def upload_files(files: List[UploadFile] = File(...)):
    responses = []
    for file in files:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".pdf", ".pptx"]:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or PPTX files.")
        content = await file.read()
        extracted_text = extract_text_from_pdf(content) if ext == ".pdf" else extract_text_from_pptx(content)
        api_response = examkeypoints(extracted_text)
        responses.append({"filename": filename, "api_response": api_response})
    return {"responses": responses}

@router.post("/exampaper")
async def upload_files(files: List[UploadFile] = File(...),typeoftopic: str = Form(...), numoftopic: int = Form(...)):
    responses = []
    for file in files:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".pdf", ".pptx"]:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or PPTX files.")
        content = await file.read()
        extracted_text = extract_text_from_pdf(content) if ext == ".pdf" else extract_text_from_pptx(content)
        api_response = exampaper(extracted_text,typeoftopic,numoftopic)
        responses.append({"filename": filename, "api_response": api_response})
    return {"responses": responses}

@router.post("/feedback")
async def create_feedback_route(feedback: FeedbackCreate):
    return create_feedback(feedback)

@router.get("/feedback", response_model=List[FeedbackCreate])
async def get_feedback_route():
    return read_feedback()