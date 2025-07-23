from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from fpdf import FPDF
from dotenv import load_dotenv
import os
import shutil
import pytesseract
import requests


load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/process/")
async def process_image(file: UploadFile):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = pytesseract.image_to_string(Image.open(file_path))

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://google.com",
        "X-Title": "Image Summary App"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system",
                "content": "Summarize the following prompt in 300 to 400 words."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 500
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    result = response.json()

    if "choices" not in result:
        return {"error": "API Error", "details": result}

    summary = result["choices"][0]["message"]["content"]

    clean_summary = summary.encode("ascii", "ignore").decode()

    os.makedirs("output", exist_ok=True)
    pdf_path = f"output/{file.filename.split('.')[0]}_summary.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in clean_summary.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))
