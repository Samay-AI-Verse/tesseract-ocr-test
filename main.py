



from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import uuid

app = FastAPI(title="Tesseract OCR API", version="1.0")

# Supported languages — make sure they're installed on the server
LANGS = "eng+hin+mar+mal"
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path), lang=LANGS)
    return text.strip()

def extract_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    all_text = ""
    for i, page in enumerate(pages):
        temp_img = f"/tmp/page_{uuid.uuid4().hex}.png"
        page.save(temp_img, "PNG")
        all_text += f"\n\n--- Page {i+1} ---\n{extract_from_image(temp_img)}"
        os.remove(temp_img)
    return all_text.strip()

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        file_ext = file.filename.split(".")[-1].lower()
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if file_ext in ["png", "jpg", "jpeg"]:
            text = extract_from_image(file_path)
        elif file_ext == "pdf":
            text = extract_from_pdf(file_path)
        else:
            return JSONResponse({"error": "Unsupported file type."}, status_code=400)

        os.remove(file_path)
        return {"filename": file.filename, "text": text[:2000]}  # return first 2000 chars
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
def home():
    return {"message": "Welcome to Tesseract OCR API", "endpoint": "/ocr (POST)"}




