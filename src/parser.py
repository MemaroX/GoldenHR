import PyPDF2
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""
    return text

if __name__ == "__main__":
    # Example usage:
    # Create a dummy PDF for testing if it doesn't exist
    dummy_pdf_path = "data/dummy.pdf"
    if not os.path.exists(dummy_pdf_path):
        print(f"Creating a dummy PDF at {dummy_pdf_path} for testing...")
        # For actual testing, you'd need a real PDF file.
        # This part is just a placeholder to avoid immediate errors
        # if no PDF is present. User needs to provide a real PDF.
        with open(dummy_pdf_path, "w") as f:
            f.write("This is a dummy PDF file content.\n")
            f.write("It contains keywords like Python, FastAPI, and Machine Learning.\n")
            f.write("Also JavaScript and React for frontend development.")
        print(f"Please replace '{dummy_pdf_path}' with a real PDF file for proper testing.")

    extracted_content = extract_text_from_pdf(dummy_pdf_path)
    if extracted_content:
        print("\n--- Extracted Text ---")
        print(extracted_content)
        print("----------------------")
    else:
        print("\nNo text extracted.")
