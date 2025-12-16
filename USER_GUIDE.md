# User Guide / 使用说明书

**What Changed** is a simple yet powerful tool for comparing documents. This guide will help you get the most out of it.
**What Changed** 是一个简单而强大的文档对比工具。本指南将帮助您充分利用它的功能。

---

## 1. Installation / 安装

### Windows
1. Download `what_changed.exe` from the [Releases](https://github.com/GhostXia/what-changed/releases) page.
   - 从 [Releases](https://github.com/GhostXia/what-changed/releases) 页面下载 `what_changed.exe`。
2. Double-click the file to run. No installation is required.
   - 双击文件即可运行，无需安装。
3. (Optional) You can move the `.exe` file to any folder you like.
   - (可选) 您可以将 `.exe` 文件移动到任意文件夹。

### macOS
1. Download `what_changed_macos.dmg` from the [Releases](https://github.com/GhostXia/what-changed/releases) page.
   - 从 [Releases](https://github.com/GhostXia/what-changed/releases) 页面下载 `what_changed_macos.dmg`。
2. Double-click the `.dmg` file to open it.
   - 双击 `.dmg` 文件打开。
3. Drag the `What Changed` app to your `Applications` folder (or run it directly).
   - 将 `What Changed` 应用程序拖入您的 `应用程序 (Applications)` 文件夹（或直接运行）。
4. If you see a security warning ("App cannot be opened because it is from an unidentified developer"), go to **System Settings > Privacy & Security** and click **Open Anyway**.
   - 如果遇到安全警告（“无法打开应用，因为它来自身份不明的开发者”），请前往 **系统设置 > 隐私与安全性**，点击 **仍要打开**。

---

## 2. Interface Overview / 界面概览

The interface consists of three main areas:
界面主要由三个区域组成：

1.  **Top Bar / 顶部栏**:
    *   **Compare Button / 开始对比**: Triggers the comparison process.
        - 触发对比流程。
    *   **Synchronize Scrolling / 同步滚动**: Toggles whether the two text panels scroll together.
        - 切换左右两个文本面板是否同步滚动。
    *   **Whiteboard Mode / 白板模式**: Switches between File Mode and Whiteboard Mode.
        - 在“文件模式”和“白板模式”之间切换。
    *   **Language Selector / 语言选择**: Switches the UI language.
        - 切换界面语言。

2.  **File Selectors / 文件选择区** (File Mode only / 仅限文件模式):
    *   **Original Document / 原文档**: The older version of your document.
        - 文档的旧版本。
    *   **Revised Document / 修改后文档**: The newer version of your document.
        - 文档的新版本。

3.  **Comparison View / 对比视图**:
    *   **Left Panel / 左侧面板**: Shows the Original document content.
        - 显示原文档内容。
    *   **Right Panel / 右侧面板**: Shows the Revised document content.
        - 显示修改后文档内容。
    *   **Colors / 颜色**: <span style="color:red">Red</span> indicates deletion, <span style="color:green">Green</span> indicates addition.
        - <span style="color:red">红色</span> 表示删除，<span style="color:green">绿色</span> 表示新增。

---

## 3. Features / 功能详解

### 📄 File Comparison / 文件对比
1.  Ensure **Whiteboard Mode** is unchecked.
    - 确保未勾选 **白板模式**。
2.  Click **Browse** to select your Original and Revised files.
    - 点击 **浏览** 选择您的原文档和修改后文档。
    *   **Supported Formats**: `.docx` (Word), `.txt`, `.md` (Markdown), `.tex` (LaTeX), `.py`, `.js`, `.html`, etc.
    *   **支持格式**：`.docx` (Word), `.txt`, `.md` (Markdown), `.tex` (LaTeX), `.py`, `.js`, `.html` 等。
3.  Click **COMPARE DOCUMENTS**.
    - 点击 **开始对比** 按钮。
4.  The tool will analyze the files and display differences side-by-side.
    - 工具将分析文件并并排显示差异。

### 📝 Whiteboard Mode / 白板模式
Useful for quick comparisons of text snippets without saving files.
适用于无需保存文件、快速对比文本片段的场景。

1.  Check **Whiteboard Mode** in the top bar.
    - 在顶部栏勾选 **白板模式**。
2.  The file selection area will be disabled.
    - 文件选择区域将被禁用。
3.  Paste or type your text directly into the **Left** (Original) and **Right** (Revised) text panels.
    - 直接在 **左侧** (原文) 和 **右侧** (修改稿) 文本面板中粘贴或输入文本。
4.  Click **COMPARE DOCUMENTS**.
    - 点击 **开始对比** 按钮。

### 📜 Synchronized Scrolling / 同步滚动
*   **Enabled (Default)**: Scrolling one panel automatically scrolls the other to keep matching paragraphs aligned.
    - **开启 (默认)**：滚动一个面板会自动滚动另一个面板，保持对应段落对齐。
*   **Disabled**: Panels scroll independently. Useful if you want to look at different parts of the documents simultaneously.
    - **关闭**：面板独立滚动。适用于需要同时查看文档不同部分的情况。

### 🧠 Block-Aware Diff / 智能分块
The tool automatically detects paragraphs that have **no changes** and hides them (or collapses them) to reduce visual clutter. You will only see the parts of the document that have actually been modified.
工具会自动检测并隐藏**未修改**的段落，减少视觉干扰。您只会看到真正发生变化的部分。

---

## 4. Troubleshooting / 常见问题

**Q: Why does it say ".doc format is not supported"?**
**问：为什么提示不支持 .doc 格式？**
A: The tool uses a modern library that only supports `.docx`. Please open your `.doc` file in Word and "Save As" `.docx`.
答：工具使用的现代库仅支持 `.docx`。请在 Word 中打开您的 `.doc` 文件并“另存为” `.docx` 格式。

**Q: The text encoding looks wrong (gibberish).**
**问：文字显示乱码。**
A: The tool automatically tries `UTF-8` and `GBK` encodings. If your text file uses a different encoding, please convert it to UTF-8 first.
答：工具会自动尝试 `UTF-8` 和 `GBK` 编码。如果您的文本文件使用其他编码，请先将其转换为 UTF-8。

**Q: Can I compare code files?**
**问：可以对比代码文件吗？**
A: Yes! It supports many code formats like `.py`, `.js`, `.html`, `.css`, `.json`, `.xml`.
答：可以！支持多种代码格式，如 `.py`, `.js`, `.html`, `.css`, `.json`, `.xml`。
