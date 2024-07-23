import os
from pdf_utils.extract import extract_text_from_pdf

def search_text_in_pdf(text_list, search_term):
    search_results = {}
    for page_num, page_text in enumerate(text_list):
        if search_term.lower() in page_text.lower():
            search_results[page_num + 1] = page_text
    return search_results

def search_pdfs_in_folder(folder_path, search_term, progress_callback=None):
    results = {}
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    total_files = len(pdf_files)
    
    for idx, file_path in enumerate(pdf_files):
        if progress_callback:
            progress_callback(idx + 1, total_files)
        
        text_list = extract_text_from_pdf(file_path)
        search_results = search_text_in_pdf(text_list, search_term)
        if search_results:
            count = sum(page_text.lower().count(search_term.lower()) for page_text in text_list)
            results[file_path] = count
    
    return results
