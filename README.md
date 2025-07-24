# image-summary-pdf-generator-model
FastAPI app that extracts text from images using OCR, summarizes it with GPT-4, and generates a downloadable PDF.

# Features

- Upload any image (PNG, JPG)
- AI-generated description/summary using OpenAI
- Downloadable PDF with image and summary
- Clean HTML-based output
- Lightweight and fast

# How to Run on windows

# 1. Clone the repo
- git clone https://github.com/HitendraSinghPanwar/image-summary-pdf-generator-model.git
- cd image-summary-pdf-generator-model

# 2. Create virtual environment and activate it
- python -m venv venv
- venv\Scripts\activate  

# 3. Install dependencies
-pip install -r requirements.txt

# 4. Run the app
-uvicorn app.main:app --reload
