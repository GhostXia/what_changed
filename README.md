# What Changed - Academic Document Comparison Tool
# 论文对比工具 - 专为学术写作设计

![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)

> **[📺 在线演示](https://ghostxia.github.io/what_changed/)** — 一分钟内了解这个工具能做什么

---

## 🎯 它解决什么问题？

您是否经历过这些场景：

- 📄 论文修改到第 N 版，已经忘了哪里改过了
- 🔍 Word 的「修订模式」让文档变得混乱不堪
- 🕵️ 逐行对比太累，但在线工具又担心隐私
- ⏳ 导师说「就改了几个地方」，结果您翻遍全文也找不到

**What Changed** 就是为此而生：

✅ **只看修改，不看废话** — 自动隐藏未修改的段落，让您专注于真正的变化  
✅ **词级精准高亮** — 红色删除，绿色新增，一目了然  
✅ **100% 本地运行** — 您的论文永远不会离开您的电脑，没有隐私担忧  
✅ **单文件、免安装** — 下载即用，双击运行

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 🔒 **隐私优先** | 100% 本地运行，无需联网，数据永不上传 |
| 📄 **双栏并排对比** | 左侧原文，右侧修改稿，直观对照 |
| 🧠 **智能分块 Diff** | 自动忽略未修改段落，减少视觉干扰 |
| 🎨 **词级高亮** | <span style="color:red">红色</span>表示删除，<span style="color:green">绿色</span>表示新增 |
| 📜 **同步滚动** | 左右面板同步滚动，保持上下文对齐 |
| 📝 **白板模式** | 无需加载文件，直接粘贴文本对比 |
| 🌐 **中英双语** | 界面支持中英文即时切换 |

---

## 🚀 快速开始

### 1. 下载
从 [Releases](https://github.com/GhostXia/what-changed/releases) 页面下载 `what_changed.exe`

### 2. 运行
双击 `what_changed.exe`，无需安装任何依赖

### 3. 对比
- 点击 **浏览** 选择您的原文档和修改后文档
- 支持格式：`.docx` (推荐), `.txt`, `.md`, `.tex` 及各类代码文件
- 点击蓝色的 **开始对比** 按钮

### 4. 查看结果
- 只有修改过的段落会显示
- 使用「同步滚动」保持两侧对齐
- 右键点击可复制文本

> 📘 **需要更多帮助？** 请查看详细的 [使用说明书](USER_GUIDE.md)

---

## 🛠️ 系统要求

| 平台 | 要求 |
|------|------|
| **Windows** | Windows 10/11 |
| **文件格式** | `.docx` (推荐), `.txt`, `.md`, `.tex`, `.py`, `.js` 等 |
| **编码** | 推荐 UTF-8，自动兼容 GBK |

> ⚠️ `.doc` 格式需要先在 Word 中另存为 `.docx`

---

## ❌ 这个工具**不**做什么

我们相信「专注」比「全能」更重要：

- ❌ **不提供在线版本** — 您的论文应该留在您的电脑里
- ❌ **不支持多人协作** — 这是一个个人工具
- ❌ **不集成云存储** — 没有账号，没有同步
- ❌ **不使用 AI 改写** — 只展示差异，不替您做决定
- ❌ **不需要复杂配置** — 下载即用

> "先把「哪里改了」这件事做到极致，其它的都可以慢慢来。"

---

## 📝 许可证

本项目采用 [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) 许可证开源。

---

## 🔗 相关链接

- [📺 在线演示](./demo/index.html)
- [📖 使用说明书](USER_GUIDE.md)
- [📋 发布说明](RELEASE_NOTES.md)
- [🐛 提交问题](https://github.com/GhostXia/what-changed/issues)