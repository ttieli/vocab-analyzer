# Web Frontend Specification - Vocab Analyzer

**文档版本**: v1.0
**创建日期**: 2025-11-04
**优先级**: P1 (高优先级 - Phase 2 增强功能)
**预计工期**: 2-3天

---

## 📋 目录

1. [需求概述](#1-需求概述)
2. [功能需求](#2-功能需求)
3. [技术方案](#3-技术方案)
4. [界面设计](#4-界面设计)
5. [实施计划](#5-实施计划)
6. [验收标准](#6-验收标准)

---

## 1. 需求概述

### 业务需求

为vocab-analyzer添加简单的Web界面，允许用户通过浏览器上传书籍文件，在线查看分析结果，并支持下载多种格式。

### 核心目标

- ✅ **简单快速**：最短时间内实现可用版本
- ✅ **用户友好**：无需命令行知识
- ✅ **单文件分析**：支持单本书籍上传分析
- ✅ **进度可视化**：实时显示分析进度
- ✅ **结果展示**：美观的在线结果展示
- ✅ **多格式下载**：支持JSON/CSV/Markdown下载

### 非目标（本次不包含）

- ❌ 批量上传
- ❌ 用户登录/注册
- ❌ 数据库存储
- ❌ 历史记录
- ❌ 复杂权限控制

---

## 2. 功能需求

### 2.1 文件上传

**功能描述**：
用户通过Web界面上传待分析的书籍文件。

**详细需求**：

1. **支持的文件格式**：
   - TXT（纯文本）
   - PDF（非扫描版）
   - DOCX（Word文档）
   - JSON（结构化数据）

2. **文件大小限制**：
   - 最大：50MB
   - 推荐：<10MB（显示警告）

3. **上传方式**：
   - 拖拽上传（Drag & Drop）
   - 点击选择文件（File Picker）

4. **前端验证**：
   - 文件格式验证
   - 文件大小检查
   - 清晰的错误提示

**示例界面**：
```
┌─────────────────────────────────────────────┐
│   📚 Vocab Analyzer - Upload Your Book      │
├─────────────────────────────────────────────┤
│                                             │
│   ┌───────────────────────────────────┐    │
│   │                                   │    │
│   │   📁 Drag & drop your book here   │    │
│   │        or click to browse         │    │
│   │                                   │    │
│   │  Supported: TXT, PDF, DOCX, JSON  │    │
│   │       Max size: 50MB              │    │
│   │                                   │    │
│   └───────────────────────────────────┘    │
│                                             │
│   Selected: pride_and_prejudice.txt (735KB) │
│                                             │
│   [  Analyze  ]  [ Cancel ]                │
│                                             │
└─────────────────────────────────────────────┘
```

### 2.2 分析进度显示

**功能描述**：
实时显示分析过程的各个阶段和进度。

**详细需求**：

1. **进度阶段**（共5个阶段）：
   ```
   Stage 1: 📄 Extracting text...          [████████░░] 80%
   Stage 2: 🔤 Processing NLP...           [██░░░░░░░░] 20%
   Stage 3: 🔍 Detecting phrases...        [░░░░░░░░░░] 0%
   Stage 4: 📊 Matching levels...          [░░░░░░░░░░] 0%
   Stage 5: 📈 Generating statistics...    [░░░░░░░░░░] 0%
   ```

2. **进度信息**：
   - 当前阶段名称
   - 进度百分比
   - 预计剩余时间（可选）
   - 已处理词数/总词数

3. **视觉反馈**：
   - 进度条动画
   - 当前阶段高亮
   - 完成阶段显示✓
   - 加载动画

4. **技术实现**：
   - 后端：Server-Sent Events (SSE) 或 WebSocket
   - 前端：实时更新进度条

**示例界面**：
```
┌─────────────────────────────────────────────┐
│   📚 Analyzing: pride_and_prejudice.txt     │
├─────────────────────────────────────────────┤
│                                             │
│   Overall Progress                          │
│   ████████████████░░░░░░░░░░░  60%         │
│                                             │
│   ✓ Stage 1: Extracting text      (2.3s)  │
│   ✓ Stage 2: Processing NLP       (8.7s)  │
│   ⏳ Stage 3: Detecting phrases    ...     │
│   ⏸ Stage 4: Matching levels               │
│   ⏸ Stage 5: Generating statistics         │
│                                             │
│   Processing: 3,456 / 6,000 words           │
│   Estimated time remaining: 15s             │
│                                             │
└─────────────────────────────────────────────┘
```

### 2.3 结果展示

**功能描述**：
分析完成后，在网页上直接展示结果，包括统计信息和词汇列表。

**详细需求**：

1. **统计概览区**：
   ```
   ┌─────────────────────────────────────────┐
   │  📊 Analysis Summary                    │
   ├─────────────────────────────────────────┤
   │  Total Words: 127,377                   │
   │  Unique Words: 6,544                    │
   │  Unique Phrases: 18                     │
   │  Analysis Time: 23.5s                   │
   └─────────────────────────────────────────┘
   ```

2. **等级分布可视化**：
   - 柱状图或饼图
   - 显示各CEFR等级的词数和占比
   - 可交互（点击查看详情）

   ```
   ┌─────────────────────────────────────────┐
   │  📈 CEFR Level Distribution             │
   ├─────────────────────────────────────────┤
   │                                         │
   │  A1 ████████░░░░░░░░  569 (8.7%)       │
   │  A2 ██████████░░░░░░  906 (13.8%)      │
   │  B1 ████████████████  2,145 (32.8%)    │
   │  B2 ██████████████░░  1,456 (22.3%)    │
   │  C1 ██████████░░░░░░  892 (13.6%)      │
   │  C2 ████░░░░░░░░░░░░  398 (6.1%)       │
   │  C2+ ██░░░░░░░░░░░░░  178 (2.7%)       │
   │                                         │
   └─────────────────────────────────────────┘
   ```

3. **词汇列表区**：
   - 分页显示（每页50-100词）
   - 按等级分组（可折叠/展开）
   - 按频率排序
   - 搜索/过滤功能

   ```
   ┌─────────────────────────────────────────────────┐
   │  📚 Vocabulary List                             │
   ├─────────────────────────────────────────────────┤
   │  🔍 Search: [_______]  Filter: [All Levels ▼]  │
   ├─────────────────────────────────────────────────┤
   │                                                 │
   │  ▼ B1 Level (2,145 words)                      │
   │                                                 │
   │  ┌──────────────────────────────────────────┐  │
   │  │ develop  (verb)  B1                       │  │
   │  │ 发展；开发；研制                            │  │
   │  │ Frequency: 14 times                       │  │
   │  └──────────────────────────────────────────┘  │
   │                                                 │
   │  ┌──────────────────────────────────────────┐  │
   │  │ society  (noun)  B1                       │  │
   │  │ 社会                                       │  │
   │  │ Frequency: 23 times                       │  │
   │  └──────────────────────────────────────────┘  │
   │                                                 │
   │  [1] [2] [3] ... [43]  Showing 1-50 of 2,145  │
   │                                                 │
   └─────────────────────────────────────────────────┘
   ```

4. **词组列表区**（可折叠）：
   ```
   ┌─────────────────────────────────────────────────┐
   │  ▼ Phrasal Verbs (18 phrases)                   │
   │                                                 │
   │  • look up (B1) - 查找 - 8 times                │
   │  • give up (B2) - 放弃 - 5 times                │
   │  • carry on (B2) - 继续 - 3 times               │
   │                                                 │
   └─────────────────────────────────────────────────┘
   ```

### 2.4 结果下载

**功能描述**：
提供多种格式的下载选项。

**详细需求**：

1. **下载格式**：
   - JSON（完整数据）
   - CSV（适合Excel）
   - Markdown（适合阅读）

2. **下载按钮组**：
   ```
   ┌─────────────────────────────────────────┐
   │  💾 Download Results                    │
   ├─────────────────────────────────────────┤
   │  [ JSON ]  [ CSV ]  [ Markdown ]        │
   └─────────────────────────────────────────┘
   ```

3. **文件命名规则**：
   - `{原文件名}_vocabulary.{格式}`
   - 例如：`pride_and_prejudice_vocabulary.json`

4. **下载反馈**：
   - 点击后显示"Downloading..."
   - 下载完成提示
   - 错误处理

---

## 3. 技术方案

### 3.1 技术栈选择

基于"简单快速可实现"的原则，选择：

#### 方案A：Flask + 纯HTML/JS（推荐 - 最简单）

**后端**：
- Flask 3.0+（轻量级Web框架）
- Flask-CORS（跨域支持）
- 直接复用现有vocab_analyzer Python代码

**前端**：
- HTML5
- Tailwind CSS（无需配置，CDN即可）
- Vanilla JavaScript（原生JS，无需构建）
- Chart.js（图表库，CDN）

**优势**：
- ✅ 最简单，无需额外构建工具
- ✅ 部署容易（单服务器）
- ✅ 开发快速（2-3天可完成）
- ✅ 与现有CLI代码零冲突

**劣势**：
- ⚠️ 前端功能相对简单
- ⚠️ 扩展性一般

#### 方案B：Streamlit（最快 - 原型）

**技术**：
- Streamlit（Python Web框架）
- 自动生成界面

**优势**：
- ✅ 最快（1天可完成）
- ✅ 纯Python，无需前端知识
- ✅ 自带进度条、文件上传

**劣势**：
- ⚠️ 界面自定义受限
- ⚠️ 不适合生产环境

#### 方案C：FastAPI + Vue.js（现代化）

**后端**：
- FastAPI（异步高性能）
- WebSocket（实时进度）

**前端**：
- Vue.js 3
- Vite（构建工具）

**优势**：
- ✅ 现代化、高性能
- ✅ 扩展性强

**劣势**：
- ⚠️ 开发时间长（4-5天）
- ⚠️ 需要前端构建

### 3.2 推荐方案：Flask + Tailwind CSS

基于您的需求，推荐**方案A：Flask + Tailwind CSS**。

#### 项目结构

```
vocab-analyzer/
├── src/vocab_analyzer/          # 现有代码（无需修改）
│   └── ...
├── web/                          # 新增Web模块
│   ├── __init__.py
│   ├── app.py                   # Flask应用入口
│   ├── routes.py                # 路由处理
│   ├── static/                  # 静态资源
│   │   ├── css/
│   │   │   └── custom.css      # 自定义样式
│   │   └── js/
│   │       └── app.js          # 前端逻辑
│   └── templates/               # HTML模板
│       └── index.html          # 单页应用
├── uploads/                      # 临时上传目录（自动创建）
└── requirements-web.txt          # Web额外依赖
```

#### 核心技术细节

**1. 后端路由设计**

```python
# web/app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from vocab_analyzer import VocabularyAnalyzer

app = Flask(__name__)
CORS(app)

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 上传并分析
@app.route('/api/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    # 保存临时文件
    # 调用分析
    # 返回结果
    return jsonify(result)

# 下载文件
@app.route('/api/download/<format>')
def download(format):
    # 生成并返回文件
    return send_file(...)
```

**2. 实时进度方案**

使用**Server-Sent Events (SSE)**：

```python
# 后端
@app.route('/api/progress/<task_id>')
def progress(task_id):
    def generate():
        for stage, percent in analysis_progress(task_id):
            yield f"data: {json.dumps({'stage': stage, 'percent': percent})}\n\n"
    return Response(generate(), mimetype='text/event-stream')

# 前端
const eventSource = new EventSource('/api/progress/123');
eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateProgressBar(data.stage, data.percent);
};
```

**3. 前端UI框架**

使用**Tailwind CSS CDN**（无需构建）：

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <!-- 上传区域 -->
        <div class="bg-white rounded-lg shadow-lg p-8">
            <!-- 拖拽上传 -->
        </div>
    </div>
</body>
</html>
```

---

## 4. 界面设计

### 4.1 主界面布局

```
┌─────────────────────────────────────────────────────────────┐
│  📚 Vocab Analyzer                              [About] [?] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │              📁 Upload Your Book                      │ │
│  │                                                       │ │
│  │     Drag & drop or click to select a file            │ │
│  │     Supported: TXT, PDF, DOCX, JSON (max 50MB)       │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Recent Analysis: None                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 分析中界面

```
┌─────────────────────────────────────────────────────────────┐
│  📚 Vocab Analyzer - Analyzing...              [Cancel]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  File: pride_and_prejudice.txt (735KB)                      │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Overall Progress                                     │ │
│  │  ████████████████████░░░░░░░░░░░░░░  60%            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ✅ 1. Extracting text (2.3s)                              │
│  ✅ 2. Processing NLP (8.7s)                               │
│  ⏳ 3. Detecting phrases...                                │
│  ⏸ 4. Matching levels                                      │
│  ⏸ 5. Generating statistics                                │
│                                                             │
│  Processed: 3,456 / 6,544 words                             │
│  Estimated time: 15 seconds remaining                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 结果展示界面

```
┌─────────────────────────────────────────────────────────────┐
│  📚 Vocab Analyzer - Results                [New Analysis]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Analysis Summary                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  File: pride_and_prejudice.txt                      │   │
│  │  Total Words: 127,377                               │   │
│  │  Unique Words: 6,544                                │   │
│  │  Phrasal Verbs: 18                                  │   │
│  │  Analysis Time: 23.5s                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💾 Download: [ JSON ] [ CSV ] [ Markdown ]                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📈 CEFR Level Distribution                         │   │
│  │                                                     │   │
│  │  [Bar Chart showing A1-C2+ distribution]            │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📚 Vocabulary List                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🔍 [Search...]  Filter: [All Levels ▼] Sort: [▼]  │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  ▼ B1 Level (2,145 words)                          │   │
│  │                                                     │   │
│  │  develop (verb) | B1 | 发展；开发 | 14 times        │   │
│  │  society (noun) | B1 | 社会 | 23 times              │   │
│  │  ...                                                │   │
│  │                                                     │   │
│  │  [1] [2] [3] ... Showing 1-50 of 2,145             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 移动端适配

使用响应式设计：
- 桌面：侧边栏布局
- 平板：堆叠布局
- 手机：单列布局

---

## 5. 实施计划

### 5.1 开发任务分解

**Phase 1: 基础框架（Day 1，4-6小时）**

- [x] **T001**: 创建web目录结构
- [x] **T002**: 安装Flask和依赖（Flask, Flask-CORS）
- [x] **T003**: 创建基础Flask应用（app.py, routes.py）
- [x] **T004**: 创建HTML模板框架（index.html）
- [x] **T005**: 集成Tailwind CSS（CDN）
- [x] **T006**: 测试基础服务器启动

**Phase 2: 文件上传（Day 1-2，3-4小时）**

- [x] **T007**: 实现拖拽上传UI
- [x] **T008**: 实现文件选择UI
- [x] **T009**: 前端文件验证（格式、大小）
- [x] **T010**: 后端文件接收API（/api/upload）
- [x] **T011**: 文件保存到临时目录
- [x] **T012**: 错误处理和用户反馈

**Phase 3: 分析集成（Day 2，4-5小时）**

- [x] **T013**: 集成VocabularyAnalyzer
- [x] **T014**: 创建分析API（/api/analyze）
- [x] **T015**: 实现分析任务管理（后台运行）
- [x] **T016**: 实现SSE进度推送（/api/progress/<id>）
- [x] **T017**: 前端进度条UI
- [x] **T018**: 阶段状态更新
- [x] **T019**: 测试完整分析流程

**Phase 4: 结果展示（Day 2-3，5-6小时）**

- [x] **T020**: 统计概览UI
- [x] **T021**: 集成Chart.js图表库
- [x] **T022**: CEFR分布柱状图
- [x] **T023**: 词汇列表展示（分页）
- [x] **T024**: 词组列表展示
- [x] **T025**: 搜索过滤功能
- [x] **T026**: 排序功能

**Phase 5: 下载功能（Day 3，2-3小时）**

- [x] **T027**: JSON下载API
- [x] **T028**: CSV下载API
- [x] **T029**: Markdown下载API
- [x] **T030**: 前端下载按钮
- [x] **T031**: 文件命名规则
- [x] **T032**: 下载进度反馈

**Phase 6: 优化和测试（Day 3，3-4小时）**

- [x] **T033**: 响应式设计调整
- [x] **T034**: 错误处理完善
- [x] **T035**: 加载动画优化
- [x] **T036**: 浏览器兼容性测试
- [x] **T037**: 性能测试（大文件）
- [x] **T038**: 用户体验优化
- [x] **T039**: 编写README（Web部分）
- [x] **T040**: 部署文档

### 5.2 时间线

```
Day 1 (8小时)
├── 上午 (4h): T001-T006 基础框架
└── 下午 (4h): T007-T012 文件上传

Day 2 (8小时)
├── 上午 (4h): T013-T019 分析集成
└── 下午 (4h): T020-T026 结果展示（部分）

Day 3 (6-7小时)
├── 上午 (3h): T020-T026 结果展示（完成）
├── 中午 (2h): T027-T032 下载功能
└── 下午 (2h): T033-T040 优化测试
```

**总计**：2.5-3天（约22-23小时开发时间）

### 5.3 依赖关系

```
T001-T006 (基础框架)
    ↓
T007-T012 (文件上传)
    ↓
T013-T019 (分析集成)
    ↓
T020-T026 (结果展示) ← 最复杂
    ↓
T027-T032 (下载功能)
    ↓
T033-T040 (优化测试)
```

---

## 6. 验收标准

### 6.1 功能验收

**文件上传**：
- [ ] 支持拖拽上传
- [ ] 支持点击选择
- [ ] 文件格式验证（TXT/PDF/DOCX/JSON）
- [ ] 文件大小限制（50MB）
- [ ] 清晰的错误提示

**分析进度**：
- [ ] 5个阶段清晰显示
- [ ] 进度百分比准确更新
- [ ] 当前阶段高亮
- [ ] 完成阶段显示✓
- [ ] 预计时间显示（可选）

**结果展示**：
- [ ] 统计概览正确显示
- [ ] CEFR分布图表正确
- [ ] 词汇列表分页显示
- [ ] 搜索功能正常
- [ ] 过滤功能正常
- [ ] 词组列表正确

**下载功能**：
- [ ] JSON格式下载正常
- [ ] CSV格式下载正常
- [ ] Markdown格式下载正常
- [ ] 文件命名正确
- [ ] 内容完整准确

### 6.2 性能验收

- [ ] 小文件(<5MB)：上传<1s，分析<5s
- [ ] 中文件(5-20MB)：上传<3s，分析<30s
- [ ] 大文件(20-50MB)：上传<10s，分析<90s
- [ ] 界面响应流畅（无卡顿）
- [ ] 内存使用<500MB

### 6.3 用户体验验收

- [ ] 界面美观，布局合理
- [ ] 操作流程直观
- [ ] 加载状态明确
- [ ] 错误提示友好
- [ ] 移动端基本可用（可选）

### 6.4 兼容性验收

**浏览器**：
- [ ] Chrome/Edge（最新版）
- [ ] Firefox（最新版）
- [ ] Safari（最新版）

**操作系统**：
- [ ] macOS
- [ ] Windows
- [ ] Linux

---

## 7. 技术实现细节

### 7.1 核心代码框架

#### Flask应用入口（web/app.py）

```python
"""
Flask Web Application for Vocab Analyzer
"""
import os
import uuid
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from vocab_analyzer import VocabularyAnalyzer
from vocab_analyzer.exporters import JsonExporter, CsvExporter, MarkdownExporter

app = Flask(__name__)
CORS(app)

# 配置
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx', 'json'}

# 确保上传目录存在
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# 存储分析任务
analysis_tasks = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """分析文件API"""
    # 检查文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400

    # 保存文件
    task_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
    file.save(filepath)

    try:
        # 创建分析器
        analyzer = VocabularyAnalyzer()

        # 执行分析（TODO: 异步执行 + 进度更新）
        result = analyzer.analyze(filepath)

        # 存储结果
        analysis_tasks[task_id] = {
            'filename': filename,
            'result': result,
            'status': 'completed'
        }

        # 返回结果
        return jsonify({
            'task_id': task_id,
            'filename': filename,
            'statistics': {
                'total_words': result.total_words,
                'unique_words': len(result.words),
                'unique_phrases': len(result.phrases)
            },
            'level_distribution': _get_level_distribution(result),
            'words': _format_words(result.words),
            'phrases': _format_phrases(result.phrases)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # 清理临时文件
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/api/download/<task_id>/<format>')
def download(task_id, format):
    """下载分析结果"""
    if task_id not in analysis_tasks:
        return jsonify({'error': 'Task not found'}), 404

    task = analysis_tasks[task_id]
    result = task['result']
    filename = task['filename']
    base_name = Path(filename).stem

    # 临时输出文件
    output_file = f"{app.config['UPLOAD_FOLDER']}/{task_id}_output.{format}"

    try:
        if format == 'json':
            exporter = JsonExporter()
            exporter.export(result, output_file)
            download_name = f"{base_name}_vocabulary.json"

        elif format == 'csv':
            exporter = CsvExporter()
            exporter.export(result, output_file)
            download_name = f"{base_name}_vocabulary.csv"

        elif format == 'markdown':
            exporter = MarkdownExporter()
            exporter.export(result, output_file)
            download_name = f"{base_name}_vocabulary.md"
        else:
            return jsonify({'error': 'Invalid format'}), 400

        return send_file(
            output_file,
            as_attachment=True,
            download_name=download_name
        )

    finally:
        # 清理临时文件
        if os.path.exists(output_file):
            os.remove(output_file)

def _get_level_distribution(result):
    """获取等级分布"""
    distribution = {}
    for word in result.words.values():
        level = word.level
        distribution[level] = distribution.get(level, 0) + 1
    return distribution

def _format_words(words):
    """格式化词汇列表（前100个）"""
    word_list = sorted(
        words.values(),
        key=lambda w: w.frequency,
        reverse=True
    )[:100]

    return [
        {
            'word': w.lemma,
            'word_type': w.word_type,
            'level': w.level,
            'frequency': w.frequency,
            'definition_cn': w.definition_cn or ''
        }
        for w in word_list
    ]

def _format_phrases(phrases):
    """格式化词组列表"""
    return [
        {
            'phrase': p.phrase,
            'level': p.level,
            'frequency': p.frequency,
            'definition_cn': p.definition_cn or ''
        }
        for p in phrases.values()
    ]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### HTML模板（web/templates/index.html）

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vocab Analyzer - Web Interface</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <!-- 标题 -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">
                📚 Vocab Analyzer
            </h1>
            <p class="text-gray-600">
                Analyze English books and classify vocabulary by CEFR levels
            </p>
        </div>

        <!-- 上传区域 -->
        <div id="uploadSection" class="bg-white rounded-lg shadow-lg p-8 mb-8">
            <div
                id="dropZone"
                class="border-4 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition cursor-pointer"
            >
                <div class="text-6xl mb-4">📁</div>
                <h2 class="text-2xl font-semibold text-gray-700 mb-2">
                    Upload Your Book
                </h2>
                <p class="text-gray-500 mb-4">
                    Drag & drop your file here or click to browse
                </p>
                <p class="text-sm text-gray-400">
                    Supported formats: TXT, PDF, DOCX, JSON (Max 50MB)
                </p>
                <input type="file" id="fileInput" class="hidden" accept=".txt,.pdf,.docx,.json">
            </div>
            <div id="fileInfo" class="mt-4 hidden">
                <p class="text-gray-700">
                    Selected: <span id="fileName" class="font-semibold"></span>
                    (<span id="fileSize"></span>)
                </p>
                <button
                    id="analyzeBtn"
                    class="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg transition"
                >
                    Analyze
                </button>
                <button
                    id="cancelBtn"
                    class="mt-4 ml-2 bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg transition"
                >
                    Cancel
                </button>
            </div>
        </div>

        <!-- 进度区域 -->
        <div id="progressSection" class="bg-white rounded-lg shadow-lg p-8 mb-8 hidden">
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">
                Analyzing: <span id="analyzingFile"></span>
            </h2>

            <!-- 整体进度 -->
            <div class="mb-6">
                <div class="flex justify-between mb-2">
                    <span class="text-gray-700">Overall Progress</span>
                    <span id="overallPercent" class="text-gray-700 font-semibold">0%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-4">
                    <div
                        id="overallProgress"
                        class="bg-blue-500 h-4 rounded-full transition-all duration-300"
                        style="width: 0%"
                    ></div>
                </div>
            </div>

            <!-- 阶段列表 -->
            <div id="stagesList" class="space-y-2">
                <div class="stage-item flex items-center text-gray-500">
                    <span class="stage-icon mr-2">⏸</span>
                    <span>1. Extracting text</span>
                </div>
                <div class="stage-item flex items-center text-gray-500">
                    <span class="stage-icon mr-2">⏸</span>
                    <span>2. Processing NLP</span>
                </div>
                <div class="stage-item flex items-center text-gray-500">
                    <span class="stage-icon mr-2">⏸</span>
                    <span>3. Detecting phrases</span>
                </div>
                <div class="stage-item flex items-center text-gray-500">
                    <span class="stage-icon mr-2">⏸</span>
                    <span>4. Matching levels</span>
                </div>
                <div class="stage-item flex items-center text-gray-500">
                    <span class="stage-icon mr-2">⏸</span>
                    <span>5. Generating statistics</span>
                </div>
            </div>
        </div>

        <!-- 结果区域 -->
        <div id="resultSection" class="hidden">
            <!-- 统计概览 -->
            <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">
                    📊 Analysis Summary
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <p class="text-gray-600 text-sm">Total Words</p>
                        <p id="totalWords" class="text-3xl font-bold text-blue-600">-</p>
                    </div>
                    <div class="bg-green-50 p-4 rounded-lg">
                        <p class="text-gray-600 text-sm">Unique Words</p>
                        <p id="uniqueWords" class="text-3xl font-bold text-green-600">-</p>
                    </div>
                    <div class="bg-purple-50 p-4 rounded-lg">
                        <p class="text-gray-600 text-sm">Phrasal Verbs</p>
                        <p id="uniquePhrases" class="text-3xl font-bold text-purple-600">-</p>
                    </div>
                </div>

                <!-- 下载按钮 -->
                <div class="mt-6">
                    <p class="text-gray-700 mb-2">💾 Download Results:</p>
                    <div class="flex gap-2">
                        <button onclick="downloadResult('json')" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
                            JSON
                        </button>
                        <button onclick="downloadResult('csv')" class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded">
                            CSV
                        </button>
                        <button onclick="downloadResult('markdown')" class="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded">
                            Markdown
                        </button>
                    </div>
                </div>
            </div>

            <!-- CEFR分布图 -->
            <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">
                    📈 CEFR Level Distribution
                </h2>
                <canvas id="levelChart"></canvas>
            </div>

            <!-- 词汇列表 -->
            <div class="bg-white rounded-lg shadow-lg p-8">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">
                    📚 Vocabulary List (Top 100)
                </h2>
                <div id="wordsList" class="space-y-2">
                    <!-- 动态生成 -->
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
```

#### 前端JavaScript（web/static/js/app.js）

```javascript
// 全局变量
let currentFile = null;
let currentTaskId = null;

// 拖拽上传
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-blue-400');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-blue-400');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-blue-400');
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
});

// 文件选择处理
function handleFileSelect(file) {
    if (!file) return;

    // 验证文件类型
    const allowedTypes = ['text/plain', 'application/pdf',
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'application/json'];
    if (!allowedTypes.includes(file.type) &&
        !file.name.match(/\.(txt|pdf|docx|json)$/i)) {
        alert('Unsupported file type. Please upload TXT, PDF, DOCX, or JSON file.');
        return;
    }

    // 验证文件大小
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
        alert('File too large. Maximum size is 50MB.');
        return;
    }

    currentFile = file;

    // 显示文件信息
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    document.getElementById('fileInfo').classList.remove('hidden');
}

// 分析按钮
document.getElementById('analyzeBtn').addEventListener('click', analyzeFile);
document.getElementById('cancelBtn').addEventListener('click', () => {
    currentFile = null;
    fileInput.value = '';
    document.getElementById('fileInfo').classList.add('hidden');
});

// 执行分析
async function analyzeFile() {
    if (!currentFile) return;

    // 显示进度区域
    document.getElementById('uploadSection').classList.add('hidden');
    document.getElementById('progressSection').classList.remove('hidden');
    document.getElementById('analyzingFile').textContent = currentFile.name;

    // 创建FormData
    const formData = new FormData();
    formData.append('file', currentFile);

    try {
        // 发送请求
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }

        const data = await response.json();
        currentTaskId = data.task_id;

        // 显示结果
        showResults(data);

    } catch (error) {
        alert('Error: ' + error.message);
        resetUI();
    }
}

// 显示结果
function showResults(data) {
    // 隐藏进度，显示结果
    document.getElementById('progressSection').classList.add('hidden');
    document.getElementById('resultSection').classList.remove('hidden');

    // 填充统计数据
    document.getElementById('totalWords').textContent =
        data.statistics.total_words.toLocaleString();
    document.getElementById('uniqueWords').textContent =
        data.statistics.unique_words.toLocaleString();
    document.getElementById('uniquePhrases').textContent =
        data.statistics.unique_phrases.toLocaleString();

    // 绘制图表
    drawLevelChart(data.level_distribution);

    // 显示词汇列表
    displayWords(data.words);
}

// 绘制CEFR分布图
function drawLevelChart(distribution) {
    const ctx = document.getElementById('levelChart').getContext('2d');

    const levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'C2+'];
    const counts = levels.map(level => distribution[level] || 0);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: levels,
            datasets: [{
                label: 'Number of Words',
                data: counts,
                backgroundColor: [
                    'rgba(59, 130, 246, 0.5)',
                    'rgba(16, 185, 129, 0.5)',
                    'rgba(245, 158, 11, 0.5)',
                    'rgba(239, 68, 68, 0.5)',
                    'rgba(139, 92, 246, 0.5)',
                    'rgba(236, 72, 153, 0.5)',
                    'rgba(107, 114, 128, 0.5)'
                ],
                borderColor: [
                    'rgba(59, 130, 246, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(139, 92, 246, 1)',
                    'rgba(236, 72, 153, 1)',
                    'rgba(107, 114, 128, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 显示词汇列表
function displayWords(words) {
    const wordsList = document.getElementById('wordsList');
    wordsList.innerHTML = '';

    words.forEach(word => {
        const wordItem = document.createElement('div');
        wordItem.className = 'border-b border-gray-200 py-3';
        wordItem.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <span class="font-semibold text-lg">${word.word}</span>
                    <span class="ml-2 text-sm text-gray-500">(${word.word_type})</span>
                    <span class="ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">${word.level}</span>
                </div>
                <div class="text-gray-500 text-sm">
                    ${word.frequency} times
                </div>
            </div>
            ${word.definition_cn ? `<div class="text-gray-600 mt-1">${word.definition_cn}</div>` : ''}
        `;
        wordsList.appendChild(wordItem);
    });
}

// 下载结果
function downloadResult(format) {
    if (!currentTaskId) return;

    const url = `/api/download/${currentTaskId}/${format}`;
    window.location.href = url;
}

// 工具函数
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function resetUI() {
    document.getElementById('uploadSection').classList.remove('hidden');
    document.getElementById('progressSection').classList.add('hidden');
    document.getElementById('resultSection').classList.add('hidden');
    currentFile = null;
    currentTaskId = null;
    fileInput.value = '';
    document.getElementById('fileInfo').classList.add('hidden');
}
```

---

## 8. 部署说明

### 8.1 本地开发运行

```bash
# 1. 安装Web依赖
pip install Flask Flask-CORS

# 2. 启动Web服务器
cd web
python app.py

# 3. 打开浏览器
# 访问 http://localhost:5000
```

### 8.2 生产部署（可选）

使用Gunicorn + Nginx：

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
```

---

## 附录

### A. 依赖文件

**requirements-web.txt**：
```
Flask==3.0.0
Flask-CORS==4.0.0
gunicorn==21.2.0  # 生产部署
```

### B. 目录结构（完整）

```
vocab-analyzer/
├── src/vocab_analyzer/          # 现有CLI代码（不变）
├── web/                          # 新增Web模块
│   ├── __init__.py
│   ├── app.py                   # Flask应用
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       └── index.html
├── uploads/                      # 临时上传（自动创建）
├── requirements-web.txt          # Web依赖
└── README.md                     # 更新文档
```

### C. 测试清单

- [ ] 文件上传（拖拽和点击）
- [ ] 文件验证（格式、大小）
- [ ] 分析功能（各种文件格式）
- [ ] 进度显示
- [ ] 结果展示
- [ ] 图表渲染
- [ ] 下载功能（3种格式）
- [ ] 错误处理
- [ ] 浏览器兼容性

---

**文档版本**: v1.0
**创建日期**: 2025-11-04
**预计完成**: 2025-11-07（3天后）
**状态**: ✅ 规格完成，待开发

**下一步行动**: 开始实施 Phase 1 - 基础框架搭建
