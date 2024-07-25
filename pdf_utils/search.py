import os
import re
from pdf_utils.extract import extract_text_from_pdf

# Searches for a term in the text extracted from a PDF.
def search_text_in_pdf(text_list, search_term, pattern):
    search_results = {}
    
    for page_num, page_text in enumerate(text_list):
        if pattern.search(page_text):
            search_results[page_num + 1] = page_text
    return search_results

# Searches for a term in all PDF files within a specified folder and its subfolders.
def search_pdfs_in_folder(folder_path, search_term, progress_callback=None):
    results = {}
    pdf_files = []
    
    # Define a regular expression pattern for the search term as a whole word
    pattern = re.compile(r'\b' + re.escape(search_term) + r'\b', re.IGNORECASE)
    
    # Collect all PDF files in the specified folder and subfolders
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    total_files = len(pdf_files)
    
    # Process each PDF file
    for idx, file_path in enumerate(pdf_files):
        if progress_callback:
            try:
                progress_callback(idx + 1, total_files)
            except Exception as e:
                print(f"Progress callback error: {e}")
        
        try:
            # Extract text from the PDF file
            text_list = extract_text_from_pdf(file_path)
            
            # Search for the term in the extracted text
            search_results = search_text_in_pdf(text_list, search_term, pattern)
            
            # Count the occurrences of the search term as whole words
            if search_results:
                count = sum(len(pattern.findall(page_text)) for page_text in text_list)
                results[file_path] = count
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    return results
