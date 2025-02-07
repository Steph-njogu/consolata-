from PIL import Image
import pytesseract
import pdf2image

def extract_text_from_pdf(file_path):
    try:
        # Convert PDF pages to images
        images = pdf2image.convert_from_path(file_path)
        
        # Use OCR on each image page
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        
        if text.strip() == '':
            return "No text found in the PDF (OCR might not have detected anything)."
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF using OCR: {str(e)}")
