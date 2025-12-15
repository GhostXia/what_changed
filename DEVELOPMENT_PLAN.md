# 📄 Vibe Coding 开发计划

> **项目目标**：
> 构建一个面向论文 / 长文档作者的本地工具，
> 能够以「增量式、低噪音」的方式清晰展示**哪里被修改了**，
> 并最终打包为 **Windows 单文件 `.exe`，双击即用**。

---

## 0️⃣ 总体原则（始终牢记）

```
- One exe
- One window
- One job
```

- 这是一个**文档工具**，不是编译器、不是 IDE
- 用户是**学术作者**，不是程序员
- 清晰 > 完整
- 可读性 > 技术炫技
- 默认行为 > 配置选项

---

## 1️⃣ 项目问题定义（Why）

### 现实痛点
- 论文 / 长文档体量大
- 多轮修改后，作者很难看清：
  - 这一次到底改了哪里？
  - 是润色，还是实质性修改？

### 现有工具的问题
- 传统 diff：噪音过大
- Git diff：面向程序员，不面向作者
- Word 修订：跨版本、跨编辑者时不直观

### 本项目的立场
> **只关心“实际发生变化的地方”**

---

## 2️⃣ 最终产品形态（强约束）

### 用户视角
- 双击一个 `.exe`
- 打开一个简洁窗口
- 选择：
  - 原稿文件
  - 修改稿文件
- 点击「Compare」
- 立即看到：
  - 哪些段落被改了
  - 每个段落里具体改了什么

### 技术边界
```
- Python
- tkinter
- 本地运行
- 无网络依赖
- 可 PyInstaller 单文件打包
```

---

## 3️⃣ 用户体验设计（先于代码）

### 窗口结构
- 文件选择按钮：Original / Revised
- 一个 Compare 按钮
- 一个可滚动文本输出区域

### 体验目标
- 作者在 **30 秒内**理解修改内容
- 未修改内容默认不出现或折叠
- 视觉安静、学术风格

---

## 4️⃣ 核心技术思想：增量式 · 分块 Diff

### 文档分块策略（Block-aware）

优先级从大到小：
1. 章节 / 标题（如存在）
2. 段落（空行分隔）
3. 句子（用于精细 diff）

每个段落作为一个 **稳定 block**。

---

### 增量 Diff 逻辑

```
原稿 blocks ──┐
               ├─ 找出变化 blocks
修改稿 blocks ──┘
                    ↓
            只对变化 blocks 做精细 diff
```

- 完全相同的段落：忽略
- 只展示：
  - 新增
  - 删除
  - 被修改的段落

> 目标：**极大减少噪音**

---

## 5️⃣ MVP 功能范围（必须克制）

### 必须有
- 本地文件读取（UTF-8）
- 段落级变化识别
- 词级差异高亮
- 仅展示变化内容

### 明确不做（现在）
- 语义理解
- AI / LLM
- 多语言界面
- 协作 / 多人版本
- 云同步

---

## 6️⃣ 实现约束（为 EXE 服务）

### GUI 约束
- tkinter only
- 单窗口
- 无多线程 / async

### 代码约束
- 无动态 import
- 无运行时下载
- 路径处理安全
- 编码处理明确

---

## 7️⃣ Vibe Coding 实施提示词（可直接喂给 AI）

### 7.1 定调 Prompt

```
You are building a small, practical Windows desktop tool for non-technical users.

Final goal:
- a single Windows .exe file
- double-click to run
- no installation

The tool helps authors compare two large documents
and clearly see what actually changed.

Constraints:
- Python
- tkinter only
- simple GUI
- clarity over features

Design everything with PyInstaller in mind.
```

---

### 7.2 用户体验 Prompt（禁止写代码）

```
Describe the user experience of this desktop app.
Focus only on what the user sees and clicks.
No technical details.
```

---

### 7.3 增量 Diff Prompt（核心）

```
Design a block-aware incremental diff strategy for long academic documents.
Unchanged blocks should be ignored.
Only changed blocks are shown.
Explain why this is clearer than traditional diff.
```

---

### 7.4 实现 MVP Prompt

```
Implement a minimal working version.

Requirements:
- Python
- tkinter GUI
- two file selectors
- one Compare button
- one scrollable output area

Behavior:
- load both files
- split into paragraphs
- ignore unchanged paragraphs
- show word-level differences for changed ones

Keep the code readable and simple.
```

---

### 7.5 输出样式 Prompt

```
Improve the output format.

Goals:
- easy to scan
- calm and academic
- minimal visual noise

Show an example output.
```

---

### 7.6 PyInstaller 检查 Prompt

```
Review the code for PyInstaller compatibility.
Ensure it can be packaged as a single .exe file.
Explain the build steps.
```

---

## 8️⃣ EXE 打包方式（最终交付）

```bash
pyinstaller --onefile --noconsole paper_diff.py
```

输出：
```
dist/paper_diff.exe
```

用户只需要这个文件。

---

## 9️⃣ 未来方向（不承诺）

- 变化类型标注（润色 / 改写 / 新增）
- 段落折叠与展开
- 导出修改报告（PDF / TXT）
- 轻量语义辅助（可选）

> 所有未来功能 **不影响当前 MVP 的纯净性**

---

## ✅ 结语

这是一个：
- 克制的工具
- 人类友好的工具
- 为真实写作者服务的工具

**先把“哪里改了”这件事，做到极致。**
