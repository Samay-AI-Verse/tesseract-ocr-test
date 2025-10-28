import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# ==========================================
# 1️⃣ CONFIG — set languages here
# Make sure to install these language packs in build.sh
LANGS = "eng+hin+mar+mal"  # English, Hindi, Marathi, Malayalam
POPPLER_PATH = None  # We’ll install poppler in Render (system)
# ==========================================

def extract_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    print(f"🔹 Extracting from image: {image_path}")
    text = pytesseract.image_to_string(Image.open(image_path), lang=LANGS)
    return text.strip()

def extract_from_pdf(pdf_path):
    """Extract text from each page of a PDF using Tesseract OCR."""
    print(f"📘 Extracting from PDF: {pdf_path}")
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    all_text = ""
    for i, page in enumerate(pages):
        temp_img = f"/tmp/page_{i}.png"
        page.save(temp_img, "PNG")
        page_text = extract_from_image(temp_img)
        all_text += f"\n\n--- Page {i+1} ---\n{page_text}"
    return all_text.strip()

if __name__ == "__main__":
    # You can test with local file
    file_path = input("Enter image/pdf file path: ").strip()
    if file_path.lower().endswith(".pdf"):
        text = extract_from_pdf(file_path)
    else:
        text = extract_from_image(file_path)
    
    print("\n✅ Extracted Text:")
    print("-" * 60)
    print(text)
