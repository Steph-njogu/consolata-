from django.shortcuts import render, redirect, get_object_or_404
from .models import Timetable
from PyPDF2 import PdfReader
from django.http import HttpResponse 


# Create your views here.
def timetable_view(request):
    timetable = Timetable.objects.all().order_by('-date_added')
    context = {'timetable' : timetable }
    return render (request, 'timetable/timetable.html', context)



def timetable_detail(request, slug_entry):
    timetable = get_object_or_404(Timetable, slug=slug_entry)

    if timetable.document:
        # Process PDF (e.g., extract text)
        document_path = timetable.document.path
        
        try:
            # Open the PDF file and read content (optional: extract text or metadata)
            with open(document_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ''
                # Extract text from each page
                for page in pdf_reader.pages:
                    text += page.extract_text()

            # Optional: You can process the text (log it, save it, etc.)
            print(text)  # For example, just print the extracted text to the console
        except Exception as e:
            print(f"Error processing PDF: {e}")

        # Serve the file for download
        with open(document_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{timetable.document.name}"'
            return response
    
    else:
        return redirect('timetable:timetable_view')
