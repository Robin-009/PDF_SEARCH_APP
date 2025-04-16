import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pdf_utils.search import search_pdfs_in_folder
import threading
import webbrowser
# FUnction to open the folder 
def open_folder(folder_path_var, folder_path_entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)
        folder_path_entry.config(state=tk.NORMAL)
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)
        folder_path_entry.config(state=tk.DISABLED)

def search_pdfs(search_entry, folder_path_var, tree, progress_var, progress_label):
    folder_path = folder_path_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder first.")
        return

    search_term = search_entry.get()
    if not search_term:
        messagebox.showerror("Error", "Please enter a search term.")
        return

    # Clear existing results
    for item in tree.get_children():
        tree.delete(item)

    # Start a new thread for the search operation
    threading.Thread(target=perform_search, args=(folder_path, search_term, tree, progress_var, progress_label)).start()

def perform_search(folder_path, search_term, tree, progress_var, progress_label):
    results = search_pdfs_in_folder(folder_path, search_term, progress_callback=lambda idx, total: update_progress(idx, total, progress_var, progress_label))
    
    if not results:
        progress_label.after(0, lambda: messagebox.showinfo("No PDFs Found", "No PDF files containing the search term were found in the selected folder."))
        return
    
    # Insert new results
    for file_path, count in results.items():
        tree.insert("", tk.END, values=(file_path, count))
    
    # Hide progress bar when done
    progress_var.set(0)
    progress_label.after(0, lambda: progress_label.config(text=""))

    # Updating the progress
def update_progress(current, total, progress_var, progress_label):
    progress = (current / total) * 100
    progress_var.set(progress)
    progress_label.after(0, lambda: progress_label.config(text=f"Processing: {current} of {total} files"))
    
    # Open the file by double clicking (in the default view selected by the user)
def open_file(event):
    selected_item = tree.selection()[0]
    file_path = tree.item(selected_item, 'values')[0]
    if os.path.exists(file_path):
        webbrowser.open_new(file_path)
    else:
        messagebox.showerror("Error", f"File not found: {file_path}")

def run_app():
    app = tk.Tk()
    app.title("PDF Folder Content Search")
    app.geometry("800x600")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))

    # Configure Treeview Style
    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    background="#003366",
                    foreground="blue",
                    relief="flat")
    style.configure("Treeview",
                    font=("Arial", 12),
                    rowheight=25,
                    background="white",
                    foreground="black")
    style.map("Treeview", background=[("selected", "#003366")], foreground=[("selected", "white")])
    
    # Title label
    title_label = tk.Label(app, text="PDF SEARCH APP", font=("Arial", 24, "bold"), fg="#003366")
    title_label.pack(pady=20)

    frame = tk.Frame(app)
    frame.pack(pady=10)

    folder_path_var = tk.StringVar()

    search_label = ttk.Label(frame, text="Search Term:")
    search_label.grid(row=0, column=0, padx=10)

    search_entry = ttk.Entry(frame, width=50)
    search_entry.grid(row=0, column=1, padx=10)

    # Adjust the position of the Open Folder button
    folder_path_label = ttk.Label(frame, text="Selected Folder:")
    folder_path_label.grid(row=1, column=0, padx=10, pady=10)

    folder_path_entry = ttk.Entry(frame, width=50, textvariable=folder_path_var, state=tk.DISABLED)
    folder_path_entry.grid(row=1, column=1, padx=10, pady=10)

    open_folder_button = ttk.Button(frame, text="Open Folder", command=lambda: open_folder(folder_path_var, folder_path_entry))
    open_folder_button.grid(row=1, column=2, padx=10, pady=10)

    search_button = ttk.Button(frame, text="Search", command=lambda: search_pdfs(search_entry, folder_path_var, tree, progress_var, progress_label))
    search_button.grid(row=0, column=2, padx=10)

    tree_frame = tk.Frame(app)
    tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    columns = ("File Path", "Keyword Count")
    global tree
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("File Path", text="File Path", anchor="center")
    tree.heading("Keyword Count", text="Keyword Count", anchor="center")
    tree.column("File Path", width=500, anchor="w")
    tree.column("Keyword Count", width=100, anchor="center")
    tree.grid(row=0, column=0, sticky='nsew')

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=100)
    progress_bar.pack(pady=10, padx=20, fill=tk.X)

    progress_label = ttk.Label(app, text="")
    progress_label.pack()

    # Bind the treeview to open file on double-click
    tree.bind("<Double-1>", open_file)

    app.mainloop()  