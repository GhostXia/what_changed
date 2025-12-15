import tkinter as tk
from tkinter import filedialog, scrolledtext
import difflib
import os

def load_file(filepath):
    """Reads a file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def split_paragraphs(text):
    """Splits text into paragraphs based on double newlines."""
    # Normalize line endings and split by double newline
    return [p.strip() for p in text.replace('\r\n', '\n').split('\n\n') if p.strip()]

def compare_texts(text1, text2):
    """Compares two texts paragraph by paragraph."""
    paragraphs1 = split_paragraphs(text1)
    paragraphs2 = split_paragraphs(text2)
    
    matcher = difflib.SequenceMatcher(None, paragraphs1, paragraphs2)
    diffs = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue  # Ignore unchanged blocks
        
        # For changed blocks, we want to show what happened
        if tag == 'replace':
            for k in range(i2 - i1):
                p1 = paragraphs1[i1 + k]
                # Try to match with corresponding paragraph in revised
                if k < (j2 - j1):
                    p2 = paragraphs2[j1 + k]
                    diffs.append(('change', p1, p2))
                else:
                    diffs.append(('delete', p1, None))
            
            # If there are more paragraphs in revised, they are additions
            if (j2 - j1) > (i2 - i1):
                for k in range((i2 - i1), (j2 - j1)):
                    diffs.append(('insert', None, paragraphs2[j1 + k]))
                    
        elif tag == 'delete':
            for k in range(i1, i2):
                diffs.append(('delete', paragraphs1[k], None))
        elif tag == 'insert':
            for k in range(j1, j2):
                diffs.append(('insert', None, paragraphs2[k]))
                
    return diffs

def perform_compare():
    file1_path = entry_original.get()
    file2_path = entry_revised.get()
    
    if not file1_path or not file2_path:
        text_output.delete('1.0', tk.END)
        text_output.insert(tk.END, "Please select both files.")
        return

    content1 = load_file(file1_path)
    content2 = load_file(file2_path)
    
    diffs = compare_texts(content1, content2)
    
    text_output.delete('1.0', tk.END)
    
    if not diffs:
        text_output.insert(tk.END, "No differences found (or files are identical).")
        return

    for type, p1, p2 in diffs:
        if type == 'change':
            text_output.insert(tk.END, "[MODIFIED]\n", 'header_mod')
            
            # Simple word-level diff for the paragraph
            # This is a basic implementation. For better word diff, we'd need more logic.
            # Here we just show old and new.
            
            # Let's try a slightly better word diff using difflib.ndiff
            # But for MVP, maybe just showing Old vs New is clearer?
            # The requirement says "show word-level differences".
            
            s = difflib.SequenceMatcher(None, p1.split(), p2.split())
            for opcode, a0, a1, b0, b1 in s.get_opcodes():
                if opcode == 'equal':
                    text_output.insert(tk.END, " ".join(p1.split()[a0:a1]) + " ")
                elif opcode == 'insert':
                    text_output.insert(tk.END, " ".join(p2.split()[b0:b1]) + " ", 'added')
                elif opcode == 'delete':
                    text_output.insert(tk.END, " ".join(p1.split()[a0:a1]) + " ", 'removed')
                elif opcode == 'replace':
                    text_output.insert(tk.END, " ".join(p1.split()[a0:a1]) + " ", 'removed')
                    text_output.insert(tk.END, " ".join(p2.split()[b0:b1]) + " ", 'added')
            
            text_output.insert(tk.END, "\n\n")

        elif type == 'delete':
            text_output.insert(tk.END, "[DELETED]\n", 'header_del')
            text_output.insert(tk.END, p1 + "\n\n", 'removed_block')
        elif type == 'insert':
            text_output.insert(tk.END, "[ADDED]\n", 'header_add')
            text_output.insert(tk.END, p2 + "\n\n", 'added_block')

def browse_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

def main():
    global entry_original, entry_revised, text_output
    
    # GUI Setup
    root = tk.Tk()
    root.title("Paper Diff MVP")
    root.geometry("800x600")

    # Frame for file selection
    frame_top = tk.Frame(root, pady=10)
    frame_top.pack(fill=tk.X, padx=10)

    # Original File
    tk.Label(frame_top, text="Original:").grid(row=0, column=0, sticky="w")
    entry_original = tk.Entry(frame_top, width=50)
    entry_original.grid(row=0, column=1, padx=5)
    tk.Button(frame_top, text="Browse", command=lambda: browse_file(entry_original)).grid(row=0, column=2)

    # Revised File
    tk.Label(frame_top, text="Revised:").grid(row=1, column=0, sticky="w")
    entry_revised = tk.Entry(frame_top, width=50)
    entry_revised.grid(row=1, column=1, padx=5)
    tk.Button(frame_top, text="Browse", command=lambda: browse_file(entry_revised)).grid(row=1, column=2)

    # Compare Button
    btn_compare = tk.Button(root, text="Compare", command=perform_compare, bg="#dddddd", font=("Arial", 10, "bold"))
    btn_compare.pack(pady=5)

    # Output Area
    text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
    text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tags for styling
    text_output.tag_config('header_mod', foreground='blue', font=("Arial", 10, "bold"))
    text_output.tag_config('header_add', foreground='green', font=("Arial", 10, "bold"))
    text_output.tag_config('header_del', foreground='red', font=("Arial", 10, "bold"))

    text_output.tag_config('added', foreground='green', background='#e6ffec')
    text_output.tag_config('removed', foreground='red', background='#ffe6e6', overstrike=True)

    text_output.tag_config('added_block', foreground='green')
    text_output.tag_config('removed_block', foreground='red')

    root.mainloop()

if __name__ == "__main__":
    main()
