import fitz  # PyMuPDF
from pathlib import Path

def check_pdf_for_forms(pdf_path):
    print(f"\nChecking PDF: {pdf_path}")
    try:
        doc = fitz.open(pdf_path)
        print(f"PDF has {len(doc)} pages")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            widgets = list(page.widgets())
            
            if widgets:
                print(f"Page {page_num + 1} has {len(widgets)} form widgets")
                for i, widget in enumerate(widgets, 1):
                    print(f"  Widget {i}: {widget.field_type_string} - {widget.field_name} = {widget.field_value}")
            else:
                print(f"Page {page_num + 1}: No form widgets found")
                
            # Check for form annotations
            for annot in page.annots():
                if annot.type[0] in (fitz.PDF_ANNOT_WIDGET, fitz.PDF_ANNOT_TEXT, 
                                  fitz.PDF_ANNOT_CHOICE, fitz.PDF_ANNOT_SIGNATURE):
                    print(f"  Found form annotation on page {page_num + 1}: {annot.type}")
        
        doc.close()
        return True
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return False

if __name__ == "__main__":
    test_files = [
        "demo/Form.pdf",
        "demo/w8.pdf"
    ]
    
    for file in test_files:
        file_path = Path(file)
        if file_path.exists():
            check_pdf_for_forms(file_path)
        else:
            print(f"File not found: {file}")
