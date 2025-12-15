import tkinter as tk
from tkinter import filedialog, scrolledtext
import difflib
import re

# Configuration
FONT_TEXT = ("Georgia", 11)
FONT_HEADER = ("Segoe UI", 10, "bold")
COLOR_BG_DEL = "#ffebee" # Light Red
COLOR_FG_DEL = "#b71c1c" # Dark Red
COLOR_BG_ADD = "#e8f5e9" # Light Green
COLOR_FG_ADD = "#1b5e20" # Dark Green
COLOR_SEPARATOR = "#cfd8dc"

def load_file(filepath):
    """Reads a file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def split_paragraphs(text):
    """Splits text into paragraphs based on double newlines."""
    return [p.strip() for p in text.replace('\r\n', '\n').split('\n\n') if p.strip()]

def tokenize(text):
    """Splits text into words and spaces."""
    return re.findall(r'\S+|\s+', text)

def insert_separator(text_widget):
    text_widget.insert(tk.END, "\n" + "─"*40 + "\n", 'separator')

def perform_compare():
    file1_path = entry_original.get()
    file2_path = entry_revised.get()
    
    if not file1_path or not file2_path:
        text_left.delete('1.0', tk.END)
        text_right.delete('1.0', tk.END)
        text_left.insert(tk.END, "Please select both files.")
        return

    content1 = load_file(file1_path)
    content2 = load_file(file2_path)
    
    paragraphs1 = split_paragraphs(content1)
    paragraphs2 = split_paragraphs(content2)
    
    matcher = difflib.SequenceMatcher(None, paragraphs1, paragraphs2)
    
    text_left.delete('1.0', tk.END)
    text_right.delete('1.0', tk.END)
    
    has_changes = False
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
        
        has_changes = True
        
        # Handle block of changes
        p1_block = paragraphs1[i1:i2]
        p2_block = paragraphs2[j1:j2]
        
        # We try to match them up 1-to-1 as much as possible for display
        max_len = max(len(p1_block), len(p2_block))
        
        for k in range(max_len):
            p1 = p1_block[k] if k < len(p1_block) else None
            p2 = p2_block[k] if k < len(p2_block) else None
            
            # Header / Context
            if p1 and p2:
                # Modified
                text_left.insert(tk.END, "● Modified\n", 'header_mod')
                text_right.insert(tk.END, "● Modified\n", 'header_mod')
                
                # Word-level diff
                s = difflib.SequenceMatcher(None, tokenize(p1), tokenize(p2))
                for opcode, a1, a2, b1, b2 in s.get_opcodes():
                    if opcode == 'equal':
                        text_left.insert(tk.END, "".join(tokenize(p1)[a1:a2]))
                        text_right.insert(tk.END, "".join(tokenize(p2)[b1:b2]))
                    elif opcode == 'replace':
                        text_left.insert(tk.END, "".join(tokenize(p1)[a1:a2]), 'removed')
                        text_right.insert(tk.END, "".join(tokenize(p2)[b1:b2]), 'added')
                    elif opcode == 'delete':
                        text_left.insert(tk.END, "".join(tokenize(p1)[a1:a2]), 'removed')
                    elif opcode == 'insert':
                        text_right.insert(tk.END, "".join(tokenize(p2)[b1:b2]), 'added')
                        
            elif p1 and not p2:
                # Deleted
                text_left.insert(tk.END, "● Deleted\n", 'header_del')
                text_left.insert(tk.END, p1, 'removed_block')
                
                text_right.insert(tk.END, "\n(Deleted)\n", 'placeholder')
                
            elif not p1 and p2:
                # Added
                text_left.insert(tk.END, "\n(Added)\n", 'placeholder')
                
                text_right.insert(tk.END, "● Added\n", 'header_add')
                text_right.insert(tk.END, p2, 'added_block')
            
            insert_separator(text_left)
            insert_separator(text_right)

    if not has_changes:
        text_left.insert(tk.END, "No differences found.")
        text_right.insert(tk.END, "No differences found.")

def browse_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

def main():
    global entry_original, entry_revised, text_left, text_right
    
    root = tk.Tk()
    root.title("Paper Diff")
    root.geometry("1200x800")
    
    # 1. Top Bar
    frame_top = tk.Frame(root, pady=10)
    frame_top.pack(side=tk.TOP, fill=tk.X)
    
    btn_compare = tk.Button(frame_top, text="COMPARE DOCUMENTS", command=perform_compare, 
                            bg="#1976d2", fg="white", font=("Segoe UI", 12, "bold"), padx=30, pady=8, relief=tk.FLAT, cursor="hand2")
    btn_compare.pack(side=tk.LEFT, padx=20)
    
    # Sync Scroll Checkbox
    global var_sync
    var_sync = tk.BooleanVar(value=True)
    chk_sync = tk.Checkbutton(frame_top, text="Synchronize Scrolling", variable=var_sync, 
                              font=("Segoe UI", 10), bg="#f0f0f0", activebackground="#f0f0f0")
    chk_sync.pack(side=tk.LEFT)
    
    # 2. File Selectors
    frame_files = tk.Frame(root, pady=5, padx=20)
    frame_files.pack(side=tk.TOP, fill=tk.X)
    
    # Left Selector
    frame_f_left = tk.Frame(frame_files)
    frame_f_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    tk.Label(frame_f_left, text="Original Document", font=FONT_HEADER, fg=COLOR_FG_DEL).pack(anchor="w")
    entry_original = tk.Entry(frame_f_left)
    entry_original.pack(fill=tk.X, pady=2)
    tk.Button(frame_f_left, text="Browse...", command=lambda: browse_file(entry_original)).pack(anchor="e")
    
    # Right Selector
    frame_f_right = tk.Frame(frame_files)
    frame_f_right.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
    tk.Label(frame_f_right, text="Revised Document", font=FONT_HEADER, fg=COLOR_FG_ADD).pack(anchor="w")
    entry_revised = tk.Entry(frame_f_right)
    entry_revised.pack(fill=tk.X, pady=2)
    tk.Button(frame_f_right, text="Browse...", command=lambda: browse_file(entry_revised)).pack(anchor="e")
    
    # 3. Output Area (Two Panels)
    frame_output = tk.Frame(root, pady=10, padx=20)
    frame_output.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    # Left Text
    text_left = scrolledtext.ScrolledText(frame_output, font=FONT_TEXT, wrap=tk.WORD, width=40)
    text_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    
    # Right Text
    text_right = scrolledtext.ScrolledText(frame_output, font=FONT_TEXT, wrap=tk.WORD, width=40)
    text_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
    
    # Sync Scrolling Logic
    def sync_scroll_left(*args):
        text_left.vbar.set(*args)
        if var_sync.get():
            text_right.yview_moveto(args[0])
            
    def sync_scroll_right(*args):
        text_right.vbar.set(*args)
        if var_sync.get():
            text_left.yview_moveto(args[0])
            
    text_left.config(yscrollcommand=sync_scroll_left)
    text_right.config(yscrollcommand=sync_scroll_right)
    
    # Configure Tags (Apply to both)
    for t in [text_left, text_right]:
        t.tag_config('header_mod', foreground='#455a64', font=FONT_HEADER, spacing3=5)
        t.tag_config('header_add', foreground=COLOR_FG_ADD, font=FONT_HEADER, spacing3=5)
        t.tag_config('header_del', foreground=COLOR_FG_DEL, font=FONT_HEADER, spacing3=5)
        
        t.tag_config('removed', foreground=COLOR_FG_DEL, background=COLOR_BG_DEL, overstrike=True)
        t.tag_config('added', foreground=COLOR_FG_ADD, background=COLOR_BG_ADD)
        
        t.tag_config('removed_block', foreground=COLOR_FG_DEL, background=COLOR_BG_DEL)
        t.tag_config('added_block', foreground=COLOR_FG_ADD, background=COLOR_BG_ADD)
        
        t.tag_config('placeholder', foreground='#90a4ae', font=("Segoe UI", 9, "italic"), justify='center')
        t.tag_config('separator', foreground=COLOR_SEPARATOR, justify='center')

    root.mainloop()

if __name__ == "__main__":
    main()
