import tkinter as tk
from tkinter import filedialog, ttk
from pdf_utils.search import search_pdfs_in_folder
import threading

def open_folder(search_entry, tree, progress_var, progress_label):
    folder_path = filedialog.askdirectory()
    if folder_path:
        search_term = search_entry.get()
        
        # Clear existing results
        for item in tree.get_children():
            tree.delete(item)
        
        # Start a new thread for the search operation
        threading.Thread(target=search_pdfs, args=(folder_path, search_term, tree, progress_var, progress_label)).start()

def search_pdfs(folder_path, search_term, tree, progress_var, progress_label):
    results = search_pdfs_in_folder(folder_path, search_term, progress_callback=lambda idx, total: update_progress(idx, total, progress_var, progress_label))
    
    # Insert new results
    for file_path, count in results.items():
        tree.insert("", tk.END, values=(file_path, count))
    
    # Hide progress bar when done
    progress_var.set(0)
    progress_label.config(text="")

def update_progress(current, total, progress_var, progress_label):
    progress = (current / total) * 100
    progress_var.set(progress)
    progress_label.config(text=f"Processing: {current} of {total} files")

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

    search_label = ttk.Label(frame, text="Search Term:")
    search_label.grid(row=0, column=0, padx=10)

    search_entry = ttk.Entry(frame, width=50)
    search_entry.grid(row=0, column=1, padx=10)

    search_button = ttk.Button(frame, text="Open Folder & Search", command=lambda: open_folder(search_entry, tree, progress_var, progress_label))
    search_button.grid(row=0, column=2, padx=10)

    tree_frame = tk.Frame(app)
    tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    columns = ("File Path", "Keyword Count")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("File Path", text="File Path", anchor="center")
    tree.heading("Keyword Count", text="Keyword Count", anchor="center")
    tree.column("File Path", width=500, anchor="w")
    tree.column("Keyword Count", width=100, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=100)
    progress_bar.pack(pady=10, padx=20, fill=tk.X)

    progress_label = ttk.Label(app, text="")
    progress_label.pack()

    app.mainloop()
