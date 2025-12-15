import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import difflib
import re
import docx
import os

# Configuration
FONT_TEXT = ("Georgia", 11)
FONT_HEADER = ("Segoe UI", 10, "bold")
COLOR_BG_DEL = "#ffebee" # Light Red
COLOR_FG_DEL = "#b71c1c" # Dark Red
COLOR_BG_ADD = "#e8f5e9" # Light Green
COLOR_FG_ADD = "#1b5e20" # Dark Green
COLOR_SEPARATOR = "#cfd8dc"
# Language Dictionary
LANGUAGES = {
    "English": {
        "window_title": "What Changed",
        "btn_compare": "COMPARE DOCUMENTS",
        "chk_sync": "Synchronize Scrolling",
        "lbl_original": "Original Document",
        "lbl_revised": "Revised Document",
        "btn_browse": "Browse...",
        "msg_select_files": "Please select both files.",
        "msg_no_diff": "No differences found.",
        "header_mod": "● Modified\n",
        "header_del": "● Deleted\n",
        "header_add": "● Added\n",
        "placeholder_del": "\n(Deleted)\n",
        "placeholder_add": "\n(Added)\n",
        "ctx_copy": "Copy"
    },
    "中文": {
        "window_title": "文档对比工具",
        "btn_compare": "开始对比",
        "chk_sync": "同步滚动",
        "lbl_original": "原文档",
        "lbl_revised": "修改后文档",
        "btn_browse": "浏览...",
        "msg_select_files": "请选择两个文件。",
        "msg_no_diff": "未发现差异。",
        "header_mod": "● 修改\n",
        "header_del": "● 删除\n",
        "header_add": "● 新增\n",
        "placeholder_del": "\n(已删除)\n",
        "placeholder_add": "\n(新增)\n",
        "ctx_copy": "复制"
    }
}

current_lang = "中文" # Default to Chinese as user requested

def get_text(key):
    return LANGUAGES[current_lang].get(key, key)

def read_docx(filepath):
    """Reads a .docx file and returns its content."""
    try:
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading .docx file: {e}"

def load_file(filepath):
    """Reads a file and returns its content."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.docx':
        return read_docx(filepath)
    elif ext == '.doc':
        return "Error: .doc format is not supported directly. Please save as .docx and try again."
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try different encoding
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file (encoding): {e}"
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
        text_left.insert(tk.END, get_text("msg_select_files"))
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
        
        max_len = max(len(p1_block), len(p2_block))
        
        for k in range(max_len):
            p1 = p1_block[k] if k < len(p1_block) else None
            p2 = p2_block[k] if k < len(p2_block) else None
            
            # Header / Context
            if p1 and p2:
                # Modified
                text_left.insert(tk.END, get_text("header_mod"), 'header_mod')
                text_right.insert(tk.END, get_text("header_mod"), 'header_mod')
                
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
                text_left.insert(tk.END, get_text("header_del"), 'header_del')
                text_left.insert(tk.END, p1, 'removed_block')
                
                text_right.insert(tk.END, get_text("placeholder_del"), 'placeholder')
                
            elif not p1 and p2:
                # Added
                text_left.insert(tk.END, get_text("placeholder_add"), 'placeholder')
                
                text_right.insert(tk.END, get_text("header_add"), 'header_add')
                text_right.insert(tk.END, p2, 'added_block')
            
            insert_separator(text_left)
            insert_separator(text_right)

    if not has_changes:
        text_left.insert(tk.END, get_text("msg_no_diff"))
        text_right.insert(tk.END, get_text("msg_no_diff"))

def browse_file(entry_widget):
    filetypes = [
        ("Supported Files", "*.txt;*.md;*.docx;*.doc;*.tex;*.py;*.js;*.html;*.css;*.json;*.xml"),
        ("Word Documents", "*.docx;*.doc"),
        ("Text Files", "*.txt"),
        ("Markdown", "*.md"),
        ("LaTeX", "*.tex"),
        ("Code Files", "*.py;*.js;*.html;*.css;*.json;*.xml"),
        ("All Files", "*.*")
    ]
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

def update_ui_text():
    root.title(get_text("window_title"))
    btn_compare.config(text=get_text("btn_compare"))
    chk_sync.config(text=get_text("chk_sync"))
    lbl_original.config(text=get_text("lbl_original"))
    lbl_revised.config(text=get_text("lbl_revised"))
    btn_browse_left.config(text=get_text("btn_browse"))
    btn_browse_right.config(text=get_text("btn_browse"))

def change_language(event):
    global current_lang
    current_lang = combo_lang.get()
    update_ui_text()

def main():
    global root, entry_original, entry_revised, text_left, text_right
    global btn_compare, chk_sync, lbl_original, lbl_revised, btn_browse_left, btn_browse_right, combo_lang
    
    root = tk.Tk()
    root.geometry("1280x720")
    
    # 1. Top Bar
    frame_top = tk.Frame(root, pady=10)
    frame_top.pack(side=tk.TOP, fill=tk.X)
    
    btn_compare = tk.Button(frame_top, command=perform_compare, 
                            bg="#1976d2", fg="white", font=("Segoe UI", 12, "bold"), padx=30, pady=8, relief=tk.FLAT, cursor="hand2")
    btn_compare.pack(side=tk.LEFT, padx=20)
    
    # Sync Scroll Checkbox
    global var_sync
    var_sync = tk.BooleanVar(value=True)
    chk_sync = tk.Checkbutton(frame_top, variable=var_sync, 
                              font=("Segoe UI", 10), bg="#f0f0f0", activebackground="#f0f0f0")
    chk_sync.pack(side=tk.LEFT)
    
    # Language Selector
    frame_lang = tk.Frame(frame_top)
    frame_lang.pack(side=tk.RIGHT, padx=20)
    tk.Label(frame_lang, text="Language / 语言: ").pack(side=tk.LEFT)
    combo_lang = ttk.Combobox(frame_lang, values=["English", "中文"], state="readonly", width=10)
    combo_lang.set(current_lang)
    combo_lang.pack(side=tk.LEFT)
    combo_lang.bind("<<ComboboxSelected>>", change_language)
    
    # 2. File Selectors
    frame_files = tk.Frame(root, pady=5, padx=20)
    frame_files.pack(side=tk.TOP, fill=tk.X)
    
    # Left Selector
    frame_f_left = tk.Frame(frame_files)
    frame_f_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    lbl_original = tk.Label(frame_f_left, font=FONT_HEADER, fg=COLOR_FG_DEL)
    lbl_original.pack(anchor="w")
    entry_original = tk.Entry(frame_f_left)
    entry_original.pack(fill=tk.X, pady=2)
    btn_browse_left = tk.Button(frame_f_left, command=lambda: browse_file(entry_original))
    btn_browse_left.pack(anchor="e")
    
    # Right Selector
    frame_f_right = tk.Frame(frame_files)
    frame_f_right.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
    lbl_revised = tk.Label(frame_f_right, font=FONT_HEADER, fg=COLOR_FG_ADD)
    lbl_revised.pack(anchor="w")
    entry_revised = tk.Entry(frame_f_right)
    entry_revised.pack(fill=tk.X, pady=2)
    btn_browse_right = tk.Button(frame_f_right, command=lambda: browse_file(entry_revised))
    btn_browse_right.pack(anchor="e")
    
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
    
    # Configure Tags
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
        
        t.tag_raise("sel")
        
    # Context Menu
    def show_context_menu(event):
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label=get_text("ctx_copy"), command=lambda: event.widget.event_generate("<<Copy>>"))
        menu.tk_popup(event.x_root, event.y_root)

    text_left.bind("<Button-3>", show_context_menu)
    text_right.bind("<Button-3>", show_context_menu)
    
    # Ctrl+C
    def copy_text(event=None):
        event.widget.event_generate("<<Copy>>")
        return "break"
    
    text_left.bind("<Control-c>", copy_text)
    text_right.bind("<Control-c>", copy_text)

    # Initial Text Update
    update_ui_text()

    root.mainloop()

if __name__ == "__main__":
    main()
